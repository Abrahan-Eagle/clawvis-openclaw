---
name: strategic-briefing-ops
description: "Briefing estrategico a nivel holding: sintetiza goals, pipeline, marketing, riesgos y decisiones pendientes en un informe ejecutivo para el CEO. Semanal o bajo demanda."
---

# Strategic Briefing Ops

Inspirado en el patron "god view" de simuladores multi-agente: una vista periodica que sintetiza el estado completo del holding en un solo documento ejecutivo. Sin motor de simulacion — usa las fuentes de datos que ya existen en el ecosistema.

## Cuando se activa

- **Semanal** como rutina del heartbeat de jarvis (recomendado: lunes AM)
- **Bajo demanda** cuando el CEO pide "como va todo" o "dame el estado general"
- **Antes de decisiones grandes** como input para `scenario-analysis-ops`
- **Despues de eventos significativos** (cierre de deal, perdida de cliente, cambio operativo)

## Diferencia con otros reportes

| Reporte | Alcance | Autor | Destinatario |
|---------|---------|-------|-------------|
| **REPORTE_SUPERVISOR_CEO** | Una empresa | Supervisor | CEO |
| **pipeline-health-ops** | Pipeline ventas | sales-hunter | jarvis/CEO |
| **Este skill** | **Todo el holding** | **jarvis** | **CEO** |

Este skill es la capa superior: toma datos de los reportes por empresa y pipeline, los sintetiza, y agrega vision cross-empresa que ningun reporte individual tiene.

## Fuentes de datos (recopilar en orden)

### 1. Goals (estado actual)

Leer `GOALS.md`. Para cada goal activo, evaluar:

```
| Goal | Metrica | Progreso | Tendencia | Nota |
|------|---------|----------|-----------|------|
| G-H01 | Agentes con heartbeat | X de Y | → | |
| G-V01 | Leads/semana | N | ↑/↓/→ | |
| G-M01 | Posts/semana | N | ↑/↓/→ | |
| ... | ... | ... | ... | |
```

**Tendencia**: ↑ mejorando, ↓ empeorando, → estable. Basada en las ultimas 2-4 semanas si hay datos.

### 2. Pipeline de ventas

Fuente: ultimo output de `pipeline-health-ops` o estado actual de Trello ventas.

Extraer:
- Coverage ratio
- Deals activos por etapa
- Deals estancados (>48h sin movimiento)
- Forecast del mes

Si no hay health check reciente: anotar "sin datos frescos" y recomendar ejecutar `pipeline-health-ops`.

### 3. Actividad de marketing

Fuente: Trello marketing, ultimos posts/carruseles, metricas si estan disponibles.

Extraer:
- Contenido publicado esta semana/periodo
- Engagement si hay datos
- Campanas activas
- Alineacion con G-M01, G-M02

### 4. Clientes activos

Fuente: `client-dossiers/` — listar dossiers con estado activo.

```
| Cliente | Empresa | Estado | Ultima actividad | Riesgo |
|---------|---------|--------|------------------|--------|
| [nombre] | marketing | Activo | [fecha/accion] | Bajo/Medio/Alto |
```

### 5. Memoria reciente

Fuente: `MEMORY.md` (ultimas entradas), `LESSONS.md`, `memory/` (ultimos 7 dias).

Extraer:
- Decisiones tomadas esta semana
- Lecciones nuevas
- Propuestas pendientes de aprobacion

### 6. Riesgos y blockers

Consolidar de todas las fuentes anteriores:
- Deals estancados (pipeline)
- Goals con tendencia ↓
- Clientes con riesgo medio/alto
- Dependencias no resueltas (tokens, permisos, activaciones pendientes)
- Blockers tecnicos (Composio, API limits, etc.)

## Estructura del briefing

```markdown
# Briefing Estrategico — Holding Jarvis

**Periodo:** [fecha inicio] – [fecha fin]
**Generado:** YYYY-MM-DD
**Proximo briefing sugerido:** [fecha]

---

## Resumen ejecutivo (3-5 oraciones)

[Estado general del holding. Que va bien, que necesita atencion, que decision
se necesita esta semana.]

---

## 1. Goals — Progreso

| Goal | Empresa | Metrica | Valor actual | Tendencia | Estado |
|------|---------|---------|-------------|-----------|--------|
| G-H01 | holding | ... | ... | ↑/↓/→ | En track / Riesgo / Bloqueado |
| G-V01 | ventas | ... | ... | ... | ... |
| G-M01 | marketing | ... | ... | ... | ... |
| G-J01 | jarvis | ... | ... | ... | ... |

**Goals en riesgo:** [lista o "ninguno"]

---

## 2. Pipeline de ventas

- **Coverage ratio:** X.Xx (saludable / riesgoso / critico)
- **Deals activos:** N (detalle por etapa)
- **Deals estancados:** N (nombres + dias sin movimiento)
- **Forecast mes:** $XXX (conservador)
- **Accion requerida:** [prospectar mas / cerrar deals abiertos / mejorar propuestas / ninguna]

---

## 3. Marketing

- **Contenido publicado:** N piezas ([lista breve])
- **Engagement:** [datos si hay, "sin metricas" si no]
- **Campanas activas:** [lista o "ninguna"]
- **Alineacion G-M02:** X% del contenido apunta a servicio vendible

---

## 4. Clientes

| Cliente | Empresa | Estado | Riesgo | Nota |
|---------|---------|--------|--------|------|
| ... | ... | ... | ... | ... |

---

## 5. Riesgos y blockers

| # | Riesgo/Blocker | Empresa | Impacto | Accion sugerida |
|---|----------------|---------|---------|-----------------|
| 1 | ... | ... | Alto/Medio | ... |
| 2 | ... | ... | ... | ... |

---

## 6. Decisiones pendientes

| Decision | Contexto | Opciones | Recomendacion jarvis |
|----------|----------|----------|---------------------|
| ... | ... | A / B | [cual y por que] |

---

## 7. Prioridades proxima semana

1. [Prioridad 1] — goal: G-XXX — responsable: [agente/empresa]
2. [Prioridad 2] — ...
3. [Prioridad 3] — ...

---

## 8. Lecciones y patrones recientes

[Solo si hay entradas nuevas en LESSONS.md o session-learner-ops esta semana.
Si no hay, omitir esta seccion.]
```

## Reglas de calidad

1. **Concision** — El briefing no debe superar 2 paginas. Si hay mucho que decir, resumir y enlazar a fuentes.
2. **Datos, no opiniones vagas** — Cada afirmacion debe tener un dato o enlace. "Las ventas van bien" no sirve; "Coverage 2.8x, 3 deals en negociacion" si.
3. **Tendencias, no solo snapshots** — Comparar con periodo anterior siempre que haya datos.
4. **Acciones, no solo diagnostico** — Cada seccion que tenga problema debe tener accion sugerida.
5. **Resumen ejecutivo primero** — El CEO debe poder leer solo las primeras 5 lineas y saber si necesita profundizar.

## Cadencia recomendada

| Frecuencia | Cuando | Notas |
|------------|--------|-------|
| **Semanal** | Lunes AM (heartbeat jarvis) | Standard; el CEO revisa antes de planificar la semana |
| **Bajo demanda** | CEO pide estado general | Puede ser version reducida (solo secciones relevantes) |
| **Post-evento** | Cierre deal, perdida, cambio operativo | Solo secciones afectadas + impacto en goals |

## Integracion con otros skills

- **pipeline-health-ops**: datos del pipeline van a seccion 2
- **scenario-analysis-ops**: el briefing puede disparar un analisis de escenarios si hay decisiones complejas
- **session-learner-ops**: lecciones recientes van a seccion 8
- **dual-retrieval-ops**: si se necesita anclar datos a fuentes especificas

## Donde guardar el briefing

- **Trello:** No crear tarjeta (no es una tarea, es un reporte)
- **Discord/Telegram:** Enviar resumen ejecutivo (seccion 0) al canal del CEO si esta configurado
- **Disco:** `~/Documents/JARVIS-DOCUMENTS/holding/briefings/YYYY-MM-DD.md` (solo si el CEO lo pide archivado)
- **Memoria:** Anotar decisiones tomadas despues del briefing en `MEMORY.md`

## Checklist

- [ ] Lei GOALS.md y evalúe progreso de cada goal activo
- [ ] Recopile datos de pipeline (Trello o ultimo health check)
- [ ] Recopile actividad de marketing
- [ ] Revise dossiers de clientes activos
- [ ] Revise MEMORY.md y LESSONS.md (ultimas 1-2 semanas)
- [ ] Consolide riesgos y blockers de todas las fuentes
- [ ] Identifique decisiones pendientes con opciones
- [ ] Escribi resumen ejecutivo AL INICIO (3-5 oraciones)
- [ ] Cada afirmacion tiene dato o fuente
- [ ] Prioridades de la proxima semana con goal y responsable

## Output esperado

Entregar:
- Briefing completo usando la plantilla
- Resumen ejecutivo que se pueda enviar standalone por mensaje
- Lista de decisiones pendientes con recomendacion
- Prioridades top-3 para la semana
