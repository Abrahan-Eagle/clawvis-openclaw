# Verificación Fase 4 — Discord / Telegram (documental)

**Objetivo:** comprobar que la **documentación del ecosistema Jarvis** refleja que Discord y Telegram **ya operan vía OpenClaw**, no que falte integrar.

**Integraciones (estado técnico):** [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md).

---

## Checklist (solo coherencia doc ↔ realidad)

- [ ] [MEMORY.md](../agents/jarvis/MEMORY.md) indica integración OpenClaw configurada para Discord/Telegram (sin asumir servidor “pendiente de crear”).
- [ ] [DISCORD_ESTRUCTURA_CHECKLIST.md](DISCORD_ESTRUCTURA_CHECKLIST.md) se usa como guía de **organización** de canales/roles si se amplía el equipo, no como “paso 1 instalar Discord”.
- [ ] [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) consultada cuando haya que nombrar canales alineados al holding.
- [ ] Esqueleto de canales en el servidor **Jarvis** creado según [BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) §2 (Dirección / Operación / Clientes).

---

## Qué no es esta verificación

- No sustituye crear canales o roles en Discord (eso es en la app Discord / política del superusuario).
- No valida tokens: viven fuera del repo (`~/.openclaw/`).
