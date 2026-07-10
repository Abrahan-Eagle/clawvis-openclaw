# Informe forense 360° — clawvis-openclaw (julio 2026)

> Auditoría consolidada del monorepo `/var/www/clawvis-openclaw`.  
> Principio: **OpenClaw es el centro**; el resto (Jarvis, Agent Town, automations) lo fortalece.  
> Evidencia recogida con exploración en paralelo (ecosistema, Agent Town, higiene git/seguridad).  
> **No se reproducen secretos completos** en este documento.

---

## Tabla de contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Mapa de madurez](#2-mapa-de-madurez)
3. [Hallazgos por severidad](#3-hallazgos-por-severidad)
4. [Diagnóstico por área](#4-diagnóstico-por-área)
5. [Backlog Trello (TAREA-NNN)](#5-backlog-trello-tarea-nnn)
6. [Roadmap de remediación](#6-roadmap-de-remediación)
7. [Veredicto](#7-veredicto)

---

## 1. Resumen ejecutivo

> **Estado post-remediación (olas 1+2, 2026-07-10):** los secretos P0 de la auditoría inicial (OpenRouter en `models.json`, `.env` trackeado, `identity/`, bak, auth-profiles, browser user-data) **ya no están en el índice Git**. La ola 2 corrigió además tokens operator en `devices/paired.json`, PII de teléfono en `USER.md`, firma rota de `server.prod.mjs`, y alineó docs. **Pendiente humano:** rotar keys/tokens en dashboards y decidir purga de historial.

El monorepo es un **respaldo operativo + código** alrededor de OpenClaw, Jarvis (holding multi-empresa) y Agent Town (UI Next.js). La arquitectura es coherente para un operador único.

| Dimensión | Estado (post ola 2) |
|-----------|---------------------|
| Arquitectura | Viable (gateway + workspaces + UI) |
| Seguridad de repo | **Mejorada** (scanner CI; residuales destrackeados; historial aún puede tener secretos viejos) |
| Agent Town calidad | CI + Vitest `lib/` (6 suites); helpers path/origin; prod server alineado |
| Jarvis ecosystem | Rico en skills/docs; `reset-jarvis` acotado; automations check en CI |
| Docs vs realidad | Alineadas en ola 2 (este informe + README/AGENTS) |

---

## 2. Mapa de madurez

| Área | Madurez (ola 1) | Madurez (ola 2) | Notas |
|------|-----------------|-----------------|-------|
| Arquitectura | 7/10 | 7/10 | Sin cambio estructural |
| Seguridad / secretos | 2/10 | **7/10** | Índice limpio + scanner; historial/rotación humana pendiente |
| DevOps / deploy | 6/10 | **8/10** | CI secrets + automations; `server.prod` firmas OK |
| QA / tests | 5/10 | **6/10** | +path-safety + ws-origin; sin E2E WS real |
| Datos / estado | 3/10 | **6/10** | Política cumplida en prohibidos; espejo docs 819 aún opcional |
| Producto / gobierno | 7/10 | 7/10 | — |
| Agent Town UX | 6/10 | 6/10 | Threat model documentado |
| Documentación | 6/10 | **8/10** | Coherencia post-ola 2 |

**Promedio ponderado (seguridad ×2):** ~7.0/10 (antes ~5.0).

---

## 3. Hallazgos por severidad

### CRÍTICO (P0)

| ID | Hallazgo | Evidencia |
|----|----------|-----------|
| H-01 | API key OpenRouter real en Git (`sk-or-v1-…`, len≈73) | `config/openclaw-home/agents/jarvis/agent/models.json`, `…/jarvis-auto-light/…/models.json`, `openclaw-state/agents/jarvis/agent/models.json` |
| H-02 | `jarvis-ecosystem/.env` trackeado pese a ignore | `git ls-files jarvis-ecosystem/.env` |
| H-03 | README sanitizada afirma “sin secretos” | `config/openclaw-home/README.md` — contradice H-01 |

### ALTO (P1)

| ID | Hallazgo | Evidencia |
|----|----------|-----------|
| H-04 | `openclaw.json.bak*` trackeados | `openclaw-state/openclaw.json.bak` … `.bak.3` (ignore no aplica a índice) |
| H-05 | `auth-profiles.json` trackeado | `openclaw-state/agents/jarvis/agent/auth-profiles.json` |
| H-06 | Perfil Chromium parcial en Git | `openclaw-state/browser/openclaw/user-data*` |
| H-07 | Espejo docs OpenClaw (~819 archivos) en state | `openclaw-state/workspace/docs/` — infla repo |
| H-08 | `gateway.auth.mode: "none"` + PII en USER.md | Config versionada / agentes |

### MEDIO (P2)

| ID | Hallazgo | Evidencia |
|----|----------|-----------|
| H-09 | Duplicación automations raíz↔subcarpetas | `jarvis-ecosystem/automations/` + sync script |
| H-10 | `reset-jarvis.sh` hace `pkill -f node` global | `jarvis-ecosystem/reset-jarvis.sh:10` |
| H-11 | `auggie-bridge.mjs` duplicado del `.ts` | `agent-town/lib/auggie-bridge.{ts,mjs}` |
| H-12 | Sin tests de `ws-proxy` / `discover` | Solo 4 suites en `lib/__tests__/` |
| H-13 | `NEXT_PUBLIC_GATEWAY_TOKEN` en bundle cliente | Threat model débil |
| H-14 | career-ops embebido + node_modules en disco | `agents/ventas/career-ops/` |
| H-15 | Test huérfano pycache sin fuente | `jmc/tests/__pycache__/test_v19_features*` |

### BAJO (P3)

| ID | Hallazgo | Evidencia |
|----|----------|-----------|
| H-16 | `tools/stem-splitter/.venv` ~5.6 GB local | No en git; infla backups |
| H-17 | Docs densos (~142 md) riesgo drift | `jarvis-ecosystem/docs/` |

---

## 4. Diagnóstico por área

### 4.1 Arquitectura

- **Patrón:** monorepo de respaldo + runtime en `~/.openclaw` / `~/.jarvis-ecosystem`.
- **Componentes:** gateway (18789), proxy Cursor (4646), Agent Town (3000 → `/api/gateway`), agentes Jarvis/Marketing/Ventas + stubs.
- **Riesgo:** drift entre repo y HOME si el symlink no apunta al clon correcto (ya documentado en README).

### 4.2 Seguridad

- Superficie principal: **secretos en el índice Git** (H-01, H-02).
- Agent Town: proxy inyecta device auth desde `~/.openclaw`; discover lee FS; CSP permisiva por Phaser.
- Acción humana obligatoria: **rotar key OpenRouter**; decidir purga de historial si el repo fue compartido/público.

### 4.3 DevOps

- CI: lint/typecheck/build/test Agent Town; audit continue-on-error.
- Falta: job de escaneo de secretos, `sync-automations-yaml.sh --check`, pytest JMC.

### 4.4 QA

- Agent Town: cobertura umbral 40% solo `lib/**/*.ts`; hooks/Phaser/API sin tests.
- JMC: 3 tests + conftest; pycache huérfano.

### 4.5 Datos / openclaw-state

- Política en `docs/OPENCLAW_STATE_GIT_POLICY.md` correcta; **índice Git no la cumple**.
- Preferir `config/openclaw-home/` como plantilla sanitizada real.

### 4.6 Producto / gobierno

- Holding Marketing+Ventas activo; legal/contadores/dev-agency stub.
- GOALS/LESSONS y gobierno V2 dan continuidad operativa fuerte.

---

## 5. Backlog Trello (TAREA-NNN)

```
TAREA-001 [P0] [seguridad] [interno]
Titulo: Sanitizar models.json (OpenRouter → placeholder)
Descripcion: Reemplazar apiKey real por OPENROUTER_API_KEY / env en 3+ models.json; verificar con script.
Criterio: rg no encuentra sk-or-v1- en working tree (excl. historial).
Esfuerzo: 1h

TAREA-002 [P0] [seguridad] [interno]
Titulo: Destrackear jarvis-ecosystem/.env
Descripcion: git rm --cached; conservar en disco; confirmar .gitignore.
Criterio: git ls-files no lista el .env.
Esfuerzo: 15m

TAREA-003 [P0] [docs] [interno]
Titulo: Corregir README config/openclaw-home + script check-secrets
Descripcion: Documentar qué está sanitizado; añadir scripts/check-no-secrets.sh.
Criterio: README honesto; script falla si hay patrones de key.
Esfuerzo: 1h

TAREA-004 [P0] [humano] [OpenRouter]
Titulo: Rotar API key OpenRouter comprometida
Descripcion: Dashboard OpenRouter → revoke + nueva key solo en ~/.openclaw (no git).
Criterio: Key antigua inválida; nueva fuera de git.
Esfuerzo: 15m (humano)

TAREA-005 [P1] [git] [interno]
Titulo: Destrackear bak / auth-profiles / browser user-data
Descripcion: git rm --cached según política; reforzar .gitignore raíz.
Criterio: git ls-files limpio; política alineada.
Esfuerzo: 1h

TAREA-006 [P1] [git] [opcional]
Titulo: Evaluar destrackear espejo docs openclaw-state/workspace
Descripcion: ~819 archivos; dejar puntero a docs oficiales.
Criterio: Decisión documentada; OK usuario.
Esfuerzo: 2h

TAREA-007 [P2] [agent-town] [interno]
Titulo: Eliminar auggie-bridge.mjs duplicado + tests proxy/discover
Descripcion: Una sola fuente; Vitest para checkOrigin y path traversal.
Criterio: pnpm test verde; sin .mjs paralelo drift.
Esfuerzo: 4h

TAREA-008 [P2] [jarvis] [interno]
Titulo: Acotar reset-jarvis.sh + sync automations en CI
Descripcion: No pkill node global; CI --check automations.
Criterio: Script seguro; CI falla si drift YAML.
Esfuerzo: 2h

TAREA-009 [P2] [docs] [interno]
Titulo: Alinear README / política state / AGENTS.md post-remediación
Descripcion: Reflejar estado real tras P0/P1.
Criterio: Docs = comportamiento.
Esfuerzo: 1h
```

---

## 6. Roadmap de remediación

### Ola 1 (2026-07-10 mañana)

| Fase | Acciones | Estado |
|------|----------|--------|
| **0** | Informe inicial | Hecho |
| **1** | P0 secretos + script + README | **Aplicado** |
| **2** | Higiene openclaw-state + gitignore | **Aplicado** |
| **3** | Agent Town + jarvis hardening | **Aplicado** (parcial H-12: helpers, no E2E WS) |
| **4** | Docs + verificación | **Aplicado** |

### Ola 2 (2026-07-10 tarde) — re-forense

| ID | Hallazgo | Estado |
|----|----------|--------|
| W2-01 | `server.prod.mjs` firmas rotas | **Aplicado** |
| W2-02 | `devices/paired.json` tokens operator | **Aplicado** (destrackeado; **rotar tokens humano**) |
| W2-03 | PII teléfono / cron runs / delivery-queue | **Aplicado** (destrack + placeholder USER.md) |
| W2-04 | Scanner incompleto | **Aplicado** |
| W2-05 | `prepublishOnly` sin regenerar `.mjs` | **Aplicado** |
| W2-06 | `reset-jarvis` pkill amplio | **Aplicado** |
| W2-07…W2-11 | Incoherencias docs | **Aplicado** (esta sección + README/AGENTS/CLAUDE) |

### Estado de hallazgos ola 1 (H-xx)

| ID | Estado |
|----|--------|
| H-01…H-06 | **Resuelto** en índice (historial puede conservar copias) |
| H-07 | **Pendiente opcional** (espejo 819 docs) |
| H-08 | **Parcial** (`gateway.auth.mode: none` sigue; PII nombre en USER.md intencional) |
| H-09 | **Mitigado** (CI `--check` automations) |
| H-10 | **Resuelto** |
| H-11 | **Resuelto** (mjs = artefacto esbuild) |
| H-12 | **Parcial** (tests helpers; no suite E2E proxy) |
| H-13 | **Documentado** (threat model) |
| H-14…H-17 | **Pendiente / bajo** |

**Pendiente humano:** rotar OpenRouter + 4 tokens operator; decidir purga historial; OK espejo workspace docs.

---

## 7. Veredicto

Tras olas 1+2, el **índice Git está en condición razonable** para un repo **privado** de un solo operador: plantilla sanitizada, scanner en CI, producción Agent Town con firmas correctas. **No** asumir que el historial está limpio ni que tokens antiguos están rotados. Compartir el repo o hacerlo público **sigue requiriendo** rotación + (opcional) `git filter-repo`.

*Informe generado 2026-07-10 — auditoría forense 360° + ola 2 clawvis-openclaw.*
