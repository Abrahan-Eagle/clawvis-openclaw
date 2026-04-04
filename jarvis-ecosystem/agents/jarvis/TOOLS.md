# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## ClawFlows / Jarvis (2026-03)

- **Automatizaciones**: raíz del ecosistema `../../automations/` — ver `../../CLAWFLOWS.md`.
- **CLI**: `clawflows`; cargar entorno con `source ../../scripts/clawflows-env.sh` (y opcionalmente `../../.env` para Ollama). Ver `../../CLAWFLOWS.md`.
- **Skills instalados** (también enlazados desde marketing/ventas): `gog`, `himalaya`, `xurl`, `slack`, `blogwatcher`, `summarize`, `notion`, `trello`, `session-logs`, `nano-pdf`, `mcporter`, `tmux`, `video-frames` bajo `./skills/<nombre>/`.
- **ClawHub CLI**: `clawhub` (npm global) para buscar/instalar más skills.
- `lobster` está permitido en `~/.openclaw/openclaw.json` → `tools.alsoAllow`.

Configura credenciales por skill según cada `SKILL.md` (Google, Notion, Trello, etc.).

## Variables de entorno (referencia en el monorepo)

No pegues API keys en este archivo; usa `~/.openclaw/.env` u otra tienda segura.

| Integración | Documentación |
|-------------|----------------|
| Trello + OpenClaw | [docs/TRELLO_OPENCLAW.md](../../../docs/TRELLO_OPENCLAW.md) (`TRELLO_API_KEY`, `TRELLO_TOKEN`, `exec`, `jq`) |
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