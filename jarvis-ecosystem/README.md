# Ecosistema Jarvis (dentro de `clawvis-openclaw`)

**Jarvis** es el **agente maestro** de un holding de empresas. Este directorio agrupa agentes, skills, automatizaciones ClawFlows, scripts y la documentación de gobierno del holding. La documentación operativa global está en el [README.md del monorepo](../README.md).

---

## Estructura del holding

```
Superusuario (Abrahan) ←→ Jarvis (agente maestro)
                              |
        ┌─────────────────────┼─────────────────────┐
   Marketing          Ventas          (Planificadas:
   CEO / Sup / Eq     CEO / Sup / Eq   dev-agency,
                                        legal,
                                        contadores)
```

| Recurso | Ruta | Contenido |
|---------|------|-----------|
| **Registro de empresas** | [COMPANIES.md](COMPANIES.md) | Todas las unidades (activas + planificadas), CEOs, servicios, checklist de alta. |
| **Dossiers de cliente** | [client-dossiers/](client-dossiers/) | Un JSON por cliente con `dossier_id`, rubro, servicios, objetivos, planificación. |

---

## Tres sitios distintos: no confundir

| Ubicación | Rol |
|-----------|-----|
| **`jarvis-ecosystem/openclaw.json`** (este árbol) | **Plantilla / referencia** mínima (modelos de ejemplo, bindings de ejemplo). El gateway **no** la lee salvo que la copies a mano. |
| **`~/.openclaw/openclaw.json`** | **Fuente de verdad** del gateway: modelos reales, canales (Telegram, Discord, WhatsApp), `bindings`, `tools`, agentes. Editar aquí para cambiar comportamiento en producción. |
| **`config/openclaw-home/`** (en el monorepo) | **Instantánea sanitizada** (sin `.env`, sin sesiones ni credenciales) para revisión y backup en Git. |

## Contenido principal

| Ruta | Descripción |
|------|-------------|
| `agents/jarvis/` | Workspace del agente maestro: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `MEMORY.md`, `skills/`, `scripts/` (model-router), `memory/`. |
| `agents/marketing/` | Empresa Marketing & Comunicación: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`. **Skills de marketing (40)** en [`agents/marketing/skills/`](agents/marketing/skills/README.md) (adaptadas de [marketingskills](https://github.com/coreyhaines31/marketingskills)); skills compartidas y variantes `*-ops` siguen en [`agents/jarvis/skills/`](agents/jarvis/skills/). |
| `agents/ventas/` | Empresa Ventas: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `skills/career-ops/` (solo Ventas), [`career-ops/`](agents/ventas/career-ops/) (herramienta local). Resto de skills: [`agents/jarvis/skills/`](agents/jarvis/skills/). Detalle: [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md). |
| `agents/dev-agency/`, `agents/legal/`, `agents/contadores/` | Empresas **planificadas**: scaffold (`IDENTITY`, `AGENTS`, `SOUL`, `USER`, `MEMORY`). Sin agentes en gateway hasta activación — [COMPANIES.md](COMPANIES.md). |
| `automations/` | YAML ClawFlows; ver [automations/README.md](automations/README.md). |
| `scripts/` | `clawflows-env.sh`, `openclaw-path.sh` (PATH para `openclaw` en pruebas/CI), verificación del registry, `generate_marketing_skills.py` / `validate-marketing-skills.sh` (skills marketing), etc. |
| [CLAWFLOWS.md](CLAWFLOWS.md) | Guía ClawFlows + Lobster. |
| [docs/MANUAL_RRSS_JARVIS.md](docs/MANUAL_RRSS_JARVIS.md) | Loop agencia RRSS (modo C): heartbeats, dispatcher, judge-run pre-AG-12, approval-gate, mkt-publish. |
| [contexts/](contexts/) | Context packs `research` / `produce` / `review` (`JARVIS_CONTEXT_MODE`). |
| `skills/global/judge-run/`, `session-compact-ops/`, `memory-store/` | Eval pre-gate, compactación estratégica, memoria estructurada (`memory.json`). |
| `scripts/lessons-scan.sh`, `scripts/memory-consolidate.sh` | Learning loop HITL (candidatos LESSONS / memory.json; sin auto-escribir). |

**Dos capas de skills en Marketing:** (a) variantes rápidas **`*-ops`** en **`agents/jarvis/skills/`** (una sola copia compartida); (b) librería **profunda** (40 skills MIT/adaptadas) en **`agents/marketing/skills/`** — **no** es duplicado del árbol Jarvis; regeneración: `scripts/generate_marketing_skills.py`. **Runtime:** sincronizar ambas capas al workspace del gateway con `sync-jarvis-skills-from-repo.sh` **y** [`sync-marketing-skills-from-repo.sh`](scripts/sync-marketing-skills-from-repo.sh) — [docs/COHERENCIA_RUNTIME_REPO.md](docs/COHERENCIA_RUNTIME_REPO.md). **Excepción Ventas:** `agents/ventas/skills/career-ops/` — ver [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md).

## Documentación de gobierno

| Documento | Contenido |
|-----------|-----------|
| [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md) | Modelo operativo: Jarvis master, empresas con CEO/supervisor/equipo, clientes como dossier, coordinación inter-empresa. |
| [docs/OPERACION_POST_GOBIERNO.md](docs/OPERACION_POST_GOBIERNO.md) | Índice del plan operativo (fases 0–6): verificación, roles, dossiers, Trello, Discord, reportes, expansión. |
| [docs/CLIENT_DOSSIER_SCHEMA.md](docs/CLIENT_DOSSIER_SCHEMA.md) | Esquema mínimo del dossier por cliente (`dossier_id`, rubro, servicios). |
| [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) | Roles y canales Discord/Telegram por empresa (sin cliente→Jarvis). |
| [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md) | Tableros, listas, etiquetas y vínculo `dossier_id`. |
| [docs/FLUJO_TRELLO_ECOSISTEMA.md](docs/FLUJO_TRELLO_ECOSISTEMA.md) | **Obligatorio:** flujo Kanban, tarjetas, Done; Jarvis, agentes y subagentes. |
| [docs/JARVIS_DOCUMENTS_ON_DISK.md](docs/JARVIS_DOCUMENTS_ON_DISK.md) | Entregables en el PC bajo `~/Documents/JARVIS-DOCUMENTS/` (carpeta del sistema **Documents** en inglés; empresas, clientes, estados). |
| [docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) | Trello, Discord y Telegram ya en OpenClaw; Jarvis no debe asumir integración pendiente. |
| [docs/RECURSOS_COMUNIDAD_OPENCLAW.md](docs/RECURSOS_COMUNIDAD_OPENCLAW.md) | Inventario forense de repos comunidad (skills, awesome lists, patrones); **§2** marketing + Claude y mapeo `mkt-*`; **§2.8** patrones LightRAG portados; criterios antes de adoptar. |
| [docs/DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md](docs/DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md) | Patrones LightRAG (dual retrieval) implementados vía skill `dual-retrieval-ops` — sin servidor LightRAG. |
| [docs/CAROUSEL_IG_JARVIS.md](docs/CAROUSEL_IG_JARVIS.md) | Carruseles IG y disenos redes: skill `carousel-ops` (brief + calidad + handoff), open-carrusel (local PNG) y Canva via Composio (API); flujo combinado. |
| [docs/TROUBLESHOOTING_COMPOSIO_OPENCLAW.md](docs/TROUBLESHOOTING_COMPOSIO_OPENCLAW.md) | Composio + OpenClaw: `fetch failed` tras `composio doctor`, proxy, criterio de exito en gateway; script `scripts/composio-diagnose.sh`. |
| [docs/VERIFICACION_DISCORD_FASE4.md](docs/VERIFICACION_DISCORD_FASE4.md) | Coherencia documental Discord/Telegram vs gateway. |
| [docs/plantillas/REPORTE_SUPERVISOR_CEO.md](docs/plantillas/REPORTE_SUPERVISOR_CEO.md) | Plantilla copiable para reporte supervisor → CEO. |
| [docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) | Primera pasada: tableros Trello + canales Discord alineados a la convención. |
| [docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md](docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md) | Token Trello con escritura, `exec` en OpenClaw, Discord bot — checklist. |
| [docs/COHERENCIA_RUNTIME_REPO.md](docs/COHERENCIA_RUNTIME_REPO.md) | `~/.openclaw` vs repo vs snapshot: evitar deriva. |
| [docs/CLAWWORK_FORENSE.md](docs/CLAWWORK_FORENSE.md) | Análisis HKUDS/ClawWork (benchmark Nanobot): qué adoptar vs qué rechazar. |
| [docs/AUTONOMIA_MODOS.md](docs/AUTONOMIA_MODOS.md) | Modos de autonomía **A/B/C/D** (default **D**) + matriz con AG-01..AG-13. |
| [docs/ESCALACION_ASYNC.md](docs/ESCALACION_ASYNC.md) | Escalación al CEO por Telegram/WhatsApp cuando el modo lo exija (`waiting_for_user`). |
| [docs/SECURITY_GATEWAY.md](docs/SECURITY_GATEWAY.md) | Auth del gateway y superficie de red; `plugins.allow`. |
| [../docs/TROUBLESHOOTING_OPENCLAW_CPU.md](../docs/TROUBLESHOOTING_OPENCLAW_CPU.md) | CPU al 100%, proceso `rg`, ajustes `memorySearch` / concurrencia / `exec`. |
| [docs/PRUEBAS_JARVIS_PROMPTS.md](docs/PRUEBAS_JARVIS_PROMPTS.md) | Prompts copy-paste para pruebas del ecosistema (smoke, ClawFlows, OpenClaw, coordinación, RRSS, gobierno). |
| [docs/RESEARCH_MARKETING_SKILLS.md](docs/RESEARCH_MARKETING_SKILLS.md) | Investigación forense + matriz: import de `coreyhaines31/marketingskills` (40 skills) en `agents/marketing/skills/`. |

## Checklist rápido

- Tras **git pull** en `clawvis-openclaw`, si el gateway usa una copia en `$HOME/jarvis-ecosystem` (no symlink al repo), sincronizar skills desde la raiz del monorepo: `JARVIS_WORKSPACE_BASE=$HOME/jarvis-ecosystem ./jarvis-ecosystem/scripts/sync-jarvis-skills-from-repo.sh` **y** `./jarvis-ecosystem/scripts/sync-marketing-skills-from-repo.sh` — o desde `jarvis-ecosystem/`: `JARVIS_WORKSPACE_BASE=$HOME/jarvis-ecosystem ./scripts/sync-jarvis-skills-from-repo.sh && ./scripts/sync-marketing-skills-from-repo.sh` — ver [docs/COHERENCIA_RUNTIME_REPO.md](docs/COHERENCIA_RUNTIME_REPO.md).
- Cambiar **Telegram / modelo / binding** → `~/.openclaw/openclaw.json` + reinicio del gateway.
- Cambiar **skill o prompt del agente** → `agents/jarvis/skills/`; skills **marketing profundas** → `agents/marketing/skills/` (regenerar con `scripts/generate_marketing_skills.py`); **career-ops** solo en `agents/ventas/` (ver [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md)).
- **Backup de config en Git** → actualizar `config/openclaw-home/` según el procedimiento del README raíz (sin secretos).
- **Agregar empresa nueva** → ver checklist en [COMPANIES.md](COMPANIES.md).
