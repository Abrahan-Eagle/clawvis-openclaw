# Forense Agency Agents — Resumen

**Fecha:** 2026-04-14  
**Repo analizado:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (79.9k stars, 144 agentes en 12 divisiones)  
**Objetivo:** Extraer patrones de ventas avanzadas y SEO para fortalecer el ecosistema Jarvis.

---

## Hallazgos clave

Los agentes de Sales y Marketing de agency-agents tienen frameworks de venta y auditoria significativamente mas profundos que los skills existentes de Jarvis:

1. **Gap critico cubierto:** No habia skill para escribir propuestas estructuradas. Ahora `proposal-ops` cubre win themes, narrativa en 3 actos y executive summary.
2. **Discovery Coach** aporto 3 frameworks de venta probados (SPIN, Gap Selling, Sandler Pain Funnel) + AECR para objeciones.
3. **Outbound Strategist** aporto signal-based selling, ICP tiering y secuencia multicanal de 10 touches en 28 dias.
4. **SEO Specialist** aporto cannibalization audit como paso bloqueante, keyword clusters y link building plan.
5. **Pipeline Analyst** aporto metricas de pipeline, forecasting bottom-up y sistema de alertas.

## Que se adopto

### Skills nuevos (2)

| Skill | Origen | Que resuelve |
|-------|--------|-------------|
| `proposal-ops` | Proposal Strategist | Gap critico: no habia skill para propuestas. Win themes, narrativa 3 actos, executive summary, adaptacion Workana (200 palabras). |
| `pipeline-health-ops` | Pipeline Analyst | Monitoreo de salud del pipeline: metricas volumen/velocidad/calidad, coverage ratio, deals estancados, forecasting, alertas. Integra con heartbeat semanal de sales-hunter. |

### Skills enriquecidos (3)

| Skill | Que se agrego | Impacto |
|-------|--------------|---------|
| `deep-interview-ops` | SPIN Selling, Gap Selling, Sandler Pain Funnel, framework AECR (objeciones), regla 60/40 | De cuestionamiento generico a calificacion de ventas profesional. Preguntas de Implicacion (SPIN) y causa raiz (Gap) crean urgencia real. |
| `cold-email-ops` | Signal-based selling (3 tiers), ICP definition (firmographic + behavioral + disqualifiers), secuencia multicanal (10 touches/28 dias), benchmarks de reply rate | De emails basicos a outreach estrategico. Reply rate esperado sube de 1-3% (generico) a 12-25% (signal-based). |
| `seo-audit-ops` | Cannibalization audit (bloqueante), keyword cluster framework, link building plan, E-E-A-T compliance, scorecard 22->29 items | Cannibalization impide que optimizacion de una pagina dañe a otra. Keyword clusters previenen duplicacion. E-E-A-T es factor de ranking directo. |

## Que NO se adopto

| Division | Agentes | Razon |
|----------|---------|-------|
| Engineering | 28 | dev-agency no activa |
| Design | 8 | sin proyectos UI activos |
| Game Development | 18 | irrelevante |
| Spatial Computing | 6 | irrelevante |
| Academic | 5 | irrelevante |
| Paid Media | 7 | sin gasto publicitario |
| Testing | 8 | especificos de dev |
| Finance | 5 | contadores no activa |
| Support | 6 | sin operaciones de soporte |
| Product | 5 | sin producto SaaS propio |
| Project Management | 6 | task-pipeline-ops ya cubre workflow |
| Orchestrator | 1 | task-pipeline-ops similar conceptualmente |
| 30+ especializados | varios | demasiado nicho (blockchain, XR, gaming) |

## Archivos modificados

### Creados
- `agents/jarvis/skills/proposal-ops/SKILL.md`
- `agents/jarvis/skills/pipeline-health-ops/SKILL.md`
- `docs/FORENSE_AGENCY_AGENTS_RESUMEN.md` (este archivo)

### Editados
- `agents/jarvis/skills/deep-interview-ops/SKILL.md` — +frameworks SPIN/Gap/Sandler, +AECR, +regla 60/40
- `agents/jarvis/skills/cold-email-ops/SKILL.md` — +signal-based selling, +ICP, +secuencia 10 touches, +benchmarks
- `agents/jarvis/skills/seo-audit-ops/SKILL.md` — +cannibalization audit, +keyword clusters, +link building, +E-E-A-T, scorecard 29 items
- `agents/jarvis/AGENTS.md` — +proposal-ops, +pipeline-health-ops en protocolo de calidad
- `agents/ventas/AGENTS.md` — +proposal-ops, +pipeline-health-ops en skills, deep-interview mejorado
- `agents/marketing/AGENTS.md` — seo-audit-ops descripcion actualizada
- `agents/jarvis/MEMORY.md` — log de decision
- `docs/OPERACION_POST_GOBIERNO.md` — indice actualizado
- `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md` — seccion 14 agregada

## Frameworks adoptados (referencia rapida)

| Framework | Skill donde vive | Uso |
|-----------|-----------------|-----|
| SPIN Selling | deep-interview-ops | Descubrimiento: Situation-Problem-Implication-Need-Payoff |
| Gap Selling | deep-interview-ops | Cuantificar: estado actual vs futuro vs gap |
| Sandler Pain Funnel | deep-interview-ops | Profundizar: tecnico -> negocio -> personal |
| AECR | deep-interview-ops | Objeciones: Acknowledge-Empathize-Clarify-Reframe |
| Win Themes | proposal-ops | Propuestas: afirmaciones centradas en cliente |
| Narrativa 3 actos | proposal-ops | Propuestas: entender -> solucionar -> transformar |
| Signal-based selling | cold-email-ops | Outreach: senales Tier 1/2/3 de compra |
| ICP tiering | cold-email-ops | Targeting: firmographic + behavioral + disqualifiers |
| Cannibalization audit | seo-audit-ops | SEO: cross-page query map, ownership, resolucion |
| E-E-A-T | seo-audit-ops | SEO: Experience-Expertise-Authoritativeness-Trust |
| Pipeline coverage | pipeline-health-ops | Forecasting: ratio pipeline/meta |
