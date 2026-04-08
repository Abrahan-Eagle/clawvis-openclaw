---
name: career-ops
description: Pipeline de evaluacion de oportunidades (URLs, portales, scoring, PDFs) en el repo career-ops; reutilizable para prospeccion de clientes y ofertas comerciales desde Ventas.
homepage: https://github.com/santifer/career-ops
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":[]}}}
---

# career-ops (Ventas)

Codigo y flujo del proyecto **career-ops** vive en este workspace en [`../../career-ops/`](../../career-ops/) (desde esta carpeta `skills/career-ops/`).

## Uso en Ventas

En **Ventas**, el mismo motor sirve para **prospeccion y calificacion de oportunidades** (clientes, licitaciones, RFPs, partners) — no solo empleo. Adapta lenguaje y criterios: "oferta" = oportunidad comercial; el scoring y los modos del repo son plantillas.

## Que hace el repo

- Evaluacion estructurada (scoring), PDFs, escaneo de portales con Playwright, tracker, batch.
- Comando mental: `/career-ops` en Claude Code apunta a los modos documentados en [`../../career-ops/README.md`](../../career-ops/README.md).

## Requisitos locales

- Desde `agents/ventas/career-ops/`: `npm install` (hecho en integracion).
- PDF / navegacion: por defecto [`../../career-ops/config/playwright.env`](../../career-ops/config/playwright.env) usa **Chrome** del sistema; alternativa: `npx playwright install chromium`. La variable `CAREER_OPS_PLAYWRIGHT_CHANNEL` en el entorno pisa el archivo.
- Config: copiar `config/profile.example.yml` → `config/profile.yml` y `templates/portals.example.yml` → `portals.yml` segun necesidad.

## Lineas rojas

- No enviar aplicaciones ni emails masivos sin confirmacion humana; el upstream enfatiza revision humana.
- Datos sensibles de clientes: mismas reglas que el resto del workspace Ventas (Trello, dossiers, canales autorizados).

## Stack acordado (cero coste extra)

- **Solo career-ops** en esta carpeta: evaluacion, PDFs, portales, `npm run doctor`. Sin Docker ni otro producto paralelo.
- **No** se integra [job-ops](https://github.com/DaKheera47/job-ops) ni herramientas similares que exijan servicios 24/7, scraping agresivo de terceros o stacks adicionales.
- **Seguimiento** despues de contactar o aplicar: [Trello y dossiers](../../../../docs/FLUJO_TRELLO_ECOSISTEMA.md) del ecosistema — sin automatizar buzon; la disciplina de no perder el hilo es la misma utilidad sin dependencias nuevas.

## Referencias

- README y docs: [`../../career-ops/README.md`](../../career-ops/README.md), [`../../career-ops/docs/SETUP.md`](../../career-ops/docs/SETUP.md)
