# Prompt: Analisis Forense Profundo + Evaluacion de Repos Externos -- Ecosistema JARVIS

> **Como usar este prompt:** Copia todo el contenido de este archivo y pegalo en una nueva sesion de Cursor (o cualquier LLM con acceso al repositorio `/var/www/clawvis-openclaw`). Si quieres analizar repositorios de GitHub externos, pega sus URLs en la seccion `REPOSITORIOS EXTERNOS A EVALUAR`. La IA debe leer los archivos referenciados, clonar/inspeccionar los repos externos, ejecutar el analisis completo y generar el informe con plan de implementacion.

---

## PRINCIPIO FUNDAMENTAL

**OpenClaw es el CENTRO del ecosistema.** Todo gira alrededor del gateway OpenClaw y su agente maestro Jarvis. Los repositorios externos de GitHub son **fuentes de ideas, patrones y codigo** para fortalecer a Jarvis y OpenClaw. Nunca al reves: no se adapta JARVIS a un repo externo, se extraen las partes utiles del repo externo para potenciar JARVIS/OpenClaw.

---

## REPOSITORIOS EXTERNOS A EVALUAR

> **Instruccion:** Pega aqui las URLs de los repositorios de GitHub que quieres analizar. Puedes pegar 1 o mas. Si no pegas ninguno, el analisis sera solo forense interno del ecosistema JARVIS.

```
REPO_1: [pegar URL aqui]
REPO_2: [pegar URL aqui]
REPO_3: [pegar URL aqui]
... (agregar mas si es necesario)
```

**Para cada repo externo, la IA debe:**
1. Clonar o inspeccionar el repositorio (usar `gh repo view`, `WebFetch` del README, o clonar si es necesario)
2. Leer el README, package.json/requirements.txt, estructura de carpetas, archivos clave
3. Identificar el stack tecnologico, arquitectura, funcionalidades principales
4. Evaluar compatibilidad con el ecosistema JARVIS/OpenClaw
5. Generar el analisis por cada uno de los 44 expertos

---

## CONTEXTO DEL PROYECTO BASE (JARVIS / OpenClaw)

El repositorio `clawvis-openclaw` (ruta: `/var/www/clawvis-openclaw`) es el **monorepo operativo** del **Ecosistema JARVIS**: una plataforma de orquestacion IA que administra un **holding de empresas** mediante agentes autonomos.

### Arquitectura del ecosistema

```
                    ┌─────────────────────────────────────┐
                    │         SUPERUSUARIO (Abraham)       │
                    └──────────────┬──────────────────────┘
                                   │ unico canal humano
                    ┌──────────────▼──────────────────────┐
                    │     JARVIS (agente maestro)          │
                    │  jarvis-ecosystem/agents/jarvis/     │
                    └──────────────┬──────────────────────┘
                                   │ orquesta
              ┌────────────────────┼────────────────────┐
              │                    │                     │
    ┌─────────▼────────┐ ┌────────▼─────────┐ ┌────────▼─────────┐
    │   MARKETING      │ │    VENTAS        │ │  (PLANIFICADAS)  │
    │ CEO/Sup/Equipo   │ │ CEO/Sup/Equipo   │ │ dev, legal, cont.│
    └─────────┬────────┘ └────────┬─────────┘ └──────────────────┘
              │                    │
    ┌─────────▼────────────────────▼─────────┐
    │          OpenClaw GATEWAY               │
    │  (motor central: LLM, tools, canales)  │
    │  Puerto 18789 / systemd                │
    ├────────────────────────────────────────┤
    │ Canales: Telegram, Discord, WhatsApp   │
    │ Proveedores: Groq, OpenRouter, Gemini  │
    │         Ollama, Cursor proxy, OpenCode │
    │ Tools: Trello API, navegador, ClawHub  │
    │ Memoria: SQLite, sesiones JSONL        │
    └─────────┬──────────────────────────────┘
              │ WebSocket proxy
    ┌─────────▼──────────────────────────────┐
    │         AGENT TOWN                     │
    │  Next.js 16 + React 19 + Phaser 3     │
    │  UI pixel-office / Puerto 3000         │
    └────────────────────────────────────────┘
```

### Componentes del monorepo

| Componente | Ruta | Rol |
|------------|------|-----|
| **OpenClaw Gateway** | Proceso externo (`~/.openclaw/`) | Motor central: LLM multi-proveedor, herramientas, canales |
| **Jarvis** | `jarvis-ecosystem/agents/jarvis/` | Agente maestro: gobierno, memoria, skills, model-router |
| **Agente Marketing** | `jarvis-ecosystem/agents/marketing/` | Empresa de marketing: IDENTITY, SOUL, skills |
| **Agente Ventas** | `jarvis-ecosystem/agents/ventas/` | Empresa de ventas: IDENTITY, SOUL, skills |
| **Agent Town** | `agent-town/` | App web Next.js 16 + Phaser 3; WebSocket proxy al gateway |
| **Automatizaciones** | `jarvis-ecosystem/automations/` | ClawFlows YAML: competitor-monitor, pipeline-report, registry |
| **Gobierno** | `jarvis-ecosystem/docs/` | GOBIERNO_JARVIS_V2, dossiers, Trello, Discord, reportes |
| **Config sanitizada** | `config/openclaw-home/` | Copia de `~/.openclaw` sin secretos |
| **Estado** | `openclaw-state/` | Sesiones, memoria SQLite, transcripts |
| **Deploy** | `deploy/systemd/` | Units: gateway, proxy Cursor, Agent Town |
| **Docs operativos** | `docs/` | Forense runbook, modelos, proveedores, Trello |

### Stack tecnologico

| Capa | Tecnologias |
|------|-------------|
| **Runtime** | Node.js 22+, OpenClaw CLI (npm global) |
| **Frontend** | Next.js 16, React 19, Tailwind CSS 4, Phaser 3, TypeScript, pnpm |
| **Comunicacion** | WebSocket (proxy gateway:18789), API Routes Next.js |
| **LLM** | Groq, OpenRouter, Google Gemini, Ollama, Cursor proxy, OpenCode |
| **Canales** | Telegram, Discord, WhatsApp |
| **Herramientas** | Trello API, navegador embebido, skills ClawHub |
| **Persistencia** | SQLite (memoria gateway), JSONL (sesiones), JSON (dossiers) |
| **CI/CD** | GitHub Actions (lint, typecheck, build, test, audit) |
| **Despliegue** | systemd units en servidor unico (sin Docker) |

### Modelo de gobierno del holding

| Actor | Rol | Interaccion |
|-------|-----|-------------|
| **Superusuario** (Abraham) | Unico humano con acceso directo a Jarvis | Chat Telegram directo |
| **Jarvis** | Agente maestro, orquestador | Gobierna todas las empresas |
| **CEO** (por empresa) | Responsable de resultado de su unidad | Recibe tareas de Jarvis via Trello/Discord |
| **Supervisor** (por empresa) | Calidad, Trello, Discord, reportes | Reporta al CEO semanal/quincenal |
| **Clientes externos** | Organizaciones que contratan servicios | Representados por dossiers JSON |
| **Empresas activas** | Marketing, Ventas | Con CEO/Supervisor/Equipo |
| **Empresas planificadas** | Dev-agency, legal, contadores | Pendientes de activacion |

---

## OBJETIVO DEL ANALISIS

Este analisis tiene **dos fases**:

### FASE I: Forense interno del ecosistema JARVIS

Cada experto analiza el estado actual del ecosistema desde su dominio:
1. **LEER** archivos del repositorio relevantes (rutas especificas indicadas por rol)
2. **DIAGNOSTICAR** con evidencia (citar archivos, lineas, configuraciones)
3. **IDENTIFICAR** hallazgos criticos, riesgos, deuda tecnica, oportunidades
4. **CALIFICAR** madurez de su area (escala 1-10 con justificacion)

### FASE II: Evaluacion de repos externos para fortalecer JARVIS/OpenClaw

Si hay repos externos listados arriba, cada experto adicionalmente:
1. **ANALIZAR** el repo externo desde su perspectiva profesional
2. **MAPEAR** que funcionalidades del repo externo resuelven carencias detectadas en Fase I
3. **EVALUAR** compatibilidad tecnica con OpenClaw (lenguaje, arquitectura, licencia, dependencias)
4. **PROPONER** que extraer/adaptar y como integrarlo al ecosistema
5. **ESTIMAR** esfuerzo de adaptacion y riesgo de integracion
6. **CLASIFICAR** cada elemento como: ADOPTAR / ADAPTAR / INSPIRARSE / DESCARTAR

### FASE III: Plan de implementacion consolidado

Generar un plan accionable que combine los hallazgos de ambas fases.

---

## FORMATO DE SALIDA POR EXPERTO

Cada experto genera su seccion con esta estructura:

```markdown
### [NUMERO.NUMERO] [ROL]
**Area:** [dominio especifico]
**Madurez actual JARVIS:** [X/10]

#### FASE I: Diagnostico forense del ecosistema

**Archivos analizados:**
- [ruta completa de cada archivo leido]

**Hallazgos:**
1. [HALLAZGO] -- Evidencia: [archivo:linea o configuracion]
2. ...

**Riesgos:**
| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| ... | CRITICO/ALTO/MEDIO/BAJO | ... | ... |

**Oportunidades:**
1. [Oportunidad con justificacion]

**Recomendaciones internas:**
| # | Prioridad | Accion | Esfuerzo | Impacto |
|---|-----------|--------|----------|---------|
| 1 | P0 | ... | ... | ... |

#### FASE II: Evaluacion de repos externos (si aplica)

**Repo: [nombre/URL]**

**Resumen del repo:** [que hace, stack, licencia, estrellas, actividad]

**Funcionalidades relevantes para mi area:**
| Funcionalidad | Archivo/modulo en el repo | Resuelve carencia en JARVIS | Clasificacion |
|---------------|--------------------------|------------------------------|---------------|
| ... | ... | ... | ADOPTAR/ADAPTAR/INSPIRARSE/DESCARTAR |

**Compatibilidad con OpenClaw:**
- Lenguaje/runtime: [compatible/requiere adaptacion/incompatible]
- Puede ser skill de OpenClaw: [si/no/parcial]
- Puede ser ClawFlow: [si/no/parcial]
- Puede ser modulo de Agent Town: [si/no/parcial]
- Licencia: [compatible/revisar/incompatible]

**Propuesta de integracion:**
[Descripcion concreta de como integrar lo util al ecosistema JARVIS]

**Esfuerzo estimado:** [horas/dias] | **Riesgo:** [bajo/medio/alto]
```

---

## EMPRESA 1: AGENCIA DE DESARROLLO DE SOFTWARE

> 16 expertos analizan calidad tecnica, arquitectura, seguridad, operaciones y producto.

---

### 1.1 Arquitecto de Software

**Mision:** Evaluar arquitectura general, patrones de diseno, acoplamiento, escalabilidad. En repos externos: evaluar si su arquitectura es superior y que patrones adoptar.

**Archivos JARVIS a leer:**
- `README.md` (raiz)
- `jarvis-ecosystem/README.md`
- `agent-town/package.json`
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `agent-town/lib/gateway.ts`
- `agent-town/app/layout.tsx`
- `agent-town/app/api/agents/discover/route.ts`
- `agent-town/app/api/internal/seat-sync/route.ts`
- `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/agents/jarvis/AGENTS.md`
- `deploy/systemd/` (todos)

**Preguntas forense (Fase I):**
- Cual es el patron arquitectonico dominante y es el adecuado?
- Como se comunican los componentes (gateway, Agent Town, agentes, canales)?
- Existen dependencias circulares o acoplamiento excesivo?
- Es extensible para empresas planificadas (dev-agency, legal, contadores)?
- Que tan resiliente es ante fallos de un componente?

**Preguntas repo externo (Fase II):**
- El repo externo usa una arquitectura superior para orquestacion de agentes?
- Que patrones arquitectonicos del repo externo faltan en JARVIS?
- Se puede reemplazar algun componente de JARVIS con algo del repo externo?
- El repo externo resuelve problemas de escalabilidad que JARVIS tiene?

---

### 1.2 Lider Tecnico (Tech Lead)

**Mision:** Evaluar calidad de codigo, convenciones, CI/CD, deuda tecnica. En repos externos: comparar practicas y adoptar las mejores.

**Archivos JARVIS a leer:**
- `agent-town/` (estructura de `components/`, `lib/`, `types/`)
- `agent-town/.github/workflows/ci.yml`
- `agent-town/tsconfig.json`
- `agent-town/eslint.config.mjs`
- `jarvis-ecosystem/agents/jarvis/scripts/` (todos)
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`
- `.gitignore`

**Preguntas forense (Fase I):**
- El codigo sigue convenciones consistentes?
- La pipeline CI es suficiente?
- Donde se concentra la deuda tecnica?
- Es mantenible por un equipo pequeno?

**Preguntas repo externo (Fase II):**
- El repo externo tiene mejor CI/CD, linting, testing?
- Que convenciones o tooling del repo externo deberiamos adoptar?
- Su estructura de proyecto es mas escalable que la nuestra?

---

### 1.3 Desarrollador Senior (Senior Developer)

**Mision:** Analizar calidad de implementacion, patrones, manejo de errores, testing. En repos externos: identificar codigo de alta calidad reutilizable.

**Archivos JARVIS a leer:**
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `agent-town/lib/gateway.ts`
- `agent-town/components/` (archivos `.tsx`)
- `agent-town/components/game/` (Phaser)
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`

**Preguntas forense (Fase I):**
- Hay manejo adecuado de errores y edge cases?
- Existen antipatrones o code smells?
- El WebSocket/proxy es robusto ante desconexiones?

**Preguntas repo externo (Fase II):**
- Que modulos del repo externo tienen calidad de codigo superior?
- Hay utilidades, helpers o librerias internas que podriamos extraer?
- El manejo de errores es mejor y podemos copiarlo?

---

### 1.4 Ingeniero de DevOps

**Mision:** Evaluar infraestructura, despliegue, monitoreo, automatizacion. En repos externos: adoptar mejores practicas de ops.

**Archivos JARVIS a leer:**
- `deploy/systemd/` (todos)
- `agent-town/.github/workflows/ci.yml`
- `agent-town/package.json` (scripts)
- `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`
- `jarvis-ecosystem/automations/` (todos los YAML)
- `jarvis-ecosystem/scripts/`

**Preguntas forense (Fase I):**
- Existe despliegue reproducible y documentado?
- Hay monitoreo y alertas?
- Que pasa si el servidor se reinicia?
- Existe disaster recovery?
- Por que no hay Docker y deberia haberlo?

**Preguntas repo externo (Fase II):**
- El repo externo tiene Docker/Kubernetes/Terraform que podamos adaptar?
- Tiene mejor monitoreo, logging o health checks?
- Sus scripts de deploy son reutilizables?

---

### 1.5 Especialista en Ciberseguridad

**Mision:** Auditar seguridad: secretos, autenticacion, superficie de ataque. En repos externos: evaluar postura de seguridad antes de integrar.

**Archivos JARVIS a leer:**
- `.gitignore`
- `config/openclaw-home/README.md`
- `config/openclaw-home/openclaw.json`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md` (Fase D)
- `openclaw-state/` (estructura)
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `jarvis-ecosystem/.env` (verificar .gitignore)
- `PUSH-A-GITHUB.md`

**Preguntas forense (Fase I):**
- Hay secretos expuestos en el repositorio?
- La autenticacion del gateway es adecuada?
- El proxy WebSocket valida origen?
- Hay riesgo de prompt injection?

**Preguntas repo externo (Fase II):**
- El repo externo tiene vulnerabilidades conocidas (CVEs, dependencias desactualizadas)?
- Introduce nuevas superficies de ataque al integrarlo?
- Maneja secretos/auth de forma segura?
- Su licencia permite uso comercial?

---

### 1.6 Arquitecto de Cloud

**Mision:** Evaluar estrategia cloud, escalabilidad, costos. En repos externos: identificar servicios cloud o patrones cloud-native utiles.

**Archivos JARVIS a leer:**
- `deploy/systemd/` (todos)
- `agent-town/package.json`
- `agent-town/server.ts`
- `config/openclaw-home/openclaw.json`
- `docs/PROVEEDOR_CURSOR_OPENCLAW.md`
- `docs/MODELOS_JARVIS_OPENCLAW.md`

**Preguntas forense (Fase I):**
- Esta listo para despliegue cloud?
- Como se gestionan costos de proveedores LLM?
- El despliegue systemd en servidor unico es adecuado?

**Preguntas repo externo (Fase II):**
- El repo externo es cloud-native y podemos aprender de su infra?
- Tiene integraciones con servicios cloud que JARVIS necesita?
- Su modelo de costos es replicable?

---

### 1.7 Disenador de UX/UI

**Mision:** Evaluar experiencia de usuario de Agent Town. En repos externos: identificar mejores patrones de UI/UX.

**Archivos JARVIS a leer:**
- `agent-town/app/page.tsx`
- `agent-town/app/layout.tsx`
- `agent-town/app/globals.css`
- `agent-town/components/` (todos)
- `agent-town/public/` (assets)
- `agent-town/components/game/config/`

**Preguntas forense (Fase I):**
- La interfaz pixel-office es intuitiva?
- Existe sistema de diseno coherente?
- Agent Town es accesible (a11y)?
- La experiencia mobile es adecuada?

**Preguntas repo externo (Fase II):**
- El repo externo tiene una UI/UX superior para interaccion con agentes IA?
- Hay componentes visuales que podamos integrar en Agent Town?
- Tiene un sistema de diseno reutilizable?

---

### 1.8 Ingeniero de QA

**Mision:** Evaluar testing, cobertura, calidad. En repos externos: adoptar estrategias de testing superiores.

**Archivos JARVIS a leer:**
- `agent-town/.github/workflows/ci.yml`
- `agent-town/package.json` (scripts test)
- Buscar `*.test.*` y `*.spec.*` en el repo
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`

**Preguntas forense (Fase I):**
- Cual es la cobertura de tests?
- Hay tests para flujos criticos (WebSocket, proxy, agentes)?
- Los ClawFlows tienen validacion?

**Preguntas repo externo (Fase II):**
- El repo externo tiene tests que podamos adaptar para JARVIS?
- Usa frameworks de testing que deberiamos adoptar?
- Tiene tests de integracion o e2e para agentes IA?

---

### 1.9 Gerente de Producto (Product Manager)

**Mision:** Evaluar vision de producto, roadmap, viabilidad comercial. En repos externos: identificar features de producto que fortalezcan la propuesta de valor de JARVIS.

**Archivos JARVIS a leer:**
- `README.md` (raiz)
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense (Fase I):**
- Existe vision de producto clara?
- Hay roadmap priorizado?
- El holding multi-empresa es viable como producto?
- Que tan lejos esta de ser comercializable?

**Preguntas repo externo (Fase II):**
- El repo externo tiene funcionalidades de producto que JARVIS necesita?
- Su modelo de negocio es relevante para el holding?
- Que features le darian ventaja competitiva a JARVIS?

---

### 1.10 Cientifico de Datos

**Mision:** Evaluar flujo de datos, analiticas, metricas. En repos externos: identificar pipelines de datos o analiticas replicables.

**Archivos JARVIS a leer:**
- `openclaw-state/memory/` (estructura)
- `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`

**Preguntas forense (Fase I):**
- Que datos genera el ecosistema y como se almacenan?
- Se rastrean metricas de LLM (tokens, costos, latencia)?
- Los transcripts son explotables para insights?

**Preguntas repo externo (Fase II):**
- El repo externo tiene dashboards, analiticas o pipelines de datos?
- Tiene modelos de datos que podamos adoptar?
- Ofrece visualizacion de metricas de agentes IA?

---

### 1.11 Ingeniero de Machine Learning

**Mision:** Evaluar estrategia IA/ML, modelos, prompts. En repos externos: identificar tecnicas de ML, RAG, fine-tuning o evaluacion de prompts.

**Archivos JARVIS a leer:**
- `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`
- `docs/MODELOS_JARVIS_OPENCLAW.md`
- `docs/CIERRE_MODULO_OLLAMA_LOCAL.md`
- Todos los `IDENTITY.md` y `SOUL.md` de agentes

**Preguntas forense (Fase I):**
- La estrategia multi-modelo es optima?
- Existe evaluacion sistematica de respuestas?
- Los prompts de sistema estan optimizados?

**Preguntas repo externo (Fase II):**
- El repo externo implementa RAG, fine-tuning o evaluacion de LLM?
- Tiene un framework de evaluacion de prompts?
- Su routing de modelos es mas inteligente que el nuestro?
- Implementa tecnicas como tool-use, function-calling o agentic patterns?

---

### 1.12 Administrador de Bases de Datos (DBA)

**Mision:** Evaluar almacenamiento, integridad, backups. En repos externos: identificar esquemas de datos o estrategias de persistencia superiores.

**Archivos JARVIS a leer:**
- `openclaw-state/` (estructura)
- `openclaw-state/memory/` (SQLite)
- `openclaw-state/agents/` (sesiones)
- `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `jarvis-ecosystem/client-dossiers/` (si existe)

**Preguntas forense (Fase I):**
- SQLite es adecuado para el volumen esperado?
- Existe estrategia de backup?
- Los JSONL crecen sin limite?
- Se necesita BD vectorial dedicada?

**Preguntas repo externo (Fase II):**
- El repo externo usa una estrategia de datos superior (vector DB, graph DB, time-series)?
- Tiene migraciones o esquemas formales que podamos adaptar?
- Su gestion de memoria/sesiones de agentes es mas robusta?

---

### 1.13 Desarrollador Mobile

**Mision:** Evaluar viabilidad mobile. En repos externos: identificar soluciones mobile o PWA adaptables.

**Archivos JARVIS a leer:**
- `agent-town/app/layout.tsx`
- `agent-town/app/globals.css`
- `agent-town/components/`
- `agent-town/public/`
- `agent-town/package.json`

**Preguntas forense (Fase I):**
- Agent Town es responsive?
- Phaser 3 funciona en mobile?
- Los canales (Telegram, WhatsApp) cubren la necesidad mobile?

**Preguntas repo externo (Fase II):**
- El repo externo tiene app mobile o PWA para interaccion con agentes?
- Tiene componentes responsive que podamos integrar?
- Su experiencia mobile es replicable en Agent Town?

---

### 1.14 Desarrollador Backend

**Mision:** Analizar logica de servidor, APIs, integraciones. En repos externos: identificar APIs, middleware o integraciones reutilizables.

**Archivos JARVIS a leer:**
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `agent-town/lib/gateway.ts`
- `agent-town/app/api/` (todas las rutas)
- `jarvis-ecosystem/automations/` (YAML)
- `jarvis-ecosystem/agents/jarvis/scripts/` (todos)

**Preguntas forense (Fase I):**
- El servidor custom es robusto para produccion?
- Las API Routes tienen validacion adecuada?
- Las automatizaciones son fiables?

**Preguntas repo externo (Fase II):**
- El repo externo tiene APIs o integraciones que JARVIS necesita?
- Tiene middleware reutilizable (auth, rate-limiting, logging)?
- Su manejo de WebSocket/real-time es superior?

---

### 1.15 Desarrollador Frontend

**Mision:** Analizar calidad frontend, rendimiento, modernidad. En repos externos: identificar componentes o patrones frontend adoptables.

**Archivos JARVIS a leer:**
- `agent-town/app/` (paginas)
- `agent-town/components/` (componentes)
- `agent-town/lib/` (utilidades)
- `agent-town/types/`
- `agent-town/app/globals.css`

**Preguntas forense (Fase I):**
- Se usan correctamente Server/Client Components?
- El rendimiento de Phaser 3 embebido es aceptable?
- Hay gestion de estado adecuada?

**Preguntas repo externo (Fase II):**
- El repo externo tiene componentes de UI para chat/agentes IA?
- Tiene un sistema de componentes reutilizable?
- Su experiencia de interaccion con IA es superior?

---

### 1.16 Desarrollador Fullstack

**Mision:** Evaluar coherencia end-to-end. En repos externos: evaluar como una integracion afectaria al flujo completo.

**Archivos JARVIS a leer:**
- Todos los de Backend y Frontend
- `jarvis-ecosystem/agents/jarvis/AGENTS.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`

**Preguntas forense (Fase I):**
- El flujo usuario → Agent Town → WebSocket → Gateway → LLM → UI es coherente?
- Los tipos TypeScript cubren contratos entre capas?
- Es debuggeable end-to-end?

**Preguntas repo externo (Fase II):**
- La integracion del repo externo romperia el flujo end-to-end?
- El repo externo resuelve brechas entre capas que JARVIS tiene?
- Hay lecciones de DX (developer experience) que adoptar?

---

## EMPRESA 2: AGENCIA DE MARKETING DIGITAL

> 16 expertos analizan capacidades de marketing digital del ecosistema y como los repos externos las fortalecen.

---

### 2.1 Estratega Digital (Digital Strategist)

**Mision:** Evaluar estrategia digital y capacidad de generar estrategias para clientes. En repos externos: identificar frameworks o herramientas de estrategia digital.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/marketing/IDENTITY.md`
- `jarvis-ecosystem/agents/marketing/AGENTS.md`
- `jarvis-ecosystem/agents/marketing/SOUL.md`
- `jarvis-ecosystem/automations/marketing-competitor-monitor.yaml`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense (Fase I):**
- El agente de marketing tiene estrategia digital definida?
- Puede generar estrategias personalizadas por cliente (dossier)?
- Hay analisis competitivo automatizado?
- Que KPIs se pueden rastrear nativamente?

**Preguntas repo externo (Fase II):**
- El repo externo tiene frameworks de estrategia digital automatizada?
- Tiene generacion de planes de marketing con IA?
- Su analisis de competencia es mas completo?
- Puede convertirse en skill de OpenClaw para el agente de marketing?

---

### 2.2 Especialista en SEO

**Mision:** Evaluar capacidades SEO. En repos externos: herramientas SEO integrables.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/agents/jarvis/skills/` (xurl, summarize)
- `agent-town/app/layout.tsx`

**Preguntas forense (Fase I):**
- Hay skills de SEO integradas?
- Agent Town tiene SEO basico?
- Se puede auditar SEO de clientes?

**Preguntas repo externo (Fase II):**
- El repo tiene herramientas de auditoria SEO automatizada?
- Puede generar contenido SEO-optimizado?
- Tiene integracion con Search Console/APIs de SEO?
- Se puede envolver como skill de OpenClaw?

---

### 2.3 Especialista en SEM / Paid Search

**Mision:** Evaluar capacidad de gestion de ads. En repos externos: herramientas de gestion de campanas.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Seguir el formato estandar evaluando integracion con Google Ads, Meta Ads; generacion de copys para anuncios; automatizacion de campanas; reportes de rendimiento.

---

### 2.4 Gerente de Performance

**Mision:** Evaluar medicion de rendimiento. En repos externos: dashboards y herramientas de performance.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/automations/` (todos)
- `jarvis-ecosystem/agents/marketing/`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas forense y repo externo:** Dashboards, conversion tracking, integracion con Analytics/Tag Manager, reportes automaticos, metas y cumplimiento.

---

### 2.5 Social Media Manager

**Mision:** Evaluar gestion de redes sociales. En repos externos: herramientas de social media management.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/IDENTITY.md`
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/marketing-competitor-monitor.yaml`
- `config/openclaw-home/openclaw.json`

**Preguntas forense y repo externo:** Publicacion programada, monitoreo de menciones, calendario editorial, engagement automatizado, gestion multi-plataforma.

---

### 2.6 Estratega de Contenido (Content Strategist)

**Mision:** Evaluar planificacion y creacion de contenido. En repos externos: herramientas de content generation/curation.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/jarvis/skills/` (summarize, xurl)
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/registry/` (github-trending)
- `jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md`

**Preguntas forense y repo externo:** Generacion de contenido (blogs, posts, emails), flujo de aprobacion, calendario editorial en Trello, content curation automatizada.

---

### 2.7 Copywriter Creativo

**Mision:** Evaluar voz de marca y generacion de copy. En repos externos: herramientas de copywriting IA.

**Archivos JARVIS a leer:**
- Todos los `SOUL.md` e `IDENTITY.md`
- `jarvis-ecosystem/agents/jarvis/AGENTS.md`
- `jarvis-ecosystem/agents/marketing/AGENTS.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Voz de marca consistente, generacion de copy multi-canal, plantillas, adaptacion de tono por cliente, optimizacion de prompts para creatividad.

---

### 2.8 Media Buyer

**Mision:** Evaluar gestion de compra de medios. En repos externos: herramientas de media buying/optimization.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Integracion con plataformas de medios, tracking de presupuestos/ROI, planificacion de medios, optimizacion de gasto automatizada.

---

### 2.9 Analista de Datos de Marketing

**Mision:** Evaluar analisis de datos de marketing. En repos externos: herramientas de analitica y BI.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/automations/`
- `openclaw-state/memory/`
- `jarvis-ecosystem/agents/jarvis/scripts/`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas forense y repo externo:** Datos de marketing recolectados, visualizacion, insights automaticos, integracion BI, segmentacion de audiencias.

---

### 2.10 Especialista en Email Marketing / Automation

**Mision:** Evaluar email marketing y automatizacion de comunicacion. En repos externos: herramientas de email/automation.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/agents/jarvis/skills/`

**Preguntas forense y repo externo:** Integracion con plataformas de email, flujos de nurturing, ClawFlows para emails, segmentacion, metricas (open rate, CTR).

---

### 2.11 Gerente de Cuentas (Account Manager)

**Mision:** Evaluar gestion de relaciones con clientes. En repos externos: herramientas de account management.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/` (si existe)
- `jarvis-ecosystem/docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas forense y repo externo:** Dossiers suficientes para gestion de cuentas, visibilidad de estado de clientes, reportes por cliente, alertas para clientes desatendidos.

---

### 2.12 Community Manager

**Mision:** Evaluar gestion de comunidades. En repos externos: herramientas de community management.

**Archivos JARVIS a leer:**
- `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/agents/jarvis/AGENTS.md` (Group Chats)
- `jarvis-ecosystem/docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md`
- `jarvis-ecosystem/docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md`

**Preguntas forense y repo externo:** Jarvis como community manager, moderacion automatica, engagement proactivo, metricas de comunidad.

---

### 2.13 Especialista en Inbound Marketing

**Mision:** Evaluar estrategia inbound. En repos externos: funnels, lead capture, nurturing.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/marketing/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/` (como landing)

**Preguntas forense y repo externo:** Funnel definido, Agent Town como captacion, lead nurturing automatizado, lead scoring, landing pages.

---

### 2.14 Especialista en CRM

**Mision:** Evaluar gestion de relaciones y datos de contactos. En repos externos: CRM o gestion de contactos.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/jarvis/skills/`

**Preguntas forense y repo externo:** Dossiers como CRM minimo, integracion con CRM comerciales, ciclo de vida del cliente, pipeline visible, follow-ups automatizados.

---

### 2.15 Disenador UX/UI para Conversion

**Mision:** Evaluar interfaces para conversion. En repos externos: patrones de conversion, A/B testing.

**Archivos JARVIS a leer:**
- `agent-town/app/page.tsx`
- `agent-town/components/`
- `agent-town/app/globals.css`

**Preguntas forense y repo externo:** CTAs, onboarding, A/B testing, flujos optimizados, journey map, metricas de conversion.

---

### 2.16 Gerente de Afiliados (Affiliate Manager)

**Mision:** Evaluar potencial de programa de afiliados. En repos externos: sistemas de referidos/afiliados.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Tracking de referidos, programa de afiliados, comisiones, alianzas inter-empresa.

---

## EMPRESA 3: DESARROLLO DE NEGOCIOS Y VENTAS

> 12 expertos evaluan capacidades comerciales, prospeccion, negociacion y cierre.

---

### 3.1 Gerente de Desarrollo de Negocios (BDM)

**Mision:** Evaluar capacidad de identificar y desarrollar oportunidades. En repos externos: herramientas de business development.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/ventas/IDENTITY.md`
- `jarvis-ecosystem/agents/ventas/AGENTS.md`
- `jarvis-ecosystem/agents/ventas/SOUL.md`
- `jarvis-ecosystem/automations/ventas-pipeline-report.yaml`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Capacidad de prospeccion, pipeline visible, cross-selling entre empresas, reporte automatizado, integracion con bases de prospectos.

---

### 3.2 Ejecutivo de Cuentas (Account Executive)

**Mision:** Evaluar herramientas para el ciclo completo de venta. En repos externos: herramientas de sales cycle management.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/`
- `jarvis-ecosystem/docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md`
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md`

**Preguntas forense y repo externo:** Dossier para ciclo de venta completo, propuestas comerciales, tracking de interacciones, diferenciacion lead/oportunidad/cliente, cotizaciones.

---

### 3.3 Gerente de Ventas (Sales Manager)

**Mision:** Evaluar gestion y optimizacion del equipo de ventas. En repos externos: herramientas de sales management.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`
- `jarvis-ecosystem/automations/ventas-pipeline-report.yaml`
- `jarvis-ecosystem/agents/ventas/`

**Preguntas forense y repo externo:** Visibilidad de pipeline, metas de ventas, forecast, rendimiento por vendedor, dashboards.

---

### 3.4 Director de Nuevo Negocio

**Mision:** Evaluar estrategia de adquisicion y expansion. En repos externos: frameworks de expansion de negocios.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`

**Preguntas forense y repo externo:** Estrategia de expansion, plan de lanzamiento de empresas planificadas, viabilidad de nuevas lineas, analisis de mercado, go-to-market.

---

### 3.5 Representante de Ventas (Sales Representative)

**Mision:** Evaluar herramientas para venta dia a dia. En repos externos: herramientas de sales enablement.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `config/openclaw-home/openclaw.json`

**Preguntas forense y repo externo:** Jarvis como asistente de ventas, acceso a info de productos, seguimientos automaticos, briefings pre-reunion, templates de mensajes.

---

### 3.6 Gerente de Alianzas Estrategicas (Partnership Manager)

**Mision:** Evaluar potencial de alianzas. En repos externos: ecosistemas de partnerships.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Alianzas inter-empresa, framework de partnerships, partners tecnologicos, servicios bundled, rastreo de beneficios.

---

### 3.7 Inside Sales Specialist

**Mision:** Evaluar venta remota y digital. En repos externos: herramientas de inside sales.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/ventas/`
- `jarvis-ecosystem/automations/`

**Preguntas forense y repo externo:** Venta remota, outreach automatizado, demos, scripts de venta, seguimiento de leads frios.

---

### 3.8 Especialista en Generacion de Leads

**Mision:** Evaluar captacion y cualificacion de leads. En repos externos: herramientas de lead generation.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/`

**Preguntas forense y repo externo:** Captacion de leads, cualificacion automatica, lead scoring, fuentes de leads (LinkedIn, web), pipeline lead-MQL-SQL.

---

### 3.9 Gerente de Licitaciones (Bid Manager)

**Mision:** Evaluar capacidad de preparar propuestas. En repos externos: herramientas de proposal/bid management.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/agents/jarvis/skills/`
- `jarvis-ecosystem/docs/JARVIS_DOCUMENTS_ON_DISK.md`

**Preguntas forense y repo externo:** Propuestas formales, plantillas, JARVIS-DOCUMENTS para propuestas, presupuestos detallados, reutilizacion de componentes.

---

### 3.10 Growth Manager / Growth Hacker

**Mision:** Evaluar potencial de crecimiento acelerado. En repos externos: herramientas de growth hacking.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/automations/registry/`
- `agent-town/`

**Preguntas forense y repo externo:** Growth automatizado, potencial viral, experimentos rapidos, metricas (MRR, CAC, LTV), open source como palanca de growth.

---

### 3.11 Comercial Externo (Field Sales)

**Mision:** Evaluar herramientas para ventas en campo. En repos externos: herramientas mobile para sales.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/agents/ventas/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas forense y repo externo:** Acceso mobile, materiales de venta remotos, actualizacion de dossiers en campo, registro de reuniones.

---

### 3.12 Consultor de Soluciones (Pre-sales)

**Mision:** Evaluar capacidad de disenar soluciones para clientes. En repos externos: herramientas de solution design.

**Archivos JARVIS a leer:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/agents/` (todos)
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`
- `agent-town/` (demo)

**Preguntas forense y repo externo:** Propuestas tecnicas personalizadas, Agent Town como demo, POCs rapidos, mapeo necesidad-servicios, requirement gathering.

---

## SINTESIS CRUZADA INTER-EMPRESAS

> Generar despues de los 44 reportes individuales.

---

### S.1 Hallazgos convergentes

Hallazgos mencionados por 3+ expertos de diferentes empresas, agrupados por:
- Infraestructura y arquitectura
- Datos y analiticas
- Experiencia de usuario
- Integraciones faltantes
- Seguridad y compliance
- Escalabilidad y crecimiento

### S.2 Mapa de madurez consolidado

| Area | Empresa Dev | Empresa Marketing | Empresa Ventas | Promedio |
|------|-------------|-------------------|----------------|----------|
| Arquitectura | X/10 | - | - | ... |
| Seguridad | X/10 | - | - | ... |
| UX/UI | X/10 | X/10 | - | ... |
| Datos y analitica | X/10 | X/10 | X/10 | ... |
| Automatizacion | X/10 | X/10 | X/10 | ... |
| Gestion de clientes | - | X/10 | X/10 | ... |
| Capacidad comercial | - | X/10 | X/10 | ... |
| Integraciones | X/10 | X/10 | X/10 | ... |
| Documentacion | X/10 | X/10 | X/10 | ... |
| Escalabilidad | X/10 | X/10 | X/10 | ... |

### S.3 Mapa de repos externos vs carencias JARVIS

| Carencia en JARVIS | Repo externo que la resuelve | Modulo/funcionalidad especifica | Tipo de integracion | Esfuerzo | Prioridad |
|---------------------|------------------------------|---------------------------------|---------------------|----------|-----------|
| ... | REPO_1 | ... | Skill OpenClaw / ClawFlow / Modulo Agent Town / Inspiracion | ... | P0-P3 |

### S.4 Top 10 brechas criticas

Lista ordenada por impacto, indicando si algun repo externo las resuelve.

### S.5 Top 10 oportunidades

Lista ordenada por potencial, indicando que repos externos las habilitan.

### S.6 Elementos a ADOPTAR de repos externos

Lista de elementos concretos clasificados como ADOPTAR, con plan de integracion:

| # | Elemento | Origen (repo) | Destino en JARVIS | Forma de integracion | Esfuerzo | Dependencias |
|---|----------|----------------|--------------------|----------------------|----------|--------------|
| 1 | ... | REPO_1 | Skill de Jarvis | Fork + adaptar como skill OpenClaw | 2 dias | Node.js compatible |

### S.7 Elementos a ADAPTAR de repos externos

Elementos que requieren modificacion significativa pero valen la pena.

### S.8 Elementos para INSPIRARSE (no copiar codigo)

Patrones, ideas o enfoques que no se pueden integrar directamente pero inspiran mejoras propias.

---

## PLAN DE IMPLEMENTACION CONSOLIDADO

> Generar al final, integrando hallazgos forenses internos + aportes de repos externos.

### P.1 Roadmap (horizonte 12 meses)

| Fase | Periodo | Acciones internas | Integraciones de repos externos | Expertos involucrados | Impacto |
|------|---------|-------------------|---------------------------------|-----------------------|---------|
| **Fase 0: Cimientos** | Mes 1-2 | Corregir riesgos P0, seguridad, estabilidad | Elementos ADOPTAR mas urgentes | ... | ... |
| **Fase 1: Fortalecimiento** | Mes 3-4 | Mejorar testing, CI/CD, monitoring | Integrar skills y herramientas clave | ... | ... |
| **Fase 2: Expansion** | Mes 5-8 | Activar empresas planificadas, escalar | Adaptar componentes complejos | ... | ... |
| **Fase 3: Escala** | Mes 9-12 | Comercializacion, growth, cloud | Consolidar integraciones, optimizar | ... | ... |

### P.2 Backlog priorizado de tareas

Generar una lista de tareas concretas en formato compatible con Trello (titulo + descripcion + labels):

```
TAREA-001 [P0] [seguridad] [interno]
Titulo: ...
Descripcion: ...
Criterio de aceptacion: ...
Esfuerzo estimado: ...

TAREA-002 [P0] [integracion] [REPO_1]
Titulo: ...
Descripcion: ...
Criterio de aceptacion: ...
Esfuerzo estimado: ...
```

### P.3 Dependencias y riesgos del plan

| Dependencia/Riesgo | Impacto si no se resuelve | Mitigacion |
|---------------------|---------------------------|------------|
| ... | ... | ... |

### P.4 Metricas de exito del plan

| Metrica | Valor actual | Meta mes 3 | Meta mes 6 | Meta mes 12 |
|---------|-------------|------------|------------|-------------|
| Madurez promedio (10 areas) | X/10 | ... | ... | ... |
| Cobertura de tests | ...% | ... | ... | ... |
| Skills de OpenClaw activas | N | ... | ... | ... |
| Empresas activas del holding | 2 | ... | ... | ... |
| Clientes con dossier | N | ... | ... | ... |

### P.5 Veredicto final del comite de 44 expertos

Un parrafo de sintesis ejecutiva: estado actual, viabilidad, riesgos criticos, potencial del ecosistema, y como los repos externos evaluados lo fortalecen (o no). Firmado por el comite completo.

---

## INSTRUCCIONES FINALES PARA LA IA

1. **Lee TODOS los archivos indicados por rol** antes de emitir cada veredicto. Si un archivo no existe, registralo como hallazgo.
2. **Para repos externos:** usa `WebFetch` del README de GitHub, `gh repo view`, o clona el repo. Lee al menos README, estructura de carpetas, package.json/requirements.txt, y archivos clave de cada uno.
3. **No inventes datos.** Si no puedes verificar algo, indica "no verificable con los archivos disponibles".
4. **Cita evidencia.** Cada hallazgo referencia al menos un archivo, ruta o configuracion.
5. **Se implacablemente honesto.** Analisis forense = exponer debilidades es mas valioso que confirmar fortalezas.
6. **Prioriza lo accionable.** Cada recomendacion debe ser convertible en tarea concreta.
7. **Respeta la escala.** Proyecto operado por una persona (superusuario) con agentes IA. Calibra recomendaciones.
8. **OpenClaw es el centro.** Todo repo externo se evalua como potencial fortalecimiento de OpenClaw/Jarvis, nunca al reves.
9. **Clasifica cada elemento externo** como ADOPTAR / ADAPTAR / INSPIRARSE / DESCARTAR con justificacion.
10. **El informe completo contiene:** 44 secciones de expertos (Fase I + Fase II) + sintesis cruzada + plan de implementacion.
11. **Genera el informe como un unico documento Markdown** con tabla de contenidos al inicio.
12. **El plan de implementacion debe ser ejecutable:** tareas con formato Trello, esfuerzos estimados, dependencias claras.

---

*Prompt generado para el Ecosistema JARVIS -- Analisis forense multi-experto (44 roles, 3 empresas) + evaluacion de repos GitHub externos + plan de implementacion consolidado.*
