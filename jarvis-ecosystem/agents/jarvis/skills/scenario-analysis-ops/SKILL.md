---
name: scenario-analysis-ops
description: >
  Analisis what-if estrategico sin motor de simulacion: semilla, variables, escenarios, matriz de riesgos, iteracion.
  Trigger: que pasa si, escenarios, comparar opciones estrategicas, riesgos de decision.
license: UNLICENSED
metadata:
  author: JARVIS Global
  version: "1.0"
  scope: [global]
  category: ops
  upstream: clawvis:scenario-analysis-ops
  auto_invoke:
    - "Que pasa si decision estrategica"
    - "Comparar escenarios base optimista pesimista"
    - "Matriz de riesgos what-if"
  triggers: what-if, escenarios, que pasa si, analisis estrategico, matriz riesgos
  related-skills:
    - strategic-briefing-ops
    - scenario-router
    - strangeverse
    - deep-interview-ops
    - brainstorming-ops
    - task-pipeline-ops
    - writing-plans
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash]
---

# Scenario Analysis Ops

Patrón **semilla → contexto → variables → escenarios → informe iterativo**, inspirado en simuladores multi-agente (MiroFish / StrangeVerse) pero **sin motor de simulación** ni dependencias externas. Para simulación social con muchos agentes, escalar a `strangeverse` vía `scenario-router`.

## Cuándo usar

- Decisiones estratégicas (pricing, expansión, priorización, inversión)
- Evaluar riesgos operativos o de mercado sin coste LLM
- Comparar alternativas antes de Spec Kit o implementación
- Cualquier "¿qué pasa si X cambia?" donde no hace falta simular redes sociales

**No usar para:**

- Tareas operativas del día (`task-pipeline-ops`)
- Implementar feature o bugfix (`sdd-router`)
- Brainstorming libre de ideas (`brainstorming-ops`)
- Dinámica social / opinión pública masiva (`strangeverse`)

## Relación con otros skills

```
deep-interview-ops  (semilla vaga)
        ↓
scenario-analysis-ops  (este skill)
        ↓
brainstorming-ops → writing-plans / sdd-router / task-pipeline-ops
```

## Prerrequisitos

**Antes de analizar (repo Cursor genérico):**

1. `AGENTS.md` del proyecto activo
2. `docs/active_context.md` si existe
3. Docs de producto relevantes (`README.md`, `docs/product-marketing-context.md`, brand, etc.)
4. **Opcional:** briefing reciente de `strategic-briefing-ops` (decisiones pendientes, riesgos) como input de contexto
5. Si el cwd es **clawvis** `jarvis-ecosystem`: además `GOALS.md`, `LESSONS.md`, `client-dossiers/` según aplique

Documentar fuentes en el informe — cada claim trazable.

## Proceso

### Fase 1: Semilla concreta

| Semilla débil | Semilla fuerte |
|---------------|----------------|
| "Mejorar ventas" | "¿Qué pasa si subimos comisión a 3% en Q3 con solo rubro Animales activo?" |
| "Expandir mercado" | "¿Si abrimos Zonix en Valencia con 5 farmacias piloto, qué CAC asumimos?" |
| "Competencia" | "Si un competidor baja precio 30% en carruseles IG, ¿cómo afecta retención?" |

Semilla vaga → `deep-interview-ops` primero.

### Fase 2: Contexto

Recopilar del repo y datos del usuario:

```
Contexto = {
  producto:   AGENTS.md + active_context + docs dominio,
  restricciones: stack, regulación, deuda técnica citada,
  datos:      métricas que el usuario proporcione,
  externo:    búsqueda web solo si el usuario pide o falta dato crítico
}
```

### Fase 3: Variables (3–6)

| Variable | Actual | Rango | Unidad | Controlable? |
|----------|--------|-------|--------|--------------|
| … | … | … | … | Sí / Parcial / No |

### Fase 4: Escenarios (mínimo 3)

- **Base:** continuidad actual
- **Optimista:** variables controlables a favor
- **Pesimista:** externos en contra
- Opcional: escenario nombrado por el usuario

Tabla comparativa con **confianza** (Alta / Media / Baja).

### Fase 5: Matriz de riesgos

Probabilidad × Impacto; deal-breakers = Alta + Alto.

### Fase 6: Resumen ejecutivo

**Al inicio del informe** (5–7 oraciones): qué se analizó, recomendación, riesgo principal, decisión requerida.

### Fase 7: Acciones recomendadas

| # | Acción | Área | Plazo |
|---|--------|------|-------|
| 1 | … | Backend/PM/… | … |

Sin herramientas externas obligatorias; el usuario decide tracking.

## Iteración

Si el usuario cambia una variable:

1. Recalcular escenarios afectados
2. Actualizar riesgos y resumen
3. Marcar `--- Iteración N (variable: …) ---`
4. Máximo **5 iteraciones**; luego pedir más datos o escalar a `strangeverse`

## Escalar a StrangeVerse

Cuando hace falta **simulación multi-agente** (opinión pública, narrativa emergente, semilla larga en PDFs):

1. Confirmar coste LLM/Zep con el usuario
2. `scenario-router` → `strangeverse status`
3. Flujo API: ontology → build → sim → report (ver skill `strangeverse`)

## Plantilla de informe

```markdown
# Análisis de escenarios: [título]

**Fecha:** YYYY-MM-DD | **Semilla:** … | **Iteración:** 1

## Resumen ejecutivo
[5-7 oraciones]

## Contexto
[fuentes citadas]

## Variables
| Variable | Actual | Rango | Controlable? |

## Escenarios
### Base / Optimista / Pesimista

## Tabla comparativa
| Escenario | … | Resultado | Confianza |

## Matriz de riesgos
| Riesgo | Probabilidad | Impacto | Mitigación |

## Acciones recomendadas
| # | Acción | Área | Plazo |

## Decisión requerida
[qué debe decidir el líder del proyecto]
```

## Dónde guardar

- Repo producto: `docs/scenarios/YYYY-MM-DD-<slug>.md` (con aprobación del usuario)
- clawvis holding: `~/Documents/JARVIS-DOCUMENTS/...` según convención local

## Checklist

- [ ] Semilla concreta
- [ ] Contexto con fuentes
- [ ] ≥3 escenarios + tabla
- [ ] Matriz de riesgos
- [ ] Resumen al inicio
- [ ] Decisión explícita
- [ ] `verification-before-completion` al cerrar

---

## Overlay clawvis — holding OpenClaw

### Contexto automático (Fase 2 escenarios)

Recopilar antes de informe what-if:

- `GOALS.md` — goals activos de empresas involucradas
- Pipeline Trello o último `pipeline-health-ops`
- `client-dossiers/` relevantes
- `MEMORY.md`, `LESSONS.md`
- Opcional: `last30days-openclaw` para pulso de mercado

### Acciones post-informe

- Crear/actualizar tarjetas Trello con acciones recomendadas
- Escalar al CEO decisiones con deal-breakers (Probabilidad Alta + Impacto Alto)

Doc holding: [FORENSE_MIROFISH_RESUMEN.md](../../../docs/FORENSE_MIROFISH_RESUMEN.md), [FLUJO_TRELLO_ECOSISTEMA.md](../../../docs/FLUJO_TRELLO_ECOSISTEMA.md).
