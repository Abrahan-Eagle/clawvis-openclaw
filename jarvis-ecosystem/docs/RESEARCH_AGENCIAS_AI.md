# Research: como construyen "agencias de marketing" con agentes IA

**Fecha:** abril 2026
**Proposito:** documentar las referencias externas analizadas para diseñar la mejora v2 de jarvis-ecosystem.
**No se copia codigo de ningun proyecto referenciado.** Esto es analisis estructural.

---

## 1. Fuentes consultadas

### 1.1 Documentacion oficial OpenClaw

- [docs.openclaw.ai/multi-agent](https://docs.openclaw.ai/multi-agent) — routing por bindings, paths estandar, RFC Agent Teams.
- [clawdocs.org/guides/multi-agent](http://clawdocs.org/guides/multi-agent) — workflows multi-agente, separate instances, Mission Control, Antfarm.
- [docs.openclaw.ai/cli/agents.md](https://docs.openclaw.ai/cli/agents.md) — comandos `openclaw agents add/bind/unbind/delete/set-identity`.
- [openclaw-openclaw.mintlify.app/configuration](https://openclaw-openclaw.mintlify.app/configuration) — estructura `openclaw.json`.
- [open-clawai.com/en/blog/build-multi-agent-system](https://www.open-clawai.com/en/blog/build-multi-agent-system) — guia step-by-step.

### 1.2 Repos GitHub de "agencias de marketing con IA"

| Repo | Stars | Licencia | Lenguaje |
|---|---|---|---|
| [TheCMOAI/Agents4Marketing](https://github.com/TheCMOAI/Agents4Marketing) | high | MIT | Markdown + MCP |
| [iamevandrake/opensoul](https://github.com/iamevandrake/opensoul) | mid | Apache 2.0 (sobre Paperclip) | YAML + JSON |
| [Citedy/adclaw](https://github.com/Citedy/adclaw) | high | MIT | Python + React |
| [ericosiu/marketing-os-starter](https://github.com/ericosiu/marketing-os-starter) | mid | MIT | Markdown + JSON |
| [ruvnet/marketing](https://github.com/ruvnet/marketing) | mid | MIT | YAML + Claude-Flow |

---

## 2. Hallazgos clave por proyecto

### 2.1 TheCMOAI/Agents4Marketing

**Estructura por agente — patron a adoptar:**
- Cada agente es un "knowledge package" con 5 piezas: identity, rules, workflow, quality checklist, decision-tree playbook.
- Una base de conocimiento compartida (`knowledge/`) con `unit-economics.md`, `frameworks.md` (Schwartz, Hormozi, StoryBrand, Cialdini), `funnel-architecture.md`.
- Un archivo maestro `CLAUDE.md` que auto-carga todo el contexto.

**Lo que NO se replica:** los 10 agentes hiperverticales (Google Ads, Meta Ads, GBP) son fuera de scope inicial. Demasiado vertical para un holding de propósito general.

### 2.2 iamevandrake/opensoul

**Patron a adoptar:**
- Estructura de "agencia real": Director > Strategist > Producer > Creative > Growth Marketer > Analyst.
- Heartbeats: cada agente despierta en cron y revisa su queue.
- Delegacion top-down desde el Director.
- Audit trail completo de cada decision/draft/revision.
- Budget control mensual por agente.

**Lo que NO se replica:** corre sobre Paperclip (otro orquestador). Aqui ya tenemos OpenClaw — solo tomamos la idea de roles y heartbeats.

### 2.3 Citedy/adclaw

**Patron a adoptar:**
- **Memoria dual:** ReMe (file-based, per-agente) + AOM (vector compartida).
- **Routing por @tag** en Telegram: `@researcher find AI trends` enruta solo a ese agente.
- **Coordinator con sintesis:** lee AOM, analiza con LLM, emite `TaskStrategy` con delegaciones especificas. Logica continue / pivot / abandon.
- **Self-healing skills:** si un YAML de skill se rompe, el LLM lo arregla automaticamente.

**Lo que NO se replica de inmediato:** vector DB compartido (AOM) requiere infra que no tenemos (lightrag, qdrant, etc.). Por ahora, "memoria compartida" es `state/activity-log.jsonl` + dossiers, lo cual es mas simple y debuggable. Self-healing es bonito pero anti-determinista — fuera de v1.

### 2.4 ericosiu/marketing-os-starter

**Patron a adoptar (el mas alineado con nuestro v2):**
- 4 agentes: **Orchestrator** (router), **Researcher**, **Strategist**, **Copywriter**.
- 5 skills con triggers de intent: `/research`, `/campaign-brief`, `/copywriting`, `/social-content`, `/email-sequence`.
- **Handoffs JSON estrictos con `schemas/`**: cada paso emite un objeto JSON validado contra schema antes de pasar al siguiente.
- Memoria persistente en `memory/` (voice, campaigns, frameworks, task queue).
- Brand files en `brands/` por cliente.

**Lo que se adopta directamente como inspiracion:** la idea de schemas JSON por handoff es exactamente lo que necesitabamos. Implementacion propia en `skills/global/handoff/schemas/`.

### 2.5 ruvnet/marketing (AI Marketing Swarms)

**Patron a adoptar:**
- 15 agentes en mesh jerarquico para Google Ads / Meta / TikTok / LinkedIn / Pinterest / Snapchat.
- Atribucion causal multi-touch.
- Creative DNA: descomponer ads ganadores en hook + promise + proof + CTA y "criar" variantes.
- Fatigue forecaster.

**Lo que NO se replica:** demasiado vertical hacia gestion publicitaria con APIs de plataformas (necesita cuentas de anuncios reales y presupuestos). Fuera de scope hasta tener clientes con ads activos.

---

## 3. Patrones que adopta jarvis-ecosystem v2

| Patron | Origen | Implementacion |
|---|---|---|
| Estructura por agente: identity / soul / rules / workflow / quality | Agents4Marketing + opensoul | `agents/<name>/{IDENTITY.md, SOUL.md, AGENTS.md, MEMORY.md}` (ya existente) |
| Roles tipo "agencia real" | opensoul | mkt-content (creative), mkt-analytics (analyst), mkt-social (producer), mkt-ads (growth), jarvis (director) |
| Heartbeats programados | opensoul + adclaw | Ya existian (jarvis 30m, sales-hunter 1h, mkt-content 2h) — se documentan en [HEARTBEAT_OPERATIVO.md](HEARTBEAT_OPERATIVO.md) |
| Coordinator que sintetiza estado | adclaw | `skills/global/coordinator/` |
| Handoffs JSON con schemas | marketing-os-starter | `skills/global/handoff/schemas/` |
| Memoria dual (per-agente + compartida) | adclaw | per-agente: `agents/<name>/memory.json`. compartida: `state/activity-log.jsonl` + dossiers |
| Audit trail completo | opensoul | `state/activity-log.jsonl` append-only |
| Brand files por cliente | marketing-os-starter | `client-dossiers/<id>/brand.json` |
| Routing por bindings de canal | OpenClaw nativo | ya configurado en `openclaw.json` |

---

## 4. Patrones descartados (para v1) y razon

| Patron | Por que se descarta hoy |
|---|---|
| Vector DB compartido (AOM tipo adclaw) | Infra adicional (qdrant/lightrag), complejidad, poco debuggable. JSONL append-only basta para empezar |
| Self-healing skills via LLM | Anti-determinista, dificil de auditar. Mejor invertir en tests |
| 10 agentes hiperverticales | Sobreingenieria; el holding tiene 6 agentes activos hoy |
| Generacion publicitaria con APIs (Meta Ads, Google Ads) | Requiere cuentas activas y presupuestos. Fuera de scope sin clientes con ads vivos |
| Mission Control (kanban WS dashboard) | UI extra, mantenimiento, dependencias. Trello hace 80% del trabajo. v1.2 si se justifica |
| Antfarm (CLI de team) | Orquestacion en memoria, no persistente. Nuestros schemas + JSONL son mas auditables |

---

## 5. Videos de YouTube relevantes (a transcribir cuando aplique)

Lista curada para que `youtube-transcript` la procese cuando el equipo quiera profundizar:

| Tema | Sugerencia de busqueda |
|---|---|
| Multi-agente con OpenClaw | "OpenClaw multi agent setup" |
| Pipelines de marketing con IA | "AI marketing agency multi agent 2026" |
| Reels y carruseles "stack libre" | "free open source video editing pipeline reels" |
| edge-tts para narracion | "edge-tts python tutorial" |
| Remotion para reels verticales | "Remotion vertical video tutorial" |

Procedimiento (ya existente):

```bash
youtube-transcript transcript --url "https://youtu.be/..." > /tmp/t.txt
summarize /tmp/t.txt > docs/research/<tema>.md
```

Nota honesta: la API publica de `youtube-transcript-api` rate-limita; en la practica, tomar 3-5 videos por sesion y descansar.

---

## 6. Comparativa final: opciones evaluadas vs decision

| Opcion | Pros | Cons | Decision |
|---|---|---|---|
| Construir capa propia sobre OpenClaw | Coherente con stack, no agrega infra, debuggable | Requiere disciplina del equipo de agentes | **Adoptada** |
| Mission Control (kanban WS dashboard) | UI lista, kanban visual | Otra app que mantener; storage SQLite separado | Pospuesto a v1.2 |
| Migrar a Paperclip (opensoul base) | Heartbeats nativos, governance built-in | Cambio de orquestador completo, perder OpenClaw | Descartado |
| Esperar al RFC Agent Teams de OpenClaw | Solucion oficial | Fecha incierta | Descartado en v1, plan migracion en v2 |
| Vector DB compartido (estilo adclaw AOM) | Memoria semantica entre agentes | Complejidad y dependencias | Pospuesto a v2 |

---

## 7. Conclusion del research

La mejora v2 de jarvis-ecosystem aplica una sintesis pragmatica:

1. **Estructura por agente** ya existente (heredada del MK37 forense + skills propios) — no se toca.
2. **Coordinacion** mediante capa propia local (`state/`) inspirada en marketing-os-starter (handoffs JSON con schemas) y adclaw (coordinator que sintetiza), sin vector DB ni dashboards extras.
3. **Produccion de contenido** con stack 100% gratis: Pillow + Pollinations + Edge TTS + Remotion + ffmpeg, suficiente para Reels editoriales y carruseles de calidad agencia.
4. **Governance** existente (Approval Gates, Trello, dossiers) se extiende con AG-12/AG-13.

Sin agregar infraestructura nueva, sin vendor lock-in, sin gastar dinero, y manteniendo coherencia con la arquitectura OpenClaw + ClawFlows ya presente.
