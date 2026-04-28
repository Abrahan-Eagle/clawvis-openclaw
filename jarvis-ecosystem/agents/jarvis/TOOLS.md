# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## ClawFlows / Jarvis (2026-03)

- **Memoria estructurada:** `../../skills/global/memory-store/` + `memory.json` (misma carpeta de agente).
- **Core prompt (protocolo compartido):** `../../skills/global/core-prompt.md`.
- **Nuevos skills en repo (2026-04, forense MK37):** `../../skills/weather-report/`, `../../skills/youtube-transcript/`, `../../skills/browser-playwright/`, orquestación `../../skills/planner/`, `task-queue/`, `executor/`, `error-recovery/` (ver `../../docs/FORENSE_JARVIS_MK37.md`).
- **v2 abril 2026 — coordinacion + RRSS local (todos free / sin GPU):**
  - Coordinacion: `../../skills/global/activity-log/`, `../../skills/global/handoff/` (con schemas JSON), `../../skills/global/coordinator/`. Ver [../../docs/COORDINACION_AGENTES.md](../../docs/COORDINACION_AGENTES.md).
  - Pipeline carruseles: `../../skills/brand-kit/`, `../../skills/image-render/` (Pillow), `../../skills/image-ai-free/` (Pollinations), `../../skills/carousel-render/`. Ver [../../docs/CAROUSEL_PIPELINE_FREE.md](../../docs/CAROUSEL_PIPELINE_FREE.md).
  - Pipeline reels/tiktoks: `../../skills/tts-free/` (Edge TTS), `../../skills/subtitles/`, `../../skills/video-compose/` (ffmpeg), `../../skills/video-short/` (Remotion, esqueleto). Ver [../../docs/REELS_TIKTOK_PIPELINE_FREE.md](../../docs/REELS_TIKTOK_PIPELINE_FREE.md).
  - Approval gates nuevos: **AG-12** (publicar contenido) y **AG-13** (uso de IA generativa). Ver [../../docs/APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md).
  - Estado runtime no versionado: `../../state/` (gitignored). Manifest de cada asset: `out/<brand>/<slug>/index.json` con `ai_used` declarado.
- **Automatizaciones**: raíz del ecosistema `../../automations/` — ver `../../CLAWFLOWS.md`.
- **CLI**: `clawflows`; cargar entorno con `source ../../scripts/clawflows-env.sh` (y opcionalmente `../../.env` para Ollama). Ver `../../CLAWFLOWS.md`.
- **Skills instalados** (también enlazados desde marketing/ventas): `gog`, `himalaya`, `xurl`, `slack`, `blogwatcher`, `summarize`, `notion`, `trello`, `session-logs`, `nano-pdf`, `mcporter`, `tmux`, `video-frames` bajo `./skills/<nombre>/`.
- **ClawHub CLI**: `clawhub` (npm global) para buscar/instalar más skills.
- `lobster` está permitido en `~/.openclaw/openclaw.json` → `tools.alsoAllow`.

Configura credenciales por skill según cada `SKILL.md` (Google, Notion, Trello, etc.).

## OpenClaw: canales ya integrados

**Trello, Discord y Telegram** están configurados en el gateway OpenClaw (`~/.openclaw/openclaw.json` y `~/.openclaw/.env` donde aplique). Resumen para Jarvis: [../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md). Para **crear tableros/listas** hace falta token Trello con escritura + herramienta `exec`: [../../docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md](../../docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md).

## Variables de entorno (referencia en el monorepo)

No pegues API keys en este archivo; usa `~/.openclaw/.env` u otra tienda segura.

| Integración | Documentación |
|-------------|----------------|
| Trello + OpenClaw | [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md), [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md) (`TRELLO_*`, `exec`, `jq`) |
| Ollama local | Variables `OLLAMA_*` en [`.env`](../../.env) del ecosistema (ejemplo) |

Otras skills (Notion, Slack, etc.): seguir el `SKILL.md` de cada carpeta bajo `./skills/<nombre>/`.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Telegram

- Token del bot (BotFather) y chat: configurar en `~/.openclaw` / canal Telegram; **no** guardar secretos en este repo.