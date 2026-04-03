#!/usr/bin/env node
/**
 * Valida coherencia básica del store de sesiones OpenClaw (sessions.json vs transcriptos .jsonl).
 *
 * Uso:
 *   node validate-jarvis-sessions.mjs
 *
 * Env:
 *   SESSIONS_STORE      — ruta a sessions.json (default: ~/.openclaw/agents/jarvis/sessions/sessions.json)
 *   EXPECTED_WORKSPACE  — si está definido, se compara el cwd de la primera línea de cada .jsonl con este prefijo
 *   VALIDATE_STRICT_CWD — si es "1" y EXPECTED_WORKSPACE está definido, cwd que no empiece por el prefijo → exit 3
 */

import fs from "fs";
import os from "os";
import path from "path";

const store =
  process.env.SESSIONS_STORE ||
  path.join(os.homedir(), ".openclaw/agents/jarvis/sessions/sessions.json");
const expectedPrefix = process.env.EXPECTED_WORKSPACE || "";
const strictCwd = process.env.VALIDATE_STRICT_CWD === "1";

if (!fs.existsSync(store)) {
  console.error(`Session store not found: ${store}`);
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(store, "utf8"));
const missing = [];
const cwdWarnings = [];

for (const [key, entry] of Object.entries(data)) {
  if (!entry || typeof entry !== "object") continue;
  const sf = entry.sessionFile;
  if (!sf || typeof sf !== "string") continue;

  if (!fs.existsSync(sf)) {
    missing.push({ key, sessionFile: sf });
    continue;
  }

  if (expectedPrefix && sf.endsWith(".jsonl")) {
    try {
      const fd = fs.openSync(sf, "r");
      const buf = Buffer.alloc(65536);
      const n = fs.readSync(fd, buf, 0, 65536, 0);
      fs.closeSync(fd);
      const firstLine = buf.subarray(0, n).toString("utf8").split("\n")[0];
      if (!firstLine) continue;
      const row = JSON.parse(firstLine);
      if (
        row.type === "session" &&
        row.cwd &&
        typeof row.cwd === "string" &&
        !row.cwd.startsWith(expectedPrefix)
      ) {
        cwdWarnings.push({ key, cwd: row.cwd, file: sf });
      }
    } catch (e) {
      cwdWarnings.push({ key, error: String(e), file: sf });
    }
  }
}

if (missing.length) {
  console.error("Missing session files:");
  for (const m of missing) {
    console.error(`  ${m.key} -> ${m.sessionFile}`);
  }
  process.exit(1);
}

const keyCount = Object.keys(data).length;
console.log(`OK: ${keyCount} keys checked, all sessionFile paths exist.`);

if (cwdWarnings.length && expectedPrefix) {
  console.warn(
    `cwd prefix warnings (expected prefix: ${expectedPrefix}):`,
  );
  for (const w of cwdWarnings) {
    console.warn(`  ${w.key}: ${w.cwd ?? w.error} (${w.file})`);
  }
  if (strictCwd) process.exit(3);
}

process.exit(0);
