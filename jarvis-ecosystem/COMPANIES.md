# Empresas del holding (registro central)

**Fuente de verdad** para las unidades de negocio que Jarvis orquesta.  
Gobierno operativo: [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md).  
**Ultima actualizacion:** abril 2026.

**CEO / Supervisor (Fase 1):** rellenar [docs/ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) y, si quieres una sola tabla canonica, copiar aqui los nombres.

---

## Registro de empresas

| ID | Nombre | Servicios principales | CEO | Supervisor | Estado | Workspace |
|----|--------|-----------------------|-----|------------|--------|-----------|
| `marketing` | Marketing & Comunicacion | Marketing digital, gestion de redes, branding, contenido, publicidad | [ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) | [ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) | **Activa** | `agents/marketing/` |
| `ventas` | Ventas | Prospeccion, cierre, gestion de cuentas, pipeline comercial | [ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) | [ASIGNACION_ROLES.md](docs/ASIGNACION_ROLES.md) | **Activa** | `agents/ventas/` |
| `dev-agency` | Agencia de Programacion | Desarrollo de software, mantenimiento, APIs, apps moviles, web | (por asignar) | (por asignar) | Planificada | — |
| `legal` | Bufete Legal | Asesoria juridica, contratos, propiedad intelectual, regulacion | (por asignar) | (por asignar) | Planificada | — |
| `contadores` | Contabilidad & Finanzas | Contabilidad, impuestos, nomina, auditorias, reportes financieros | (por asignar) | (por asignar) | Planificada | — |

**Nota:** las empresas "Planificada" no tienen workspace ni agentes en OpenClaw todavia. Se crearan cuando el superusuario lo autorice (ver checklist de alta abajo).

---

## Agentes por empresa (OpenClaw `agents.list`)

Mapeo actual entre agentes y workspaces:

| Agente ID | Empresa | Rol / especialidad |
|-----------|---------|---------------------|
| `jarvis` | (master) | Orquestador del holding; dialogo directo con el superusuario |
| `mkt-content` | marketing | Contenido y copywriting |
| `mkt-social` | marketing | Gestion de redes sociales |
| `mkt-analytics` | marketing | Analitica y reportes de campanas |
| `mkt-ads` | marketing | Publicidad paga (ads) |
| `mkt-email` | marketing | Email marketing y automatizacion |
| `sales-hunter` | ventas | Prospeccion y generacion de leads |
| `sales-closer` | ventas | Cierre de ventas |
| `sales-account` | ventas | Gestion de cuentas (post-venta) |

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
  Equipo (empleados segun rol)
```

- **CEO:** responsable final de la empresa; recibe rendicion de cuentas del supervisor; interlocutor de negocio con Jarvis.
- **Supervisor:** revisa calidad del equipo, planifica y mantiene Trello y Discord, reporta al CEO (semanal/quincenal).
- **Equipo:** empleados con roles segun el tipo de empresa.

Detalle completo: [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md).

---

## Comunicacion entre empresas

Cuando una empresa necesita a otra (ej. marketing pide una landing a dev-agency, o contadores piden criterio legal):

1. Se documenta con el mismo `dossier_id` del cliente si aplica.
2. Tarjetas enlazadas en Trello con etiqueta `delegado-a:<empresa>` (ver [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md)).
3. Jarvis puede proponer la division del trabajo; los CEOs/supervisores cierran alcance y fechas.

---

## Checklist: dar de alta una empresa nueva

Cuando el superusuario autorice una empresa nueva:

1. **Crear workspace:** `agents/<id>/` con `IDENTITY.md`, `AGENTS.md`, `SOUL.md`, `USER.md` (copiar estructura de `agents/marketing/` como plantilla).
2. **Actualizar esta tabla:** agregar fila con estado "Activa" y ruta del workspace.
3. **Agregar agentes en OpenClaw:** entrada(s) en `openclaw.json` bajo `agents.list` apuntando al nuevo workspace.
4. **Copiar skills:** replicar `agents/jarvis/skills/` al nuevo workspace (o enlace simbolico si se soporta).
5. **Trello:** crear board `Empresa-<NombreCorto> — Operaciones` con listas segun [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md); documentar board ID en MEMORY.md de Jarvis.
6. **Discord:** crear categoria o servidor segun [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) con roles CEO / Supervisor / Equipo.
7. **Automatizaciones:** si la empresa necesita cron/ClawFlow propio, crear YAML en `automations/<id>/`.
8. **Reiniciar gateway:** `systemctl --user restart openclaw-gateway` para que reconozca los nuevos agentes.

---

## Referencias

- [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md) — modelo operativo completo.
- [docs/CLIENT_DOSSIER_SCHEMA.md](docs/CLIENT_DOSSIER_SCHEMA.md) — esquema de dossier por cliente.
- [client-dossiers/](client-dossiers/) — dossiers activos.
- [docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md) — tableros y etiquetas.
- [docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) — canales y roles.
