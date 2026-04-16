# Forense MiroFish — Resumen

**Fecha:** 2026-04-16  
**Repo analizado:** [666ghj/MiroFish](https://github.com/666ghj/MiroFish) (simulacion multi-agente, Python 57% + Vue 41%, Docker, AGPL-3.0)  
**Objetivo:** Evaluar que patrones conceptuales de MiroFish pueden fortalecer el ecosistema Jarvis sin clonar su stack ni incorporar codigo AGPL.

---

## Que es MiroFish

Motor de "swarm intelligence" / prediccion mediante simulacion: semillas del mundo real (noticias, politicas, senales financieras) construyen un mundo digital paralelo con muchos agentes con memoria y evolucion social, y generan informes de prediccion.

- **Flujo declarado:** construccion de grafo / GraphRAG -> configuracion de entorno y personas -> simulacion dual-plataforma -> generacion de informes -> chat con agentes del mundo simulado.
- **Stack:** backend Python, frontend Vue, Docker Compose, API LLM estilo OpenAI, Zep para memoria cloud.
- **Licencia:** AGPL-3.0 (copyleft fuerte; requiere revision legal antes de incorporar cualquier codigo).

## Hallazgos clave

Se cruzo cada patron de MiroFish contra los 37 skills, 6 agentes, 38 docs y toda la infraestructura de memoria del ecosistema Jarvis:

1. **Patron semilla-a-informe:** MiroFish toma un seed (pregunta, situacion) y produce un informe estructurado con multiples angulos. Jarvis tenia `proposal-ops` (propuestas de venta) y `brainstorming-ops` (alternativas pre-ejecucion), pero **ningun skill para analisis de escenarios what-if** con variables iterables.

2. **Patron god-view periodica:** MiroFish muestra una vista consolidada del mundo simulado. Jarvis tenia `pipeline-health-ops` (solo ventas), `REPORTE_SUPERVISOR_CEO` (por empresa) y `morning-brief` (calendario + clima), pero **ningun briefing estrategico a nivel holding** que sintetice goals + pipeline + marketing + riesgos.

3. **Variables + iteracion:** MiroFish permite cambiar supuestos y regenerar simulacion. En Jarvis, `carousel-ops` itera disenos pero no hay patron formal de "cambiar variable y recalcular escenario".

4. **Memoria en el tiempo:** MiroFish usa Zep para memoria episodica. Jarvis ya cubre esto con MemPalace + MEMORY.md + memory/ + session-learner-ops — **no hay hueco**.

5. **Grafo + contexto:** MiroFish usa GraphRAG. Jarvis ya cubre esto con Graphify + dual-retrieval-ops + MemPalace KG — **no hay hueco**.

6. **Miles de agentes en paralelo:** MiroFish simula miles de personas. Para un holding real de 6 empresas con agentes de negocio, esto **no aporta valor** — los subagentes OpenClaw y cron cubren el paralelismo necesario.

## Que se adopto

### Skills nuevos (2)

| Skill | Patron MiroFish | Que resuelve |
|-------|----------------|-------------|
| `scenario-analysis-ops` | Semilla -> contexto -> variables -> escenarios -> informe iterativo | Gap critico: no habia skill para analisis what-if. Toma una pregunta estrategica, inyecta contexto automatico (goals, pipeline, dossiers, memoria), define variables con rangos, genera 3+ escenarios con tabla comparativa, matriz de riesgos, acciones con Trello, y protocolo de iteracion (cambiar variable -> regenerar). |
| `strategic-briefing-ops` | God-view periodica del holding | Gap critico: no habia briefing a nivel holding. Sintetiza estado de todos los goals, pipeline de ventas, actividad marketing, clientes activos, riesgos cross-empresa, decisiones pendientes con recomendacion, y prioridades semanales. Diferente del REPORTE_SUPERVISOR_CEO que es por empresa. |

### Patrones integrados en skills existentes (0)

No se modificaron skills existentes; los patrones adoptados (iteracion, context injection) estan encapsulados en los 2 skills nuevos.

## Que NO se adopto

| Elemento MiroFish | Razon de exclusion |
|--------------------|--------------------|
| Frontend Vue + API 5001 | Stack distinto; Jarvis opera via CLI/chat/Telegram/Discord |
| Motor OASIS de simulacion masiva | Miles de agentes ficticios no sirven para un holding real de 6 empresas |
| Zep como memoria cloud | MemPalace + MEMORY.md + memory/ ya cubren memoria episodica y semantica |
| GraphRAG de mundo simulado | Graphify (mapa del repo) + MemPalace KG (hechos de negocio) ya cubren grounding |
| Codigo fuente de MiroFish | Licencia AGPL-3.0; cero lineas copiadas, solo patrones conceptuales |
| Simulacion dual-plataforma | Irrelevante para operaciones de negocio del holding |
| Chat con agentes simulados | Jarvis ya tiene agentes reales con roles de negocio |

## Archivos modificados

### Creados
- `agents/jarvis/skills/scenario-analysis-ops/SKILL.md`
- `agents/jarvis/skills/strategic-briefing-ops/SKILL.md`
- `docs/FORENSE_MIROFISH_RESUMEN.md` (este archivo)

### Editados
- `agents/jarvis/AGENTS.md` — +scenario-analysis-ops y +strategic-briefing-ops en protocolo de calidad e indice
- `agents/jarvis/MEMORY.md` — log de decision de gobierno
- `agents/jarvis/skills/README.md` — filas en tabla de skills destacados
- `docs/OPERACION_POST_GOBIERNO.md` — entrada Forense MiroFish en indice

## Patrones adoptados (referencia rapida)

| Patron | Skill donde vive | Uso |
|--------|-----------------|-----|
| Semilla-a-informe | scenario-analysis-ops | Pregunta concreta -> contexto automatico -> informe con escenarios |
| Variables iterables | scenario-analysis-ops | Parametros explicitos con rangos; cambiar uno y regenerar |
| 3 escenarios (base/optimista/pesimista) | scenario-analysis-ops | Tabla comparativa con confianza por escenario |
| Matriz de riesgos | scenario-analysis-ops | Probabilidad x impacto con mitigaciones |
| God-view holding | strategic-briefing-ops | Vista consolidada: goals + pipeline + marketing + riesgos |
| Context injection automatica | ambos | Pre-flight: GOALS.md + LESSONS.md + dossiers + MemPalace |

## Nota legal

MiroFish esta bajo **AGPL-3.0**. No se copio ninguna linea de codigo; los skills creados son implementaciones originales de patrones conceptuales (analisis de escenarios, reportes periodicos) que existen en la literatura de decision-making y son anteriores a MiroFish. La referencia al repo es puramente bibliografica.
