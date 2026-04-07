# Informe forense: Ecosistema JARVIS (clawvis-openclaw)

**Alcance:** monorepo en `/var/www/clawvis-openclaw` — OpenClaw (gateway), Jarvis y workspaces, Agent Town, automatizaciones, documentación de gobierno.  
**Fecha de elaboración:** abril 2026.  
**Metodología:** análisis según [PROMPT_FORENSE_ECOSISTEMA_JARVIS.md](./PROMPT_FORENSE_ECOSISTEMA_JARVIS.md); evidencia en rutas del repositorio; lo no verificable en disco se marca explícitamente.  
**Holding:** [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md) — activas `marketing`, `ventas`; planificadas `dev-agency`, `legal`, `contadores` (sin `agents/<id>/` en el clon analizado).

---

## Tabla de contenidos

- [Empresa 1 — Agencia de software (1.1–1.16)](#empresa-1--agencia-de-desarrollo-de-software)
- [Empresa 2 — Marketing digital (2.1–2.16)](#empresa-2--agencia-de-marketing-digital)
- [Empresa 3 — Ventas (3.1–3.12)](#empresa-3--ventas-y-desarrollo-comercial)
- [Síntesis cruzada (S.1–S.6)](#síntesis-cruzada-inter-empresas)

---

## Empresa 1 — Agencia de desarrollo de software

### [ROL] Arquitecto de Software

**Área:** Arquitectura global del ecosistema  
**Madurez:** 7/10

#### Archivos analizados

- [README.md](../README.md)
- [jarvis-ecosystem/README.md](../jarvis-ecosystem/README.md)
- [agent-town/package.json](../agent-town/package.json)
- [agent-town/server.ts](../agent-town/server.ts)
- [agent-town/lib/ws-proxy.ts](../agent-town/lib/ws-proxy.ts)
- [agent-town/lib/gateway.ts](../agent-town/lib/gateway.ts) (referenciado; patrón import en server)
- [agent-town/app/layout.tsx](../agent-town/app/layout.tsx) (estructura app)
- [agent-town/app/api/agents/discover/route.ts](../agent-town/app/api/agents/discover/route.ts)
- [agent-town/app/api/internal/seat-sync/route.ts](../agent-town/app/api/internal/seat-sync/route.ts)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json)
- [jarvis-ecosystem/agents/jarvis/AGENTS.md](../jarvis-ecosystem/agents/jarvis/AGENTS.md)
- [deploy/systemd/openclaw-gateway.service](../deploy/systemd/openclaw-gateway.service)
- [deploy/systemd/cursor-agent-api.service.example](../deploy/systemd/cursor-agent-api.service.example)
- [deploy/systemd/agent-town-dev.service.example](../deploy/systemd/agent-town-dev.service.example)
- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)

#### Hallazgos

1. Patrón dominante: **gateway OpenClaw** (WebSocket, puerto 18789 en snapshot) + **Agent Town** como aplicación Next.js que **proxifica** el WebSocket hacia el gateway (`README.md`, `server.ts`, `ws-proxy.ts`), evitando que el navegador abra el puerto del gateway directamente.
2. `gateway.bind: loopback` y `gateway.mode: local` en `config/openclaw-home/openclaw.json` acotan la superficie de red al host.
3. Extensibilidad multi-empresa: [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md) define checklist de alta de nuevas unidades; en el repo solo existen workspaces `agents/jarvis`, `agents/marketing`, `agents/ventas` — **no** hay aún `agents/dev-agency`, `legal`, `contadores` (coherente con estado “Planificada”).
4. Riesgo de **deriva de configuración**: tres ubicaciones de verdad documentadas (`~/.openclaw`, plantilla en `jarvis-ecosystem`, snapshot `config/openclaw-home/`) — [README.md](../README.md) exige coherencia vía symlink `~/.jarvis-ecosystem`.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Config runtime ≠ repo | MEDIO | [README.md](../README.md) L30–31 | Cambios no reflejados en producción |
| Dependencia de un solo host | MEDIO | systemd usuario, sin orquestador | Caída total si el nodo falla |

#### Oportunidades

1. Script de verificación `readlink -f ~/.jarvis-ecosystem` vs ruta del repo documentado en runbook.
2. Plantilla IaC futura solo si el holding exige HA (no impuesta por el diseño actual).

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Checklist post-clon en README o script | Bajo | Menos incidentes de ruta |
| 2 | P2 | Documentar RTO/RPO solo si se expone a clientes externos | Medio | Expectativas claras |

---

### [ROL] Líder técnico (Tech Lead)

**Área:** Calidad, convenciones, CI  
**Madurez:** 6/10

#### Archivos analizados

- [agent-town/.github/workflows/ci.yml](../agent-town/.github/workflows/ci.yml)
- [agent-town/tsconfig.json](../agent-town/tsconfig.json)
- [agent-town/eslint.config.mjs](../agent-town/eslint.config.mjs)
- [.gitignore](../.gitignore)
- [jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs](../jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs) (existencia)
- [jarvis-ecosystem/agents/jarvis/model-router.rules.yaml](../jarvis-ecosystem/agents/jarvis/model-router.rules.yaml)

#### Hallazgos

1. CI en GitHub: `format:check`, `lint`, `typecheck`, `build`, `test`, `audit --audit-level=high` (continue-on-error) — cobertura razonable para Agent Town.
2. **Node 20** en CI vs **Node 22+** citado en [README.md](../README.md) para OpenClaw: posible divergencia de versión entre CI de Agent Town y runtime del gateway (no bloqueante si Agent Town es compatible con 20).
3. **Remediado en repo:** [.gitignore](../.gitignore) incluye `jarvis-ecosystem/.env` y `jarvis-ecosystem/.env.*` (además de `agent-town/.env.local`).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Secreto filtrado en historial Git antes del ignore | MEDIO | Commits antiguos | Credencial expuesta en remoto |

#### Oportunidades

- Alinear versión Node en CI con la documentada para OpenClaw cuando se unifique pipeline.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | ~~Añadir `jarvis-ecosystem/.env` a `.gitignore`~~ **Hecho** | Bajo | Menor riesgo de leak futuro |
| 2 | P2 | Matriz README: versión Node por componente | Bajo | Menos confusión |
| 3 | P2 | Si hubo `.env` en commits previos, rotar claves y usar `git filter-repo` o equivalente | Alto | Limpieza historial |

---

### [ROL] Desarrollador senior

**Área:** Implementación y pruebas  
**Madurez:** 7/10

#### Archivos analizados

- [agent-town/server.ts](../agent-town/server.ts)
- [agent-town/lib/ws-proxy.ts](../agent-town/lib/ws-proxy.ts)
- [agent-town/lib/__tests__/gateway-handler.test.ts](../agent-town/lib/__tests__/gateway-handler.test.ts) (referencia volumen)
- [jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs](../jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs) (referenciado en runbook)

#### Hallazgos

1. `handleDispatch` limita a localhost y exige `x-dispatch-secret` ([server.ts](../agent-town/server.ts)).
2. Proxy WS: buffer máx. 100 mensajes, timeout upstream 15s ([ws-proxy.ts](../agent-town/lib/ws-proxy.ts)).
3. Tests Vitest presentes bajo `lib/__tests__/`; cobertura fuerte en lógica de cliente gateway; **no** verificado en esta pasada test e2e del túnel completo contra gateway real.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Regresión en proxy | MEDIO | Sin e2e automatizado citado | Fallos en conexión UI |

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Test de integración WS con mock upstream | Medio | Regresiones más tempranas |

---

### [ROL] Ingeniero de DevOps

**Área:** Despliegue y operaciones  
**Madurez:** 6/10

#### Archivos analizados

- [deploy/systemd/*.service*](../deploy/systemd/)
- [docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](../docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md) (referencia README)
- [docs/OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md)
- [jarvis-ecosystem/automations/](../jarvis-ecosystem/automations/) (listado YAML)
- [jarvis-ecosystem/scripts/](../jarvis-ecosystem/scripts/) (existencia)

#### Hallazgos

1. Units de referencia para gateway, proxy Cursor, Agent Town dev — modelo **systemd --user** ([README.md](../README.md)).
2. Runbook forense detallado (fases A–E): baseline, sesiones, secretos, rutas legadas ([OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md)).
3. Múltiples YAML de automatización; monitoreo externo a Git no especificado en repo.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | `loginctl enable-linger` documentado para headless — ya en README | — | Continuidad |
| 2 | P2 | Alertas manual periódicas vía runbook si no hay Prometheus | Bajo | Detección temprana |

---

### [ROL] Especialista en ciberseguridad

**Área:** Seguridad  
**Madurez:** 5/10

#### Archivos analizados

- [.gitignore](../.gitignore)
- [config/openclaw-home/README.md](../config/openclaw-home/README.md) (si existe)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json)
- [docs/OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md) Fase D
- [agent-town/server.ts](../agent-town/server.ts)
- [agent-town/lib/ws-proxy.ts](../agent-town/lib/ws-proxy.ts)
- [PUSH-A-GITHUB.md](../PUSH-A-GITHUB.md) — **presente en raíz** (guía mínima `git add` / `commit` / `push` y remisión al README).

#### Hallazgos

1. `gateway.auth.mode: "none"` en snapshot ([openclaw.json](../config/openclaw-home/openclaw.json) L245–247); [OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md) L73–74 condiciona a loopback/firewall.
2. [README.md](../README.md) L21: el repositorio **puede contener secretos** — debe ser **privado**.
3. Identidad de dispositivo leída desde `~/.openclaw/identity/` en proxy ([ws-proxy.ts](../agent-town/lib/ws-proxy.ts)) — protección del HOME es crítica.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Auth gateway none + exposición de puerto | ALTO | openclaw.json + runbook | Abuso del gateway |
| Repo privado mal configurado en remoto | CRÍTICO | README | Filtración |

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P0 | Confirmar GitHub private + audit de historial | Medio | Confidencialidad |
| 2 | P1 | Endurecer auth si el gateway deja de ser solo loopback | Medio | Superficie reducida |

---

### [ROL] Arquitecto de Cloud

**Área:** Nube y escalado  
**Madurez:** 4/10

#### Archivos analizados

- [deploy/systemd/](../deploy/systemd/)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json)
- [docs/PROVEEDOR_CURSOR_OPENCLAW.md](../docs/PROVEEDOR_CURSOR_OPENCLAW.md) — referenciado README
- [docs/MODELOS_JARVIS_OPENCLAW.md](../docs/MODELOS_JARVIS_OPENCLAW.md) — referenciado README

#### Hallazgos

1. Diseño actual **single-node**, sin manifiestos Kubernetes ni Terraform en el árbol principal.
2. Fallbacks multi-proveedor LLM en `openclaw.json` mitigan indisponibilidad de un proveedor, no sustituyen multi-región.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Coste LLM sin quota centralizada | MEDIO | Varios providers en JSON | Factura impredecible |

#### Oportunidades

1. Hoja de ruta cloud solo tras SLA externo o equipo remoto.

#### Recomendaciones

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Diseño cloud solo si hay requisito comercial | Alto | Escala |

---

### [ROL] Diseñador UX/UI

**Área:** Agent Town UI  
**Madurez:** 6/10

#### Archivos analizados

- [agent-town/app/page.tsx](../agent-town/app/page.tsx) — lectura no exhaustiva en esta pasada
- [agent-town/app/globals.css](../agent-town/app/globals.css)
- [agent-town/components/](../agent-town/components/) (estructura)

#### Hallazgos

1. Producto definido como oficina pixel + Phaser ([package.json](../agent-town/package.json), README).
2. **No verificado:** auditoría a11y completa ni contraste en todos los paneles.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Paneles densos en HUD pixel | BAJO | Sin auditoría a11y | Exclusión de usuarios |

#### Oportunidades

1. Mapa de teclado y foco visible en panel Connection.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Pasada axe/lighthouse en build | Medio | a11y |

---

### [ROL] Ingeniero de QA

**Área:** Testing  
**Madurez:** 6/10

#### Archivos analizados

- [agent-town/.github/workflows/ci.yml](../agent-town/.github/workflows/ci.yml)
- [agent-town/vitest.config.ts](../agent-town/vitest.config.ts)
- [agent-town/lib/__tests__/](../agent-town/lib/__tests__/)
- [docs/OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md)

#### Hallazgos

1. [agent-town/.github/workflows/ci.yml](../agent-town/.github/workflows/ci.yml) ejecuta `pnpm test`.
2. Tests en `agent-town/lib/__tests__/` (vitest); no se listaron tests en raíz del monorepo fuera de Agent Town.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Cobertura desigual | MEDIO | Solo agent-town testeado en CI | Regresiones en scripts jarvis |

#### Oportunidades

1. Runbook forense como test manual complementario ([OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md)).

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Job opcional para `validate-jarvis-sessions.mjs` dry-run | Medio | Integridad sesiones |

---

### [ROL] Gerente de producto

**Área:** Visión y roadmap  
**Madurez:** 7/10

#### Archivos analizados

- [README.md](../README.md)
- [jarvis-ecosystem/README.md](../jarvis-ecosystem/README.md)
- [jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md) — referenciado desde AGENTS
- [jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md](../jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md)
- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)

#### Hallazgos

1. Gobierno y registro de empresas **bien enlazados**; empresas planificadas explícitas con checklist de alta.
2. KPIs de negocio globales **no** cuantificados en un único dashboard en repo (esperable para operación pequeña).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Roadmap implícito vs medido | MEDIO | Sin KPI central | Priorización subjetiva |

#### Oportunidades

1. Usar COMPANIES + checklist de alta como backlog de producto interno.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Revisión trimestral de “qué empresa activar” | Bajo | Alineación holding |

---

### [ROL] Científico de datos

**Área:** Datos y analítica  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md)
- [openclaw-state/](../openclaw-state/) (referencia README)

#### Hallazgos

1. [CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md) estructura datos de cliente; analítica de campañas **externa** al repo (GA4, etc.) no verificada aquí.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Silos de datos (Trello / Notion / GA) | MEDIO | Sin warehouse | Informes manuales |

#### Oportunidades

1. Exportaciones periódicas a carpeta analítica bajo convención JARVIS-DOCUMENTS.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Elegir una fuente de verdad numérica por cliente | Medio | Coherencia |

---

### [ROL] Ingeniero de Machine Learning

**Área:** Modelos y routing  
**Madurez:** 7/10

#### Archivos analizados

- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json) (defaults, providers)
- [jarvis-ecosystem/agents/jarvis/model-router.rules.yaml](../jarvis-ecosystem/agents/jarvis/model-router.rules.yaml)
- [docs/MODELOS_JARVIS_OPENCLAW.md](../docs/MODELOS_JARVIS_OPENCLAW.md) — referenciado README

#### Hallazgos

1. Router YAML con tiers light/standard/heavy y reglas por regex ([model-router.rules.yaml](../jarvis-ecosystem/agents/jarvis/model-router.rules.yaml)).
2. [jarvis/AGENTS.md](../jarvis-ecosystem/agents/jarvis/AGENTS.md) L44: OpenClaw **no aplica** el router automáticamente en canales — honestidad operativa crítica.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Expectativa de “Auto modelo” en canales | MEDIO | AGENTS.md router CLI-only | Coste o calidad subóptimos |

#### Oportunidades

1. Bindings por canal a `jarvis-deep` para tareas pesadas puntuales.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Documentar en README de operadores qué es solo CLI | Bajo | Expectativas |

---

### [ROL] Administrador de bases de datos (DBA)

**Área:** Persistencia  
**Madurez:** 5/10

#### Archivos analizados

- [docs/OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md)
- [jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs](../jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs)
- [README.md](../README.md)

#### Hallazgos

1. Estado OpenClaw (sesiones, memoria) descrito en runbook; `openclaw-state/` en repo como referencia histórica ([README.md](../README.md)).
2. Retención/purga de JSONL: política operativa en [OPENCLAW_FORENSE_RUNBOOK.md](../docs/OPENCLAW_FORENSE_RUNBOOK.md), no automatización vista en repo.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Crecimiento ilimitado de transcripts | MEDIO | Política manual | Disco lleno |

#### Oportunidades

1. `cleanup --dry-run` periódico documentado en runbook.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Cron humano mensual + script validate | Bajo | Salud de sesiones |

---

### [ROL] Desarrollador mobile

**Área:** Mobile / PWA  
**Madurez:** 5/10

#### Archivos analizados

- [agent-town/app/layout.tsx](../agent-town/app/layout.tsx) — no exhaustivo
- [README.md](../README.md) (canales móviles)

#### Hallazgos

1. Canales Telegram/WhatsApp cubren interacción móvil del operador; Agent Town es web desktop-first por diseño (no verificado manifest PWA en esta pasada).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Phaser en móvil (memoria/touch) | MEDIO | Sin matriz de dispositivos | UX frágil |

#### Oportunidades

1. Probar Agent Town en Chrome Android de referencia.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | `viewport` y gestos documentados | Bajo | Soporte móvil web |

---

### [ROL] Desarrollador backend

**Área:** APIs y servidor  
**Madurez:** 7/10

#### Archivos analizados

- [agent-town/server.ts](../agent-town/server.ts)
- [agent-town/lib/ws-proxy.ts](../agent-town/lib/ws-proxy.ts)
- [agent-town/app/api/agents/discover/route.ts](../agent-town/app/api/agents/discover/route.ts)
- [jarvis-ecosystem/automations/](../jarvis-ecosystem/automations/)

#### Hallazgos

1. `/api/agents/discover` valida paths y `agentId` ([discover/route.ts](../agent-town/app/api/agents/discover/route.ts) L29–37).
2. Automatizaciones YAML dispersas también en raíz `automations/` con nombres duplicados lógicos (p. ej. `marketing-competitor-monitor.yaml` vs `marketing/competitor-monitor.yaml`) — posible deuda de housekeeping.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| seat-sync sin auth en OpenClaw-only | BAJO | [seat-sync/route.ts](../agent-town/app/api/internal/seat-sync/route.ts) 204 | OK por diseño actual |

#### Oportunidades

1. Unificar YAML duplicados en una ruta canónica.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Inventario automations (ver Empresa 2.16) | Medio | Menos confusión |

---

### [ROL] Desarrollador frontend

**Área:** Next / React / Phaser  
**Madurez:** 6/10

#### Archivos analizados

- [agent-town/package.json](../agent-town/package.json)
- [agent-town/app/page.tsx](../agent-town/app/page.tsx)
- [agent-town/app/globals.css](../agent-town/app/globals.css)

#### Hallazgos

1. Next 16 + React 19 + Phaser 3 ([package.json](../agent-town/package.json)).
2. Integración Phaser típicamente vía dynamic import (convención en documentación del proyecto).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Bundle pesado (Phaser) | MEDIO | Dependencia game engine | TTFB/LCP en redes lentas |

#### Oportunidades

1. Lazy load de escenas y assets ya alineado con buenas prácticas Phaser.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Medir bundle con análisis Next | Medio | Rendimiento |

---

### [ROL] Desarrollador fullstack

**Área:** Coherencia E2E  
**Madurez:** 7/10

#### Archivos analizados

- [README.md](../README.md)
- [agent-town/server.ts](../agent-town/server.ts)
- [agent-town/app/api/agents/discover/route.ts](../agent-town/app/api/agents/discover/route.ts)
- [jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md)

#### Hallazgos

1. Flujo documentado usuario → Agent Town → WS → gateway → LLM ([README.md](../README.md)).
2. Descubrimiento de agentes enlaza `~/.openclaw` con UI — coherencia depende del mismo usuario OS que ejecuta el gateway.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| “Funciona en mi máquina” por HOME distinto | ALTO | discover usa `os.homedir()` | Lista de agentes vacía o incorrecta |

#### Oportunidades

1. Variable explícita `OPENCLAW_HOME` en doc si OpenClaw lo soporta en el futuro (verificar upstream).

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Mismo usuario Linux para gateway y `pnpm dev` | Bajo | Coherencia discover |

---

## Empresa 2 — Agencia de marketing digital

### [ROL] Estratega digital — 2.1

**Área:** Estrategia digital  
**Madurez:** 6/10

#### Archivos analizados

- [jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md) (referencia cruzada)
- [jarvis-ecosystem/agents/marketing/IDENTITY.md](../jarvis-ecosystem/agents/marketing/IDENTITY.md)
- [jarvis-ecosystem/agents/marketing/AGENTS.md](../jarvis-ecosystem/agents/marketing/AGENTS.md)
- [jarvis-ecosystem/automations/marketing/competitor-monitor.yaml](../jarvis-ecosystem/automations/marketing/competitor-monitor.yaml)
- [jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md)

#### Hallazgos

1. Servicios de marketing declarados en [IDENTITY.md](../jarvis-ecosystem/agents/marketing/IDENTITY.md); gobierno Trello obligatorio en [AGENTS.md](../jarvis-ecosystem/agents/marketing/AGENTS.md).
2. Routing Discord a agentes `mkt-*` requiere bindings explícitos ([AGENTS.md](../jarvis-ecosystem/agents/marketing/AGENTS.md), [DISCORD_JERARQUIA_VS_AGENTES_IA.md](../jarvis-ecosystem/docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md)).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Un solo agente en Discord para todo | MEDIO | Documentación Discord | Voz no diferenciada |

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Bindings por canal → `mkt-social` / `mkt-content` | Medio | Alineación marca |

---

### [ROL] Especialista SEO — 2.2

**Área:** SEO  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/agents/marketing/skills/](../jarvis-ecosystem/agents/marketing/skills/) (estructura)
- [jarvis-ecosystem/agents/jarvis/skills/xurl/](../jarvis-ecosystem/agents/jarvis/skills/xurl/) (referencia skill URL)
- [agent-town/app/layout.tsx](../agent-town/app/layout.tsx) — no auditado línea a línea
- [agent-town/next.config.ts](../agent-town/next.config.ts)

#### Hallazgos

1. Skills genéricos (xurl, summarize) en workspaces; **no** hay skill dedicada “SEO audit” identificada en el listado superficial de nombres.
2. SEO on-page de Agent Town: no auditado en profundidad en esta pasada.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Visibilidad orgánica de Agent Town no gobernada | MEDIO | Sin auditoría meta/sitemap en esta pasada | Menor tráfico directo |

#### Oportunidades

1. Skill o checklist SEO en workspace marketing alineado a clientes del holding.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Revisar `layout.tsx`, `robots.txt`, sitemap en Agent Town | Bajo | SEO básico |

---

### [ROL] Especialista SEM — 2.3

**Área:** Paid media  
**Madurez:** 3/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json) (sin credenciales de Ads)

#### Hallazgos

1. Agente `mkt-ads` en [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md); integración API Google Ads **no verificable** sin credenciales y no visible en repo sanitizado.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Gestión de campañas solo asistida por LLM sin API | MEDIO | Sin conector en repo | Operación manual |

#### Oportunidades

1. Documentar qué plataformas de ads usa el holding en MEMORY o dossier, fuera del repo.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Integrar API solo si volumen de spend lo justifica | Alto | Escala paid |

---

### [ROL] Gerente de performance — 2.4

**Área:** Medición  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md](../jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md)
- [jarvis-ecosystem/automations/](../jarvis-ecosystem/automations/)

#### Hallazgos

1. [REPORTE_SUPERVISOR_CEO.md](../jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md) — plantilla humana; dashboards GA no en repo.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Decisiones sin serie temporal unificada | MEDIO | Datos en herramientas externas | Opinión vs dato |

#### Oportunidades

1. Enlazar en dossier URLs de GA/Search Console por cliente.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Campos opcionales en dossier para enlaces de analítica | Bajo | Trazabilidad |

---

### [ROL] Social Media Manager — 2.5

**Área:** Redes  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/automations/marketing/competitor-monitor.yaml](../jarvis-ecosystem/automations/marketing/competitor-monitor.yaml)
- [jarvis-ecosystem/CLAWFLOWS.md](../jarvis-ecosystem/CLAWFLOWS.md) (referencia)

#### Hallazgos

1. Competitor monitor YAML en automatizaciones; alcance real depende de implementación Lobster/CLI ([CLAWFLOWS.md](../jarvis-ecosystem/CLAWFLOWS.md) referenciado en ecosistema).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Expectativa de “publicación automática” sin OAuth | MEDIO | Canales = conversación, no siempre API social | Frustración usuario |

#### Oportunidades

1. Usar competidor monitor como insumo a Trello, no como publicador único.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Documentar qué redes son solo asistidas vs conectadas | Bajo | Expectativas claras |

---

### [ROL] Estratega de contenido — 2.6

**Área:** Contenido  
**Madurez:** 6/10

#### Archivos analizados

- [jarvis-ecosystem/automations/registry/github-trending.yaml](../jarvis-ecosystem/automations/registry/github-trending.yaml)
- [jarvis-ecosystem/automations/registry/rss-digest.yaml](../jarvis-ecosystem/automations/registry/rss-digest.yaml)
- [jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md](../jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md)

#### Hallazgos

1. `registry/github-trending.yaml`, `rss-digest.yaml` — insumos para curación; [FLUJO_TRELLO_ECOSISTEMA.md](../jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md) gobierna trabajo con cliente.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Ruido de trending sin filtro editorial humano | BAJO | Automatización + LLM | Calidad variable |

#### Oportunidades

1. Combinar RSS + dossier para verticalizar temas.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Lista de fuentes RSS por cliente en dossier | Bajo | Relevancia |

---

### [ROL] Copywriter creativo — 2.7

**Área:** Voz y prompts  
**Madurez:** 6/10

#### Archivos analizados

- [jarvis-ecosystem/agents/marketing/SOUL.md](../jarvis-ecosystem/agents/marketing/SOUL.md)
- [jarvis-ecosystem/agents/marketing/IDENTITY.md](../jarvis-ecosystem/agents/marketing/IDENTITY.md)
- [jarvis-ecosystem/agents/marketing/AGENTS.md](../jarvis-ecosystem/agents/marketing/AGENTS.md)

#### Hallazgos

1. `SOUL.md` / `IDENTITY.md` por workspace definen tono; consistencia depende de bindings y disciplina de uso.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Misma voz Jarvis en canal si binding único | MEDIO | [DISCORD_JERARQUIA_VS_AGENTES_IA.md](../jarvis-ecosystem/docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md) | Marca diluida |

#### Oportunidades

1. Handoff simulado en texto (Nivel B doc Discord) mientras no hay routing fino.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Secciones firmadas en respuestas multi-rol | Bajo | Percepción de equipo |

---

### [ROL] Especialista en branding — 2.8

**Área:** Marca  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/agents/marketing/IDENTITY.md](../jarvis-ecosystem/agents/marketing/IDENTITY.md)
- [agent-town/package.json](../agent-town/package.json)

#### Hallazgos

1. Identidad por empresa en markdown; assets visuales de Agent Town separados (pixel art) — coherencia de marca cliente ≠ coherencia UI producto sin manual explícito.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Confusión marca holding vs marca cliente | MEDIO | Dos capas visuales | Propuestas desalineadas |

#### Oportunidades

1. Guía de una página “marca holding vs entregables cliente” en `docs/`.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Brand kit por cliente en dossier (enlaces) | Bajo | Consistencia |

---

### [ROL] Especialista CRM — 2.9

**Área:** CRM  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md)
- [jarvis-ecosystem/client-dossiers/](../jarvis-ecosystem/client-dossiers/) (estructura si existe)

#### Hallazgos

1. Dossiers JSON + Trello hacen de CRM ligero; Salesforce/HubSpot **no** en repo.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Duplicación de contactos entre herramientas | MEDIO | Sin CRM único | Datos inconsistentes |

#### Oportunidades

1. Mantener `dossier_id` como clave en todas las herramientas.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Convención de nombre de tarjeta Trello con `dossier_id` | Bajo | Trazabilidad |

---

### [ROL] Analista de datos marketing — 2.10

**Área:** Analytics  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json)

#### Hallazgos

1. `mkt-analytics` como agente; fuentes de datos externas no cableadas en snapshot.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Métricas inventadas | ALTO | [IDENTITY marketing](../jarvis-ecosystem/agents/marketing/IDENTITY.md) líneas rojas en ventas similares | Confianza |

#### Oportunidades

1. Skill que exija citar fuente numérica o “no disponible”.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Recordatorio en SOUL/AGENTS de no inventar KPIs | Bajo | Riesgo legal/reputacional |

---

### [ROL] Especialista email marketing — 2.11

**Área:** Email  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)
- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json)

#### Hallazgos

1. `mkt-email` en tabla de agentes; integración ESP no visible en `openclaw.json` sanitizado.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Envíos masivos sin doble opt-in | ALTO | Proceso no en repo | Compliance |

#### Oportunidades

1. Checklist GDPR/mailing en USER.md o dossier por mercado.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Confirmación humana antes de envío masivo ([AGENTS marketing](../jarvis-ecosystem/agents/marketing/AGENTS.md) líneas rojas afines) | Bajo | Cumplimiento |

---

### [ROL] Especialista influencers — 2.12

**Área:** Influencers  
**Madurez:** 3/10

#### Archivos analizados

- [jarvis-ecosystem/agents/marketing/skills/](../jarvis-ecosystem/agents/marketing/skills/) (listado)

#### Hallazgos

1. **No verificable** en repo: herramientas específicas de discovery de influencers.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Dependencia de búsqueda manual | BAJO | Sin integración | Coste tiempo |

#### Oportunidades

1. Uso de `xurl` + summarize para briefs de perfil público.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Evaluar herramienta externa solo si volumen | Medio | Escala |

---

### [ROL] Especialista PR — 2.13

**Área:** Relaciones públicas  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../jarvis-ecosystem/docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) (referencia README ecosystem)

#### Hallazgos

1. Comunicación vía Discord/Telegram documentada; sala de prensa formal no modelada en datos.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Mensajes improvisados en canales abiertos | MEDIO | groupPolicy open en telegram snapshot | Reputación |

#### Oportunidades

1. Plantillas de comunicado en `JARVIS-DOCUMENTS` fuera del repo.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Revisar políticas de grupo/canal en `openclaw.json` vivo | Bajo | Control |

---

### [ROL] Especialista eCommerce — 2.14

**Área:** eCommerce  
**Madurez:** 3/10

#### Archivos analizados

- [jarvis-ecosystem/agents/marketing/skills/](../jarvis-ecosystem/agents/marketing/skills/)

#### Hallazgos

1. Sin conectores Shopify/WooCommerce en archivos revisados.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Inventario/precios desactualizados si se automatiza copy | MEDIO | Sin API | Errores comerciales |

#### Oportunidades

1. Skills de lectura web para comprobar precio público antes de publicar.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Integración eCommerce bajo demanda del cliente | Alto | Ingresos |

---

### [ROL] Especialista CRO — 2.15

**Área:** Optimización conversión  
**Madurez:** 4/10

#### Archivos analizados

- [agent-town/app/page.tsx](../agent-town/app/page.tsx) — no exhaustivo

#### Hallazgos

1. Experimentación A/B **no** instrumentada en código Agent Town revisado.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Opiniones sin experimentos | MEDIO | Sin framework A/B | Decisiones subóptimas |

#### Oportunidades

1. A/B en landing cliente con herramientas externas; IA solo redacta variantes.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Proceso de hipótesis en Trello por cliente | Bajo | Cultura data |

---

### [ROL] Especialista automatización — 2.16

**Área:** Marketing automation  
**Madurez:** 6/10

#### Archivos analizados

- [jarvis-ecosystem/automations/](../jarvis-ecosystem/automations/)
- [jarvis-ecosystem/CLAWFLOWS.md](../jarvis-ecosystem/CLAWFLOWS.md)
- [jarvis-ecosystem/README.md](../jarvis-ecosystem/README.md)

#### Hallazgos

1. ClawFlows YAML en `jarvis-ecosystem/automations/` + registry; dependencia de entorno `.env` ([jarvis-ecosystem/README.md](../jarvis-ecosystem/README.md)).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| YAML duplicado raíz vs subcarpeta | BAJO | Múltiples paths | Confusión operador |

#### Oportunidades

1. Normalizar nombres y documentar “source of truth” por flujo.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Inventario único en CLAWFLOWS o README automations | Medio | Mantenibilidad |

---

## Empresa 3 — Ventas y desarrollo comercial

### [ROL] Gerente desarrollo de negocios (BDM) — 3.1

**Área:** Negocio  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/agents/ventas/IDENTITY.md](../jarvis-ecosystem/agents/ventas/IDENTITY.md)
- [jarvis-ecosystem/agents/ventas/AGENTS.md](../jarvis-ecosystem/agents/ventas/AGENTS.md)
- [jarvis-ecosystem/automations/ventas/pipeline-report.yaml](../jarvis-ecosystem/automations/ventas/pipeline-report.yaml)

#### Hallazgos

1. Pipeline y servicios declarados en IDENTITY; automatización `pipeline-report` disponible en árbol.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| CEO/supervisor humano aún como placeholder en algunos IDENTITY históricos | MEDIO | Registro [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md) vs prompts | Accountability difusa |

#### Oportunidades

1. Usar pipeline-report como ritual semanal con superusuario.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Actualizar nombres CEO/supervisor en markdown cuando cierren nombramientos | Bajo | Gobierno claro |

---

### [ROL] Ejecutivo de cuentas — 3.2

**Área:** Cuentas  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)
- [jarvis-ecosystem/agents/ventas/AGENTS.md](../jarvis-ecosystem/agents/ventas/AGENTS.md)
- [jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md)

#### Hallazgos

1. `sales-account` en [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md); dossiers obligatorios para contexto ([AGENTS.md ventas](../jarvis-ecosystem/agents/ventas/AGENTS.md)).

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Cuenta sin dossier | MEDIO | Protocolo en AGENTS | Contexto mezclado |

#### Oportunidades

1. Vista única por `dossier_id` en Trello por convención ya documentada.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Checklist pre-reunión: dossier + tarjeta | Bajo | Calidad reunión |

---

### [ROL] Gerente de ventas — 3.3

**Área:** Pipeline  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md](../jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md)
- [jarvis-ecosystem/agents/ventas/AGENTS.md](../jarvis-ecosystem/agents/ventas/AGENTS.md)

#### Hallazgos

1. Flujo Trello obligatorio paralelo a marketing — gobierno simétrico documentado.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Listas desalineadas entre empresas | BAJO | Varios boards | Reporting incompleto |

#### Oportunidades

1. Etiquetas `delegado-a:<empresa>` para handoff a marketing/dev-agency futura.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Auditoría trimestral de tableros vs convención | Medio | Pipeline limpio |

---

### [ROL] Director nuevo negocio — 3.4

**Área:** Nuevos segmentos  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)

#### Hallazgos

1. Empresas planificadas (`dev-agency`, etc.) en [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md) como fuente de upsell futuro; sin workspaces aún.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Prometer servicios de unidad no activa | MEDIO | Planificadas sin `agents/` | Incumplimiento |

#### Oportunidades

1. Jarvis puede listar qué unidades están activas antes de comprometer alcance.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Comunicar estado “planificada” en propuestas | Bajo | Expectativas |

---

### [ROL] Representante de ventas — 3.5

**Área:** Ejecución ventas  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)

#### Hallazgos

1. `sales-hunter`, `sales-closer` como agentes dedicados en tabla de registro.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Confundir hunter vs closer en el mismo hilo | BAJO | Mismo workspace | Mensajes ambiguos |

#### Oportunidades

1. Bindings o instrucciones explícitas por etapa del embudo.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Plantilla de mensaje por etapa (calificación / cierre) | Bajo | Claridad |

---

### [ROL] Gerente alianzas — 3.6

**Área:** Partnerships  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md](../jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md)

#### Hallazgos

1. Alianzas tecnológicas (proveedores LLM) implícitas; partnerships comerciales no esquematizados en `CLIENT_DOSSIER_SCHEMA` más allá de campos genéricos.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Acuerdos verbales no reflejados | MEDIO | Schema mínimo | Disputas |

#### Oportunidades

1. Usar `enlaces` y `decisiones_relevantes` del dossier para partners.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Extensión opcional del schema para partners | Medio | Trazabilidad |

---

### [ROL] Inside sales — 3.7

**Área:** Venta remota  
**Madurez:** 6/10

#### Archivos analizados

- [config/openclaw-home/openclaw.json](../config/openclaw-home/openclaw.json) (canales)

#### Hallazgos

1. Telegram/Discord/WhatsApp en configuración gateway — canal natural para inside async.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Historial disperso entre canales | MEDIO | Varios canales | Seguimiento difícil |

#### Oportunidades

1. Trello como sistema de registro único por oportunidad.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P1 | Una tarjeta madre por oportunidad con `dossier_id` | Bajo | Una fuente de verdad |

---

### [ROL] Lead generation — 3.8

**Área:** Leads  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/automations/registry/lead-qualifier.yaml](../jarvis-ecosystem/automations/registry/lead-qualifier.yaml)

#### Hallazgos

1. `registry/lead-qualifier.yaml` presente; calificación automática depende de despliegue ClawFlow.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Lead pobre sin ICP en dossier | MEDIO | Schema opcional | Desperdicio de tiempo |

#### Oportunidades

1. Añadir criterios de ICP en dossier cuando exista.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Definir MQL/SQL en texto en GOBIERNO o plantilla | Medio | Calidad de pipeline |

---

### [ROL] Gerente de licitaciones — 3.9

**Área:** Propuestas  
**Madurez:** 5/10

#### Archivos analizados

- [jarvis-ecosystem/docs/JARVIS_DOCUMENTS_ON_DISK.md](../jarvis-ecosystem/docs/JARVIS_DOCUMENTS_ON_DISK.md)

#### Hallazgos

1. [JARVIS_DOCUMENTS_ON_DISK.md](../jarvis-ecosystem/docs/JARVIS_DOCUMENTS_ON_DISK.md) referenciado para entregables; plantillas formales en carpeta usuario.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Propuestas fuera de `Documents` no trazables | MEDIO | Convención ruta | Pérdida de versiones |

#### Oportunidades

1. Numeración y estados 01–04 ya descritos para entregables.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Revisión humana obligatoria pre-envío (líneas rojas ventas) | Bajo | Cumplimiento |

---

### [ROL] Growth — 3.10

**Área:** Crecimiento  
**Madurez:** 4/10

#### Archivos analizados

- [jarvis-ecosystem/automations/registry/github-trending.yaml](../jarvis-ecosystem/automations/registry/github-trending.yaml)
- [jarvis-ecosystem/README.md](../jarvis-ecosystem/README.md)

#### Hallazgos

1. Automatizaciones tipo `github-trending` aportan señal técnica, no métricas MRR/CRM integradas.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Confundir señales técnicas con pipeline de ingresos | MEDIO | Automatizaciones dev-centric | Prioridades erróneas |

#### Oportunidades

1. Separar dashboards “ecosistema interno” vs “ventas”.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P3 | Definir 2–3 KPIs de ventas en MEMORY Jarvis | Bajo | Foco |

---

### [ROL] Comercial externo (field) — 3.11

**Área:** Campo  
**Madurez:** 6/10

#### Archivos analizados

- [README.md](../README.md) (canales Telegram/WhatsApp)

#### Hallazgos

1. WhatsApp/Telegram como herramientas móviles del comercial — alineado con README canales.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Captura informal sin tarjeta Trello | MEDIO | Uso móvil | Pérdida CRM |

#### Oportunidades

1. Plantilla rápida “notas de reunión → tarjeta” vía Jarvis.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Protocolo post-reunión en AGENTS ventas | Bajo | Higiene de datos |

---

### [ROL] Consultor de soluciones (pre-sales) — 3.12

**Área:** Pre-sales  
**Madurez:** 6/10

#### Archivos analizados

- [README.md](../README.md) raíz (demo Agent Town documentada allí)
- [agent-town/README.md](../agent-town/README.md)
- [jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md) (referencia)

#### Hallazgos

1. Agent Town puede servir de demo visual; propuestas técnicas siguen dependiendo de dossier + documentos en disco.

#### Riesgos detectados

| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| Demo sin datos ficticios aprobados | MEDIO | Contenido cliente real | Confidencialidad |

#### Oportunidades

1. Demo con dossier sandbox o cliente ficticio.

#### Recomendaciones priorizadas

| # | Prioridad | Acción | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P2 | Checklist de demo (qué mostrar / qué no) | Bajo | Seguridad y venta |

---

## Síntesis cruzada inter-empresas

### S.1 Hallazgos convergentes

- **Infraestructura:** Gateway loopback + Agent Town como proxy WS; systemd usuario; fuerte dependencia de un nodo.
- **Datos:** Dossiers y Trello como columnas vertebrales; sin data warehouse en repo.
- **Multi-empresa:** [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md) lista cinco unidades; solo tres workspaces bajo `agents/` (jarvis, marketing, ventas) — **brecha esperada** para `dev-agency`, `legal`, `contadores`.
- **Seguridad:** `gateway.auth: none` en snapshot; README exige repo privado; proxy y dispatch con controles parciales (localhost, secret).
- **Integraciones:** Trello/Discord/Telegram documentados como ya configurados en flujo Jarvis ([INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../jarvis-ecosystem/docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) referenciado en AGENTS).

### S.2 Mapa de madurez (consolidado)

| Área | Empresa1_Dev | Empresa2_Mkt | Empresa3_Ventas | dev-agency | legal | contadores | Promedio ponderado |
|------|--------------|--------------|-----------------|------------|-------|------------|--------------------|
| Arquitectura | 7 | — | — | N/A | N/A | N/A | 7 |
| Seguridad | 5 | 4 | 4 | N/A | N/A | N/A | 4.3 |
| UX/UI | 6 | 5 | 5 | N/A | N/A | N/A | 5.3 |
| Datos | 4 | 4 | 4 | N/A | N/A | N/A | 4 |
| Automatización | 6 | 6 | 5 | N/A | N/A | N/A | 5.7 |
| Gobierno documental | 7 | 7 | 7 | 2 | 2 | 2 | 5.2 |
| Integraciones SaaS | 5 | 4 | 4 | 2 | 2 | 2 | 3.5 |
| Escalabilidad | 4 | 4 | 4 | N/A | N/A | N/A | 4 |

*Nota: N/A o 2 para empresas planificadas sin workspace = madurez operativa “en papel” solamente.*

### S.3 Top 10 brechas críticas

**Actualización:** Tras el informe inicial se añadieron [PUSH-A-GITHUB.md](../PUSH-A-GITHUB.md) y reglas `jarvis-ecosystem/.env` / `.env.*` en [.gitignore](../.gitignore). Los puntos antiguos “falta PUSH-A-GITHUB” y “falta ignore de `.env`” quedan **cerrados** en el repositorio; persisten riesgos de **historial Git** si algún secreto se hubiera commiteado antes.

1. `gateway.auth.mode: none` si el despliegue amplía superficie de red.
2. Deriva entre `~/.openclaw`, repo y symlinks de `jarvis-ecosystem`.
3. Workspaces ausentes para tres empresas planificadas en [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md).
4. Routing de agentes por canal (Discord) no automático — riesgo de todo vía `jarvis`.
5. Posible filtración histórica: auditar commits anteriores por `jarvis-ecosystem/.env` u otros secretos antes de las reglas nuevas en `.gitignore`.
6. CI Agent Town en Node 20 vs Node 22 recomendado para OpenClaw en README.
7. Duplicación / nombres paralelos en YAML de `automations/`.
8. Métricas de costo LLM no consolidadas en dashboard único en repo.
9. `plugins.allow` en OpenClaw: omisión de IDs de canal desactiva el plugin aunque `channels.*.enabled` sea true ([README.md](../README.md) — riesgo operativo recurrente).
10. Bus factor: una persona + agentes — riesgo operativo organizacional (fuera del código pero relevante en veredicto).

### S.4 Top 10 oportunidades

1. Endurecer autenticación del gateway ante cualquier cambio de bind.
2. Completar checklist de alta para `dev-agency` / `legal` / `contadores` cuando el negocio lo exija.
3. Bindings Discord/Telegram granular por empresa y agente.
4. Job CI opcional para validación de sesiones Jarvis.
5. Consolidar naming de automatizaciones duplicadas en raíz vs subcarpetas.
6. Dashboard mínimo de uso de tokens si OpenClaw expone logs estructurados (investigación breve).
7. PWA o documentación mobile para demos de Agent Town.
8. Ampliar tests de integración del WebSocket proxy.
9. Mantener COMPANIES.md como fuente de verdad única al añadir empresas.
10. Plantilla de informe forense versionada (este documento) para comparar mes a mes.

### S.5 Roadmap priorizado (12 meses)

| Fase | Periodo | Acciones clave | Expertos / foco | Impacto esperado |
|------|---------|----------------|-----------------|------------------|
| Fase 0 — Cimientos | Mes 1–2 | Seguridad repo, symlinks, revisión auth gateway | SecOps, DevOps | Base estable |
| Fase 1 — Estabilización | Mes 3–4 | Bindings por canal; housekeeping YAML; ~~.gitignore jarvis-ecosystem~~ hecho | TL, Backend | Menos fricción |
| Fase 2 — Expansión | Mes 5–8 | Altas de nuevas empresas según COMPANIES + workspaces | PM, Arch | Holding completo en código |
| Fase 3 — Escala | Mes 9–12 | Valorar HA/cloud solo ante requisito | Cloud | Opcional |

### S.6 Veredicto final del comité

El ecosistema **clawvis-openclaw** es **operable y bien documentado** para un holding coordinado por Jarvis: gobierno en markdown ([GOBIERNO_JARVIS_V2.md](../jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md), [COMPANIES.md](../jarvis-ecosystem/COMPANIES.md)), integraciones de colaboración ya asumidas como instaladas, Agent Town como capa de visualización y proxy, y OpenClaw como motor de agentes con **multi-proveedor LLM**. La **madurez técnica** es mayor en la columna “plataforma + Jarvis” que en “producto SaaS de marketing/ventas integrado”, donde el repo aporta **proceso y prompts**, no sustitutos de GA/Ads/CRM enterprise. Las **mayores brechas** son seguridad perimetral del gateway ante cambios de red, coherencia de despliegue runtime/repo, y **materializar** las empresas planificadas cuando el negocio las active. El potencial es **alto** para operación interna del holding; la comercialización como producto cerrado requeriría integraciones y hardening adicionales no presentes en el alcance de este repositorio.

---

*Informe generado según [PROMPT_FORENSE_ECOSISTEMA_JARVIS.md](./PROMPT_FORENSE_ECOSISTEMA_JARVIS.md). Comité: 44 roles + síntesis S.1–S.6.*

*Addendum: alineación con el estado del repo tras commit de documentación y remedios (`PUSH-A-GITHUB.md`, `.gitignore` para `jarvis-ecosystem/.env`).*
