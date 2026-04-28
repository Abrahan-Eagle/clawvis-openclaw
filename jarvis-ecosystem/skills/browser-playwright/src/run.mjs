/**
 * Control mínimo de navegador (Chromium).
 * Dominios: solo allowlist (AG en SKILL.md + APPROVAL_GATES).
 */
import { chromium } from "playwright";
import fs from "fs";
import path from "path";
import os from "os";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const out = { cmd: argv[0], flags: {} };
  const rest = argv.slice(1);
  for (const a of rest) {
    const m = /^--([^=]+)=(.*)$/.exec(a);
    if (m) out.flags[m[1]] = m[2];
    else if (!out._pos) out._pos = a;
  }
  return out;
}

function defaultAllow() {
  const e = process.env.BROWSER_PLAYWRIGHT_ALLOW || "localhost,127.0.0.1,open-meteo.com,example.com";
  return e.split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
}

function hostAllowed(urlStr, allow) {
  let u;
  try {
    u = new URL(urlStr);
  } catch {
    return false;
  }
  const h = u.hostname.toLowerCase();
  return allow.some((a) => h === a || h.endsWith("." + a));
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length < 1 || argv[0] === "-h" || argv[0] === "--help") {
    console.log(
      JSON.stringify({
        usage:
          "node run.mjs <go-to|get-text|screenshot|close> --url=... [--path=out.png]",
        allowlist: "BROWSER_PLAYWRIGHT_ALLOW=host1,host2",
        profile: "PLAYWRIGHT_USER_DATA under ~/.openclaw/playwright-profile",
        note: "Solo hostnames en allowlist; resto requiere aprobación CEO (AG-09, dominios críticos).",
      }, null, 2)
    );
    process.exit(0);
  }
  const { cmd, flags } = parseArgs(argv);
  const allow = defaultAllow();
  const userDataDir =
    process.env.PLAYWRIGHT_USER_DATA ||
    path.join(os.homedir(), ".openclaw", "playwright-profile");
  fs.mkdirSync(userDataDir, { recursive: true });

  const url = flags.url;
  if (!url) {
    console.log(JSON.stringify({ error: "missing --url" }));
    process.exit(1);
  }
  if (!hostAllowed(url, allow)) {
    console.log(
      JSON.stringify({
        error: "host_not_allowlisted",
        host: (() => {
          try {
            return new URL(url).hostname;
          } catch {
            return null;
          }
        })(),
        allowlist: allow,
        approval: "Añadir a BROWSER_PLAYWRIGHT_ALLOW o pedir aprobación según docs/APPROVAL_GATES.md (AG-09, AG-10, AG-11).",
      })
    );
    process.exit(2);
  }

  // En muchos Linux, `npx playwright install chromium` falla (host antiguo); usar Chrome/Edge del sistema.
  // PLAYWRIGHT_CHANNEL: chrome | msedge | chromium (bundled) | vacío = chrome
  const ch = (process.env.PLAYWRIGHT_CHANNEL ?? "chrome").trim();
  const launchOpts = { headless: true, args: ["--no-sandbox"] };
  if (ch && ch !== "bundled") {
    launchOpts.channel = ch;
  }

  const browser = await chromium.launchPersistentContext(userDataDir, launchOpts);
  const page = await browser.newPage();
  const out = { cmd, url };

  try {
    if (cmd === "go-to") {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
      out.status = "navigated";
      out.title = await page.title();
    } else if (cmd === "get-text") {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
      const text = await page.evaluate(() => document.body?.innerText?.slice(0, 20000) || "");
      out.text = text;
      out.len = text.length;
    } else if (cmd === "screenshot") {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
      const p = flags.path || path.join(userDataDir, "shot.png");
      await page.screenshot({ path: p, fullPage: true });
      out.screenshot = p;
    } else if (cmd === "close") {
      out.status = "no-op (close the Node process; context closes with exit)";
    } else {
      out.error = "unknown cmd";
    }
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => {
  console.log(JSON.stringify({ error: String(e) }));
  process.exit(1);
});
