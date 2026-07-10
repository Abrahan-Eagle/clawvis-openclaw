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

El monorepo es un **respaldo operativo + código** alrededor de OpenClaw, Jarvis (holding multi-empresa) y Agent Town (UI Next.js). La arquitectura es coherente para un operador único, pero la **higiene de secretos y de `openclaw-state/` está rota**: hay una API key OpenRouter real en Git, `.env` trackeado pese a `.gitignore`, y backups/browser/auth-profiles versionados en contra de la política documentada.

| Dimensión | Estado |
|-----------|--------|
| Arquitectura | Viable (gateway + workspaces + UI) |
| Seguridad de repo | **Crítica** (secretos en índice) |
| Agent Town calidad | Buena base (CI, Vitest en `lib/`), gaps en proxy/discover |
| Jarvis ecosystem | Rico en skills/docs; deuda en duplicación y scripts destructivos |
| Docs vs realidad | Desalineados (`config/openclaw-home` “sin secretos” es falso) |

---

## 2. Mapa de madurez

| Área | Madurez | Justificación breve |
|------|---------|---------------------|
| Arquitectura | 7/10 | Flujo claro: canales → gateway → agentes → Agent Town |
| Seguridad / secretos | 2/10 | Key OpenRouter en Git; `.env` trackeado; gateway auth none |
| DevOps / deploy | 6/10 | systemd documentado; CI Agent Town; sin check de secretos/automations |
| QA / tests | 5/10 | Vitest `lib/` + pytest JMC; sin tests ws-proxy/discover |
| Datos / estado | 3/10 | Política clara, incumplimiento parcial; espejo docs enorme |
| Producto / gobierno | 7/10 | GOBIERNO_V2, dossiers, GOALS/LESSONS maduros |
| Agent Town UX | 6/10 | Pixel-office usable; token client-side; stub seat-sync |
| Documentación | 6/10 | Densa y útil; contradicciones sanitización/política |

**Promedio ponderado (seguridad ×2):** ~5.0/10.

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

| Fase | Acciones | Estado plan |
|------|----------|-------------|
| **0** | Este informe | Hecho |
| **1** | P0 secretos + script + README | **Aplicado 2026-07-10** (placeholders; `.env` destrackeado; `scripts/check-no-secrets.sh`) |
| **2** | Higiene openclaw-state + gitignore | **Aplicado** (`identity/`, bak, auth-profiles, browser user-data fuera del índice) |
| **3** | Agent Town + jarvis-ecosystem hardening | **Aplicado** (tests path/origin; auggie-bridge vía esbuild; reset-jarvis acotado; CI) |
| **4** | Docs + verificación | **Aplicado** |

**Pendiente humano:** rotar key OpenRouter en dashboard; decidir purga de historial Git; OK opcional para destrackear espejo `openclaw-state/workspace/docs/`.

**Fuera de alcance automático:** rotación OpenRouter (humano), purga `git filter-repo` (requiere orden explícita), destrackear espejo docs workspace (requiere OK).

---

## 7. Veredicto

El ecosistema es **operativamente útil y bien documentado** para un superusuario, pero **no está listo para compartir el repo** ni para tratar `config/openclaw-home` como plantilla segura hasta completar P0. Prioridad absoluta: **sanitizar índice + rotar key**. Después, higiene de state y tests del perímetro Agent Town.

*Informe generado 2026-07-10 — auditoría forense 360° clawvis-openclaw.*
