---
name: llm-as-judge-ops
description: >
  Auditoría LLM-as-judge pre-gate: rúbrica ponderada, score 0-1, threshold, salida JSON.
  Trigger: auditar entregable antes de gate humano, score de calidad, must_fix antes de merge/publicar.
license: UNLICENSED
metadata:
  author: JARVIS Global
  version: "1.0"
  scope: [global]
  category: ops
  upstream: clawvis-openclaw:llm-as-judge-ops
  auto_invoke:
    - "Auditoría automática pre-gate con rúbrica y score"
    - "Evaluar entregable con LLM-as-judge antes de aprobación humana"
    - "Score de calidad y must_fix antes de publicar o mergear"
  triggers: llm as judge, LLM-as-judge, rúbrica score, pre-gate audit, must_fix, threshold pass
  related-skills:
    - jarvis-core
    - human-in-the-loop-ops
    - parallel-judge-ops
    - doubt-driven-development
    - verification-before-completion
    - code-review-playbook
    - approval-gate
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash, Task]
---

## JARVIS / Cursor (mandatory)

- **Precedencia:** `jarvis-core` > esta skill. **Gate humano:** `human-in-the-loop-ops`, `approval-gate`, `git-guardrails-ops`.
- **No reemplaza** juicio humano ni gates irreversibles. Si `score < threshold_pass` o `must_fix` no está vacío → **bloquear** hasta corrección o escalación explícita.
- **vs `parallel-judge-ops`:** un juez con rúbrica + score; parallel-judge = 2+ jueces independientes en paralelo.
- **vs `doubt-driven-development`:** doubt-driven = duda in-flight; esta skill = auditoría de entregable casi terminado.
- Overlay dominio (marketing, AG gates holding): ver repo producto / clawvis `OVERLAY.md`. Doc sync: [docs/CLAWVIS_INTEGRATION.md](../../docs/CLAWVIS_INTEGRATION.md).

# LLM-as-Judge Ops

## Cuándo usar

- Entregable de **calidad verificable** antes de pedir aprobación humana (PR, doc, feature, publicación).
- Necesitas **score numérico** y lista `must_fix` accionable antes del gate.
- Handoff entre fases donde un auditor automático filtra ruido antes del humano.

**Cuándo NO usar:**

- Cambio trivial obvio → `verification-before-completion` basta.
- Alto riesgo y necesitas **varios jueces independientes** → `parallel-judge-ops`.
- Duda sobre **una decisión** mientras implementas → `doubt-driven-development`.

## Salida JSON estándar

El auditor devuelve **solo** este bloque (markdown fenced `json`):

```json
{
  "score": 0.0,
  "threshold_pass": 0.75,
  "category": "code_change|documentation|other",
  "riesgos": [],
  "must_fix": [],
  "sugerencias": [],
  "human_gates_hint": []
}
```

| Campo | Significado |
|-------|-------------|
| `score` | 0–1, calidad global según rúbrica |
| `threshold_pass` | Umbral mínimo para proponer gate humano (default 0.75; ajustar por riesgo) |
| `category` | Tipo de entregable evaluado |
| `must_fix` | Bloqueantes; si no vacío → no cerrar hasta resolver |
| `human_gates_hint` | Gates humanos probables (push, deploy, publicación) — informativo |

## Rúbricas de ejemplo (genéricas)

Adaptar pesos al repo activo. Productos pueden añadir categorías vía overlay.

### code_change (PR / diff)

| Criterio | Peso |
|----------|------|
| Cumple spec/intent declarado | 30% |
| Tests/verificación según alcance | 25% |
| Sin regresiones obvias / edge cases críticos | 25% |
| Legibilidad y scope acotado | 20% |

### documentation

| Criterio | Peso |
|----------|------|
| Describe comportamiento **actual** (no futuro) | 35% |
| Ejemplos/comandos verificables | 35% |
| Baja carga cognitiva (estructura escaneable) | 30% |

## Procedimiento

1. Definir **categoría** y rúbrica (criterios + pesos = 100%).
2. Fijar `threshold_pass` (subir en auth/prod/irreversible).
3. Ejecutar auditoría con contexto mínimo necesario (artefacto + criterio de éxito).
4. Parsear JSON; si falla bloqueo → re-auditar o escalar humano.
5. Si pasa → proceder a gate humano (`human-in-the-loop-ops`) o cierre (`verification-before-completion`).

## Anti-patrones

- Juez único **auto-evaluándose** sin rúbrica escrita (self-preferential bias).
- `threshold_pass` cosmético (siempre 0.5) sin calibrar por riesgo.
- Ignorar `must_fix` no vacío "porque el score pasó".
- Sustituir `parallel-judge-ops` en diffs críticos por un solo juez barato.

## Skills relacionadas

- `parallel-judge-ops` — verificación adversarial paralela (2+ jueces).
- `human-in-the-loop-ops` — gates y escalamiento humano.
- `verification-before-completion` — evidencia empírica antes de declarar done.
- `code-review-playbook` — proceso de review técnico.

---

## Overlay clawvis — holding OpenClaw

Extensiones para el ecosistema Jarvis holding. Precede sobre la base global solo donde se contradiga.

### Cuándo invocar (holding)

- Handoff hacia publicación (`copy-to-design` → `design-to-producer` → `producer-to-publisher`).
- Antes de escalar según [ESCALACION_ASYNC.md](../../../docs/ESCALACION_ASYNC.md).
- Antes de AG-03 (publicar), AG-12, AG-13 — ver [APPROVAL_GATES.md](../../../docs/APPROVAL_GATES.md).

### Categorías adicionales JSON

Usar en `category`: `carousel_ig`, `copy_editing`, `cold_email`, `ad_creative` además de las genéricas.

Campo `ag_gates_touched` en lugar de `human_gates_hint` cuando el entregable toque gates CEO (información al CEO).

### Rúbricas holding (marketing / ventas)

#### carousel_ig

| Criterio | Peso |
|----------|------|
| Coherencia narrativa slide a slide | 25% |
| CTA claro y único | 15% |
| Alineación con marketing-context / dossier | 25% |
| Legal/marca (sin promesas falsas) | 20% |
| Formato técnico (1080×1350, legibilidad) | 15% |

#### copy_editing / cold_email / ad_creative

Ver rúbricas en commit histórico clawvis; aplicar antes de publicación o envío comercial.

### Gate AG-13

Si el entregable usa IA generativa en asset final, marcar `ag_gates_touched` incluyendo `"AG-13"` y listar assets en `riesgos` si hay duda de derechos/atribución.

### Handoff

Referencias a `skills/global/handoff/schemas/*.json` y paths en `out/` — no duplicar binarios en JSON.
