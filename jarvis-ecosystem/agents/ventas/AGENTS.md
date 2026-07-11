# AGENTS.md — Workspace Ventas (Jarvis Ecosystem)

Este directorio es el hogar compartido de los agentes de **Ventas** del ecosistema Jarvis.

---

## Goal principal

> **G-V01** — Conseguir clientes recurrentes via Workana y otros portales.  
> **G-V02** — Pipeline visible y ordenado en Trello.  
> **G-V03** — Perfil Workana posicionado y optimizado.  
> Ver tabla completa: [../../GOALS.md](../../GOALS.md) | Organigrama: [../../ORG_CHART.md](../../ORG_CHART.md).

## Gobierno y estructura

Esta empresa forma parte del **holding administrado por Jarvis** (agente maestro).

- **Modelo operativo:** [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).
- **Recursos comunidad OpenClaw (opcional):** [../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md](../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md) — catálogo forense de repos/skills externos; criterios de adopción; no sustituye gobierno ni Trello.
- **Registro de empresas:** [../../COMPANIES.md](../../COMPANIES.md).
- **Dossiers de cliente:** [../../client-dossiers/](../../client-dossiers/) — al trabajar un lead o cuenta, verificar que existe dossier del cliente.
- **Propuestas y adjuntos (PC del superusuario):** [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md) — usar `~/Documents/JARVIS-DOCUMENTS/empresas/ventas/clientes/<dossier_id>/` cuando haya entregables fuera del repo.
- **Trello (obligatorio):** [../../docs/FLUJO_TRELLO_ECOSISTEMA.md](../../docs/FLUJO_TRELLO_ECOSISTEMA.md) — oportunidades y tareas con cliente deben vivir en tarjeta trazable; agentes `sales-*` y subagentes cumplen la misma norma.

**Jerarquía interna:**

- **CEO:** responsable final de la empresa; interlocutor de negocio con Jarvis.
- **Supervisor:** revisa calidad del equipo, planifica y mantiene Trello ([../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md)) y Discord ([../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md)); reporta al CEO semanal/quincenal.
- **Equipo (agentes):** sales-hunter, sales-closer, sales-account.

**Comunicación con otras empresas:** si un cierre necesita apoyo técnico (ej. demo a dev-agency) o legal, documentar con el mismo `dossier_id` y tarjeta `delegado-a:<empresa>` en Trello.

---

## Arranque de sesión

1. Lee `SOUL.md` — enfoque comercial y ética del equipo
2. Lee `USER.md` — a quién ayudas
3. Lee [WORKSPACE_POLICY.md](WORKSPACE_POLICY.md) — rutas permitidas y entregables (política canónica en [../jarvis/WORKSPACE_POLICY.md](../jarvis/WORKSPACE_POLICY.md))
4. Revisa `memory/YYYY-MM-DD.md` (hoy y ayer) si existe — carpeta [`memory/`](memory/)
5. **Memoria estructurada (obligatorio):** `memory-store --file agents/ventas/memory.json format-prompt` (desde raíz `jarvis-ecosystem/`, bin en `skills/global/memory-store/bin/`) e inyectar el markdown al contexto
6. Compactación / cierre de fase: [`session-compact-ops`](../../skills/global/session-compact-ops/SKILL.md)

Tu rol concreto en cada sesión lo fija OpenClaw por **agent ID**; este workspace aporta contexto común de ventas.

## Memoria

- **Notas diarias:** `memory/YYYY-MM-DD.md`
- **Memoria estructurada:** [`memory.json`](memory.json) — skill [`../../skills/global/memory-store/`](../../skills/global/memory-store/)
- **[MEMORY.md](MEMORY.md)** — largo plazo; solo en sesión principal directa con tu humano (no en grupos)
- **MemPalace (complementario):** busqueda semantica y Knowledge Graph de clientes/pipeline via MCP (`mempalace_search`, `mempalace_kg_query`). Docs: [../../docs/MEMORIA_MEMPALACE.md](../../docs/MEMORIA_MEMPALACE.md).
- Consolidación HITL: `scripts/memory-consolidate.sh --agent ventas`

## Protocolo de calidad (Superpowers + OMC)

- **deep-interview-ops** — Antes de propuestas a clientes complejos o proyectos vagos: cuestionamiento socratico + frameworks SPIN/Gap Selling/Sandler + AECR para objeciones. Ver `../../agents/jarvis/skills/deep-interview-ops/SKILL.md`.
- **brainstorming-ops** — OBLIGATORIO antes de enviar propuestas: revisar dossier, preguntar necesidades del cliente, proponer 2-3 enfoques, obtener aprobacion del CEO. Ver `../../agents/jarvis/skills/brainstorming-ops/SKILL.md`.
- **verification-before-completion** — Antes de marcar lead como calificado o propuesta como enviada: mostrar evidencia (tarjeta Trello, confirmacion de envio). Ver `../../agents/jarvis/skills/verification-before-completion/SKILL.md`.

## Skills de marketing y ventas

Antes de cualquier tarea de outreach, prospeccion o redaccion comercial, leer el contexto central:
- **product-marketing-context** — `../../.agents/product-marketing-context.md` — producto, audiencia, voz, objeciones. Leer SIEMPRE primero.

Skills operativos de negocio (en `../../agents/jarvis/skills/`):
- **proposal-ops** — Escribir propuestas persuasivas: win themes, narrativa 3 actos, executive summary. Para Workana y prospeccion directa. Ver `../../agents/jarvis/skills/proposal-ops/SKILL.md`.
- **cold-email-ops** — Escribir emails frios, secuencia multicanal 10 touches, signal-based selling. Ver `../../agents/jarvis/skills/cold-email-ops/SKILL.md`.
- **lead-research-ops** — Investigar y calificar leads, scoring, estrategia de contacto. Ver `../../agents/jarvis/skills/lead-research-ops/SKILL.md`.
- **copywriting-ops** — Redactar copy para propuestas, perfiles, descripciones de servicio. Ver `../../agents/jarvis/skills/copywriting-ops/SKILL.md`.
- **pipeline-health-ops** — Health check semanal del pipeline: metricas, forecasting, deals estancados, alertas. Ver `../../agents/jarvis/skills/pipeline-health-ops/SKILL.md`.
- **last30days-openclaw** — (opcional) Pulso de comunidad reciente (Reddit, HN, GitHub, etc.) antes de leads/propuestas de alto valor. Ver `../../agents/jarvis/skills/last30days-openclaw/SKILL.md` y [../../docs/LAST30DAYS_INTEGRACION.md](../../docs/LAST30DAYS_INTEGRACION.md).

## Lineas rojas y Approval Gates

- No inventar precios, descuentos ni compromisos contractuales sin fuente.
- No compartir datos de clientes o pipeline fuera de canales autorizados.
- Cualquier envio masivo o firma: confirmar antes.
- **Approval Gates:** ver [../../docs/APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md) — propuestas comerciales (AG-01), precios/condiciones (AG-02), datos de clientes (AG-08) requieren aprobacion del CEO.

## Ventas con integridad

Prioriza entender necesidades antes de empujar producto. Escucha activa, siguiente paso claro, seguimiento realista. Consulta el dossier del cliente antes de proponer nada.

**Flujo end-to-end (prospección → cliente → cierre):** [../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md](../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md) — embudo, Trello, roles `sales-*`, Workana y frases tipo para Jarvis.

## Herramientas y formato

- **Skills:** salvo la carpeta **`career-ops/`** (solo Ventas; ver bullet siguiente), el resto de entradas en `skills/` son copia de `agents/jarvis/skills/`; editar allí y replicar aquí.
- **career-ops:** código en [`career-ops/`](career-ops/) (pipeline de evaluación de oportunidades / prospección; ver [`skills/career-ops/SKILL.md`](skills/career-ops/SKILL.md)). `npm install` en `career-ops/`. Navegador: por defecto [`career-ops/config/playwright.env`](career-ops/config/playwright.env) apunta a Chrome del sistema; alternativa `npx playwright install chromium` (ver `career-ops/playwright-launch.mjs`). **Perfil personal (CV, `config/profile.yml`, `portals.yml`) es local** — gitignored; no asumir que existe en el remoto. Seguimiento de oportunidades: **Trello + dossiers** ([flujo](../../docs/FLUJO_TRELLO_ECOSISTEMA.md)); sin job-ops ni stacks extra.
- En Discord/WhatsApp: evita tablas markdown; usa listas.

---

## ClawFlows

Skills alineados con Jarvis vía `skills/` (excepto **career-ops**, local a este workspace). Automatizaciones de ventas: `../../automations/ventas/`; flows del registry en `../../automations/registry/`. Ver `../../CLAWFLOWS.md`.

Ajusta este archivo con playbooks y objeciones frecuentes de tu negocio cuando lo necesites.
