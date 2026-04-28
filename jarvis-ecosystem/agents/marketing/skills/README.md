# Skills de marketing (coreyhaines31/marketingskills adaptadas)

**Fuente upstream:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución en cada `SKILL.md` y en [`LICENSE_UPSTREAM.md`](LICENSE_UPSTREAM.md).

**Ubicación:** `agents/marketing/skills/<nombre>/SKILL.md` (40 skills). **No** es duplicado del árbol Jarvis: aquí vive la librería **profunda** (briefs, dossiers, marcos en español). Las variantes rápidas `*-ops` siguen **solo** en [`agents/jarvis/skills/`](../../jarvis/skills/README.md).

Cada `SKILL.md` (adaptación **v2**, abril 2026) incluye:

1. **Frontmatter** (`description` ES+EN compacto, `metadata.jarvis_ecosystem`, versión upstream).
2. **Resumen, disparadores, contexto dossier-first** — sin contradicciones con `.claude/`; fuente canónica = `client-dossiers/<id>/marketing-context.md` o `.agents/product-marketing-context.md`.
3. **Marcos / metodología** en español (hooks a `skills/` globales cuando aplica: `brand-kit`, `carousel-render`, `tts-free`, etc.).
4. **Puertas AG-11/12/13**, **Coordinación** con comandos reales (`activity-log`, `handoff`).
5. **Referencias:** texto upstream completo en `<skill>/references/upstream-en.md` (por carpeta), no embebido en el cuerpo principal.

**Fichas YAML por skill (fuente declarativa):** [`scripts/marketing_skills_data/<skill>.yaml`](../../../scripts/marketing_skills_data/) — regeneradas junto con los `SKILL.md`.

**Herramientas y docs copiados del repo upstream** (enlaces `../../tools/` resueltos): [`docs/upstream-marketingskills/tools/`](../../../docs/upstream-marketingskills/tools/).

**Regeneración:** clone upstream en `/tmp/marketingskills-upstream`, luego desde `jarvis-ecosystem/`:

```bash
python3 scripts/generate_marketing_skills.py
./scripts/validate-marketing-skills.sh
```

**Runtime OpenClaw:** sincronizar al workspace del gateway con [`scripts/sync-marketing-skills-from-repo.sh`](../../../scripts/sync-marketing-skills-from-repo.sh) — ver [`docs/COHERENCIA_RUNTIME_REPO.md`](../../../docs/COHERENCIA_RUNTIME_REPO.md).

**Investigación y matriz:** [`docs/RESEARCH_MARKETING_SKILLS.md`](../../../docs/RESEARCH_MARKETING_SKILLS.md).

## Índice (40)

| Skill | Carpeta |
|-------|---------|
| product-marketing-context | [product-marketing-context](./product-marketing-context/SKILL.md) |
| ab-test-setup | [ab-test-setup](./ab-test-setup/SKILL.md) |
| ad-creative | [ad-creative](./ad-creative/SKILL.md) |
| ai-seo | [ai-seo](./ai-seo/SKILL.md) |
| analytics-tracking | [analytics-tracking](./analytics-tracking/SKILL.md) |
| aso-audit | [aso-audit](./aso-audit/SKILL.md) |
| churn-prevention | [churn-prevention](./churn-prevention/SKILL.md) |
| cold-email | [cold-email](./cold-email/SKILL.md) |
| community-marketing | [community-marketing](./community-marketing/SKILL.md) |
| competitor-alternatives | [competitor-alternatives](./competitor-alternatives/SKILL.md) |
| competitor-profiling | [competitor-profiling](./competitor-profiling/SKILL.md) |
| content-strategy | [content-strategy](./content-strategy/SKILL.md) |
| copy-editing | [copy-editing](./copy-editing/SKILL.md) |
| copywriting | [copywriting](./copywriting/SKILL.md) |
| customer-research | [customer-research](./customer-research/SKILL.md) |
| directory-submissions | [directory-submissions](./directory-submissions/SKILL.md) |
| email-sequence | [email-sequence](./email-sequence/SKILL.md) |
| form-cro | [form-cro](./form-cro/SKILL.md) |
| free-tool-strategy | [free-tool-strategy](./free-tool-strategy/SKILL.md) |
| image | [image](./image/SKILL.md) |
| launch-strategy | [launch-strategy](./launch-strategy/SKILL.md) |
| lead-magnets | [lead-magnets](./lead-magnets/SKILL.md) |
| marketing-ideas | [marketing-ideas](./marketing-ideas/SKILL.md) |
| marketing-psychology | [marketing-psychology](./marketing-psychology/SKILL.md) |
| onboarding-cro | [onboarding-cro](./onboarding-cro/SKILL.md) |
| page-cro | [page-cro](./page-cro/SKILL.md) |
| paid-ads | [paid-ads](./paid-ads/SKILL.md) |
| paywall-upgrade-cro | [paywall-upgrade-cro](./paywall-upgrade-cro/SKILL.md) |
| popup-cro | [popup-cro](./popup-cro/SKILL.md) |
| pricing-strategy | [pricing-strategy](./pricing-strategy/SKILL.md) |
| programmatic-seo | [programmatic-seo](./programmatic-seo/SKILL.md) |
| referral-program | [referral-program](./referral-program/SKILL.md) |
| revops | [revops](./revops/SKILL.md) |
| sales-enablement | [sales-enablement](./sales-enablement/SKILL.md) |
| schema-markup | [schema-markup](./schema-markup/SKILL.md) |
| seo-audit | [seo-audit](./seo-audit/SKILL.md) |
| signup-flow-cro | [signup-flow-cro](./signup-flow-cro/SKILL.md) |
| site-architecture | [site-architecture](./site-architecture/SKILL.md) |
| social-content | [social-content](./social-content/SKILL.md) |
| video | [video](./video/SKILL.md) |

## Variantes `*-ops` en Jarvis (atalhos)

| Tema | Ops Jarvis |
|------|------------|
| Page CRO | [page-cro-ops](../../jarvis/skills/page-cro-ops/SKILL.md) |
| Copywriting | [copywriting-ops](../../jarvis/skills/copywriting-ops/SKILL.md) |
| Cold email | [cold-email-ops](../../jarvis/skills/cold-email-ops/SKILL.md) |
| SEO audit | [seo-audit-ops](../../jarvis/skills/seo-audit-ops/SKILL.md) |
| Investigación / entrevistas | [deep-interview-ops](../../jarvis/skills/deep-interview-ops/SKILL.md) |
| Ideas | [brainstorming-ops](../../jarvis/skills/brainstorming-ops/SKILL.md) |
| Lanzamiento | [strategic-briefing-ops](../../jarvis/skills/strategic-briefing-ops/SKILL.md) |
| Ventas / propuestas | [proposal-ops](../../jarvis/skills/proposal-ops/SKILL.md) |
