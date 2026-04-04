# Integraciones ya configuradas en OpenClaw

**Estado:** Trello, Discord y Telegram **ya están enlazados al gateway OpenClaw** (`~/.openclaw/openclaw.json`, variables en `~/.openclaw/.env` según cada integración). Jarvis **no** debe asumir que hay que “instalar desde cero” esas conexiones; la fuente operativa es la configuración del gateway.

---

## Qué implica para el agente

1. **No** proponer reconfigurar credenciales salvo que el superusuario lo pida.
2. Para **Trello** (API / skill): credenciales y uso con `curl`/`jq` — [../../docs/TRELLO_OPENCLAW.md](../../docs/TRELLO_OPENCLAW.md).
3. **Discord y Telegram:** canales y bindings los define OpenClaw; las plantillas de organización ([PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md)) son referencia de **roles y nombres**, no un checklist de integración técnica pendiente.
4. Convención de negocio tableros/clientes: [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md).

---

## Seguridad

- **No** commitear tokens, `openclaw.json` completo con secretos, ni contenido de `.env`.
- Tablas de referencia en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md) pueden listar IDs públicos de tablero Trello si el superusuario lo desea; no pegar API keys.

## Permisos para automatizar (Trello escritura, exec, Discord bot)

Checklist y comandos de verificación: [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md).

---

## Historial

- **2026-04-04:** Documento añadido para alinear el ecosistema Jarvis con el estado real de integraciones OpenClaw.
- **2026-04-04:** Enlace a [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md) (token Trello escritura, `exec`, Discord).
