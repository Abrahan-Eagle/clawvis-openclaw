# Recursos comunidad OpenClaw / Claude Code (curado para Jarvis)

**Ámbito:** inventario **externo** al monorepo `clawvis-openclaw`; sirve para **descubrir** plantillas, skills y patrones sin obligar a instalarlos.  
**Última revisión:** abril 2026 (ampliación: §2 investigación marketing + Claude y mapeo a `mkt-*`).

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
- **Uso para el holding:** tomar **pocas** plantillas como inspiración, adaptarlas a identidad y líneas rojas de la empresa Marketing, y atar todo a **dossier + Trello** (ver §2.5).

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

- Gobierno: [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md)
- Integraciones gateway: [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)
- Flujo Kanban: [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md)
- Empresa Marketing (roles `mkt-*`): [../agents/marketing/AGENTS.md](../agents/marketing/AGENTS.md)
