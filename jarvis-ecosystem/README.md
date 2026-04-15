# Ecosistema Jarvis (dentro de `clawvis-openclaw`)

**Jarvis** es el **agente maestro** de un holding de empresas. Este directorio agrupa agentes, skills, automatizaciones ClawFlows, scripts y la documentación de gobierno del holding. La documentación operativa global está en el [README.md del monorepo](../README.md).

---

## Estructura del holding

```
Superusuario (Abraham) ←→ Jarvis (agente maestro)
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
| `agents/marketing/` | Empresa Marketing & Comunicación: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`. Las skills compartidas viven solo en [`agents/jarvis/skills/`](agents/jarvis/skills/) (sin copias duplicadas aquí). |
| `agents/ventas/` | Empresa Ventas: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `skills/career-ops/` (solo Ventas), [`career-ops/`](agents/ventas/career-ops/) (herramienta local). Resto de skills: [`agents/jarvis/skills/`](agents/jarvis/skills/). Detalle: [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md). |
| `agents/dev-agency/`, `agents/legal/`, `agents/contadores/` | Empresas **planificadas**: scaffold (`IDENTITY`, `AGENTS`, `SOUL`, `USER`, `MEMORY`). Sin agentes en gateway hasta activación — [COMPANIES.md](COMPANIES.md). |
| `automations/` | YAML ClawFlows; ver [automations/README.md](automations/README.md). |
| `scripts/` | `clawflows-env.sh`, verificación del registry, etc. |
| [CLAWFLOWS.md](CLAWFLOWS.md) | Guía ClawFlows + Lobster. |

**Skills canónicas:** toda skill compartida está en **`agents/jarvis/skills/`** (una sola copia; evita drift). Marketing y Ventas **no** duplican esas carpetas. **Excepción:** `agents/ventas/skills/career-ops/` (y `agents/ventas/career-ops/`) es solo Ventas — ver [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md). Los README en `agents/marketing/skills/` y `agents/ventas/skills/` enlazan a Jarvis.

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
| [docs/CAROUSEL_IG_JARVIS.md](docs/CAROUSEL_IG_JARVIS.md) | Carruseles Instagram: skill `carousel-ops`; app open-carrusel opcional fuera del repo. |
| [docs/VERIFICACION_DISCORD_FASE4.md](docs/VERIFICACION_DISCORD_FASE4.md) | Coherencia documental Discord/Telegram vs gateway. |
| [docs/plantillas/REPORTE_SUPERVISOR_CEO.md](docs/plantillas/REPORTE_SUPERVISOR_CEO.md) | Plantilla copiable para reporte supervisor → CEO. |
| [docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) | Primera pasada: tableros Trello + canales Discord alineados a la convención. |
| [docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md](docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md) | Token Trello con escritura, `exec` en OpenClaw, Discord bot — checklist. |
| [docs/COHERENCIA_RUNTIME_REPO.md](docs/COHERENCIA_RUNTIME_REPO.md) | `~/.openclaw` vs repo vs snapshot: evitar deriva. |
| [docs/SECURITY_GATEWAY.md](docs/SECURITY_GATEWAY.md) | Auth del gateway y superficie de red; `plugins.allow`. |
| [../docs/TROUBLESHOOTING_OPENCLAW_CPU.md](../docs/TROUBLESHOOTING_OPENCLAW_CPU.md) | CPU al 100%, proceso `rg`, ajustes `memorySearch` / concurrencia / `exec`. |

## Checklist rápido

- Cambiar **Telegram / modelo / binding** → `~/.openclaw/openclaw.json` + reinicio del gateway.
- Cambiar **skill o prompt del agente** → `agents/jarvis/skills/` (y alinear copias en marketing/ventas); **career-ops** solo en `agents/ventas/` (ver [agents/ventas/AGENTS.md](agents/ventas/AGENTS.md)).
- **Backup de config en Git** → actualizar `config/openclaw-home/` según el procedimiento del README raíz (sin secretos).
- **Agregar empresa nueva** → ver checklist en [COMPANIES.md](COMPANIES.md).
