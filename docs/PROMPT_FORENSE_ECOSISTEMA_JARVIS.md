# Prompt: Analisis Forense Profundo del Ecosistema JARVIS

> **Instruccion para la IA:** Copia este prompt completo y pegalo en una nueva sesion de Cursor (o cualquier LLM con acceso al repositorio). La IA debe leer los archivos referenciados, ejecutar el analisis completo y generar el informe consolidado.

---

## CONTEXTO DEL PROYECTO

El repositorio `clawvis-openclaw` (ruta: `/var/www/clawvis-openclaw`) es el **monorepo operativo** del **Ecosistema JARVIS**: una plataforma de orquestacion IA que administra un **holding de empresas** mediante agentes autonomos.

### Componentes principales

| Componente | Ruta | Descripcion |
|------------|------|-------------|
| **OpenClaw Gateway** | Proceso externo (`~/.openclaw/`) | Motor de agentes: LLM multi-proveedor, herramientas, canales (Telegram, Discord, WhatsApp) |
| **Jarvis (agente maestro)** | `jarvis-ecosystem/agents/jarvis/` | Orquestador central del holding; gobierno, memoria, skills, model-router |
| **Agent Town** | `agent-town/` | App web Next.js 16 + React 19 + Phaser 3 (oficina pixel); WebSocket proxy al gateway |
| **Ecosistema Jarvis** | `jarvis-ecosystem/` | Agentes por empresa (`marketing/`, `ventas/`), automatizaciones ClawFlows YAML, gobierno documental |
| **Config sanitizada** | `config/openclaw-home/` | Instantanea de `~/.openclaw` sin secretos, para backup en Git |
| **Estado OpenClaw** | `openclaw-state/` | Sesiones, memoria SQLite, logs, transcripts historicos |
| **Documentacion** | `docs/`, `jarvis-ecosystem/docs/`, `documentos-jarvis-openclaw/` | Gobierno, runbooks, integraciones, convenciones |
| **Deploy** | `deploy/systemd/` | Units systemd para gateway, proxy Cursor, Agent Town |

**Catalogo opcional (comunidad OpenClaw):** [jarvis-ecosystem/docs/RECURSOS_COMUNIDAD_OPENCLAW.md](../jarvis-ecosystem/docs/RECURSOS_COMUNIDAD_OPENCLAW.md) — inventario forense de repos y skills externos, criterios de adopcion; **no** sustituye gobierno documental, Trello ni integraciones ya configuradas en el gateway.

### Stack tecnologico

- **Runtime:** Node.js 22+, OpenClaw CLI (npm global)
- **Frontend:** Next.js 16, React 19, Tailwind CSS 4, Phaser 3, TypeScript, pnpm
- **Comunicacion:** WebSocket (proxy a gateway en puerto 18789), API Routes Next.js
- **Proveedores LLM:** Groq, OpenRouter, Google Gemini, Ollama, Cursor proxy, OpenCode
- **Canales:** Telegram, Discord, WhatsApp
- **Herramientas:** Trello (API), navegador embebido, skills ClawHub
- **Base de datos:** SQLite (memoria del gateway), sin BD relacional de aplicacion
- **CI/CD:** GitHub Actions (lint, typecheck, build, test, audit)
- **Despliegue:** systemd units, sin Docker

### Modelo de gobierno

- **Superusuario** (Abraham): unico canal humano directo con Jarvis
- **Jarvis**: agente maestro, orquestador del holding
- **Empresas activas:** Marketing, Ventas (cada una con CEO/Supervisor/Equipo)
- **Empresas planificadas:** Agencia de programacion, bufete legal, contadores
- **Clientes externos:** representados por dossiers JSON (`client-dossiers/`)
- **Coordinacion:** Trello (tableros Kanban por empresa/cliente), Discord (roles logicos), Telegram

---

## OBJETIVO DEL ANALISIS

Realizar un **analisis forense exhaustivo** del Ecosistema JARVIS. Cada experto debe:

1. **LEER** los archivos del repositorio relevantes a su dominio (se indican rutas especificas)
2. **DIAGNOSTICAR** el estado actual con evidencia (citar archivos, lineas, configuraciones)
3. **IDENTIFICAR** hallazgos criticos, riesgos, deuda tecnica, oportunidades perdidas
4. **RECOMENDAR** acciones priorizadas (P0 = urgente, P1 = importante, P2 = mejora, P3 = futuro)
5. **CALIFICAR** la madurez de su area en escala 1-10 con justificacion

---

## FORMATO DE SALIDA POR EXPERTO

Cada experto debe generar su seccion con esta estructura exacta:

```
### [ROL] - [Nombre del Experto]
**Area:** [dominio especifico]
**Madurez:** [X/10]

#### Archivos analizados
- [lista de archivos leidos con ruta completa]

#### Hallazgos
1. [Hallazgo con evidencia: archivo, linea, configuracion]
2. ...

#### Riesgos detectados
| Riesgo | Severidad | Evidencia | Impacto |
|--------|-----------|-----------|---------|
| ... | CRITICO/ALTO/MEDIO/BAJO | ... | ... |

#### Oportunidades
1. [Oportunidad con justificacion]
2. ...

#### Recomendaciones priorizadas
| # | Prioridad | Accion | Esfuerzo | Impacto esperado |
|---|-----------|--------|----------|------------------|
| 1 | P0 | ... | ... | ... |
| 2 | P1 | ... | ... | ... |
```

---

## EMPRESA 1: AGENCIA DE DESARROLLO DE SOFTWARE

> Los 16 expertos de esta empresa analizan la calidad tecnica, arquitectura, seguridad, operaciones y producto del ecosistema.

---

### 1.1 Arquitecto de Software

**Mision:** Evaluar la arquitectura general del ecosistema, patrones de diseno, acoplamiento entre componentes, escalabilidad y coherencia estructural.

**Archivos a leer obligatoriamente:**
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
- `deploy/systemd/` (todos los archivos)

**Preguntas a responder:**
- Cual es el patron arquitectonico dominante y es el adecuado para el problema?
- Como se comunican los componentes (gateway, Agent Town, agentes, canales)?
- Existen dependencias circulares o acoplamiento excesivo?
- Es la arquitectura extensible para las empresas planificadas (dev-agency, legal, contadores)?
- Que tan resiliente es ante fallos de un componente?

---

### 1.2 Lider Tecnico (Tech Lead)

**Mision:** Evaluar calidad de codigo, convenciones, consistencia, documentacion tecnica y capacidad del equipo para mantener/escalar el proyecto.

**Archivos a leer obligatoriamente:**
- `agent-town/` (estructura completa de `components/`, `lib/`, `types/`)
- `agent-town/.github/workflows/ci.yml`
- `agent-town/tsconfig.json`
- `agent-town/eslint.config.mjs`
- `jarvis-ecosystem/agents/jarvis/scripts/` (todos)
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`
- `.gitignore`

**Preguntas a responder:**
- El codigo sigue convenciones consistentes (naming, estructura, tipado)?
- La pipeline de CI es suficiente para garantizar calidad?
- Existe deuda tecnica visible? Donde se concentra?
- Es realista que un equipo pequeno mantenga este ecosistema?
- Que tan bien documentadas estan las decisiones tecnicas?

---

### 1.3 Desarrollador Senior (Senior Developer)

**Mision:** Analizar la calidad de implementacion, patrones de codigo, manejo de errores, testing y buenas practicas en el codigo ejecutable.

**Archivos a leer obligatoriamente:**
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `agent-town/lib/gateway.ts`
- `agent-town/components/` (todos los archivos `.tsx`)
- `agent-town/components/game/` (estructura Phaser)
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`

**Preguntas a responder:**
- Hay manejo adecuado de errores y edge cases?
- Existen patrones antipatron o code smells?
- Cual es la cobertura de tests y es adecuada?
- El codigo de WebSocket/proxy es robusto ante desconexiones?
- Los scripts de validacion cubren todos los escenarios de fallo?

---

### 1.4 Ingeniero de DevOps

**Mision:** Evaluar la infraestructura, despliegue, monitoreo, automatizacion operativa y reproducibilidad del entorno.

**Archivos a leer obligatoriamente:**
- `deploy/systemd/` (todos los units)
- `agent-town/.github/workflows/ci.yml`
- `agent-town/package.json` (scripts)
- `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`
- `jarvis-ecosystem/automations/` (todos los YAML)
- `jarvis-ecosystem/scripts/`

**Preguntas a responder:**
- Existe un proceso de despliegue reproducible y documentado?
- Hay monitoreo y alertas configuradas?
- Que pasa si el servidor se reinicia inesperadamente?
- Existe un plan de disaster recovery?
- Las automatizaciones ClawFlows son fiables y estan monitoreadas?
- Por que no hay contenedorizacion (Docker) y deberia haberla?

---

### 1.5 Especialista en Ciberseguridad

**Mision:** Auditar la seguridad del ecosistema: secretos, autenticacion, superficie de ataque, datos sensibles en el repo, hardening.

**Archivos a leer obligatoriamente:**
- `.gitignore`
- `config/openclaw-home/README.md`
- `config/openclaw-home/openclaw.json`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md` (Fase D - Secretos)
- `openclaw-state/` (estructura, sin leer contenido sensible)
- `agent-town/server.ts` (autenticacion dispatch)
- `agent-town/lib/ws-proxy.ts` (inyeccion de identidad)
- `jarvis-ecosystem/.env` (verificar si esta en .gitignore)
- `PUSH-A-GITHUB.md`

**Preguntas a responder:**
- Hay secretos expuestos en el repositorio (tokens, API keys, credenciales)?
- La autenticacion del gateway es adecuada (`gateway.auth`)?
- Que datos sensibles contiene `openclaw-state/` y deberian estar en Git?
- El proxy WebSocket valida origen y autenticacion?
- Existe control de acceso por agente/canal?
- El `.gitignore` cubre todos los archivos sensibles?
- Hay riesgo de inyeccion de prompts o manipulacion de agentes?

---

### 1.6 Arquitecto de Cloud

**Mision:** Evaluar la estrategia de infraestructura cloud, escalabilidad, costos, y viabilidad de despliegue en nube.

**Archivos a leer obligatoriamente:**
- `deploy/systemd/` (todos)
- `agent-town/package.json`
- `agent-town/server.ts`
- `config/openclaw-home/openclaw.json`
- `docs/PROVEEDOR_CURSOR_OPENCLAW.md`
- `docs/MODELOS_JARVIS_OPENCLAW.md`

**Preguntas a responder:**
- El ecosistema esta listo para despliegue cloud (AWS/GCP/Azure)?
- Que se necesitaria para escalar horizontalmente?
- Como se gestionan los costos de proveedores LLM?
- Existe una estrategia de alta disponibilidad?
- El modelo de despliegue actual (systemd en servidor unico) es adecuado?
- Que servicios cloud se beneficiarian mas el ecosistema?

---

### 1.7 Disenador de UX/UI

**Mision:** Evaluar la experiencia de usuario de Agent Town y la interfaz visual del ecosistema.

**Archivos a leer obligatoriamente:**
- `agent-town/app/page.tsx`
- `agent-town/app/layout.tsx`
- `agent-town/app/globals.css`
- `agent-town/components/` (todos)
- `agent-town/public/` (estructura de assets)
- `agent-town/components/game/config/` (configuracion Phaser)

**Preguntas a responder:**
- La interfaz pixel-office es intuitiva para el usuario objetivo?
- Existe un sistema de diseno coherente (colores, tipografia, espaciado)?
- Agent Town es accesible (a11y)?
- La experiencia en mobile es adecuada?
- El flujo de interaccion con los agentes es claro?
- Los assets visuales (sprites, mapas, audio) son de calidad profesional?

---

### 1.8 Ingeniero de QA (Quality Assurance)

**Mision:** Evaluar la estrategia de testing, cobertura, calidad de pruebas existentes y procesos de aseguramiento de calidad.

**Archivos a leer obligatoriamente:**
- `agent-town/.github/workflows/ci.yml`
- `agent-town/package.json` (scripts de test)
- `agent-town/vitest.config.ts` (si existe)
- Buscar archivos `*.test.*` y `*.spec.*` en todo el repo
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`

**Preguntas a responder:**
- Cual es la cobertura de tests (unitarios, integracion, e2e)?
- Existen tests para los flujos criticos (WebSocket, proxy, agentes)?
- El runbook forense funciona como test manual? Es suficiente?
- Hay estrategia de regression testing?
- Los ClawFlows tienen tests o validacion?
- Que porcentaje del codigo tiene tests automatizados?

---

### 1.9 Gerente de Producto (Product Manager)

**Mision:** Evaluar la vision de producto, roadmap, alineacion con necesidades de usuario y viabilidad comercial.

**Archivos a leer obligatoriamente:**
- `README.md` (raiz)
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`
- `jarvis-ecosystem/COMPANIES.md` (si existe, sino `jarvis-ecosystem/docs/` buscar empresas)
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/README.md` (si existe)

**Preguntas a responder:**
- Existe una vision de producto clara y documentada?
- Hay un roadmap priorizado?
- Como se mide el exito del ecosistema (KPIs)?
- El modelo de holding multi-empresa es viable como producto?
- Que tan lejos esta de ser un producto comercializable?
- Quienes son los usuarios objetivo y estan bien definidos?
- Las empresas planificadas (dev-agency, legal, contadores) tienen especificacion?

---

### 1.10 Cientifico de Datos (Data Scientist)

**Mision:** Evaluar el flujo de datos, analiticas, metricas, y potencial de inteligencia de datos del ecosistema.

**Archivos a leer obligatoriamente:**
- `openclaw-state/memory/` (estructura)
- `config/openclaw-home/openclaw.json` (seccion de modelos/metricas)
- `jarvis-ecosystem/automations/` (datos que generan)
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`

**Preguntas a responder:**
- Que datos genera el ecosistema y como se almacenan?
- Existe un pipeline de analiticas?
- Se rastrean metricas de uso de LLM (tokens, costos, latencia)?
- Se puede medir la efectividad de cada agente?
- Hay potencial para modelos predictivos (churn de clientes, forecasting)?
- Los transcripts de sesiones son explotables para insights?

---

### 1.11 Ingeniero de Machine Learning

**Mision:** Evaluar la estrategia de IA/ML, uso de modelos, fine-tuning, evaluacion y optimizacion.

**Archivos a leer obligatoriamente:**
- `config/openclaw-home/openclaw.json` (modelos, proveedores)
- `jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`
- `jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`
- `docs/MODELOS_JARVIS_OPENCLAW.md`
- `docs/CIERRE_MODULO_OLLAMA_LOCAL.md`
- `docs/PROVEEDOR_CURSOR_OPENCLAW.md`
- Todos los `IDENTITY.md` y `SOUL.md` de los agentes

**Preguntas a responder:**
- La estrategia multi-modelo (Groq, OpenRouter, Gemini, Ollama) es optima?
- El model-router aplica reglas inteligentes o es estatico?
- Existe evaluacion sistematica de calidad de respuestas?
- Se hace fine-tuning o RAG con datos propios?
- Hay oportunidad para modelos locales (Ollama) en produccion?
- Los prompts de sistema (SOUL.md, IDENTITY.md) estan optimizados?
- Existe un framework de evaluacion de prompts?

---

### 1.12 Administrador de Bases de Datos (DBA)

**Mision:** Evaluar el almacenamiento de datos, integridad, rendimiento, backups y estrategia de persistencia.

**Archivos a leer obligatoriamente:**
- `openclaw-state/` (estructura completa)
- `openclaw-state/memory/` (archivos SQLite)
- `openclaw-state/agents/` (estructura de sesiones)
- `config/openclaw-home/openclaw.json` (configuracion de memoria)
- `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`
- `jarvis-ecosystem/client-dossiers/` (si existe)

**Preguntas a responder:**
- SQLite es adecuado para el volumen y concurrencia esperados?
- Existe estrategia de backup de datos (sesiones, memoria, dossiers)?
- Hay riesgo de corrupcion de datos en SQLite con multiples procesos?
- Los archivos JSONL de sesiones crecen sin limite?
- Se necesita una base de datos relacional o vectorial dedicada?
- Como se gestiona la retencion y purga de datos historicos?

---

### 1.13 Desarrollador Mobile

**Mision:** Evaluar la viabilidad y necesidad de una experiencia mobile nativa o PWA para el ecosistema.

**Archivos a leer obligatoriamente:**
- `agent-town/app/layout.tsx` (viewport, meta tags)
- `agent-town/app/globals.css` (responsive design)
- `agent-town/components/` (adaptabilidad)
- `agent-town/public/` (iconos, manifest)
- `agent-town/package.json`

**Preguntas a responder:**
- Agent Town es responsive o esta optimizada para desktop?
- Phaser 3 funciona bien en dispositivos moviles?
- Hay una PWA configurada o seria viable?
- Los canales existentes (Telegram, WhatsApp) ya cubren la necesidad mobile?
- Se necesita una app nativa o un wrapper (Capacitor/Expo)?
- Que experiencia mobile tienen los CEOs/supervisores del holding?

---

### 1.14 Desarrollador Backend

**Mision:** Analizar la logica de servidor, APIs, manejo de estado, integraciones y robustez del backend.

**Archivos a leer obligatoriamente:**
- `agent-town/server.ts`
- `agent-town/lib/ws-proxy.ts`
- `agent-town/lib/gateway.ts`
- `agent-town/app/api/` (todas las rutas)
- `jarvis-ecosystem/automations/` (todos los YAML)
- `jarvis-ecosystem/agents/jarvis/scripts/` (todos)

**Preguntas a responder:**
- El servidor custom de Agent Town es robusto para produccion?
- El proxy WebSocket maneja reconexion, backpressure y errores?
- Las API Routes tienen validacion de entrada adecuada?
- Como se gestiona el estado entre sesiones del gateway?
- Las automatizaciones ClawFlows son fiables? Tienen retry/fallback?
- Hay logging estructurado y trazabilidad de requests?

---

### 1.15 Desarrollador Frontend

**Mision:** Analizar la calidad del frontend, rendimiento, experiencia de usuario y modernidad de la interfaz.

**Archivos a leer obligatoriamente:**
- `agent-town/app/` (todas las paginas)
- `agent-town/components/` (todos los componentes)
- `agent-town/lib/` (utilidades frontend)
- `agent-town/types/` (tipos TypeScript)
- `agent-town/app/globals.css`
- `agent-town/tailwind.config.ts` (si existe)
- `agent-town/next.config.ts` (si existe)

**Preguntas a responder:**
- Se usan correctamente los Server Components vs Client Components de Next.js?
- El rendimiento de Phaser 3 embebido en Next.js es aceptable?
- Existe gestion de estado adecuada (Context, Zustand, etc.)?
- La integracion WebSocket desde el frontend es robusta?
- Los componentes son reutilizables y siguen principios SOLID?
- Hay code splitting y lazy loading donde corresponde?

---

### 1.16 Desarrollador Fullstack

**Mision:** Evaluar la coherencia end-to-end: desde el gateway hasta la UI, pasando por todas las capas.

**Archivos a leer obligatoriamente:**
- Todos los archivos que leyeron Backend y Frontend
- `jarvis-ecosystem/agents/jarvis/AGENTS.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `docs/OPENCLAW_FORENSE_RUNBOOK.md`

**Preguntas a responder:**
- El flujo completo (usuario → Agent Town → WebSocket → Gateway → LLM → respuesta → UI) es coherente?
- Hay brechas o puntos ciegos entre frontend y backend?
- Los tipos de TypeScript cubren los contratos entre capas?
- El ecosistema es debuggeable end-to-end?
- Existe una experiencia de desarrollo (DX) buena para nuevos contribuidores?
- Los errores se propagan correctamente desde el gateway hasta la UI?

---

## EMPRESA 2: AGENCIA DE MARKETING DIGITAL

> Los 16 expertos de esta empresa analizan como el ecosistema soporta, habilita y potencia operaciones de marketing digital para los clientes del holding.

---

### 2.1 Estratega Digital (Digital Strategist)

**Mision:** Evaluar si el ecosistema JARVIS tiene una estrategia digital coherente y si habilita la creacion de estrategias para clientes.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/marketing/IDENTITY.md`
- `jarvis-ecosystem/agents/marketing/AGENTS.md`
- `jarvis-ecosystem/agents/marketing/SOUL.md`
- `jarvis-ecosystem/automations/marketing-competitor-monitor.yaml`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- El agente de marketing tiene una estrategia digital definida?
- El ecosistema puede generar estrategias personalizadas por cliente (dossier)?
- Hay capacidad de analisis competitivo automatizado?
- Se pueden crear y ejecutar campanas desde el ecosistema?
- Existe alineacion entre la estrategia digital y los canales disponibles (Telegram, Discord)?
- Que KPIs de marketing se pueden rastrear nativamente?

---

### 2.2 Especialista en SEO

**Mision:** Evaluar capacidades de SEO dentro del ecosistema y para los clientes del holding.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/skills/` (buscar skills relacionadas)
- `jarvis-ecosystem/agents/jarvis/skills/` (xurl, summarize, etc.)
- `agent-town/app/layout.tsx` (meta tags)
- `agent-town/next.config.ts` (si existe)

**Preguntas a responder:**
- Hay herramientas o skills de SEO integradas?
- Agent Town tiene SEO basico (meta tags, sitemap, robots.txt)?
- El ecosistema puede auditar SEO de sitios de clientes?
- Se pueden generar contenidos SEO-optimizados automaticamente?
- Hay integracion con herramientas SEO (Search Console, Ahrefs, Semrush)?
- Existe monitoreo de posiciones y keywords?

---

### 2.3 Especialista en SEM / Paid Search (Google Ads)

**Mision:** Evaluar si el ecosistema puede gestionar o asistir campanas de publicidad pagada.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/` (buscar automatizaciones de ads)
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- Hay integracion con Google Ads, Meta Ads u otras plataformas?
- El ecosistema puede generar copys para anuncios?
- Se pueden crear reportes de rendimiento de campanas?
- Existe automatizacion de pujas o presupuestos?
- Los dossiers de cliente incluyen informacion de campanas pagadas?

---

### 2.4 Gerente de Performance (Performance Manager)

**Mision:** Evaluar las capacidades de medicion de rendimiento y optimizacion de resultados.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/automations/` (todos)
- `jarvis-ecosystem/agents/marketing/` (skills y configuracion)
- `jarvis-ecosystem/docs/` (reportes)
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas a responder:**
- Existen dashboards o reportes de performance?
- Se pueden medir conversiones y atribucion?
- Hay integracion con Google Analytics, Tag Manager, etc.?
- El ecosistema genera reportes periodicos automaticos?
- Se pueden establecer metas y rastrear cumplimiento?
- Los reportes supervisor→CEO incluyen metricas de marketing?

---

### 2.5 Social Media Manager

**Mision:** Evaluar la capacidad de gestion de redes sociales del ecosistema.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/IDENTITY.md`
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/marketing-competitor-monitor.yaml`
- Canales configurados en `config/openclaw-home/openclaw.json`

**Preguntas a responder:**
- Que redes sociales puede gestionar el ecosistema?
- Hay capacidad de publicacion programada?
- Se pueden monitorear menciones y engagement?
- El monitor de competencia analiza redes sociales?
- Existe un calendario editorial integrado?
- Los canales Telegram/Discord se usan como medio de publicacion o solo operacional?

---

### 2.6 Estratega de Contenido (Content Strategist)

**Mision:** Evaluar la capacidad de planificacion, creacion y distribucion de contenido.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/jarvis/skills/` (summarize, xurl, etc.)
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/registry/` (github-trending, etc.)
- `jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md`

**Preguntas a responder:**
- El ecosistema puede generar contenido (blogs, posts, emails)?
- Hay un flujo de aprobacion de contenido?
- Se puede mantener un calendario de contenido en Trello?
- Existe capacidad de curar contenido automaticamente (trending, noticias)?
- Los skills de resumen y URL son utiles para content curation?
- Se puede personalizar contenido por cliente/audiencia?

---

### 2.7 Copywriter Creativo

**Mision:** Evaluar la calidad de los prompts, la voz de marca y la capacidad de generacion de copy.

**Archivos a leer obligatoriamente:**
- Todos los `SOUL.md` e `IDENTITY.md` de los agentes
- `jarvis-ecosystem/agents/jarvis/AGENTS.md`
- `jarvis-ecosystem/agents/marketing/AGENTS.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- Los agentes tienen una voz de marca definida y consistente?
- Se pueden generar copys para distintos canales y tonos?
- Hay plantillas de copy reutilizables?
- El SOUL.md es efectivo como "personalidad" del agente?
- Se puede adaptar el tono por cliente (dossier)?
- Los prompts de sistema estan optimizados para creatividad?

---

### 2.8 Media Buyer (Comprador de Medios)

**Mision:** Evaluar la capacidad de gestion de compra de medios y presupuestos publicitarios.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- Hay integracion con plataformas de compra de medios?
- Se pueden rastrear presupuestos y ROI por cliente?
- El ecosistema asiste en la planificacion de medios?
- Existen automatizaciones de optimizacion de gasto?
- Los dossiers de cliente tienen campos de presupuesto?

---

### 2.9 Analista de Datos de Marketing (Data Analyst)

**Mision:** Evaluar las capacidades de analisis de datos de marketing, visualizacion y generacion de insights.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/automations/` (pipelines de datos)
- `openclaw-state/memory/` (estructura de datos)
- `jarvis-ecosystem/agents/jarvis/scripts/`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas a responder:**
- Que datos de marketing se recolectan y almacenan?
- Hay capacidad de visualizacion de datos?
- Se generan insights accionables automaticamente?
- Existe integracion con herramientas de BI?
- Los reportes incluyen datos cuantitativos de marketing?
- Se puede hacer segmentacion de audiencias?

---

### 2.10 Especialista en Email Marketing / Automation

**Mision:** Evaluar la capacidad de email marketing y automatizacion de flujos de comunicacion.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/` (buscar flujos de email)
- `jarvis-ecosystem/agents/jarvis/skills/` (herramientas de comunicacion)

**Preguntas a responder:**
- Hay integracion con plataformas de email (Mailchimp, SendGrid, etc.)?
- Se pueden crear flujos de nurturing automatizados?
- Los ClawFlows soportan automatizacion de emails?
- Existe segmentacion y personalizacion de envios?
- Se rastrean metricas de email (open rate, CTR)?
- El ecosistema puede gestionar listas de contactos?

---

### 2.11 Gerente de Cuentas (Account Manager)

**Mision:** Evaluar como el ecosistema facilita la gestion de relaciones con clientes.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/` (si existe)
- `jarvis-ecosystem/docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md`
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`

**Preguntas a responder:**
- Los dossiers de cliente son suficientes para gestion de cuentas?
- Hay visibilidad del estado de cada cliente (proyectos activos, pendientes)?
- Se pueden generar reportes de avance por cliente?
- El flujo Trello permite trackear entregables por cuenta?
- Existe un sistema de alertas para clientes desatendidos?
- La comunicacion inter-empresa funciona para cuentas compartidas?

---

### 2.12 Community Manager

**Mision:** Evaluar la capacidad de gestion de comunidades y engagement en canales.

**Archivos a leer obligatoriamente:**
- Configuracion de canales en `config/openclaw-home/openclaw.json`
- `jarvis-ecosystem/agents/jarvis/AGENTS.md` (seccion Group Chats)
- `jarvis-ecosystem/docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md`
- `jarvis-ecosystem/docs/DISCORD_JERARQUIA_VS_AGENTES_IA.md`

**Preguntas a responder:**
- Jarvis puede actuar como community manager en Discord/Telegram?
- Las reglas de "cuando hablar vs cuando callar" son adecuadas?
- Se puede moderar contenido automaticamente?
- Hay capacidad de engagement proactivo con la comunidad?
- Los roles de Discord estan bien estructurados para community?
- Se rastrean metricas de comunidad (miembros, actividad, sentimiento)?

---

### 2.13 Especialista en Inbound Marketing

**Mision:** Evaluar la estrategia y capacidades de inbound marketing del ecosistema.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/marketing/` (configuracion completa)
- `jarvis-ecosystem/automations/` (flujos de contenido/lead)
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/` (como landing/punto de atraccion)

**Preguntas a responder:**
- Existe un funnel de inbound definido?
- Agent Town sirve como punto de captacion?
- Hay flujos automatizados de lead nurturing?
- Se puede crear contenido de atraccion (blogs, whitepapers)?
- El ecosistema soporta lead scoring?
- Hay integracion con formularios o landing pages?

---

### 2.14 Especialista en CRM

**Mision:** Evaluar la gestion de relaciones con clientes y el flujo de datos de contactos.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/` (estructura y contenido)
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/jarvis/skills/` (buscar skills de CRM)
- `jarvis-ecosystem/agents/marketing/skills/`

**Preguntas a responder:**
- Los dossiers JSON funcionan como CRM minimo? Es suficiente?
- Hay integracion con CRM comerciales (HubSpot, Salesforce, Pipedrive)?
- Se puede rastrear el ciclo de vida del cliente?
- Existe un pipeline de ventas visible?
- Los datos de contacto estan centralizados?
- Hay automatizacion de seguimiento (follow-ups)?

---

### 2.15 Disenador UX/UI para Conversion

**Mision:** Evaluar las interfaces del ecosistema desde la perspectiva de conversion y optimizacion.

**Archivos a leer obligatoriamente:**
- `agent-town/app/page.tsx`
- `agent-town/components/` (todos)
- `agent-town/app/globals.css`
- `agent-town/public/` (assets)

**Preguntas a responder:**
- Agent Town tiene elementos de conversion (CTAs, formularios, onboarding)?
- La experiencia facilita que un visitante se convierta en usuario/cliente?
- Hay A/B testing o personalizacion de experiencia?
- Los flujos de usuario estan optimizados para la accion deseada?
- Existe un journey map del usuario?
- Las metricas de conversion se rastrean?

---

### 2.16 Gerente de Afiliados (Affiliate Manager)

**Mision:** Evaluar el potencial de un programa de afiliados o referidos.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/` (capacidades de tracking)

**Preguntas a responder:**
- El ecosistema soporta tracking de referidos?
- Hay estructura para un programa de afiliados?
- Se pueden rastrear comisiones y payouts?
- Existe integracion con plataformas de afiliados?
- El modelo de holding permite alianzas inter-empresa para referidos?
- Es viable un programa de referidos como canal de adquisicion?

---

## EMPRESA 3: EMPRESA DE DESARROLLO DE NEGOCIOS Y VENTAS

> Los 12 expertos de esta empresa evaluan las capacidades comerciales, de prospeccion, negociacion y cierre del ecosistema.

---

### 3.1 Gerente de Desarrollo de Negocios (BDM)

**Mision:** Evaluar la capacidad del ecosistema para identificar, desarrollar y cerrar nuevas oportunidades de negocio.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/agents/ventas/IDENTITY.md`
- `jarvis-ecosystem/agents/ventas/AGENTS.md`
- `jarvis-ecosystem/agents/ventas/SOUL.md`
- `jarvis-ecosystem/automations/ventas-pipeline-report.yaml`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- El agente de ventas tiene capacidad de prospeccion?
- Hay un pipeline de negocios visible y estructurado?
- Se pueden identificar oportunidades de cross-selling entre empresas del holding?
- El reporte de pipeline esta automatizado?
- Como se documenta el proceso de descubrimiento de un nuevo cliente?
- Hay integracion con bases de datos de empresas/prospectos?

---

### 3.2 Ejecutivo de Cuentas (Account Executive)

**Mision:** Evaluar las herramientas y flujos para gestionar el ciclo completo de venta.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/client-dossiers/` (si existe)
- `jarvis-ecosystem/docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md`
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/docs/FLUJO_TRELLO_ECOSISTEMA.md`

**Preguntas a responder:**
- El dossier de cliente soporta el ciclo de venta completo (discovery → propuesta → cierre → delivery)?
- Hay plantillas de propuestas comerciales?
- Se pueden rastrear interacciones con el prospecto?
- El flujo Trello diferencia entre lead, oportunidad y cliente?
- Existe un flujo de aprobacion de propuestas?
- Se pueden generar cotizaciones desde el ecosistema?

---

### 3.3 Gerente de Ventas (Sales Manager)

**Mision:** Evaluar la capacidad de gestion, supervisión y optimizacion del equipo de ventas.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md` (jerarquia)
- `jarvis-ecosystem/docs/plantillas/REPORTE_SUPERVISOR_CEO.md`
- `jarvis-ecosystem/automations/ventas-pipeline-report.yaml`
- `jarvis-ecosystem/agents/ventas/` (configuracion completa)

**Preguntas a responder:**
- Hay visibilidad del pipeline de ventas del equipo?
- Se pueden establecer metas de ventas y rastrear cumplimiento?
- El reporte supervisor→CEO incluye metricas de ventas?
- Hay forecast de ventas?
- Se puede analizar el rendimiento por vendedor/cuenta?
- Existen dashboards de ventas?

---

### 3.4 Director de Nuevo Negocio (Director of New Business)

**Mision:** Evaluar la estrategia de adquisicion de nuevos clientes y expansion del holding.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`
- `jarvis-ecosystem/COMPANIES.md` (o donde esten listadas las empresas planificadas)

**Preguntas a responder:**
- Hay una estrategia de expansion documentada?
- Las empresas planificadas (dev-agency, legal, contadores) tienen plan de lanzamiento?
- Como se evalua la viabilidad de una nueva linea de negocio?
- Existe analisis de mercado o competencia documentado?
- El ecosistema puede soportar 5+ empresas simultaneamente?
- Hay una estrategia de go-to-market para el holding?

---

### 3.5 Representante de Ventas (Sales Representative)

**Mision:** Evaluar las herramientas disponibles para la venta dia a dia.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md`
- Canales de comunicacion en `config/openclaw-home/openclaw.json`

**Preguntas a responder:**
- Un vendedor puede usar Jarvis/agente ventas como asistente en tiempo real?
- Hay acceso rapido a informacion de productos/servicios del holding?
- Se pueden generar seguimientos automatizados?
- El agente puede preparar briefings pre-reunion con un cliente?
- Hay templates de mensajes de venta?
- La comunicacion via Telegram/WhatsApp soporta el flujo de ventas?

---

### 3.6 Gerente de Alianzas Estrategicas (Partnership Manager)

**Mision:** Evaluar el potencial de alianzas, partnerships y sinergias dentro y fuera del holding.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`

**Preguntas a responder:**
- El modelo de holding facilita alianzas entre empresas internas?
- Hay un framework para evaluar partnerships externos?
- Se documentan alianzas en el sistema de dossiers?
- Existe un ecosistema de partners tecnologicos (OpenClaw, proveedores LLM)?
- Se pueden rastrear beneficios de alianzas?
- El holding puede ofrecer servicios bundled a clientes?

---

### 3.7 Inside Sales Specialist

**Mision:** Evaluar la capacidad de venta remota y digital del ecosistema.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/ventas/` (configuracion completa)
- Canales de comunicacion disponibles
- `jarvis-ecosystem/automations/` (automatizaciones de ventas)

**Preguntas a responder:**
- El ecosistema soporta venta completamente remota?
- Hay flujos de outreach automatizado?
- Se pueden hacer demos o presentaciones desde el ecosistema?
- Los canales (Telegram, Discord, WhatsApp) son efectivos para inside sales?
- Hay scripts de venta o guiones disponibles?
- Se puede hacer seguimiento automatico de leads frios?

---

### 3.8 Especialista en Generacion de Leads (Lead Generation Specialist)

**Mision:** Evaluar la capacidad de captura, cualificacion y nutricion de leads.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/ventas/skills/`
- `jarvis-ecosystem/agents/marketing/skills/`
- `jarvis-ecosystem/automations/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `agent-town/` (como punto de captacion)

**Preguntas a responder:**
- Hay mecanismos de captacion de leads?
- Se puede cualificar leads automaticamente?
- Existe un scoring de leads?
- Agent Town puede capturar informacion de visitantes?
- Hay integracion con fuentes de leads (LinkedIn, formularios web)?
- El pipeline lead → MQL → SQL esta definido?

---

### 3.9 Gerente de Licitaciones (Bid Manager)

**Mision:** Evaluar la capacidad de preparar propuestas formales y participar en procesos de licitacion.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/agents/jarvis/skills/` (herramientas de generacion de documentos)
- `jarvis-ecosystem/docs/JARVIS_DOCUMENTS_ON_DISK.md`

**Preguntas a responder:**
- Se pueden generar propuestas formales desde el ecosistema?
- Hay plantillas de propuestas/licitaciones?
- El sistema de documentos (JARVIS-DOCUMENTS) soporta gestion de propuestas?
- Se pueden almacenar y reutilizar componentes de propuestas pasadas?
- Hay flujo de revision y aprobacion de propuestas?
- Se pueden generar presupuestos detallados?

---

### 3.10 Growth Manager / Growth Hacker

**Mision:** Evaluar el potencial de crecimiento acelerado del ecosistema y sus clientes.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/README.md`
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/automations/` (todas)
- `jarvis-ecosystem/automations/registry/` (github-trending, etc.)
- `agent-town/` (como producto de crecimiento)

**Preguntas a responder:**
- Hay mecanismos de growth automatizados?
- El ecosistema puede escalar adquisicion de clientes?
- Agent Town tiene potencial viral o de referidos?
- Se pueden ejecutar experimentos de growth rapidos?
- Las automatizaciones existentes contribuyen al crecimiento?
- Hay metricas de crecimiento definidas (MRR, CAC, LTV, churn)?
- El open source (OpenClaw) es una palanca de growth?

---

### 3.11 Comercial Externo (Field Sales)

**Mision:** Evaluar las herramientas para ventas presenciales y en campo.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/agents/ventas/`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- Canales moviles disponibles (Telegram, WhatsApp)

**Preguntas a responder:**
- Un comercial en campo puede acceder al ecosistema desde su celular?
- Hay materiales de venta accesibles remotamente?
- Se pueden actualizar dossiers de cliente desde el campo?
- La comunicacion con Jarvis via Telegram/WhatsApp es util en reuniones?
- Hay una app o interfaz movil optimizada para ventas?
- Se puede registrar informacion de reuniones presenciales?

---

### 3.12 Consultor de Soluciones (Solutions Consultant / Pre-sales)

**Mision:** Evaluar la capacidad del ecosistema para disenar y presentar soluciones tecnicas a clientes.

**Archivos a leer obligatoriamente:**
- `jarvis-ecosystem/docs/GOBIERNO_JARVIS_V2.md`
- `jarvis-ecosystem/docs/CLIENT_DOSSIER_SCHEMA.md`
- `jarvis-ecosystem/agents/` (todos los agentes)
- `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md`
- `agent-town/` (como demo/showcase)

**Preguntas a responder:**
- El ecosistema puede generar propuestas tecnicas personalizadas?
- Agent Town sirve como demo para prospectos?
- Se pueden crear POCs (proof of concept) rapidamente?
- Hay documentacion de servicios/capacidades del holding?
- Se puede mapear la necesidad del cliente a los servicios del holding automaticamente?
- El model de dossier soporta requirement gathering tecnico?

---

## SINTESIS CRUZADA INTER-EMPRESAS

> Despues de que los 44 expertos emitan sus reportes individuales, generar esta seccion consolidada.

---

### S.1 Hallazgos convergentes

Identificar hallazgos mencionados por 3+ expertos de diferentes empresas. Agrupar por tema:
- Infraestructura y arquitectura
- Datos y analiticas
- Experiencia de usuario
- Integraciones faltantes
- Seguridad y compliance
- Escalabilidad y crecimiento

### S.2 Mapa de madurez

Generar una tabla consolidada:

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

### S.3 Top 10 brechas criticas

Lista ordenada por impacto de las 10 brechas mas criticas detectadas por el comite completo.

### S.4 Top 10 oportunidades

Lista ordenada por potencial de las 10 oportunidades mas valiosas detectadas.

### S.5 Roadmap priorizado (horizonte 12 meses)

| Fase | Periodo | Acciones clave | Expertos involucrados | Impacto esperado |
|------|---------|----------------|-----------------------|------------------|
| **Fase 0: Cimientos** | Mes 1-2 | ... | ... | ... |
| **Fase 1: Estabilizacion** | Mes 3-4 | ... | ... | ... |
| **Fase 2: Expansion** | Mes 5-8 | ... | ... | ... |
| **Fase 3: Escala** | Mes 9-12 | ... | ... | ... |

### S.6 Veredicto final del comite

Un parrafo de sintesis ejecutiva: estado actual del ecosistema, viabilidad, riesgos criticos y potencial, firmado por el comite de 44 expertos.

---

## INSTRUCCIONES FINALES PARA LA IA

1. **Lee TODOS los archivos indicados** antes de emitir cada veredicto. Si un archivo no existe, registralo como hallazgo.
2. **No inventes datos.** Si no puedes verificar algo, indicalo como "no verificable con los archivos disponibles".
3. **Cita evidencia.** Cada hallazgo debe referenciar al menos un archivo, ruta o configuracion.
4. **Se implacablemente honesto.** Este es un analisis forense, no un halago. Exponer debilidades es mas valioso que confirmar fortalezas.
5. **Prioriza lo accionable.** Cada recomendacion debe poder convertirse en una tarea concreta.
6. **Respeta la escala.** Este es un proyecto operado por una persona (superusuario) con agentes IA; calibra las recomendaciones a esa realidad.
7. **El informe completo debe contener las 44 secciones de expertos + la sintesis cruzada.** No omitas ningun rol.
8. **Genera el informe como un unico documento Markdown** con tabla de contenidos al inicio.

---

*Prompt generado para el Ecosistema JARVIS -- Analisis forense multi-experto con 44 roles de 3 empresas del holding.*
