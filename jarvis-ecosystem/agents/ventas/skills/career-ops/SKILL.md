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
- PDF / navegacion: `npx playwright install chromium` si falta el browser.
- Config: copiar `config/profile.example.yml` → `config/profile.yml` y `templates/portals.example.yml` → `portals.yml` segun necesidad.

## Lineas rojas

- No enviar aplicaciones ni emails masivos sin confirmacion humana; el upstream enfatiza revision humana.
- Datos sensibles de clientes: mismas reglas que el resto del workspace Ventas (Trello, dossiers, canales autorizados).

## Referencias

- README y docs: [`../../career-ops/README.md`](../../career-ops/README.md), [`../../career-ops/docs/SETUP.md`](../../career-ops/docs/SETUP.md)
