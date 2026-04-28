# Investigacion forense: coreyhaines31/marketingskills -> jarvis-ecosystem

**Fuente:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT, Corey Haines).  
**Version referencia upstream:** tag reciente al import (abr 2026).  
**Import en jarvis-ecosystem:** `agents/marketing/skills/<skill>/SKILL.md` generadas/adaptadas el **2026-04-28**.

## Resumen ejecutivo

- **40 skills** en formato Agent Skills (`SKILL.md` + `references/` opcional).
- **Patron upstream:** frontmatter `name` / `description` (EN, triggers largos) / `metadata.version`; cuerpo operativo en ingles; seccion `Related Skills` con cross-refs.
- **Adaptacion Jarvis v2 (abr 2026):** cuerpo principal **en español** (dossier-first, hooks a `skills/` locales, tablas pipeline en `image` / `video` / `social-content`); el texto upstream íntegro queda en **`references/upstream-en.md`** por skill. Manifiesto + plantillas: `scripts/marketing_skills_v2/`; fichas declarativas: `scripts/marketing_skills_data/<skill>.yaml`.
- **Skills `*-ops` existentes** en `agents/jarvis/skills/` **no se modifican** (conviven como variantes rapidas).

## Matriz de cobertura (40 skills)

| Skill | Status | Ops Jarvis relacionada | AG tipicos (si aplica) | Hooks coordinacion |
|-------|--------|-------------------------|--------------------------|---------------------|
| product-marketing-context | NEW | — | AG-08 si datos sensibles | activity-log, handoff |
| ab-test-setup | NEW | — | — | activity-log |
| ad-creative | NEW | — | AG-13 (IA generativa en creatividades) | activity-log |
| ai-seo | NEW | — | — | activity-log |
| analytics-tracking | NEW | — | — | activity-log |
| aso-audit | NEW | — | — | activity-log |
| churn-prevention | NEW | — | — | activity-log |
| cold-email | DUAL | cold-email-ops | — | activity-log |
| community-marketing | NEW | — | — | activity-log |
| competitor-alternatives | NEW | — | — | activity-log |
| competitor-profiling | NEW | — | AG-11 si automatizacion/web nueva | activity-log |
| content-strategy | NEW | — | — | activity-log |
| copy-editing | NEW | — | — | activity-log |
| copywriting | DUAL | copywriting-ops | — | activity-log |
| customer-research | DUAL | deep-interview-ops | AG-11 si research web automatizado | activity-log |
| directory-submissions | NEW | — | AG-12 si publicacion masiva | activity-log |
| email-sequence | NEW | — | AG-12 si envio/publicacion automatica visible | activity-log |
| form-cro | NEW | — | — | activity-log |
| free-tool-strategy | NEW | — | — | activity-log |
| image | NEW | — | AG-13 | activity-log |
| launch-strategy | DERIVED | strategic-briefing-ops | AG-12 si lanzamiento implica publicar | activity-log |
| lead-magnets | NEW | — | — | activity-log |
| marketing-ideas | DERIVED | brainstorming-ops | — | activity-log |
| marketing-psychology | NEW | — | — | activity-log |
| onboarding-cro | NEW | — | — | activity-log |
| page-cro | DUAL | page-cro-ops | — | activity-log |
| paid-ads | NEW | — | AG-12 si implica publicar anuncios | activity-log |
| paywall-upgrade-cro | NEW | — | — | activity-log |
| popup-cro | NEW | — | — | activity-log |
| pricing-strategy | NEW | — | — | activity-log |
| programmatic-seo | NEW | — | AG-11 si crawl/automatizacion nueva | activity-log |
| referral-program | NEW | — | AG-12 si difusion/publicacion | activity-log |
| revops | NEW | — | — | activity-log |
| sales-enablement | DERIVED | proposal-ops | — | activity-log |
| schema-markup | NEW | — | — | activity-log |
| seo-audit | DUAL | seo-audit-ops | AG-11 si necesidad de dominio Playwright | activity-log |
| signup-flow-cro | NEW | — | — | activity-log |
| site-architecture | NEW | — | — | activity-log |
| social-content | NEW | — | AG-13 + AG-12 segun IA/publicacion | activity-log |
| video | NEW | — | AG-13 | activity-log |

**Leyenda Status:** NEW = no habia equivalente `*-ops`; DUAL = existe ops homonima o tema equivalente; DERIVED = ops con nombre distinto en Jarvis (ver tabla).

## Convenciones de rutas

- Contexto de cliente: `client-dossiers/<dossier_id>/marketing-context.md`
- Contexto holding: `jarvis-ecosystem/.agents/product-marketing-context.md`
- Plantilla: [`.agents/product-marketing-context.md.template`](../.agents/product-marketing-context.md.template)
- Skills globales (pipeline RRSS, logs): `jarvis-ecosystem/skills/*`

## Fichas por skill (compactas)

Cada skill en `agents/marketing/skills/<name>/SKILL.md` contiene:

1. **Frontmatter** (`description` ES+EN, `metadata.jarvis_ecosystem`, versión upstream).
2. **Atribución** MIT en blockquote.
3. **Resumen, disparadores, contexto dossier-first**, variante `*-ops` si aplica.
4. **Frameworks / metodología** (ES), hooks al pipeline Jarvis.
5. **Puertas de aprobación**, **Coordinación** (comandos shell reales).
6. **Referencias:** por skill, `agents/marketing/skills/<skill>/references/upstream-en.md`.

### Lista alfabetica con proposito (1 linea)

- **ab-test-setup** — Experimentacion A/B y programa de tests.
- **ad-creative** — Variaciones creativas para paid media.
- **ai-seo** — Visibilidad en motores de respuesta IA.
- **analytics-tracking** — Eventos, props, calidad de datos.
- **aso-audit** — Optimizacion de store listings.
- **churn-prevention** — Retencion y win-back.
- **cold-email** — Outbound frio B2B.
- **community-marketing** — Comunidades como canal.
- **competitor-alternatives** — Paginas comparativa/alternativas.
- **competitor-profiling** — Intel competencia desde URLs.
- **content-strategy** — Pilares, temas, agenda editorial.
- **copy-editing** — Pulido de copy existente.
- **copywriting** — Copy de paginas y conversion.
- **customer-research** — VOC, entrevistas, sintesis.
- **directory-submissions** — Listados y directorios.
- **email-sequence** — Secuencias automatizadas.
- **form-cro** — Formularios no-signup.
- **free-tool-strategy** — Herramientas gratuitas como marketing.
- **image** — Brief de imagenes + enlaces a render/IA.
- **launch-strategy** — Lanzamientos coordinados.
- **lead-magnets** — Imanes de leads.
- **marketing-ideas** — Ideacion amplia de tacticas.
- **marketing-psychology** — Sesgos y marcos mentales.
- **onboarding-cro** — Activacion post-registro.
- **page-cro** — CRO de paginas de marketing.
- **paid-ads** — Campanas de pago multicanal.
- **paywall-upgrade-cro** — Paywalls y upsell in-app.
- **popup-cro** — Overlays y modales.
- **pricing-strategy** — Precio y packaging.
- **product-marketing-context** — Documento cimiento (dossier o holding).
- **programmatic-seo** — SEO a escala con plantillas.
- **referral-program** — Referidos y afiliados.
- **revops** — Pipeline marketing-ventas.
- **sales-enablement** — Material para ventas.
- **schema-markup** — Datos estructurados.
- **seo-audit** — Auditoria SEO integral.
- **signup-flow-cro** — Registro y trial.
- **site-architecture** — Arquitectura y enlazado interno.
- **social-content** — Redes y short-form video (hooks, calendario).
- **video** — Guion/produccion video + pipeline local.

## References (`references/`)

Algunas skills upstream incluyen `references/*.md`. El generador **copia** esa carpeta cuando existe. Si una skill no trae `references/` en upstream, no se crea carpeta local vacia salvo que se haya generado por copia.

## Carpeta `tools/` del repo upstream

Los enlaces del tipo `../../tools/...` en el cuerpo upstream se resuelven contra una copia en:

`jarvis-ecosystem/docs/upstream-marketingskills/tools/`

(regenerable copiando desde el clone de [marketingskills](https://github.com/coreyhaines31/marketingskills)).

## Herramientas de generacion

- `scripts/generate_marketing_skills.py` — motor v2 (`marketing_skills_v2/`); upstream opcional en `/tmp/marketingskills-upstream/skills` para versiones y `upstream-en.md`.
- `scripts/validate-marketing-skills.sh` — validación reforzada (estructura v2, gates, hooks).
- `scripts/sync-marketing-skills-from-repo.sh` — sync al workspace del gateway (paralelo a jarvis skills).

## Adaptacion v2 — qué cambió respecto a la primera importacion

| Aspecto | Import v1 | Import v2 |
|---------|-----------|-----------|
| Cuerpo principal | Guía ES + upstream EN embebido | ES adaptado; upstream solo en `references/upstream-en.md` |
| Dossier | A veces contradecía rutas `.agents` vs `.claude` | Reglas explícitas + validador anti-legacy |
| `image` / `video` / `social-content` | Sin pipeline local jarvis | Tablas + workflows (`brand-kit`, `carousel-render`, `tts-free`, `video-compose`, …) |
| Coordinación | Mención genérica | Bloque con comandos reales `activity-log` / `handoff` |
| Runtime gateway | Solo sync `agents/jarvis/skills` | Añadido `sync-marketing-skills-from-repo.sh` |
| Validación | Frontmatter + enlaces | + description ≤500, hooks obligatorios, dual `*-ops`, sin `[SKILL.md]` como texto de enlace |

## Proximos pasos opcionales

- Anadir automatizacion ClawFlows que liste skills activas o brief pendientes (opcional).
