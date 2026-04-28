# Empresas del holding (registro central)

**Fuente de verdad** para las unidades de negocio que Jarvis orquesta.  
Gobierno operativo: [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md).  
**Última actualización:** abril 2026.

**Entregables en disco (fuera del repo):** cada empresa tiene su rama bajo `~/Documents/JARVIS-DOCUMENTS/empresas/<ID>/` (carpeta del sistema **`Documents`**, no `Documentos`) — ver [docs/JARVIS_DOCUMENTS_ON_DISK.md](docs/JARVIS_DOCUMENTS_ON_DISK.md).

**CEO / Supervisor (Fase 1):** [docs/ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) — nombres de ejemplo por empresa (no el superusuario); sustituir por personas reales cuando aplique.

---

## Registro de empresas

| ID | Nombre | Servicios principales | CEO | Supervisor | Estado | Workspace |
|----|--------|-----------------------|-----|------------|--------|-----------|
| `marketing` | Marketing & Comunicación | Marketing digital, gestión de redes, branding, contenido, publicidad | Ricardo Mena (ejemplo) | Patricia Oropeza (ejemplo) | **Activa** | `agents/marketing/` |
| `ventas` | Ventas | Prospección, cierre, gestión de cuentas, pipeline comercial | Damian Vela (ejemplo) | Lucia Fernandez (ejemplo) | **Activa** | `agents/ventas/` |
| `dev-agency` | Agencia de Programación | Desarrollo de software, mantenimiento, APIs, apps móviles, web | (por asignar) | (por asignar) | Planificada (scaffold) | `agents/dev-agency/` |
| `legal` | Bufete Legal | Asesoría jurídica, contratos, propiedad intelectual, regulación | (por asignar) | (por asignar) | Planificada (scaffold) | `agents/legal/` |
| `contadores` | Contabilidad & Finanzas | Contabilidad, impuestos, nómina, auditorías, reportes financieros | (por asignar) | (por asignar) | Planificada (scaffold) | `agents/contadores/` |

**Nota:** estado **Planificada (scaffold)** = hay carpeta `agents/<id>/` con `IDENTITY.md`, `AGENTS.md`, etc., pero **aún no** hay agentes en OpenClaw ni tableros hasta que el superusuario complete el checklist de alta.

---

## Agentes por empresa (OpenClaw `agents.list`)

Mapeo actual entre agentes y workspaces:

| Agente ID | Empresa | Rol / especialidad |
|-----------|---------|---------------------|
| `jarvis` | (master) | Orquestador del holding; diálogo directo con el superusuario |
| `mkt-content` | marketing | Contenido y copywriting |
| `mkt-social` | marketing | Gestión de redes sociales |
| `mkt-analytics` | marketing | Analítica y reportes de campañas |
| `mkt-ads` | marketing | Publicidad paga (ads) |
| `mkt-email` | marketing | Email marketing y automatización |
| `mkt-research` | marketing | Investigación de clientes, VOC, desk research (skills profundas `customer-research`, competencia) |
| `sales-hunter` | ventas | Prospección y generación de leads |
| `sales-closer` | ventas | Cierre de ventas |
| `sales-account` | ventas | Gestión de cuentas (post-venta) |

---

## Estructura interna por empresa

Cada empresa **activa** debe tener:

```
Superusuario
    |
  Jarvis (master / orquestador)
    |
  CEO de la empresa
    |
  Supervisor(es)
    |
  Equipo (empleados según rol)
```

- **CEO:** responsable final de la empresa; recibe rendición de cuentas del supervisor; interlocutor de negocio con Jarvis.
- **Supervisor:** revisa calidad del equipo, planifica y mantiene Trello y Discord, reporta al CEO (semanal/quincenal).
- **Equipo:** empleados con roles según el tipo de empresa.

Detalle completo: [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md).

---

## Comunicación entre empresas

Cuando una empresa necesita a otra (ej. marketing pide una landing a dev-agency, o contadores piden criterio legal):

1. Se documenta con el mismo `dossier_id` del cliente si aplica.
2. Tarjetas enlazadas en Trello con etiqueta `delegado-a:<empresa>` (ver [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md)).
3. Jarvis puede proponer la división del trabajo; los CEOs/supervisores cierran alcance y fechas.

---

## Checklist: dar de alta una empresa nueva

Cuando el superusuario autorice una empresa nueva:

1. **Workspace:** si no existe, crear `agents/<id>/` con `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md` (plantilla: `agents/marketing/`). Para `dev-agency`, `legal` y `contadores` ya hay **scaffold** en el repo: completar contenido y pasar la empresa a **Activa** en esta tabla.
2. **Actualizar esta tabla:** agregar fila con estado "Activa" y ruta del workspace.
3. **Agregar agentes en OpenClaw:** entrada(s) en `openclaw.json` bajo `agents.list` apuntando al nuevo workspace.
4. **Copiar skills:** replicar `agents/jarvis/skills/` al nuevo workspace (o enlace simbólico si se soporta). Si la unidad necesita herramientas propias (patrón **career-ops** en Ventas), documentar la excepción en el `AGENTS.md` de esa empresa; no todo skill tiene que existir en `agents/jarvis/skills/`.
5. **Trello:** crear board `Empresa-<NombreCorto> — Operaciones` con listas según [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md); documentar board ID en MEMORY.md de Jarvis.
6. **Discord:** crear categoría o servidor según [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) con roles CEO / Supervisor / Equipo.
7. **Automatizaciones:** si la empresa necesita cron/ClawFlow propio, crear YAML en `automations/<id>/`.
8. **Reiniciar gateway:** `systemctl --user restart openclaw-gateway` para que reconozca los nuevos agentes.

---

## Referencias

- [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md) — modelo operativo completo.
- [docs/CLIENT_DOSSIER_SCHEMA.md](docs/CLIENT_DOSSIER_SCHEMA.md) — esquema de dossier por cliente.
- [client-dossiers/](client-dossiers/) — dossiers activos.
- [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md) — tableros y etiquetas.
- [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) — canales y roles.
