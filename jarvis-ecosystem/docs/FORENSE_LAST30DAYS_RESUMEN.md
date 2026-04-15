# Forense last30days-skill — Resumen

**Fecha:** 2026-04-14  
**Repo analizado:** [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) (21.9k stars, MIT, motor Python v3)  
**Paquete adoptado en OpenClaw:** **last30days-openclaw** (ClawHub) — adaptacion con rutas y secretos OpenClaw; upstream MIT preservado en ATTRIBUTION.md.

## Hallazgo clave

El proyecto original es un **runtime** (investigacion multi-fuente + sintesis), no un patron de texto. El valor para Jarvis es **ejecutar** el skill cuando hace falta pulso externo reciente, no duplicar el motor en Markdown.

`last30days-official` en ClawHub puede fallar con **HTTP 429** (rate limit); **last30days-openclaw** instalo correctamente en la sesion de referencia.

## Que se adopto

| Entregable | Descripcion |
|------------|-------------|
| Skill en repo | Copia versionada en [`agents/jarvis/skills/last30days-openclaw/`](../agents/jarvis/skills/last30days-openclaw/) |
| Guia operativa | [`LAST30DAYS_INTEGRACION.md`](LAST30DAYS_INTEGRACION.md) |
| **lead-research-ops** | Paso opcional de intel reciente antes de scoring |
| **proposal-ops** | Paso opcional para win themes anclados en conversacion reciente |
| **AGENTS.md** | jarvis, ventas, marketing — referencia al skill y a la guia |

## Que NO se adopto

- Forkear el motor Python ni sustituir pipelines internos de OpenClaw.
- Depender de TikTok/Instagram/Polymarket como flujo principal B2B (documentado como opcional).
- Sustituir MemPalace, Graphify ni dossiers.

## Linea roja

OpenClaw sigue siendo el centro de orquestacion; last30days es **herramienta de investigacion** bajo el mismo gateway y politicas de aprobacion del CEO para acciones externas sensibles.
