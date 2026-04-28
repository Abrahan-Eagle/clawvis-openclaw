---
name: planner
description: "Produce un plan JSON (máx. 5 pasos) desde un objetivo en lenguaje natural."
metadata:
  version: "1.0.0"
---

# planner

> Inspiración: [agent/planner.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/agent/planner.py) — **texto y script propios**.

## Rol

Producir un plan JSON (máx. 5 pasos) a partir de un **objetivo** en lenguaje natural. En producción, el LLM rellena `steps` con nombres reales de tools del gateway; el binario emite **plantilla** para pruebas y contrato.

## Uso

```bash
./bin/planner "Subir resumen a Notion y avisar en Telegram"
```

## Contrato

- `schema`: `jarvis-plan-v1`
- Cada `step`: `tool`, `action`, `args` (objeto). Sin scripts Python arbitrarios.
- Cumplir [APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md) al planear envíos o publicación.

## Siguiente

Pasar el JSON a `task-queue` + `executor` o guardarlo en un archivo y ejecutar a mano.
