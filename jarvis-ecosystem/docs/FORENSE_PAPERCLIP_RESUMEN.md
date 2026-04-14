# Forense Paperclip AI — Resumen de patrones adoptados

**Repo analizado:** [paperclipai/paperclip](https://github.com/paperclipai/paperclip)  
**Fecha del analisis:** abril 2026  
**Objetivo:** Extraer patrones de organizacion de agentes autonomos para fortalecer OpenClaw/Jarvis.

---

## Que es Paperclip

Paperclip es una plataforma open-source (Node.js + React) para orquestar "empresas de IA" con agentes autonomos. Incluye:

- Organigrama jerarquico de agentes (org chart)
- Sistema de metas/goals alineados a la empresa
- Presupuestos y tracking de costes por agente
- Heartbeats (pulsos periodicos de actividad)
- Puertas de aprobacion (governance)
- Task management (issues) interno
- PostgreSQL + Drizzle ORM

## Que se adopto (dentro de OpenClaw)

| Concepto Paperclip | Implementacion en Jarvis/OpenClaw | Archivos |
|---------------------|-----------------------------------|----------|
| **Org Chart** | Diagrama Mermaid con jerarquia completa | `ORG_CHART.md` |
| **Goals** | Tabla de metas por empresa con metricas e IDs | `GOALS.md` |
| **Heartbeats** | Config nativa de OpenClaw + HEARTBEAT.md operativos | `openclaw.json`, `agents/*/HEARTBEAT.md`, `docs/HEARTBEAT_OPERATIVO.md` |
| **Budget/Cost tracking** | Script `cost-report.sh` que parsea sesiones JSONL | `scripts/cost-report.sh` |
| **Approval Gates** | Documento formal con 10 gates + flujo Mermaid | `docs/APPROVAL_GATES.md` |
| **Task alignment** | Cada rutina/ClawFlow documentada con su Goal | `CLAWFLOWS.md` (tabla "Registro completo de rutinas") |

## Que NO se adopto (y por que)

| Concepto | Razon de no adopcion |
|----------|---------------------|
| PostgreSQL/Drizzle | OpenClaw usa JSONL + archivos; no necesita DB relacional para este volumen |
| React dashboard | No hay frontend; Jarvis opera via CLI, WhatsApp, Discord, Telegram |
| Issue tracking interno | Trello ya cumple esa funcion en el ecosistema |
| Deploy de Paperclip como servidor | OpenClaw es el centro; no agregar otro runtime |
| Sistema de billing real | Los modelos usados son gratuitos (cursor-local, ollama, groq free tier); el script de costes basta |

## Principio aplicado

> "OpenClaw es el centro. Los repos externos son ideas para fortalecer a Jarvis, no para reemplazarlo."

Todo lo adoptado se implemento usando herramientas nativas de OpenClaw (config JSON, HEARTBEAT.md, scripts bash, documentacion Markdown) sin agregar dependencias externas ni servidores adicionales.

## Archivos creados/modificados en este modulo

### Archivos nuevos

| Archivo | Descripcion |
|---------|-------------|
| `GOALS.md` | Metas del holding con IDs, metricas y reglas |
| `ORG_CHART.md` | Organigrama Mermaid del ecosistema |
| `docs/HEARTBEAT_OPERATIVO.md` | Guia operativa de heartbeats |
| `docs/APPROVAL_GATES.md` | Puertas de aprobacion formalizadas |
| `docs/FORENSE_PAPERCLIP_RESUMEN.md` | Este documento |
| `scripts/cost-report.sh` | Reporte de uso/costes por agente |
| `agents/ventas/HEARTBEAT.md` | Checklist de heartbeat para ventas |
| `agents/marketing/HEARTBEAT.md` | Checklist de heartbeat para marketing |

### Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `agents/jarvis/AGENTS.md` | Seccion Goal principal + referencia a Approval Gates |
| `agents/ventas/AGENTS.md` | Seccion Goal principal + Approval Gates en lineas rojas |
| `agents/marketing/AGENTS.md` | Seccion Goal principal + Approval Gates en lineas rojas |
| `agents/jarvis/HEARTBEAT.md` | De template vacio a checklist operativo |
| `CLAWFLOWS.md` | Tabla completa de rutinas con Goals + nota heartbeats |
| `config/openclaw-home/openclaw.json` | Heartbeats para jarvis, sales-hunter, mkt-content |

## Referencias

- [GOALS.md](../GOALS.md)
- [ORG_CHART.md](../ORG_CHART.md)
- [HEARTBEAT_OPERATIVO.md](HEARTBEAT_OPERATIVO.md)
- [APPROVAL_GATES.md](APPROVAL_GATES.md)
- [CLAWFLOWS.md](../CLAWFLOWS.md)
- [MODULO_MEMPALACE_CIERRE.md](MODULO_MEMPALACE_CIERRE.md) (modulo anterior)
