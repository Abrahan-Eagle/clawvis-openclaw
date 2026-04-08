# Ecosistema Jarvis (dentro de `clawvis-openclaw`)

**Jarvis** es el **agente maestro** de un holding de empresas. Este directorio agrupa agentes, skills, automatizaciones ClawFlows, scripts y la documentacion de gobierno del holding. La documentacion operativa global esta en el [README.md del monorepo](../README.md).

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
| **Dossiers de cliente** | [client-dossiers/](client-dossiers/) | Un JSON por cliente con `dossier_id`, rubro, servicios, objetivos, planificacion. |

---

## Tres sitios distintos: no confundir

| Ubicacion | Rol |
|-----------|-----|
| **`jarvis-ecosystem/openclaw.json`** (este arbol) | **Plantilla / referencia** minima (modelos de ejemplo, bindings de ejemplo). El gateway **no** la lee salvo que la copies a mano. |
| **`~/.openclaw/openclaw.json`** | **Fuente de verdad** del gateway: modelos reales, canales (Telegram, Discord, WhatsApp), `bindings`, `tools`, agentes. Editar aqui para cambiar comportamiento en produccion. |
| **`config/openclaw-home/`** (en el monorepo) | **Instantanea sanitizada** (sin `.env`, sin sesiones ni credenciales) para revision y backup en Git. |

## Contenido principal

| Ruta | Descripcion |
|------|-------------|
| `agents/jarvis/` | Workspace del agente maestro: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `MEMORY.md`, `skills/`, `scripts/` (model-router), `memory/`. |
| `agents/marketing/` | Empresa Marketing & Comunicacion: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `skills/` (copia de jarvis). |
| `agents/ventas/` | Empresa Ventas: `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `skills/` (copia de jarvis). |
| `automations/` | YAML ClawFlows; ver [automations/README.md](automations/README.md). |
| `scripts/` | `clawflows-env.sh`, verificacion del registry, etc. |
| [CLAWFLOWS.md](CLAWFLOWS.md) | Guia ClawFlows + Lobster. |

**Skills duplicadas:** `agents/marketing/skills/` y `agents/ventas/skills/` son **copias** de `agents/jarvis/skills/`. Editar siempre en `agents/jarvis/skills/` y replicar a las otras carpetas.

## Documentacion de gobierno

| Documento | Contenido |
|-----------|-----------|
| [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md) | Modelo operativo: Jarvis master, empresas con CEO/supervisor/equipo, clientes como dossier, coordinacion inter-empresa. |
| [docs/OPERACION_POST_GOBIERNO.md](docs/OPERACION_POST_GOBIERNO.md) | Indice del plan operativo (fases 0–6): verificacion, roles, dossiers, Trello, Discord, reportes, expansion. |
| [docs/CLIENT_DOSSIER_SCHEMA.md](docs/CLIENT_DOSSIER_SCHEMA.md) | Esquema minimo del dossier por cliente (`dossier_id`, rubro, servicios). |
| [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) | Roles y canales Discord/Telegram por empresa (sin cliente→Jarvis). |
| [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md) | Tableros, listas, etiquetas y vinculo `dossier_id`. |
| [docs/FLUJO_TRELLO_ECOSISTEMA.md](docs/FLUJO_TRELLO_ECOSISTEMA.md) | **Obligatorio:** flujo Kanban, tarjetas, Done; Jarvis, agentes y subagentes. |
| [docs/JARVIS_DOCUMENTS_ON_DISK.md](docs/JARVIS_DOCUMENTS_ON_DISK.md) | Entregables en el PC bajo `~/Documents/JARVIS-DOCUMENTS/` (carpeta del sistema **Documents** en inglés; empresas, clientes, estados). |
| [docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) | Trello, Discord y Telegram ya en OpenClaw; Jarvis no debe asumir integracion pendiente. |
| [docs/RECURSOS_COMUNIDAD_OPENCLAW.md](docs/RECURSOS_COMUNIDAD_OPENCLAW.md) | Inventario forense de repos comunidad (skills, awesome lists, patrones); criterios antes de adoptar. |
| [docs/VERIFICACION_DISCORD_FASE4.md](docs/VERIFICACION_DISCORD_FASE4.md) | Coherencia documental Discord/Telegram vs gateway. |
| [docs/plantillas/REPORTE_SUPERVISOR_CEO.md](docs/plantillas/REPORTE_SUPERVISOR_CEO.md) | Plantilla copiable para reporte supervisor → CEO. |
| [docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) | Primera pasada: tableros Trello + canales Discord alineados a la convención. |
| [docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md](docs/OPENCLAW_PERMISOS_AUTOMATIZACION.md) | Token Trello con escritura, `exec` en OpenClaw, Discord bot — checklist. |

## Checklist rapido

- Cambiar **Telegram / modelo / binding** → `~/.openclaw/openclaw.json` + reinicio del gateway.
- Cambiar **skill o prompt del agente** → `agents/jarvis/skills/` (y alinear copias en marketing/ventas).
- **Backup de config en Git** → actualizar `config/openclaw-home/` segun el procedimiento del README raiz (sin secretos).
- **Agregar empresa nueva** → ver checklist en [COMPANIES.md](COMPANIES.md).
