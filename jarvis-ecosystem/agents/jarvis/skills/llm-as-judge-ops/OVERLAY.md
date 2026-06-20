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
