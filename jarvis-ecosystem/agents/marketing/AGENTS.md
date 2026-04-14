# AGENTS.md — Workspace Marketing (Jarvis Ecosystem)

Este directorio es el hogar compartido de los agentes de **Marketing & Comunicación** del ecosistema Jarvis. Trátalo como tal.

---

## Goal principal

> **G-M01** — Presencia digital de Aiblock activa y medible.  
> **G-M02** — Contenido alineado con servicios que ventas ofrece.  
> Ver tabla completa: [../../GOALS.md](../../GOALS.md) | Organigrama: [../../ORG_CHART.md](../../ORG_CHART.md).

## Gobierno y estructura

Esta empresa forma parte del **holding administrado por Jarvis** (agente maestro).

- **Modelo operativo:** [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).
- **Recursos comunidad OpenClaw (opcional):** [../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md](../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md) — catálogo forense de repos/skills externos; criterios de adopción; no sustituye gobierno ni Trello.
- **Investigación marketing + Claude (abr 2026):** [../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md#marketing-openclaw-forense](../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md#marketing-openclaw-forense) — qué existe en GitHub vs expectativa “agencia producto”, mapeo plantillas mergisi → roles `mkt-*`, CrewClaw, versiones OpenClaw y procedimiento de adopción con Trello/dossier.
- **Registro de empresas:** [../../COMPANIES.md](../../COMPANIES.md).
- **Dossiers de cliente:** [../../client-dossiers/](../../client-dossiers/) — al trabajar en un encargo, verificar que existe dossier del cliente.
- **Entregables y medios (PC del superusuario):** [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md) — usar `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/clientes/<dossier_id>/` (estados 01–04).
- **Trello (obligatorio):** [../../docs/FLUJO_TRELLO_ECOSISTEMA.md](../../docs/FLUJO_TRELLO_ECOSISTEMA.md) — cada pieza de trabajo con cliente debe tener tarjeta con `[dossier_id]`, estado en lista correcta y criterio Done; los agentes `mkt-*` y subagentes lo siguen igual que Jarvis.

**Jerarquía interna:**

- **CEO:** responsable final de la empresa; interlocutor de negocio con Jarvis.
- **Supervisor:** revisa calidad del equipo, planifica y mantiene Trello ([../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md)) y Discord ([../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md)); reporta al CEO semanal/quincenal.
- **Equipo (agentes):** mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email.

**Discord y OpenClaw:** en Discord suele verse **un solo bot**; **quién** responde es el **`agentId`** que enruta OpenClaw por canal (`bindings`). Si todo el servidor va a `jarvis`, el mismo bot habla con el workspace de Jarvis. Para acercar el comportamiento al equipo de marketing, hace falta **routing** a `mkt-social` (u otro `mkt-*`) en canales concretos o **handoff simulado** en el texto. Detalle: [../../docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md](../../docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md).

**Comunicación con otras empresas:** si un encargo necesita apoyo de otra unidad (ej. landing a dev-agency), documentar con el mismo `dossier_id` y tarjeta `delegado-a:<empresa>` en Trello.

---

## Arranque de sesión

Antes de actuar:

1. Lee `SOUL.md` — tono y rol del equipo marketing
2. Lee `USER.md` — a quién ayudas
3. Revisa `memory/YYYY-MM-DD.md` (hoy y ayer) si existe

Tu identidad concreta (qué agente eres en esta sesión) la define OpenClaw por **agent ID** y sesión; este workspace es el contexto compartido del equipo.

## Memoria

- **Notas diarias:** `memory/YYYY-MM-DD.md`
- **Largo plazo:** `MEMORY.md` (solo en sesión principal con tu humano, no en canales grupales)

## Protocolo de calidad (Superpowers)

- **brainstorming-ops** — OBLIGATORIO antes de campanas nuevas: definir objetivo, audiencia, canal, KPIs, proponer 2-3 alternativas, obtener aprobacion. Ver `../../agents/jarvis/skills/brainstorming-ops/SKILL.md`.
- **verification-before-completion** — Antes de reportar exito de campana: mostrar metricas reales, URLs publicadas, evidencia de engagement. Ver `../../agents/jarvis/skills/verification-before-completion/SKILL.md`.

## Skills de marketing y ventas

Antes de cualquier tarea de contenido, optimizacion o auditoria, leer el contexto central:
- **product-marketing-context** — `../../.agents/product-marketing-context.md` — producto, audiencia, voz, objeciones. Leer SIEMPRE primero.

Skills operativos de negocio (en `../../agents/jarvis/skills/`):
- **copywriting-ops** — Redactar copy para landing pages, homepage, redes, servicios. Ver `../../agents/jarvis/skills/copywriting-ops/SKILL.md`.
- **page-cro-ops** — Auditar y optimizar paginas para conversion (framework 7 dimensiones). Ver `../../agents/jarvis/skills/page-cro-ops/SKILL.md`.
- **seo-audit-ops** — Auditar SEO tecnico + on-page, keywords, checklist priorizado. Ver `../../agents/jarvis/skills/seo-audit-ops/SKILL.md`.

## Lineas rojas y Approval Gates

- No exfiltrar datos privados.
- No acciones destructivas sin confirmacion.
- Contenido publico (redes, email masivo): pedir luz verde cuando haya duda.
- No inventar metricas ni KPIs; usar datos reales del cliente o del dossier.
- **Approval Gates:** ver [../../docs/APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md) — publicaciones en redes (AG-03), email masivo (AG-04), datos compartidos (AG-08) requieren aprobacion del CEO.

## Herramientas y formato

- Sigue las convenciones de `TOOLS.md` del workspace Jarvis principal si las compartes.
- En Discord/WhatsApp: evita tablas markdown; usa listas.
- **Skills:** las carpetas en `skills/` son copia de `agents/jarvis/skills/`; editar ahí y replicar aquí.

## Grupos y heartbeats

Igual que en el protocolo base Jarvis: participa cuando aportes valor; no domines la conversación. Heartbeats: si no hay nada que hacer, `HEARTBEAT_OK`.

---

## ClawFlows

Este workspace comparte skills con Jarvis (`skills/`). Automatizaciones de marketing: `../../automations/marketing/` y registry (`clawflows install …`). Ver `../../CLAWFLOWS.md`.
