# Recursos comunidad OpenClaw / Claude Code (curado para Jarvis)

**Ámbito:** inventario **externo** al monorepo `clawvis-openclaw`; sirve para **descubrir** plantillas, skills y patrones sin obligar a instalarlos.  
**Última revisión:** abril 2026 (ampliación: §2 marketing; §2.7 ECC; §2.8 LightRAG; §2.9 carrusel IG; §2.10 Canva + Composio).

---

## 1. Hallazgo forense (qué hay en este repo vs fuera)

| Ámbito | En `jarvis-ecosystem` | Fuera (comunidad) |
|--------|----------------------|-------------------|
| Gobierno multi-empresa | [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md), Trello, dossiers | No sustituible por un “framework” genérico; los enlaces siguientes son **complemento opcional**. |
| Skills por agente | Carpetas `agents/*/skills/` (convención del workspace) | [openclaw/skills](https://github.com/openclaw/skills), listas awesome (abajo). |
| Automatización real | ClawFlows, gateway OpenClaw, credenciales en host | Repos de demos/uso; validar permisos y privacidad antes de copiar. |
| Marketing digital (plantillas) | Roles `mkt-*` y [AGENTS.md](../agents/marketing/AGENTS.md) | Catálogo externo (p. ej. [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents)); el desglose forense y el mapeo a Jarvis están en **§2**. |

**Conclusión:** nada de la lista siguiente **reemplaza** a Jarvis como orquestador del holding; como mucho **enriquece** plantillas (SOUL), skills puntuales o metodología de trabajo en repos de código.

---

## 2. Investigación forense — marketing digital, OpenClaw y Claude (abr 2026)

<a id="marketing-openclaw-forense"></a>

### 2.1 Resumen ejecutivo

- **Objetivo de la búsqueda:** localizar en GitHub proyectos de **agencias de marketing digital** que declaren de forma explícita **OpenClaw + Claude** como stack operativo público.
- **Hallazgo principal:** no aparece un repositorio que sea equivalente a “producto de agencia + código abierto” con esa etiqueta. La comunidad aporta **plantillas `SOUL.md`**, **skills**, **listas awesome** y artículos/blog; el valor es **patrón operativo** (roles, pipelines, revisión humana), no un fork listo para sustituir el gobierno Jarvis.
- **Uso para el holding:** tomar **pocas** plantillas como inspiración, adaptarlas a identidad y líneas rojas de la empresa Marketing, y atar todo a **dossier + Trello** (ver §2.5 para mapeo plantillas → `mkt-*`, §2.6 para el procedimiento de adopción).

### 2.2 Fuentes priorizadas

| Fuente | URL | Valor para Jarvis | Riesgos / notas |
|--------|-----|-------------------|-----------------|
| Awesome OpenClaw Agents | https://github.com/mergisi/awesome-openclaw-agents | Sección **Marketing & Content**: muchas plantillas con `SOUL.md` listas para estudiar o adaptar. | README enlaza a **CrewClaw** (despliegue comercial en terceros): solo si el superusuario acepta dependencia y términos; no es el flujo por defecto del monorepo. |
| OpenClaw Skills (oficial) | https://github.com/openclaw/skills | Skills de contribuyentes; puede haber utilidades de marketing. | Revisar licencia, datos y mantenimiento antes de instalar. |
| Awesome OpenClaw Use Cases | https://github.com/hesamsheikh/awesome-openclaw-usecases | Playbooks y ejemplos reales. | Documentación; no define gobierno multi-empresa. |
| Awesome OpenClaw (lista) | https://github.com/rylena/awesome-openclaw | Descubrimiento de recursos. | Curar antes de adoptar. |
| Artículos (p. ej. Medium) | (varios) | Metodología: equipos de N agentes, heartbeat, **human-in-the-loop**. | No son código mantenido aquí; enlazar solo como idea, no como dependencia. |

### 2.3 Claude y el gateway

**Claude no es un repositorio “agencia + OpenClaw”.** En producción, Anthropic entra como **proveedor de modelo** vía la configuración del gateway OpenClaw (API / bindings). La comunidad también menciona **Claude Code** y skills asociados en entornos de desarrollo; eso es independiente del rol de Jarvis como orquestador del holding. Detalle de integraciones ya contempladas en el ecosistema: [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md). No duplicar secretos ni rutas de credenciales en este documento.

### 2.4 Versiones de OpenClaw y dependencias comerciales

- El catálogo **mergisi** declara, para algunas plantillas de marketing avanzadas (p. ej. pipelines multimedia), requisito de **OpenClaw v2026.4.5+** en su README upstream. Antes de usar una plantilla concreta, comprobar en el repositorio upstream la nota de versión junto a esa fila.
- **CrewClaw** ofrece “deploy en 60s” y paquetes generados: implica servicio y flujo ajenos al repo; tratarlo como **opción explícita**, no como requisito de Jarvis.

### 2.5 Mapeo plantillas awesome (mergisi) → roles Jarvis (`mkt-*`)

Referencias de carpeta según [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) (tabla **Marketing & Content** del README). Es **orientación**, no obligación de usar cada plantilla.

| Plantilla (nombre) | Carpeta típica en upstream | Rol Jarvis sugerido | Riesgo / ToS / automatización |
|--------------------|-----------------------------|----------------------|--------------------------------|
| Echo | `agents/marketing/echo/` | mkt-content | Copy multi-canal; revisar tono de marca antes de publicar. |
| Buzz | `agents/marketing/social-media/` | mkt-social | Programación y redes: ToS de cada plataforma; sin spam. |
| Rank | `agents/marketing/seo-writer/` | mkt-content / mkt-analytics | GSC/APIs: credenciales por cliente; datos sensibles. |
| Digest | `agents/marketing/newsletter/` | mkt-email | Listas y RGPD/consentimiento según jurisdicción. |
| Scout | `agents/marketing/competitor-watch/` | mkt-analytics | Competencia: fuentes públicas; no scraping abusivo. |
| Reddit Scout | `agents/marketing/reddit-scout/` | mkt-social | Reglas de Reddit; riesgo de sombra de baneo si se automatiza mal. |
| Cold Outreach | `agents/marketing/cold-outreach/` | mkt-ads | Correo en frío: leyes anti-spam y políticas del dominio. |
| Brand Monitor | `agents/marketing/brand-monitor/` | mkt-analytics | Menciones y sentimiento: atribución y almacenamiento de datos. |
| Email Sequence | `agents/marketing/email-sequence/` | mkt-email | Secuencias drip: mismo cuidado que newsletter. |
| Content Repurposer | `agents/marketing/content-repurposer/` | mkt-content | Multiformato: coherencia de mensaje entre canales. |

Lista upstream completa y cambiante: [README mergisi — Marketing & Content](https://github.com/mergisi/awesome-openclaw-agents#-marketing--content).

### 2.6 Procedimiento de adopción (Marketing)

1. **Elegir una plantilla** en el catálogo upstream acorde al encargo (una sola a la vez para reducir ruido). Comprobar si exige versión mínima de OpenClaw o herramientas externas (GSC, APIs).
2. **Adaptar** el contenido del `SOUL.md` (o ideas del rol) al workspace de la empresa Marketing: `SOUL.md`, `USER.md`, líneas rojas de [AGENTS.md](../agents/marketing/AGENTS.md), sin contradecir CEO/supervisor.
3. **Abrir o actualizar** tarjeta en Trello con `[dossier_id]`, listas y etiquetas según [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md) y [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md); reflejar estado del entregable en el dossier del cliente.
4. **Human-in-the-loop:** borradores y automatismos no sustituyen la aprobación para contenido público o masivo; el supervisor o el superusuario dan luz verde según política del cliente y del holding.

**Riesgos residuales:** el catálogo mergisi evoluciona rápido (la tabla §2.5 puede quedar desfasada; usar el README upstream como fuente de verdad). Plantillas que asumen credenciales de terceros requieren **permiso explícito del cliente** y manejo seguro de secretos en el host, fuera de este repo.

### 2.7 everything-claude-code (ECC) — harness de desarrollo (no sustituto de OpenClaw)

| Campo | Detalle |
|-------|---------|
| **Repositorio** | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) |
| **Licencia** | MIT (verificar en cada release). |
| **Qué es** | Sistema orientado al *agent harness*: plugin **Claude Code**, instaladores para **Cursor**, OpenCode, Codex, Gemini, cientos de **skills**, hooks, reglas por lenguaje, MCP de ejemplo, guías (tokens, evals, paralelización) y herramientas npm (`ecc-universal`, **`ecc-agentshield`**). |

**Qué sí tiene sentido para Jarvis / este monorepo**

- **AgentShield** (`npx ecc-agentshield scan`): auditoría estática de superficies tipo config de agentes/MCP/hooks en el **repo** (el CI del monorepo puede ejecutarlo de forma **advisory**). No sustituye revisión humana ni [SECURITY_GATEWAY.md](SECURITY_GATEWAY.md).
- **Guías** (*shortform/longform* del repo ECC): lectura opcional sobre optimización de contexto y verificación en **sesiones de desarrollo**; **no** mitigan por sí solas picos de CPU de `memorySearch` ni `rg` — ver [TROUBLESHOOTING_OPENCLAW_CPU.md](../../docs/TROUBLESHOOTING_OPENCLAW_CPU.md).
- **Cherry-pick de skills:** si una skill upstream encaja, **reescribir** un `SKILL.md` compatible OpenClaw bajo `agents/*/skills/`, con atribución y criterios de la §3.

**Qué no hacer sin decisión explícita**

- Instalar el **plugin ECC completo** o copiar `hooks/hooks.json` de Claude Code **dentro** del árbol de agentes Jarvis como fuente única de verdad (duplica convenciones y rompe el modelo OpenClaw).
- Confiundir **hooks ECC** (CLI Claude Code) con **eventos del gateway OpenClaw**; son capas distintas.
- Depender de **ccg-workflow** / comandos `multi-*` que exigen runtime adicional salvo que el superusuario quiera ese flujo en el IDE.

**Shortlist de skills ECC (ideas vs Jarvis)** — referencia para priorizar port manual; no es inventario instalado.

| Idea ECC | Rol o recurso Jarvis existente |
|----------|----------------------------------|
| `search-first` | Complementa investigación; [last30days-openclaw](../agents/jarvis/skills/last30days-openclaw/) y gobierno Trello siguen siendo la fuente de verdad operativa. |
| `documentation-lookup` | Útil antes de integrar APIs nuevas; port solo si hay `_meta` y revisión. |
| `cost-aware-llm-pipeline` | Alineado conceptualmente con [MODELOS_JARVIS_OPENCLAW.md](../../docs/MODELOS_JARVIS_OPENCLAW.md) y el router en `agents/jarvis/scripts/`. |
| `article-writing` / `market-research` / `content-engine` | Comparar con agentes `mkt-*` y skills de marketing; evitar duplicar flujos ya cubiertos. |

**Reglas de IDE (solo desarrollo en `clawvis-openclaw`)**

- Para **TypeScript/Python/Go** en el código del monorepo (p. ej. `agent-town/`), se puede usar el instalador upstream con **`./install.sh --target cursor`** desde un clon de ECC **fuera** de `jarvis-ecosystem/agents/`, copiando solo `rules/common` + el lenguaje necesario según el README de ECC. Eso **no** configura el gateway OpenClaw ni los canales Telegram/Discord.

### 2.8 LightRAG (HKUDS) — patrones portados, sin instalar el servidor

| Campo | Detalle |
|-------|---------|
| **Repositorio** | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) (paper EMNLP 2025, arXiv:2410.05779; licencia MIT en upstream). |
| **Qué aporta el paper/producto** | Recuperación en **dos niveles** (local + global), **KG** combinado con vectores, consultas **mixtas**, citación de contextos; servidor opcional con API/Web UI y muchos backends de almacenamiento. |

**Qué implementamos en Jarvis (habilidades, no binario LightRAG)**

- Skill **[`dual-retrieval-ops`](../agents/jarvis/skills/dual-retrieval-ops/SKILL.md):** traduce esas ideas a **MemPalace** (búsqueda semántica + KG), **Graphify** (mapa del repo), **dossiers** y citas explícitas. Es la forma soportada de usar “lo mejor” de LightRAG sin segundo stack Python ni más carga en Ollama.
- Puente conceptual: [DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md](DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md).

**Qué no hace falta instalar para obtener esas habilidades**

- **`lightrag-hku`**, Docker del LightRAG Server o bases dedicadas **solo** para replicar el paper — salvo decisión explícita de negocio (corpus masivo fuera del palace; host separado). Ver gate abajo.

| Dimensión | Jarvis (implementado) | LightRAG upstream |
|-----------|----------------------|-------------------|
| Corpus principal | Repo + sesiones + wings MemPalace + dossiers | Documentos ingestados en índice propio |
| “Local” vs “global” | Skill `dual-retrieval-ops` + herramientas MCP | Dual retrieval + rerank en servidor |
| KG | MemPalace KG + Graphify (mapa código) | KG extraído del texto del corpus indexado |
| Coste CPU | Sin servicio RAG adicional | LLM de indexado + embeddings + DB (ver [TROUBLESHOOTING_OPENCLAW_CPU.md](../../docs/TROUBLESHOOTING_OPENCLAW_CPU.md)) |

**Gate para desplegar el servidor LightRAG algún día (opcional)**

1. Corpus claro (p. ej. PDFs de cliente) que no encaje en MemPalace/dossiers.
2. Presupuesto de máquina o contenedor **aparte** del gateway.
3. Aprobación CEO / superusuario y política de datos.

Hasta entonces: usar **solo** el skill y la documentación enlazada.

### 2.9 Open Carrusel (Hainrixz) — referencia opcional; en Jarvis solo el skill

| Campo | Detalle |
|-------|---------|
| **Repositorio** | [Hainrixz/open-carrusel](https://github.com/Hainrixz/open-carrusel) (MIT) — app local Next.js + export PNG vía Puppeteer. |
| **En jarvis-ecosystem** | Skill **[`carousel-ops`](../agents/jarvis/skills/carousel-ops/SKILL.md)** con narrativa por slides, dimensiones IG, diseño y caption; **no** se incluye la app en el monorepo. |
| **Documentación** | [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) — qué se adopta y qué se descarta. |

Instalar open-carrusel en el PC del operador es **opcional** para exportar PNGs; el gateway y los agentes no dependen de ello.

### 2.10 Canva + Composio — diseno visual via API desde OpenClaw

| Campo | Detalle |
|-------|---------|
| **Servicio** | [Canva](https://canva.com) (suite de diseno) via [Composio](https://composio.dev) (plataforma de integracion). |
| **Plugin OpenClaw** | `@composio/openclaw-plugin` v0.0.11 — instalado con `openclaw plugins install --dangerously-force-unsafe-install @composio/openclaw-plugin`. |
| **32 herramientas** | Crear disenos, autofill brand templates, exportar PNG/PDF, gestionar carpetas, comentar, listar assets. |
| **Auth** | OAuth gestionado por Composio; `consumerKey` (`ck_...`) en `~/.openclaw/openclaw.json` (no commitear). |

**Que aporta al ecosistema**

- Los agentes `mkt-*` y Jarvis pueden **crear y editar disenos Canva** desde chat (Telegram, Discord, TUI) sin intervención humana para la parte visual.
- **Brand templates:** autofill con datos del dossier del cliente para coherencia de marca.
- **Export programático:** obtener URLs de descarga de los diseños terminados.
- Complementa `carousel-ops` (guion textual) con **producción visual real**.

**Que NO hacer**

- Commitear el `consumerKey` al repo — tratarlo como secreto (`.env`, vault, o config local).
- Publicar directamente sin **AG-03**: el export es automático, la publicación requiere aprobación humana.
- Asumir que Composio reemplaza open-carrusel: son complementarios (API remota vs local HTML→PNG).

**Referencia:** [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) (flujo combinado), config snapshot en `config/openclaw-home/openclaw.json`.

---

## 3. Criterios de adopción (obligatorio antes de instalar)

1. **Licencia:** MIT/BSD preferible; AGPL/Commons Clause implica revisar redistribución y uso comercial.
2. **Datos:** skills que envíen contenido a terceros o scrapeen redes — revisar ToS y política del cliente.
3. **Operación:** evitar servicios 24/7 obligatorios salvo que el superusuario los quiera mantener.
4. **Alineación:** debe poder mapearse a **empresa + dossier + Trello** sin romper [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md).

---

## 4. Inventario por categoría (enlaces)

### Núcleo y frameworks

| Recurso | URL | Nota para Jarvis |
|---------|-----|------------------|
| OpenClaw (upstream) | https://github.com/openclaw/openclaw | Referencia de producto; alinear versiones con el gateway del host. |
| Clade (multi-agente Markdown) | https://github.com/satoh-y-0323/clade | Útil como **idea** de fases con aprobación humana en **proyectos Claude Code**; no mergear el framework entero en el monorepo sin necesidad. |
| Claude Code | https://github.com/anthropics/claude-code | Base CLI; Clade y muchos skills asumen su presencia. |
| everything-claude-code (ECC) | https://github.com/affaan-m/everything-claude-code | Harness multi-IDE + skills; resumen y límites en **§2.7**. |
| LightRAG (HKUDS) | https://github.com/HKUDS/LightRAG | Patrones dual-retrieval + KG; **implementados** en skill `dual-retrieval-ops` — ver **§2.8** (no requiere instalar el servidor). |
| Stokowski (Symphony) | https://github.com/Sugar-Coffee/stokowski | Aislamiento de agentes; evaluar solo si hace falta sandbox fuerte. |

### Plantillas y agentes

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Agents | https://github.com/mergisi/awesome-openclaw-agents | Plantillas SOUL; inspiración para marketing/ventas; no copiar ciegamente identidades ya definidas en el holding. |
| OpenClaw Agents Kit | https://github.com/shenhao-stu/openclaw-agents | Despliegue rápido de flota; contrastar con `COMPANIES.md` y roles por empresa. |

### Skills y registro

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Skills | https://github.com/VoltAgent/awesome-openclaw-skills | Catálogo grande; filtrar por categoría e instalar **pocos** skills revisados. |
| OpenClaw Official Skills | https://github.com/openclaw/skills | Registro público oficial. |
| Xiaohongshu Skills | https://github.com/white0dew/XiaohongshuSkills | Solo si el ICP incluye esa plataforma. |
| Reddit Growth Skill | https://github.com/oh-ashen-one/reddit-growth-skill | Solo si marketing prioriza Reddit. |

### Casos de uso y GTM

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Use Cases | https://github.com/hesamsheikh/awesome-openclaw-usecases | Ideas de playbooks; documentación de referencia. |
| Markster OS (GTM B2B) | https://github.com/markster-public/markster-os | Lenguaje GTM en chat; revisar prompts; no dependencia obligatoria. |
| Open Carrusel | https://github.com/Hainrixz/open-carrusel | Carruseles IG (HTML → PNG); **patrones** en skill `carousel-ops` — app upstream **opcional** fuera del repo — ver **§2.9**. |
| Canva + Composio | https://composio.dev/toolkits/canva | Diseno visual via API; plugin OpenClaw `composio` para crear/editar/exportar disenos Canva desde chat — ver **§2.10**. |

### Patrones de trabajo (recomendado para tareas grandes de código)

| Recurso | URL | Nota |
|---------|-----|------|
| Three Man Team | https://github.com/russelleNVy/three-man-team | Patrón **Arquitecto → Constructor → Revisor** (MIT); encaja con dev-agency y cambios grandes; ver [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md) sección ampliada. |

### Monitoreo y RL (baja prioridad por defecto)

| Recurso | URL | Nota |
|---------|-----|------|
| OpenClaw Office | https://github.com/WW-AI-Lab/openclaw-office | UI “oficina”; requiere servicio adicional. |
| OpenClaw-RL | https://github.com/Gen-Verse/OpenClaw-RL | RL sobre agentes; complejidad alta; solo I+D explícito. |

---

## 5. Qué no hacer desde Jarvis sin decisión explícita

- Instalar **decenas** de skills a la vez (ruido, conflictos, mantenimiento).
- Sustituir **Trello + dossier** por herramientas solo-chat sin trazabilidad.
- Incorporar repos **AGPL/Commons** en productos comerciales sin asesoría legal.

---

## 6. Referencias internas

- Carruseles Instagram: **§2.9**, [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md), skill `carousel-ops`.
- Canva + Composio: **§2.10**, plugin OpenClaw `composio`, [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) (flujo combinado).
- LightRAG (patrones): **§2.8**, [DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md](DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md), skill `dual-retrieval-ops`.
- everything-claude-code (ECC): **§2.7** (tabla y shortlist).
- Gobierno: [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md)
- Integraciones gateway: [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)
- Flujo Kanban: [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md)
- Empresa Marketing (roles `mkt-*`): [../agents/marketing/AGENTS.md](../agents/marketing/AGENTS.md)
