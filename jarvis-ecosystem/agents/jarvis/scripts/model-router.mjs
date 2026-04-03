#!/usr/bin/env node
/**
 * Resuelve tier + model + agentId según model-router.rules.yaml (+ clasificador Groq opcional).
 * Uso:
 *   node model-router.mjs "texto del usuario"
 *   node model-router.mjs --json "texto"
 * Salida JSON: { tier, model, agentId, matchedRule, usedClassifier }
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parse as parseYaml } from "yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RULES_PATH = process.env.JARVIS_MODEL_ROUTER_RULES
  ? path.resolve(process.env.JARVIS_MODEL_ROUTER_RULES)
  : path.resolve(__dirname, "..", "model-router.rules.yaml");

function loadRules() {
  const raw = fs.readFileSync(RULES_PATH, "utf8");
  return parseYaml(raw);
}

function envAgentFallback(tier) {
  const map = {
    light: process.env.JARVIS_AGENT_LIGHT,
    standard: process.env.JARVIS_AGENT_STANDARD,
    heavy: process.env.JARVIS_AGENT_HEAVY
  };
  return map[tier] || null;
}

function sortRules(rules) {
  return [...rules].sort((a, b) => (a.priority ?? 100) - (b.priority ?? 100));
}

function compilePattern(p) {
  let body = p;
  let flags = "s";
  if (body.startsWith("(?i)")) {
    body = body.slice(4);
    flags += "i";
  }
  return new RegExp(body, flags);
}

function matchRule(text, rule) {
  if (rule.minLen != null && text.length < rule.minLen) return false;
  if (rule.maxLen != null && text.length > rule.maxLen) return false;
  const patterns = Array.isArray(rule.patterns) ? rule.patterns : [];
  for (const p of patterns) {
    try {
      const re = compilePattern(p);
      if (re.test(text)) return true;
    } catch {
      continue;
    }
  }
  return false;
}

async function classifyWithGroq(text, cfg) {
  const key = process.env.GROQ_API_KEY;
  if (!key) throw new Error("GROQ_API_KEY requerido para clasificador");
  const model = cfg.classifier?.groqModel || "llama-3.1-8b-instant";
  const body = {
    model,
    temperature: 0,
    max_tokens: 80,
    messages: [
      {
        role: "system",
        content:
          'Respond only with compact JSON: {"tier":"light"|"standard"|"heavy"} for task complexity. No markdown.'
      },
      {
        role: "user",
        content: text.slice(0, 4000)
      }
    ]
  };
  const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Groq ${res.status}: ${t.slice(0, 200)}`);
  }
  const data = await res.json();
  const raw = data?.choices?.[0]?.message?.content?.trim() || "";
  const m = raw.match(/\{[\s\S]*\}/);
  const json = JSON.parse(m ? m[0] : raw);
  const tier = json.tier;
  if (!["light", "standard", "heavy"].includes(tier)) {
    throw new Error(`tier inválido: ${tier}`);
  }
  return tier;
}

export async function resolveModelRouter(text, opts = {}) {
  const cfg = loadRules();
  const tiers = cfg.tiers || {};
  const rules = sortRules(cfg.rules || []);
  let matchedRule = null;
  for (const rule of rules) {
    if (matchRule(text, rule)) {
      matchedRule = rule.name || "(unnamed)";
      const tier = rule.tier;
      const t = tiers[tier];
      if (!t) throw new Error(`Tier desconocido en regla: ${tier}`);
      let agentId = t.agentId || envAgentFallback(tier);
      if (!agentId) agentId = tier === "standard" ? "jarvis" : tier === "heavy" ? "jarvis-deep" : "jarvis-auto-light";
      return {
        tier,
        model: t.model,
        agentId,
        matchedRule,
        usedClassifier: false
      };
    }
  }

  const useClassifier =
    opts.forceClassifier === true ||
    (process.env.JARVIS_MODEL_ROUTER_CLASSIFIER === "1" &&
      text.length >= (cfg.classifier?.whenNoRuleMatchMinChars ?? 500));

  if (useClassifier) {
    try {
      const tier = await classifyWithGroq(text, cfg);
      const t = tiers[tier];
      let agentId = t?.agentId || envAgentFallback(tier);
      if (!agentId) agentId = tier === "standard" ? "jarvis" : tier === "heavy" ? "jarvis-deep" : "jarvis-auto-light";
      return {
        tier,
        model: t?.model,
        agentId,
        matchedRule: null,
        usedClassifier: true
      };
    } catch (e) {
      console.error("[model-router] classifier error:", e.message);
    }
  }

  const tier = "light";
  const t = tiers[tier];
  let agentId = t?.agentId || envAgentFallback(tier) || "jarvis-auto-light";
  return {
    tier,
    model: t?.model,
    agentId,
    matchedRule: null,
    usedClassifier: false
  };
}

async function main() {
  const argv = process.argv.slice(2);
  const jsonOut = argv[0] === "--json";
  const text = (jsonOut ? argv.slice(1) : argv).join(" ").trim();
  if (!text) {
    console.error("Uso: node model-router.mjs [--json] <mensaje>");
    process.exit(2);
  }
  const out = await resolveModelRouter(text, {});
  const line = JSON.stringify(
    {
      ...out,
      rulesFile: RULES_PATH
    },
    null,
    jsonOut ? 2 : 0
  );
  console.log(line);
}

const isMain =
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
if (isMain) {
  main().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
