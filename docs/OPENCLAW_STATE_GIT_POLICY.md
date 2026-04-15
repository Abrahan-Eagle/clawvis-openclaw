# Política Git: `openclaw-state/`

**Objetivo:** no versionar datos de **runtime** del gateway OpenClaw que cambian en cada sesión, contienen conversaciones o secretos, o inflan el repositorio sin valor reproducible.

## Qué NO va en git

| Ruta / patrón | Motivo |
|---------------|--------|
| `openclaw-state/.env` | Secretos y variables locales |
| `openclaw-state/agents/**/sessions/` | Transcripts JSONL (privacidad, volumen) |
| `openclaw-state/memory/*.sqlite` | Memoria SQLite del gateway (estado volátil) |
| `openclaw-state/openclaw.json.bak*` | Copias de respaldo locales |
| `openclaw-state/credentials/` | Ya ignorado; credenciales de canales |
| `openclaw-state/browser/.../user-data/` | Perfil Chromium pesado |

## Qué puede seguir versionado (opcional por equipo)

- `openclaw-state/workspace/` u otras instantáneas **solo si** se acuerda explícitamente (documentación embebida, plantillas).
- `openclaw-state/openclaw.json` **sin secretos** — preferir plantilla en `config/openclaw-home/openclaw.json` y no duplicar claves en el repo.

## Restauración

El estado real vive en `~/.openclaw/` en la máquina de referencia. Para respaldo operativo, ver [RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md).
