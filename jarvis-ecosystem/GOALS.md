# Metas del holding (Goals)

Cada tarea, rutina o heartbeat del ecosistema debe conectarse a un goal de esta tabla. Si no sirve a ningun goal, cuestionar si vale la pena hacerla.

**Fuente de verdad** para alineacion estrategica. Gobierno operativo: [docs/GOBIERNO_JARVIS_V2.md](docs/GOBIERNO_JARVIS_V2.md).  
**Ultima actualizacion:** abril 2026.

---

## Goals del holding

| ID | Empresa | Goal | Metrica | Estado |
|----|---------|------|---------|--------|
| `G-H01` | holding | Consolidar ecosistema Jarvis como plataforma operativa autonoma | Agentes activos con heartbeats funcionando; rutinas ejecutandose sin intervencion manual | **Activo** |
| `G-H02` | holding | Documentacion completa y replicable del ecosistema | Poder restaurar en maquina nueva siguiendo docs del repo en <2h | **Activo** |

## Goals de Ventas

| ID | Empresa | Goal | Metrica | Estado |
|----|---------|------|---------|--------|
| `G-V01` | ventas | Conseguir clientes recurrentes via Workana y otros portales | Leads calificados por semana; propuestas enviadas; tasa de cierre | **Activo** |
| `G-V02` | ventas | Pipeline visible y ordenado en Trello | Todas las oportunidades con tarjeta y estado actualizado | **Activo** |
| `G-V03` | ventas | Perfil Workana posicionado y optimizado | Perfil completo, primeros trabajos cerrados, reviews positivas | **Activo** |

## Goals de Marketing

| ID | Empresa | Goal | Metrica | Estado |
|----|---------|------|---------|--------|
| `G-M01` | marketing | Presencia digital de Aiblock activa y medible | Posts/semana, engagement, trafico web mensual | **Activo** |
| `G-M02` | marketing | Contenido alineado con servicios que ventas ofrece | % de piezas de contenido que apuntan a un servicio vendible | **Activo** |

## Goals de Jarvis (agente maestro)

| ID | Empresa | Goal | Metrica | Estado |
|----|---------|------|---------|--------|
| `G-J01` | jarvis | Orquestar agentes del holding sin intervencion constante del CEO | Heartbeats activos; decisiones escaladas solo cuando corresponde | **Activo** |
| `G-J02` | jarvis | Mantener memoria y contexto del ecosistema al dia | MemPalace auto-mine funcionando; MEMORY.md actualizado | **Activo** |

---

## Reglas

1. **Toda tarjeta de Trello** debe indicar el `G-XXX` al que sirve en la descripcion o en una etiqueta.
2. **Toda rutina/ClawFlow** debe documentar su goal en la tabla de `CLAWFLOWS.md`.
3. **En heartbeats**, el agente debe priorizar tareas alineadas a sus goals.
4. **Revision trimestral:** el CEO (superusuario) revisa esta tabla y ajusta metas, metricas y estados.

---

## Empresas planificadas (sin goals activos)

- `dev-agency`: goals se definiran al activar la empresa.
- `legal`: idem.
- `contadores`: idem.
