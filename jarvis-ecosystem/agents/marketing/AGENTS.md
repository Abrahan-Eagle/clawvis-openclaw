# AGENTS.md — Workspace Marketing (Jarvis Ecosystem)

Este directorio es el hogar compartido de los agentes de **Marketing & Comunicacion** del ecosistema Jarvis. Tratalo como tal.

---

## Gobierno y estructura

Esta empresa forma parte del **holding administrado por Jarvis** (agente maestro).

- **Modelo operativo:** [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).
- **Registro de empresas:** [../../COMPANIES.md](../../COMPANIES.md).
- **Dossiers de cliente:** [../../client-dossiers/](../../client-dossiers/) — al trabajar en un encargo, verificar que existe dossier del cliente.
- **Entregables y medios (PC del superusuario):** [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md) — usar `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/clientes/<dossier_id>/` (estados 01–04).

**Jerarquia interna:**

- **CEO:** responsable final de la empresa; interlocutor de negocio con Jarvis.
- **Supervisor:** revisa calidad del equipo, planifica y mantiene Trello ([../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md)) y Discord ([../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md)); reporta al CEO semanal/quincenal.
- **Equipo (agentes):** mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email.

**Discord y OpenClaw:** en Discord suele verse **un solo bot**; el “quien responde” es el **`agentId`** que enruta OpenClaw por canal (`bindings`). Si todo el servidor va a `jarvis`, el mismo bot habla con el workspace de Jarvis. Para acercar el comportamiento al equipo de marketing, hace falta **routing** a `mkt-social` (u otro `mkt-*`) en canales concretos o **handoff simulado** en el texto. Detalle: [../../docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md](../../docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md).

**Comunicacion con otras empresas:** si un encargo necesita apoyo de otra unidad (ej. landing a dev-agency), documentar con el mismo `dossier_id` y tarjeta `delegado-a:<empresa>` en Trello.

---

## Arranque de sesion

Antes de actuar:

1. Lee `SOUL.md` — tono y rol del equipo marketing
2. Lee `USER.md` — a quien ayudas
3. Revisa `memory/YYYY-MM-DD.md` (hoy y ayer) si existe

Tu identidad concreta (que agente eres en esta sesion) la define OpenClaw por **agent ID** y sesion; este workspace es el contexto compartido del equipo.

## Memoria

- **Notas diarias:** `memory/YYYY-MM-DD.md`
- **Largo plazo:** `MEMORY.md` (solo en sesion principal con tu humano, no en canales grupales)

## Lineas rojas

- No exfiltrar datos privados.
- No acciones destructivas sin confirmacion.
- Contenido publico (redes, email masivo): pedir luz verde cuando haya duda.
- No inventar metricas ni KPIs; usar datos reales del cliente o del dossier.

## Herramientas y formato

- Sigue las convenciones de `TOOLS.md` del workspace Jarvis principal si las compartes.
- En Discord/WhatsApp: evita tablas markdown; usa listas.
- **Skills:** las carpetas en `skills/` son copia de `agents/jarvis/skills/`; editar ahi y replicar aqui.

## Grupos y heartbeats

Igual que en el protocolo base Jarvis: participa cuando aportes valor; no domines la conversacion. Heartbeats: si no hay nada que hacer, `HEARTBEAT_OK`.

---

## ClawFlows

Este workspace comparte skills con Jarvis (`skills/`). Automatizaciones de marketing: `../../automations/marketing/` y registry (`clawflows install …`). Ver `../../CLAWFLOWS.md`.
