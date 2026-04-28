---
name: llm-as-judge-ops
description: "Auditoría LLM-as-judge antes del gate humano: rúbricas por tipo de entregable, salida JSON para handoff."
metadata:
  version: "1.0.0"
---

# llm-as-judge-ops

**Propósito:** segunda opinión **automática** sobre calidad/riesgo de un entregable **antes** de pedir aprobación CEO (AG-03, AG-12, AG-13, etc.). Inspiración conceptual en rúbricas tipo research benchmarks; **rúbricas aquí son propias del ecosistema**.

**No reemplaza** gates ni juicio humano. Si `score` &lt; umbral o `must_fix` ≠ [], **bloquear** hasta corrección o escalación explícita.

---

## Cuándo invocarla

- Handoff hacia publicación (`copy-to-design` → `design-to-producer` → `producer-to-publisher`).
- Antes de **escalar** según [`ESCALACION_ASYNC.md`](../../../docs/ESCALACION_ASYNC.md).

---

## Salida JSON estándar

El modelo auditor devuelve **solo** este bloque (markdown fenced `json`):

```json
{
  "score": 0.0,
  "threshold_pass": 0.75,
  "category": "carousel_ig|copy_editing|cold_email|ad_creative|other",
  "riesgos": [],
  "must_fix": [],
  "sugerencias": [],
  "ag_gates_touched": ["AG-12", "AG-13"]
}
```

- **`score`:** 0–1 (calidad global para publicación).
- **`must_fix`:** lista de strings; si no está vacía → **no** publicar hasta resolver.
- **`ag_gates_touched`:** qué gates humanos probablemente aplican (información al CEO).

---

## Rúbricas rápidas (prompt interno)

### carousel_ig

| Criterio | Peso |
|----------|------|
| Coherencia narrativa slide a slide | 25% |
| CTA claro y único | 15% |
| Alineación con `marketing-context` / dossier | 25% |
| Legal/marca (sin promesas falsas) | 20% |
| Formato técnico (1080×1350, legibilidad) | 15% |

### copy_editing

| Criterio | Peso |
|----------|------|
| Claridad y tono de marca | 35% |
| Precisión (sin afirmaciones inventadas) | 35% |
| SEO / lectura (sin keyword stuffing) | 30% |

### cold_email

| Criterio | Peso |
|----------|------|
| Personalización creíble | 30% |
| Un solo CTA | 20% |
| No spam / no datos sensibles | 25% |
| Longitud y legibilidad | 25% |

### ad_creative

| Criterio | Peso |
|----------|------|
| Cumplimiento políticas plataforma (sin contenido prohibido) | 35% |
| Propuesta de valor clara | 25% |
| Brand safety | 40% |

---

## Integración handoff

Si el handoff lleva `payload` grande, el juicio puede referenciar **paths** de artefactos en `out/` o hashes cortos. No duplicar binarios en el JSON.

Schemas relacionados: `skills/global/handoff/schemas/*.json`.

---

## Gateos críticos

- **AG-13:** si el entregable usa IA generativa en asset final, el audit debe marcar `ag_gates_touched` incluyendo `"AG-13"` y listar assets en `riesgos` si hay duda de derechos/atribución.
