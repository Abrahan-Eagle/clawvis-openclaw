# memory-store

> Inspirado en el patrón de memoria categorizada de [FatihMakes/Jarvis-MK37](https://github.com/FatihMakes/Jarvis-MK37) (`memory/memory_manager.py`) — **re-implementación propia** (sin copiar código; licencia MK37: CC BY-NC 4.0).

## Qué hace

- Almacena memoria **máquina-legible** en `memory.json` por agente: `identity`, `preferences`, `projects`, `relationships`, `wishes`, `notes`, `companies`, `clients`.
- **Recorte automático** al guardar según `MEMORY_MAX_CHARS` (por defecto 2200), eliminando entradas más antiguas primero.
- **`format-prompt`**: genera un bloque Markdown breve para inyectar en el contexto del modelo (equivalente conceptual a `format_memory_for_prompt` en MK37).

`MEMORY.md` en cada workspace sigue siendo el **changelog / nota humana**; `memory.json` es la **memoria operativa** que el agente puede leer con este skill.

## Requisitos

- `bash`, `jq`

## Uso

Desde la raíz de `jarvis-ecosystem` (o con ruta absoluta al JSON):

```bash
# Inicializar (crea el fichero si no existe)
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json init

# Escribir (categoría / clave / valor)
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json set identity human_name "Abrahan"

# Leer categoría completa o una clave
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json get identity
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json get identity human_name

# Olvidar
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json forget identity human_name

# Texto para prompt
./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json format-prompt

# Forzar recorte
MEMORY_MAX_CHARS=1500 ./skills/global/memory-store/bin/memory-store --file agents/jarvis/memory.json trim
```

## Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `MEMORY_FILE` | — | Ruta al `memory.json` si no usas `--file` |
| `MEMORY_MAX_CHARS` | 2200 | Tamaño máximo aproximado del JSON serializado |
| `MEMORY_MAX_VALUE_LEN` | 380 | Trunca valores largos al escribir |

## Integración OpenClaw

Registrar el binario en el `PATH` del agente o invocar con ruta absoluta en automatizaciones / `exec` según tu gateway y `APPROVAL_GATES.md`.
