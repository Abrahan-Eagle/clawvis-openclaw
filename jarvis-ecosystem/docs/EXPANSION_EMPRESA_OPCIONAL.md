# Expansion: activar dev-agency, legal o contadores (Fase 6)

**Cuando:** el superusuario decida abrir una nueva linea de negocio en el holding.

**Procedimiento:** seguir el checklist completo en [../COMPANIES.md](../COMPANIES.md) (seccion **Checklist: dar de alta una empresa nueva**).

**Resumen:**

1. Crear `agents/<id>/` (IDENTITY, AGENTS, SOUL, USER) tomando `agents/marketing/` como plantilla.
2. Actualizar tabla en `COMPANIES.md`: estado **Activa**, workspace, CEO/Supervisor en [ASIGNACION_ROLES.md](ASIGNACION_ROLES.md).
3. Anadir entradas en `~/.openclaw/openclaw.json` (`agents.list`) apuntando al nuevo workspace.
4. Apuntar el workspace nuevo a skills compartidas en `agents/jarvis/skills/` (ver [../agents/jarvis/AGENTS.md](../agents/jarvis/AGENTS.md)); no duplicar carpetas de skills salvo excepciones documentadas (p. ej. `career-ops` en Ventas).
5. Trello: board por empresa; documentar IDs en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md).
6. Discord: [DISCORD_ESTRUCTURA_CHECKLIST.md](DISCORD_ESTRUCTURA_CHECKLIST.md).
7. Automatizaciones opcionales en `automations/<id>/`.
8. `systemctl --user restart openclaw-gateway`.

**Criterio de hecho:** fila en `COMPANIES.md` con estado Activa y ruta de workspace real.
