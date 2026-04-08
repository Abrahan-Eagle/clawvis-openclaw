---
name: career-ops
description: Pipeline de evaluación de oportunidades (URLs, portales, scoring, PDFs) en el repo career-ops; reutilizable para prospección de clientes y ofertas comerciales desde Ventas.
homepage: https://github.com/santifer/career-ops
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":[]}}}
---

# career-ops (Ventas)

Código y flujo del proyecto **career-ops** vive en este workspace en [`../../career-ops/`](../../career-ops/) (desde esta carpeta `skills/career-ops/`).

## Uso en Ventas

En **Ventas**, el mismo motor sirve para **prospección y calificación de oportunidades** (clientes, licitaciones, RFPs, partners) — no solo empleo. Adapta lenguaje y criterios: "oferta" = oportunidad comercial; el scoring y los modos del repo son plantillas.

## Qué hace el repo

- Evaluación estructurada (scoring), PDFs, escaneo de portales con Playwright, tracker, batch.
- Comando mental: `/career-ops` en Claude Code apunta a los modos documentados en [`../../career-ops/README.md`](../../career-ops/README.md).

## Requisitos locales

- Desde `agents/ventas/career-ops/`: `npm install` (hecho en integración).
- PDF / navegación: por defecto [`../../career-ops/config/playwright.env`](../../career-ops/config/playwright.env) usa **Chrome** del sistema; alternativa: `npx playwright install chromium`. La variable `CAREER_OPS_PLAYWRIGHT_CHANNEL` en el entorno pisa el archivo.
- Config: copiar `config/profile.example.yml` → `config/profile.yml` y `templates/portals.example.yml` → `portals.yml` según necesidad.

## Líneas rojas

- No enviar aplicaciones ni emails masivos sin confirmación humana; el upstream enfatiza revisión humana.
- Datos sensibles de clientes: mismas reglas que el resto del workspace Ventas (Trello, dossiers, canales autorizados).

## Stack acordado (cero coste extra)

- **Solo career-ops** en esta carpeta: evaluación, PDFs, portales, `npm run doctor`. Sin Docker ni otro producto paralelo.
- **No** se integra [job-ops](https://github.com/DaKheera47/job-ops) ni herramientas similares que exijan servicios 24/7, scraping agresivo de terceros o stacks adicionales.
- **Seguimiento** después de contactar o aplicar: [Trello y dossiers](../../../../docs/FLUJO_TRELLO_ECOSISTEMA.md) del ecosistema — sin automatizar buzón; la disciplina de no perder el hilo es la misma utilidad sin dependencias nuevas.

## Referencias

- README y docs: [`../../career-ops/README.md`](../../career-ops/README.md), [`../../career-ops/docs/SETUP.md`](../../career-ops/docs/SETUP.md)
