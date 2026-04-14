# MEMORY.md - Long-term memory

Solo lectura/escritura en sesión principal con el humano (ver `AGENTS.md`).

---

## Holding / empresas

Registro completo: [../../COMPANIES.md](../../COMPANIES.md).

**CEO / Supervisor (Fase 1):** [../../docs/ASIGNACION_ROLES.md](../../docs/ASIGNACION_ROLES.md). Nombres de **ejemplo** por empresa (no el superusuario); ver tabla en ese archivo.

| Empresa | Estado | Notas rapidas |
|---------|--------|---------------|
| marketing | Activa | Workspace `agents/marketing/`. Agentes: mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email. |
| ventas | Activa | Workspace `agents/ventas/`. Agentes: sales-hunter, sales-closer, sales-account. **Flujo comercial (embudo, Trello, Workana, frases para pedir ayuda):** [../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md](../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md). |
| dev-agency | Planificada | Sin workspace aun. |
| legal | Planificada | Sin workspace aun. |
| contadores | Planificada | Sin workspace aun. |

Gobierno operativo: [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).

**Operacion post gobierno (indice):** [../../docs/OPERACION_POST_GOBIERNO.md](../../docs/OPERACION_POST_GOBIERNO.md).

**Archivos en disco (entregables, medios):** solo bajo `~/Documents/JARVIS-DOCUMENTS/` (carpeta **`Documents`**, no `Documentos`) — arbol por empresa y cliente. Especificacion completa: [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md).

**Integraciones OpenClaw (Trello, Discord, Telegram):** ya configuradas en el gateway — ver [../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md). **Permisos para automatizar** (escritura Trello, `exec`, bot Discord): [../../docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md](../../docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md).

---

## Clientes activos (dossiers)

Directorio: [../../client-dossiers/](../../client-dossiers/).  
Plantilla vacia: [../../client-dossiers/cli-PLANTILLA-vacio.json](../../client-dossiers/cli-PLANTILLA-vacio.json).

| dossier_id | Cliente | Empresa asignada | Estado |
|------------|---------|------------------|--------|
| `cli-20260404-ejemplo` | ACME Ferretería C.A. (ejemplo) | marketing | Ejemplo de documentación |
| `cli-20260404-cliente-tests-redes` | Cliente TESTS (IG + FB) | marketing | **Cliente prueba** — depuracion ecosistema; ver [BRIEF_CLIENTE_TESTS_REDES.md](../../client-dossiers/BRIEF_CLIENTE_TESTS_REDES.md) |

---

## Trello (referencia por empresa — Fase 3)

Convencion: [../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md).  
Integracion OpenClaw: **configurada** ([../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)). Credenciales API: solo `~/.openclaw/.env` (`TRELLO_API_KEY`, `TRELLO_TOKEN`).

**Esqueleto (tableros + listas):** guía paso a paso y script — [../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md), script [../../scripts/trello-bootstrap-boards.sh](../../scripts/trello-bootstrap-boards.sh). Si la API devuelve `401`, el token actual es **solo lectura**: crear tableros a mano o regenerar token con escritura en [trello.com/app-key](https://trello.com/app-key).

| Empresa | Board (nombre) | Board ID | Listas / notas |
|---------|----------------|----------|----------------|
| *(legacy)* | Mi tablero de Trello | `69d0a352e4fed9476a5f6cec` | Puede quedar como sandbox; preferir tableros `Empresa-*` para operacion |
| `marketing` | Empresa-marketing - Operaciones | *(rellenar tras crear)* | Backlog → En curso → Revisión supervisor → Bloqueado → Hecho |
| `ventas` | Empresa-ventas - Operaciones | *(rellenar tras crear)* | Listas alineadas al embudo: Inbox → Triaje/Cola → En progreso → En revisión → Listo; ver [FLUJO_VENTAS_PROSPECCION_CIERRE.md](../../docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md) §4. |

---

## Discord (Fase 4)

Integracion OpenClaw: **configurada** (Discord como canal del gateway). Referencia organizativa: [../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md](../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md), [../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md). Verificacion documental: [../../docs/VERIFICACION_DISCORD_FASE4.md](../../docs/VERIFICACION_DISCORD_FASE4.md).

**Esqueleto de canales (servidor Jarvis):** lista concreta en [../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) sección 2 — crear categorías/canales en la app Discord (no automatizable sin bot con permisos).

Telegram: mismo gateway OpenClaw; no repetir integracion desde el repo.

*(Opcional: anotar aquí IDs de servidor/categoría solo si el superusuario quiere que Jarvis los referencie en sesión; evitar secretos.)*

---

## Reportes supervisor → CEO (Fase 5)

Formato: [../../docs/SUPERVISOR_CEO_REPORTE.md](../../docs/SUPERVISOR_CEO_REPORTE.md).  
Plantilla copiable: [../../docs/plantillas/REPORTE_SUPERVISOR_CEO.md](../../docs/plantillas/REPORTE_SUPERVISOR_CEO.md).

---

## Decisiones de gobierno (log)

- **2026-04-14:** **Graphify** integrado como mapa estructural del ecosistema. Instalado via pipx (v0.4.13). Grafo generado: 1369 nodos, 1403 aristas, 128 comunidades. God nodes: README, AGENTS, OPERACION_POST_GOBIERNO, GOBIERNO_JARVIS_V2, MEMORY. Output en `graphify-out/` (gitignored). MCP server registrado en OpenClaw junto a MemPalace. Convención: Graphify = mapa del repo, MemPalace = memoria semántica. Docs: `docs/GRAPHIFY_INTEGRACION.md`.
- **2026-04-14:** Modulo **Forense Agency Agents** completado. Repo msitarzewski/agency-agents (79.9k stars, 144 agentes, 12 divisiones) analizado. 2 skills nuevos: `proposal-ops` (win themes, narrativa 3 actos, executive summary para Workana), `pipeline-health-ops` (metricas pipeline, forecasting, deals estancados, alertas). 3 skills enriquecidos: `deep-interview-ops` (+SPIN, Gap Selling, Sandler, AECR, regla 60/40), `cold-email-ops` (+signal-based selling, ICP tiering, secuencia multicanal 10 touches/28 dias, benchmarks), `seo-audit-ops` (+cannibalization audit bloqueante, keyword clusters, link building, E-E-A-T). AGENTS.md de los 3 workspaces actualizados. Resumen: `docs/FORENSE_AGENCY_AGENTS_RESUMEN.md`.
- **2026-04-14:** Modulo **Forense OMC** completado. Repo oh-my-claudecode (28.8k stars) analizado. 4 skills creados: `deep-interview-ops` (cuestionamiento socratico, gate claridad >= 3.5), `task-pipeline-ops` (plan-spec-exec-verify-fix), `structured-commits-ops` (git trailers con decision metadata), `session-learner-ops` (extraccion de patrones). `verification-before-completion` mejorado con sizing tiers y regla de frescura. AGENTS.md de los 3 workspaces actualizados con "Protocolo de calidad (Superpowers + OMC)". Resumen: `docs/FORENSE_OMC_RESUMEN.md`.
- **2026-04-14:** Modulo **Forense Skills Repos** completado. 3 repos analizados (anthropics/skills 117k, awesome-claude-skills 53.8k, marketingskills 21.1k). Patron clave adoptado: `product-marketing-context` (`.agents/product-marketing-context.md`). 5 skills creados: `copywriting-ops`, `cold-email-ops`, `page-cro-ops`, `lead-research-ops`, `seo-audit-ops`. AGENTS.md de ventas y marketing actualizados con seccion "Skills de marketing y ventas". Resumen: `docs/FORENSE_SKILLS_REPOS_RESUMEN.md`.
- **2026-04-14:** Modulo **Forense Superpowers** completado. Plugin instalado en Cursor (`~/.cursor/plugins/local/superpowers/`). 4 skills adaptados al ecosistema: `brainstorming-ops` (obligatorio antes de tareas complejas), `verification-before-completion` (evidencia antes de claims), `systematic-debugging` (4 fases, root cause primero), `dev-methodology` (TDD + planes + code review para cuando se active dev-agency). AGENTS.md de los 3 workspaces actualizados con "Protocolo de calidad (Superpowers)". Resumen: `docs/FORENSE_SUPERPOWERS_RESUMEN.md`.
- **2026-04-14:** Modulo **Forense Paperclip** completado. Patrones adoptados: Goals formales (`GOALS.md`), organigrama Mermaid (`ORG_CHART.md`), heartbeats operativos en openclaw.json (jarvis 30m, sales-hunter 1h, mkt-content 2h), cost tracking (`scripts/cost-report.sh`), approval gates (`docs/APPROVAL_GATES.md` con 10 gates AG-01..AG-10), rutinas documentadas con goals en CLAWFLOWS.md. Resumen: `docs/FORENSE_PAPERCLIP_RESUMEN.md`.
- **2026-04-08:** Módulo MemPalace **cerrado** a nivel documentación: `docs/MODULO_MEMPALACE_CIERRE.md` (réplica desde Git, checklist, `deploy/mempalace/`). Artefactos versionados; estado local (`~/.mempalace/`) opcional en backup.
- **2026-04-08:** Integrado MemPalace 3.0.0 como sistema de memoria complementario. ChromaDB local con 1270 drawers (ecosystem + sessions), Knowledge Graph temporal con 54 triples (empresas, agentes, clientes, decisiones), MCP server registrado en OpenClaw, auto-mine cada 30 min via systemd. OpenClaw memory-core activado con Ollama `nomic-embed-text` (6 archivos, 34 chunks, vector dims 768). Docs: `docs/MEMORIA_MEMPALACE.md`.
- **2026-04-08:** Documentado flujo Ventas end-to-end (`docs/FLUJO_VENTAS_PROSPECCION_CIERRE.md`); Jarvis debe usarlo al coordinar prospección, conversación con cliente y cierre; AGENTS.md del agente jarvis actualizado con enlace.
- **2026-04-04:** Modelo de gobierno v2 formalizado. Jarvis es agente maestro; cada empresa con CEO + supervisor + equipo; clientes como dossiers de contexto; solo el superusuario dialoga con Jarvis.
- **2026-04-04:** Cliente de prueba `cli-20260404-cliente-tests-redes` (Instagram + Facebook, empresa marketing) para depurar ecosistema; brief en `client-dossiers/BRIEF_CLIENTE_TESTS_REDES.md`.
- **2026-04-04:** Documentado en repo que Trello, Discord y Telegram ya están integrados en OpenClaw (`INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md`); plantilla Fase 5 y verificación Discord Fase 4 añadidas.
- **2026-04-04:** Unificada convencion de ruta: carpeta del sistema **`Documents`** (`~/Documents/`), explicitamente no `documentos` / `Documentos` / `~/Documentos/` salvo excepcion en WORKSPACE_POLICY.
- **2026-04-04:** Añadidos `BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md` y `scripts/trello-bootstrap-boards.sh`. API Trello en este entorno rechazo escritura (401); esqueleto de tableros/canales manual o token con permiso de escritura.
- **2026-04-04:** Documento `OPENCLAW_PERMISOS_AUTOMATIZACION.md` — checklist para token Trello con escritura, `exec` en gateway y permisos Discord bot.
