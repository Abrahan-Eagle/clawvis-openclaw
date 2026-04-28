---
name: economic-accountability-ops
description: "Cost footer simbólico por turno: enlaza costes reales (cost-report) con balance opcional por dossier y modo de autonomía."
metadata:
  version: "1.0.0"
---

# economic-accountability-ops

**Tipo:** skill global (protocolo; sin binario obligatorio).

Inspiración conceptual en benchmarks tipo “coworker económico” (p. ej. [HKUDS/ClawWork](https://github.com/HKUDS/ClawWork)); **este repo no implementa** GDPVal ni pagos BLS. Aquí solo hay **visibilidad de coste** y **balance simbólico** opcional.

---

## Cuándo usarla

- Al **cerrar un turno** que haya consumido API (LLM, búsqueda, Composio, etc.).
- Al **cerrar una tarea** (`activity-log end`) si quieres trazabilidad en el log.

---

## Cost footer (una línea)

Formato recomendado:

```
Cost: $<API_este_turno> | Balance: $<balance_simbolico> | Mode: <D|C|B|A> | Status: <thriving|tight|broke>
```

- **`Cost`:** estimación del turno si el gateway la expone; si no, referencia al último [`cost-report`](../../../scripts/cost-report.sh) del mes (`./scripts/cost-report.sh YYYY-MM`).
- **`Balance`:** opcional. Definición: `ingresos_simbolicos_acumulados - costes_API_mes` (no es caja real).
  - Ingresos simbólicos: solo si el CEO/documentación del dossier definen hitos (p. ej. entrega aceptada); opcionalmente `client-dossiers/<id>/economics.json` con `{ "symbolic_credits": N }`.
- **`Mode`:** `JARVIS_AUTONOMY_MODE` o `autonomy_mode` en MEMORY — ver [`AUTONOMIA_MODOS.md`](../../../docs/AUTONOMIA_MODOS.md).
- **`Status`:** heurística humana: **thriving** (margen cómodo), **tight** (cerca del límite de política), **broke** (detener trabajo costoso y escalar).

---

## Registro en activity-log

Opcional: en el JSONL de eventos, campo libre `economic` en la línea del evento:

```json
{"economic": {"cost_usd_est": 0.02, "balance_usd_sym": 124.5, "mode": "C"}}
```

Si `state/activity-log.jsonl` está gitignored, la convención sigue valiendo en runtime.

---

## Límites

- **No** sustituye [APPROVAL_GATES.md](../../../docs/APPROVAL_GATES.md).
- **No** confundir balance simbólico con ingresos facturados al cliente.
