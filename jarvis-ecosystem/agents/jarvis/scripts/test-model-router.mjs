/**
 * Matriz rápida de regresión (sin Groq). Ejecutar: node test-model-router.mjs
 */
import assert from "node:assert";
import { resolveModelRouter } from "./model-router.mjs";

const cases = [
  { text: "hola", expectTier: "light", rule: "trivial" },
  { text: "qué tiempo hace en Madrid", expectTier: "light", rule: "trivial" },
  { text: "debug this NullPointerException", expectTier: "standard", rule: "code-standard" },
  { text: "refactor the whole distributed system", expectTier: "heavy", rule: "code-heavy" },
  {
    text: "short",
    expectTier: "light",
    rule: "empty-or-short"
  }
];

let failed = false;
for (const c of cases) {
  try {
    const r = await resolveModelRouter(c.text, { forceClassifier: false });
    assert.strictEqual(
      r.tier,
      c.expectTier,
      `text=${JSON.stringify(c.text)} got tier ${r.tier}, expected ${c.expectTier}`
    );
    if (c.rule && r.matchedRule) {
      assert.ok(
        String(r.matchedRule).includes(c.rule) || r.matchedRule === c.rule,
        `expected matchedRule to mention ${c.rule}, got ${r.matchedRule}`
      );
    }
    console.log("OK:", c.text.slice(0, 40), "→", r.tier, r.matchedRule || "-");
  } catch (e) {
    failed = true;
    console.error("FAIL:", c.text, e.message);
  }
}

const longNoKeyword = "x".repeat(600);
const r2 = await resolveModelRouter(longNoKeyword, { forceClassifier: false });
assert.strictEqual(r2.tier, "light", "sin clasificador, default light");
console.log("OK: long string →", r2.tier, "(default)");

process.exit(failed ? 1 : 0);
