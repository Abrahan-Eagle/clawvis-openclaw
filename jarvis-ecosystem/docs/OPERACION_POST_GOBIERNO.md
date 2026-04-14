# Operacion post gobierno — indice

Plan operativo en fases (repo en `main`). Documentación de soporte:

| Fase | Objetivo | Documento / recurso |
|------|----------|---------------------|
| 0 | Verificar symlink y gateway | [VERIFICACION_FASE0.md](VERIFICACION_FASE0.md) |
| 1 | CEO y Supervisor | [ASIGNACION_ROLES.md](ASIGNACION_ROLES.md), [../COMPANIES.md](../COMPANIES.md) |
| 2 | Dossiers clientes reales | [../client-dossiers/](../client-dossiers/), [CLIENT_DOSSIER_SCHEMA.md](CLIENT_DOSSIER_SCHEMA.md), [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md) |
| 3 | Trello por empresa | [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md), [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md), [BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md), MEMORY.md (tabla Trello) |
| — | **Ventas: embudo y cierre** | [FLUJO_VENTAS_PROSPECCION_CIERRE.md](FLUJO_VENTAS_PROSPECCION_CIERRE.md) — prospección, cliente, Workana; `agents/jarvis/AGENTS.md` enlaza el protocolo para Jarvis |
| 4 | Discord | [DISCORD_ESTRUCTURA_CHECKLIST.md](DISCORD_ESTRUCTURA_CHECKLIST.md), [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md), [VERIFICACION_DISCORD_FASE4.md](VERIFICACION_DISCORD_FASE4.md), [BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) §2 |
| 5 | Reporte supervisor → CEO | [SUPERVISOR_CEO_REPORTE.md](SUPERVISOR_CEO_REPORTE.md), [plantillas/REPORTE_SUPERVISOR_CEO.md](plantillas/REPORTE_SUPERVISOR_CEO.md) |
| 6 | Nueva empresa (opcional) | [EXPANSION_EMPRESA_OPCIONAL.md](EXPANSION_EMPRESA_OPCIONAL.md) |

**Post-Fase 0 (opcional):** comprobar que exista la carpeta de entregables `~/Documents/JARVIS-DOCUMENTS/` en el PC del superusuario — [VERIFICACION_JARVIS_DOCUMENTS.md](VERIFICACION_JARVIS_DOCUMENTS.md).

**Memoria avanzada (MemPalace):** [MEMORIA_MEMPALACE.md](MEMORIA_MEMPALACE.md) — busqueda semantica local, Knowledge Graph temporal, auto-mine.

**Módulo MemPalace (cierre y replicación):** [MODULO_MEMPALACE_CIERRE.md](MODULO_MEMPALACE_CIERRE.md) — qué va en git, qué no, checklist restore, `deploy/mempalace/`.

**Permisos OpenClaw (automatizar Trello / herramientas):** [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md).

**Forense Paperclip (patrones adoptados, abr 2026):** [FORENSE_PAPERCLIP_RESUMEN.md](FORENSE_PAPERCLIP_RESUMEN.md) — goals, org chart, heartbeats operativos, cost tracking, approval gates. Archivos clave: [../GOALS.md](../GOALS.md), [../ORG_CHART.md](../ORG_CHART.md), [HEARTBEAT_OPERATIVO.md](HEARTBEAT_OPERATIVO.md), [APPROVAL_GATES.md](APPROVAL_GATES.md).

**Forense Superpowers (metodologia + skills, abr 2026):** [FORENSE_SUPERPOWERS_RESUMEN.md](FORENSE_SUPERPOWERS_RESUMEN.md) — brainstorming obligatorio, verificacion antes de completar, debugging sistematico, dev methodology (TDD + code review). Plugin instalado en Cursor. Skills en `agents/jarvis/skills/`.

**Forense Skills Repos (marketing + ventas skills, abr 2026):** [FORENSE_SKILLS_REPOS_RESUMEN.md](FORENSE_SKILLS_REPOS_RESUMEN.md) — patron `product-marketing-context` (`.agents/product-marketing-context.md`), 5 skills operativos: copywriting-ops, cold-email-ops, page-cro-ops, lead-research-ops, seo-audit-ops. AGENTS.md de ventas y marketing actualizados.

**Forense OMC (orquestacion multi-agente, abr 2026):** [FORENSE_OMC_RESUMEN.md](FORENSE_OMC_RESUMEN.md) — deep-interview-ops (cuestionamiento socratico), task-pipeline-ops (plan-spec-exec-verify-fix), structured-commits-ops (git trailers), session-learner-ops (extraccion de patrones), verification-before-completion mejorado con sizing tiers. Skills en `agents/jarvis/skills/`.

**Forense Agency Agents (ventas avanzadas + SEO, abr 2026):** [FORENSE_AGENCY_AGENTS_RESUMEN.md](FORENSE_AGENCY_AGENTS_RESUMEN.md) — 2 skills nuevos: proposal-ops (win themes, narrativa 3 actos, executive summary), pipeline-health-ops (metricas pipeline, forecasting, alertas). 3 skills enriquecidos: deep-interview-ops (+SPIN/Gap Selling/Sandler/AECR), cold-email-ops (+signal-based selling, ICP, secuencia 10 touches), seo-audit-ops (+cannibalization audit, keyword clusters, link building, E-E-A-T).

Modelo de gobierno: [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md).
