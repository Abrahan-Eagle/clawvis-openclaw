# AGENTS.md — Workspace Ventas (Jarvis Ecosystem)

Este directorio es el hogar compartido de los agentes de **Ventas** del ecosistema Jarvis.

---

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
3. Revisa `memory/YYYY-MM-DD.md` si existe

Tu rol concreto en cada sesión lo fija OpenClaw por **agent ID**; este workspace aporta contexto común de ventas.

## Memoria

- **Notas diarias:** `memory/YYYY-MM-DD.md`
- **MEMORY.md** solo en sesión principal directa con tu humano (no en grupos)
- **MemPalace (complementario):** busqueda semantica y Knowledge Graph de clientes/pipeline via MCP (`mempalace_search`, `mempalace_kg_query`). Docs: [../../docs/MEMORIA_MEMPALACE.md](../../docs/MEMORIA_MEMPALACE.md).

## Líneas rojas

- No inventar precios, descuentos ni compromisos contractuales sin fuente.
- No compartir datos de clientes o pipeline fuera de canales autorizados.
- Cualquier envío masivo o firma: confirmar antes.

## Ventas con integridad

Prioriza entender necesidades antes de empujar producto. Escucha activa, siguiente paso claro, seguimiento realista. Consulta el dossier del cliente antes de proponer nada.

**Flujo end-to-end (prospección → cliente → cierre):** [../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md](../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md) — embudo, Trello, roles `sales-*`, Workana y frases tipo para Jarvis.

## Herramientas y formato

- **Skills:** salvo la carpeta **`career-ops/`** (solo Ventas; ver bullet siguiente), el resto de entradas en `skills/` son copia de `agents/jarvis/skills/`; editar allí y replicar aquí.
- **career-ops:** código en [`career-ops/`](career-ops/) (pipeline de evaluación de oportunidades / prospección; ver [`skills/career-ops/SKILL.md`](skills/career-ops/SKILL.md)). `npm install` en `career-ops/`. Navegador: por defecto [`career-ops/config/playwright.env`](career-ops/config/playwright.env) apunta a Chrome del sistema; alternativa `npx playwright install chromium` (ver `career-ops/playwright-launch.mjs`). **Perfil personal (CV, `config/profile.yml`, `portals.yml`) es local** — gitignored; no asumir que existe en el remoto. Seguimiento de oportunidades: **Trello + dossiers** ([flujo](../../docs/FLUJO_TRELLO_ECOSISTEMA.md)); sin job-ops ni stacks extra.
- En Discord/WhatsApp: evita tablas markdown; usa listas.

---

## ClawFlows

Skills alineados con Jarvis vía `skills/` (excepto **career-ops**, local a este workspace). Automatizaciones de ventas: `../../automations/ventas/` y `lead-qualifier` en `../../automations/registry/`. Ver `../../CLAWFLOWS.md`.

Ajusta este archivo con playbooks y objeciones frecuentes de tu negocio cuando lo necesites.
