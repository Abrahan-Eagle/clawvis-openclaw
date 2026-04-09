# Checklist operativo — ecosistema Jarvis (P0 / P1)

Documento de **operación recurrente** para el holding Jarvis + OpenClaw. No sustituye el gobierno en [jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md) ni el flujo Trello.

## P0 — antes de depender del stack para un cliente o un cierre

| # | Comprobación | Comando / acción |
|---|----------------|------------------|
| 1 | `~/.jarvis-ecosystem` apunta al repo que editas | `readlink -f ~/.jarvis-ecosystem` y comparar con la ruta del clon |
| 2 | Gateway OpenClaw responde | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/` → `200` |
| 3 | Proxy Cursor (si lo usas) | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4646/v1/models` → `200` |
| 4 | Canales configurados | `openclaw channels list` / `openclaw channels status` |
| 5 | `plugins.allow` incluye cada canal activo + `browser` si aplica | `grep -A10 '"allow"' ~/.openclaw/openclaw.json` |
| 6 | Agente responde | `openclaw agent --agent jarvis --message "ping"` |
| 7 | Secretos fuera de Git | No commitear `~/.openclaw/.env`; repo privado si hay datos sensibles |
| 8 | Gobierno humano | Tablero Trello vivo; CEO/supervisor real por empresa; cliente en dossier, no solo en chat |

**Frecuencia sugerida:** semanal si el stack es crítico; como mínimo antes de una semana intensa de clientes.

## P1 — estabilidad y recuperación

| # | Comprobación | Notas |
|---|----------------|--------|
| 1 | Respaldo fechado de `~/.openclaw` (json relevante, sin pegar tokens en sitios inseguros) | Ver [RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md) |
| 2 | Mismo usuario Linux para gateway y Agent Town | Evita rutas de sesión inconsistentes |
| 3 | `loginctl enable-linger` si necesitas servicios `--user` sin login gráfico | Servidores headless |
| 4 | Rutas de sesión normalizadas | Si migraste de otro usuario, revisar `~/.openclaw/agents/*/sessions/` |
| 5 | Modelos y coste | Revisar `agents.defaults.model` y `agents.list` en `openclaw.json`; fallbacks probados |
| 6 | Career-ops personal | Tras cambiar `profile.yml` / `portals.yml`, validar búsquedas a mano (Workana/LinkedIn pueden exigir login) |

## Qué no es “producción” en sentido SaaS

- No hay un despliegue único que valide todo el monorepo; la fiabilidad depende de **disciplina** y del host.
- Negociación vinculante con el cliente sigue siendo **humana**; Jarvis apoya borradores y trazabilidad (dossier + Trello).

## Referencias rápidas

- Arranque y puertos: [README.md](../README.md) (raíz del repo)
- Modelos: [MODELOS_JARVIS_OPENCLAW.md](MODELOS_JARVIS_OPENCLAW.md)
- Forense OpenClaw: [OPENCLAW_FORENSE_RUNBOOK.md](OPENCLAW_FORENSE_RUNBOOK.md)
