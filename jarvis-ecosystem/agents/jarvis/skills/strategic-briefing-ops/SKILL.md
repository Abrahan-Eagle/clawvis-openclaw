---
name: strategic-briefing-ops
description: >
  Briefing estrategico consolidado: sintetiza estado del proyecto, progreso, riesgos y decisiones pendientes
  en un informe ejecutivo para el lider del proyecto. Semanal o bajo demanda.
  Trigger: como va todo, estado general, briefing estrategico, resumen ejecutivo semanal.
license: UNLICENSED
metadata:
  author: JARVIS Global
  version: "1.0"
  scope: [global]
  category: ops
  upstream: clawvis:strategic-briefing-ops
  auto_invoke:
    - "Como va todo el proyecto"
    - "Estado general del producto"
    - "Briefing estrategico semanal"
    - "Resumen ejecutivo para el founder"
  triggers: briefing estrategico, estado general, como va todo, resumen ejecutivo, god view
  related-skills:
    - scenario-analysis-ops
    - scenario-router
    - session-learner-ops
    - verification-before-completion
    - jarvis-core
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash]
---

# Strategic Briefing Ops

Patrón **god-view** inspirado en simuladores multi-agente (MiroFish): vista periódica que sintetiza el estado completo en un solo documento ejecutivo. **Sin motor de simulación** — usa fuentes ya existentes en el repo y memoria del proyecto.

Doc upstream: [docs/MIROFISH_UPSTREAM.md](../../../docs/MIROFISH_UPSTREAM.md).

## Cuándo se activa

- **Semanal** como rutina (recomendado: lunes AM)
- **Bajo demanda** cuando el líder pide "cómo va todo" o "estado general"
- **Antes de decisiones grandes** como input para `scenario-analysis-ops`
- **Después de eventos significativos** (release, pérdida de cliente, incidente, pivot)

## Diferencia con otros reportes

| Reporte | Alcance | Típico destinatario |
|---------|---------|---------------------|
| Reporte por módulo / sprint | Un feature o área | Tech lead / PM |
| `scenario-analysis-ops` | Una pregunta what-if concreta | Quien decide esa decisión |
| **Este skill** | **Vista consolidada del proyecto o holding** | **Líder / founder / CEO** |

Este skill es la capa superior: sintetiza progreso, riesgos cross-área y decisiones pendientes que ningún informe puntual cubre solo.

## Fuentes de datos (recopilar en orden)

### 1. Estado del proyecto (progreso y metas)

Leer `AGENTS.md` y `docs/active_context.md` (si existe). Extraer:

- Metas o hitos activos citados en memoria
- Módulos completados vs en curso
- Divergencias planes vs código si están documentadas

```
| Meta / hito | Métrica o criterio | Progreso | Tendencia | Nota |
|-------------|-------------------|----------|-----------|------|
| … | … | … | ↑/↓/→ | … |
```

**Tendencia:** ↑ mejorando, ↓ empeorando, → estable (últimas 2–4 semanas si hay datos).

### 2. Salud técnica (opcional pero recomendado)

- `git status` / rama activa vs `dev`/`main`
- CI reciente si el usuario menciona o hay workflow en repo
- Tests: último resultado conocido en `active_context` o walkthrough

### 3. Actividad reciente

Fuentes: `docs/active_context.md`, `.agents/plans/walkthrough.md`, changelog en `AGENTS.md` (sección Cambios recientes), commits recientes si relevante.

- Entregas de la semana/periodo
- Decisiones tomadas
- Propuestas pendientes de aprobación

### 4. Clientes / stakeholders (si aplica)

Si el usuario o el repo tienen dossiers, CRM notes o pack inversor:

```
| Stakeholder | Contexto | Estado | Última actividad | Riesgo |
|-------------|----------|--------|------------------|--------|
| … | … | … | … | Bajo/Medio/Alto |
```

Sin datos: sección "sin datos de clientes en repo" — no inventar.

### 5. Métricas de negocio (opcional)

Solo si el usuario provee datos o existen en `docs/Lanzamiento/`, dashboards, KPIs en README. No inferir cifras.

### 6. Riesgos y blockers

Consolidar de todas las fuentes:

- Metas con tendencia ↓
- Deuda técnica citada en memoria
- Dependencias no resueltas (tokens, permisos, deploy)
- Blockers de integración o regulación documentados

## Workspace clawvis (opcional)

Si el cwd incluye `clawvis-openclaw/jarvis-ecosystem`, leer además:

- `GOALS.md`, `LESSONS.md`, `MEMORY.md`
- `client-dossiers/` para clientes activos
- Último output de `pipeline-health-ops` si existe

Ver [STRANGEVERSE_INTEGRATION.md](../../../docs/STRANGEVERSE_INTEGRATION.md) § clawvis.

## Estructura del briefing

```markdown
# Briefing Estratégico — [Proyecto / Holding]

**Periodo:** [fecha inicio] – [fecha fin]
**Generado:** YYYY-MM-DD
**Próximo briefing sugerido:** [fecha]

---

## Resumen ejecutivo (3-5 oraciones)

[Estado general. Qué va bien, qué necesita atención, qué decisión se necesita esta semana.]

---

## 1. Progreso y metas

| Meta / hito | Métrica | Valor actual | Tendencia | Estado |
|-------------|---------|--------------|-----------|--------|
| … | … | … | ↑/↓/→ | En track / Riesgo / Bloqueado |

**Metas en riesgo:** [lista o "ninguna"]

---

## 2. Salud técnica

- **Rama / deploy:** …
- **Tests / CI:** …
- **Deuda técnica destacada:** …

---

## 3. Actividad reciente

- **Entregas:** …
- **Decisiones tomadas:** …
- **Pendientes de aprobación:** …

---

## 4. Stakeholders / clientes (si hay datos)

| Nombre | Contexto | Estado | Riesgo | Nota |
|--------|----------|--------|--------|------|
| … | … | … | … | … |

---

## 5. Riesgos y blockers

| # | Riesgo/Blocker | Área | Impacto | Acción sugerida |
|---|----------------|------|---------|-----------------|
| 1 | … | … | Alto/Medio | … |

---

## 6. Decisiones pendientes

| Decision | Contexto | Opciones | Recomendación JARVIS |
|----------|----------|----------|----------------------|
| … | … | A / B | [cuál y por qué] |

---

## 7. Prioridades próxima semana

1. [Prioridad 1] — meta: … — responsable: …
2. [Prioridad 2] — …
3. [Prioridad 3] — …

---

## 8. Lecciones y patrones recientes

[Solo si hay entradas nuevas en active_context o session-learner. Si no, omitir.]
```

## Reglas de calidad

1. **Concisión** — No superar ~2 páginas. Resumir y enlazar a fuentes.
2. **Datos, no opiniones vagas** — Cada afirmación con dato o fuente citada.
3. **Tendencias, no solo snapshots** — Comparar con periodo anterior cuando haya datos.
4. **Acciones, no solo diagnóstico** — Cada problema con acción sugerida.
5. **Resumen ejecutivo primero** — El líder puede leer solo las primeras líneas.

## Cadencia recomendada

| Frecuencia | Cuándo | Notas |
|------------|--------|-------|
| **Semanal** | Lunes AM | Standard antes de planificar la semana |
| **Bajo demanda** | Líder pide estado | Versión reducida (secciones relevantes) |
| **Post-evento** | Release, incidente, pivot | Solo secciones afectadas + impacto en metas |

## Integración con otros skills

- **scenario-analysis-ops:** si hay decisiones complejas en sección 6 → invocar análisis what-if
- **scenario-router:** si el briefing revela necesidad de simulación social → escalar con gate de coste
- **session-learner-ops:** lecciones recientes en sección 8
- **verification-before-completion:** antes de entregar briefing final

## Dónde guardar el briefing

- Repo producto: `docs/briefings/YYYY-MM-DD.md` (con aprobación del usuario)
- clawvis holding: `~/Documents/JARVIS-DOCUMENTS/holding/briefings/YYYY-MM-DD.md` si el CEO lo pide archivado
- No crear tarjeta de tarea por defecto — es un reporte, no una tarea

## Checklist

- [ ] Leí `AGENTS.md` y `docs/active_context.md`
- [ ] Evalué progreso de metas/hitos activos
- [ ] Revisé actividad reciente (walkthrough, cambios recientes)
- [ ] Consolidé riesgos y blockers
- [ ] Identifiqué decisiones pendientes con opciones
- [ ] Escribí resumen ejecutivo AL INICIO (3–5 oraciones)
- [ ] Cada afirmación tiene dato o fuente
- [ ] Prioridades top-3 con meta y responsable
- [ ] `verification-before-completion` al cerrar

## Output esperado

- Briefing completo usando la plantilla
- Resumen ejecutivo standalone (mensaje corto)
- Lista de decisiones pendientes con recomendación
- Prioridades top-3 para la semana

---

## Overlay clawvis — holding OpenClaw

### Cuándo (holding)

- Rutina **semanal** heartbeat jarvis (lunes AM recomendado)
- CEO pide estado general del holding
- Input previo a `scenario-analysis-ops`

### Fuentes obligatorias

1. `GOALS.md` — progreso por goal (G-H*, G-V*, G-M*)
2. Pipeline — último `pipeline-health-ops` o Trello ventas
3. Marketing — actividad reciente agentes mkt-*
4. `client-dossiers/` — clientes activos
5. Riesgos cross-empresa y decisiones pendientes CEO

### Diferencia reportes

Este skill = vista **todo el holding** (jarvis → CEO). No sustituye REPORTE_SUPERVISOR_CEO ni pipeline-health por empresa.
