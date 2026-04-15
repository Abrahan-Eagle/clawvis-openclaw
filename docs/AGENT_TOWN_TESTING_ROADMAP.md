# Roadmap de pruebas — Agent Town

Plan de cobertura incremental para [`agent-town/`](../agent-town/) (Next.js 16 + Phaser + proxy WebSocket).

## Estado actual (abr 2026)

- **Vitest** en `agent-town/lib/__tests__/`: `gateway-handler`, `reducer`, `utils`, `persistence`.
- Umbrales en `vitest.config.ts` (~40% en `lib/`).
- **CI:** [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) en la raíz del monorepo con `working-directory: agent-town` (lint, typecheck, build, test).

## Prioridad P1 — rápidas y de alto valor

| Área | Qué cubrir | Notas |
|------|------------|--------|
| `lib/ws-proxy.ts` | Handshake, buffer, timeout upstream | Lógica crítica; el `.mjs` de producción se **genera** con `pnpm build:ws-proxy` — los tests deben ejecutarse contra el módulo TS o contra comportamiento extraído testeable. |
| `app/api/agents/discover/route.ts` | Respuesta JSON estable | Smoke test con `next` request mock o integration mínima. |
| `app/api/internal/seat-sync/route.ts` | Auth localhost + cuerpo | Solo si se mantiene ruta activa. |

## Prioridad P2 — integración

| Área | Qué cubrir |
|------|------------|
| `server.ts` | Arranque mock del servidor HTTP (opcional, pesado). |
| E2E | Playwright/Puppeteer **no** está en dependencias tras la limpieza; si se reintroduce E2E, añadir devDependency explícita y un job opcional en CI. |

## Prioridad P3 — Phaser

- Pruebas de canvas en CI son costosas; preferir **tests de lógica pura** extraídas de escenas (`components/game/`) donde sea posible.

## Comandos

```bash
cd agent-town && pnpm test && pnpm build
```

Ver también [`agent-town/docs/TESTING_ROADMAP.md`](../agent-town/docs/TESTING_ROADMAP.md) (enlace corto junto al código).
