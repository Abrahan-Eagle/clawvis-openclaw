# Copia de trabajo de `~/.openclaw` (plantilla sanitizada)

Instantánea para el monorepo [`clawvis-openclaw`](https://github.com/Abrahan-Eagle/clawvis-openclaw): `openclaw.json`, agentes (sin sesiones), `workspace/` con docs, `cron/jobs.json` (sin `runs/`), etc.

## Qué NO debe ir aquí (ni en Git)

| Ítem | Motivo |
|------|--------|
| `.env` | Tokens de bots, API keys reales |
| `credentials/` | Credenciales de canales (WhatsApp, etc.) |
| `agents/**/sessions/` | Transcripts / privacidad |
| `auth-profiles.json` con claves | Auth de proveedores |
| `browser/**/user-data/` | Perfil Chromium |
| `identity/`, `devices/` | PEM y tokens operator |
| `cron/runs/`, `cron/*.bak` | sessionIds / drift de corridas |
| `delivery-queue/`, `logs/` | Runtime / PII |
| `apiKey` reales en `models.json` | Usar placeholders (`OPENROUTER_API_KEY`, `OLLAMA_API_KEY`, `not-needed`, `local`) |

## Placeholders esperados en `models.json`

- OpenRouter → `OPENROUTER_API_KEY` (valor real solo en `~/.openclaw` o env del host)
- Ollama → `OLLAMA_API_KEY` o literal documentado
- Cursor local → `local` / `not-needed`

## Verificación

Desde la raíz del monorepo:

```bash
bash scripts/check-no-secrets.sh
```

En una máquina nueva: copia `~/.openclaw/.env` y las keys reales desde un almacén seguro; **no** las subas a Git.

**Auditoría:** ver [docs/INFORME_FORENSE_360_2026-07.md](../docs/INFORME_FORENSE_360_2026-07.md).
