# Diario de Aprendizaje: Ecosistema Jarvis
> "El error es solo una iteración hacia la perfección."

## Registro de Lecciones Aprendidas

| ID | Fecha | Error | Causa Raíz | Acción Correctiva / Prevención |
|---|---|---|---|---|
| L001 | 2026-03-11 | Modelos `phi`/`tinyllama` fallaron | Falta de soporte para Tool-Calling | Migrado a `qwen2.5-coder:0.5b` que sí soporta herramientas en 4GB RAM. |
| L002 | 2026-03-11 | Bloqueo de archivos `.lock` | Ejecución concurrente accidental | Se implementó script de limpieza de locks antes de cada ejecución. |

---
*Este archivo debe ser actualizado por cualquier agente que reciba una corrección directa del usuario.*
