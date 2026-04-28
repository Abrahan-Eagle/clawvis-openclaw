---
name: executor
description: "Ejecutor dry-run de planes JSON (no ejecuta código arbitrario; lista invocaciones)."
metadata:
  version: "1.0.0"
---

# executor

> Inspiración: [agent/executor.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/agent/executor.py) — **v1 = dry-run seguro** (no genera ni ejecuta código; no llama al gateway automáticamente).

## Uso

```bash
./bin/planner "mi objetivo" > /tmp/plan.json
# Editar /tmp/plan.json con tools reales
./bin/executor /tmp/plan.json
```

La salida enumera qué se invocaría. Para ejecución real, usar las herramientas en la sesión OpenClaw o ampliar este skill con puentes explícitos y gates.

**Excluido a propósito:** `_run_generated_code` del MK37.
