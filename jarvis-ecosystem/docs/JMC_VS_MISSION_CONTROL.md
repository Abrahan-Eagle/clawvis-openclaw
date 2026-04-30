# JMC frente a OpenClaw Mission Control

Este repo incluye **Jarvis Mission Control (JMC)** como dashboard **principalmente de lectura** sobre el estado del ecosistema Jarvis (`state/`, costes, dossiers, docs de gobierno). La única escritura v1.8 acotada es **`POST /v1/modes/current`** (modo A–D en `~/.openclaw/.env` con Bearer). Es deliberadamente distinto del proyecto upstream **[openclaw-mission-control](https://github.com/abhi1693/openclaw-mission-control)**.

## Comparativa breve

| Aspecto | JMC (`jarvis-ecosystem/jmc`) | Mission Control (upstream) |
|--------|------------------------------|----------------------------|
| Alcance | Observabilidad local: lectura de archivos del repo y rutas configuradas | Plataforma operativa multi-equipo: organizaciones, tableros, usuarios |
| Persistencia en UI | No escribe `state/` ni config desde la web | CRUD de tareas, tags, tableros, aprobaciones en servidor |
| Base de datos | Ninguna en el adapter documentado | Backend con modelo propio |
| Tags | `tags[]` en JSON de tareas (`activity-log`) + filtros en UI | Catálogo de tags con colores, conteos globales, CRUD |
| Skills | Vista Agents + carga opcional de skills desde repo | Marketplace / packs como producto |
| Gateway | Vista métricas runtime (`window_hours`) | Administración de gateways distribuidos |
| Host / cron / repo | Métricas `psutil`, timeline de heartbeats, memory/files/search read-only vía API | Suele depender de otras herramientas o del IDE |
| Salud agregada / externos | **v1.10:** `GET /v1/health/deep`, healthchecks HTTP **whitelist** (`JMC_EXT_HEALTHCHECKS`), zombies/latencia desde `activity-log` | Paneles cloud / probes gestionados en SaaS |

## Cuándo usar cada uno

- **JMC**: depuración rápida, forense y gobierno documental en la máquina donde vive el repo; sin CRUD de tareas ni escritura en `state/` vía API; la UI puede **aplicar modo** (endpoint acotado anterior).
- **Mission Control**: cuando se necesita una **fuente de verdad** centralizada para trabajo de equipo, flujos de aprobación pesados y modelo de datos propio.

Los patrones de UX de Mission Control (Kanban, feed, tags visibles) pueden inspirar mejoras **solo lectura** en JMC sin igualar su alcance; véase la tabla de evolución en [`JMC_DESIGN.md`](JMC_DESIGN.md).

## Tablero en JMC (v1.6)

La vista **Tasks → Tablero** agrupa tareas en columnas tipo Mission Control **únicamente en el navegador**: no se crean columnas ni estados nuevos en disco. Las reglas combinan `jmc_status`, handoffs con aprobación pendiente y una muestra reciente del `activity-log` (`GET /v1/state/activity?limit=50`). No hay arrastre de tarjetas ni persistencia de posición en columnas: cualquier cambio real de estado sigue siendo responsabilidad de los agentes y de `activity-log` / archivos de tarea.

**v1.7:** La paleta de comandos (`Ctrl+K`) y los enlaces rápidos desde Overview solo **navegan o filtran** en el cliente (read-only); no invocan escritura en `state/` ni en el adapter.
