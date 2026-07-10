# Política Git: `openclaw-state/`

**Objetivo:** no versionar datos de **runtime** del gateway OpenClaw que cambian en cada sesión, contienen conversaciones o secretos, o inflan el repositorio sin valor reproducible.

## Qué NO va en git

| Ruta / patrón | Motivo |
|---------------|--------|
| `openclaw-state/.env` | Secretos y variables locales |
| `openclaw-state/agents/**/sessions/` | Transcripts JSONL (privacidad, volumen) |
| `openclaw-state/agents/**/auth-profiles.json` | Perfiles de auth de proveedores |
| `openclaw-state/identity/` | Claves PEM del dispositivo (`device.json`) |
| `openclaw-state/devices/` | Tokens operator / pairing |
| `openclaw-state/delivery-queue/` | Cola de mensajes (puede incluir teléfonos) |
| `openclaw-state/logs/` | Auditoría local |
| `openclaw-state/cron/runs/` | sessionIds de corridas |
| `openclaw-state/cron/*.bak` / `jobs.json.bak` | Backups de cron |
| `openclaw-state/memory/*.sqlite` | Memoria SQLite del gateway (estado volátil) |
| `openclaw-state/openclaw.json.bak*` | Copias de respaldo locales |
| `openclaw-state/credentials/` | Credenciales de canales |
| `openclaw-state/browser/.../user-data/` | Perfil Chromium pesado |
| `openclaw-state/browser/.../user-data.bak/` | Restos de perfil Chromium |

Misma higiene en la plantilla: `config/openclaw-home/cron/runs/`, `devices/`, etc. (ver `.gitignore` raíz y `config/openclaw-home/.gitignore`).

**Verificación:** `bash scripts/check-no-secrets.sh` (solo archivos trackeados).

## Qué puede seguir versionado (opcional por equipo)

- `openclaw-state/workspace/` u otras instantáneas **solo si** se acuerda explícitamente (documentación embebida, plantillas). Hoy hay un espejo grande de docs OpenClaw (~819 archivos) — candidato a destrackear.
- `openclaw-state/openclaw.json` **sin secretos** — preferir plantilla en `config/openclaw-home/openclaw.json` y no duplicar claves en el repo.

## Restauración

El estado real vive en `~/.openclaw/` en la máquina de referencia. Para plantilla reproducible usa **`config/openclaw-home/`**. Respaldo operativo: [RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md).
