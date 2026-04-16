# Carruseles Instagram y disenos para redes — ecosistema Jarvis

## Que queda en el repo (lo necesario)

- **Skill [`carousel-ops`](../agents/jarvis/skills/carousel-ops/SKILL.md):** guion por slides, dimensiones IG, caption/hashtags, y **pipeline automatizado** copy + Canva (Composio) hasta export cuando las herramientas estan disponibles. **AG-03** aplica a **publicar** en Instagram, no a crear borrador/export en Canva — ver [APPROVAL_GATES.md](APPROVAL_GATES.md).
- Referencia en [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) §2.9 y §2.10.

Jarvis y `mkt-*` deben **ejecutar** el diseno remoto via API cuando el encargo lo pide; no limitarse a texto si Composio+Canva estan configurados.

### Objetivo: cero pasos humanos en runtime (salvo publicar)

| Fase | Quien actua | Interaccion humana |
|------|-------------|---------------------|
| Config inicial (una vez) | Operador | OAuth Composio, Canva en dashboard, `alsoAllow` `COMPOSIO_*`, reinicio gateway |
| Por cada post IG con diseno | Jarvis / `mkt-*` | **Ninguna** si las herramientas responden: buscar acciones Canva, crear/exportar, devolver URLs y `design_id` |
| Publicar en IG | — | **AG-03** (aprobacion CEO) salvo politica explicita distinta |

Limites tecnicos habituales: cuenta Canva gratis sin brand templates (`items: []`), calidad export Free vs Pro, elementos premium que bloquean export — el skill documenta fallbacks.

---

## Herramienta A: open-carrusel (local, export PNG)

| Campo | Detalle |
|-------|---------|
| **Que es** | App Next.js + Puppeteer que genera slides HTML y los exporta como PNGs a dimensiones exactas de Instagram. |
| **Donde esta** | `~/tools/open-carrusel/` (fuera del monorepo). |
| **Repo upstream** | [Hainrixz/open-carrusel](https://github.com/Hainrixz/open-carrusel) (MIT). |
| **Cuando usarlo** | Cuando el operador humano quiere export PNG pixel-perfect en su PC, sin depender de servicios externos. |
| **Quien lo opera** | El humano; Jarvis le entrega el guion (via `carousel-ops`), el humano pega el contenido en la app y exporta. |

**Setup rapido:**

```bash
cd ~/tools/open-carrusel
PUPPETEER_SKIP_DOWNLOAD=true npm install   # o npm run setup si quieres Chromium
npm run dev                                 # abre http://localhost:3000
```

**Lo que NO se hace:** no se clona dentro de `clawvis-openclaw/`, no se agrega como submodulo, no se ejecuta desde el gateway OpenClaw.

---

## Herramienta B: Canva via Composio (API, diseno remoto)

| Campo | Detalle |
|-------|---------|
| **Que es** | Integracion de la API de Canva a traves de [Composio](https://composio.dev) como plugin de OpenClaw. |
| **32 herramientas** | Crear disenos, gestionar carpetas, exportar, comentar, autofill con templates de marca, etc. |
| **Donde se configura** | `~/.openclaw/openclaw.json` → `plugins.entries.composio` + `consumerKey` (no commitear el key). |
| **Cuando usarlo** | Cuando Jarvis o `mkt-*` necesitan crear/editar disenos Canva programaticamente desde chat (Telegram, Discord, TUI). |
| **Quien lo opera** | El agente (tool calling) de forma **automatica** en cada encargo; el humano solo para **publicacion** en la red (AG-03), no para cada export en Canva. |

**Herramientas destacadas de Canva via Composio:**

- `create_canva_design_with_optional_asset` — crear diseno con preset o dimensiones custom.
- `initiate_canva_design_autofill_job` — autofill brand templates.
- `initiates_canva_design_export_job` + `get_design_export_job_result` — exportar a PNG/PDF con URL de descarga.
- `list_user_designs` / `access_user_specific_brand_templates_list` — listar disenos y templates.
- `create_user_or_sub_folder` / `move_item_to_specified_folder` — organizar proyectos.

**Setup:**

1. Crear cuenta en [dashboard.composio.dev](https://dashboard.composio.dev).
2. Obtener `consumerKey` (`ck_...`).
3. `openclaw config set plugins.entries.composio.config.consumerKey "ck_TU_KEY"`.
4. `openclaw gateway restart`.
5. Autenticar Canva desde el dashboard de Composio (OAuth).

**Referencia en repo:** `config/openclaw-home/openclaw.json` tiene el placeholder `ck_REPLACE_ME` — no commitear el key real.

### Telegram / Discord y perfil `messaging`

Si el plugin Composio esta bien (consumer key + Canva conectado) pero Jarvis **dice que no puede listar Canva**, el motivo suele ser `tools.profile: "messaging"`: ese perfil solo incluye un subconjunto de herramientas core. Las herramientas del plugin (`COMPOSIO_*`) hay que **permitirlas explicitamente** en `tools.alsoAllow`, igual que `lobster` y `browser`.

En `~/.openclaw/openclaw.json`, `tools.alsoAllow` debe incluir las siete herramientas genericas de Composio que expone el MCP (nombres exactos: `COMPOSIO_MANAGE_CONNECTIONS`, `COMPOSIO_MULTI_EXECUTE_TOOL`, `COMPOSIO_REMOTE_BASH_TOOL`, `COMPOSIO_REMOTE_WORKBENCH`, `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_WAIT_FOR_CONNECTIONS`, `COMPOSIO_GET_TOOL_SCHEMAS`). El snapshot sanitizado en el repo muestra la lista completa. Tras cambiar: `openclaw gateway restart`. Comprueba con `openclaw composio doctor`.

### Como funciona Canva por API (oficial) — y por que el titular no siempre se “pega” solo

Resumen alineado con la documentacion de **Canva Connect** y el **toolkit Canva en Composio** ([docs.composio.dev/toolkits/canva](https://docs.composio.dev/toolkits/canva)):

| Capacidad | Que implica |
|-----------|-------------|
| **Crear diseno** (dimensiones custom o preset, opcionalmente con **asset**/imagen) | Es lo que suelen exponer acciones tipo crear diseno / `POST` designs: lienzo vacio o con una imagen de partida — ver [Create design (Connect)](https://www.canva.dev/docs/connect/api-reference/designs/create-design/). |
| **Subir activos** y **exportar** | Subir imagenes a la biblioteca del usuario, lanzar jobs de export a PNG/PDF, etc. |
| **Texto en el lienzo como cajas editables** | **No** hay un flujo simple universal en Connect del estilo “pon este string en un cuadro de texto en (x,y)” expuesto igual en todos los entornos. La via programatica habitual para **rellenar contenido** en plantillas es **Brand Templates + Autofill** (campos variables definidos en la plantilla; a menudo **Canva Enterprise**). Composio documenta jobs de autofill asociados a esas plantillas. |
| **Apps SDK / Design Editing API** | Otra capa de producto (apps **dentro** del editor de Canva o APIs de edicion avanzada) — **no** es lo mismo que el conjunto de acciones que un agente usa vía Composio MCP en un chat. |

Por eso es **coherente** que Jarvis pueda **crear** un diseno 1080×1350 e **insertar el logo** (asset / URL), pero **no** colocar automaticamente el titular como texto en el lienzo: el toolkit Composio prioriza **creacion, activos, export, plantillas/autofill**, no edicion libre de cada elemento de texto del lienzo. La finalizacion del copy en el editor — o una **plantilla de marca con campos de autofill** preparada en Canva — es el camino realista hasta que exista una herramienta equivalente en tu stack.

**Si “Recientes” en canva.com esta vacio:** abre el enlace **“Editar en Canva”** que devuelve la API (mismo usuario OAuth que conectaste en Composio). Si entras con **otra** cuenta de Canva, no veras el diseno.

### “Que analice plantillas predisenadas del buscador y arme un post completo como en la UI”

Lo que haces en Canva al elegir **Redes → Instagram → plantilla** es un flujo **del producto web**: miles de plantillas publicas en el explorador. Eso **no** es el mismo catalogo al que la **Connect API** (y por tanto **Composio**) puede decir: *“usa exactamente esta plantilla del buscador por nombre o miniatura”* y rellenarla como en la UI.

| Que pide el usuario | Que hace hoy Composio/Connect en la practica | Por que |
|---------------------|---------------------------------------------|--------|
| “Usa una plantilla ya predisenada del buscador de Canva” | **No** hay un paso API equivalente a elegir fila/columna del explorador y clonar ese diseno con un clic | El catalogo publico web no se expone como lista de IDs para autofill masivo; ver [Create design](https://www.canva.dev/docs/connect/api-reference/designs/create-design/) (preset de tamano o lienzo + assets, no “template URL del buscador”). |
| Crear lienzo 1080×1080 + logo + export | **Si** — suele funcionar | `POST` designs + assets + export |
| Misma estetica que una plantilla concreta del buscador | Solo si la convertis a flujo soportado por API (abajo) | Sin eso, el agente solo puede aproximar con layout vacio + imagenes |

**No es un bug de Jarvis:** es limite de producto/API. El diseno “nuevo” que ves es un **lienzo con dimensiones** (y quizas imagenes), no un **clon** de una plantilla del explorador.

**Tercera via (estetica generada, no plantilla del buscador):** el [MCP oficial de Canva](https://www.canva.dev/docs/mcp/) expone `generate-design` / `create-design-from-candidate` (generacion y edicion con lenguaje natural). Tampoco elige una miniatura concreta del explorador; aproxima layout por prompt. Requiere intake y configuracion del cliente MCP aparte de Composio.

**Camino automatizable “completo” (texto + imagenes en campos definidos):**

1. **Canva for Teams / Enterprise** con **Brand templates**: plantillas de equipo con **campos de datos** (titular, cuerpo, foto, etc.).
2. En Composio existen acciones del estilo **listar brand templates**, **obtener definicion del dataset** y **iniciar job de autofill** (`CANVA_INITIATE_CANVA_DESIGN_AUTOFILL_JOB`) con un objeto `data` cuyas claves coinciden con los campos de la plantilla — ver [toolkit Canva en Composio](https://docs.composio.dev/toolkits/canva).
3. Jarvis puede entonces: listar plantillas → elegir una → rellenar campos con el copy del post → crear el diseno autofillado (sujeto a plan y permisos).

**Sin Enterprise / sin brand templates:** el flujo realista es **hibrido**: tu eliges la plantilla en Canva, afinas una **maqueta maestra**, y el agente aporta **copy por slide + assets**; o duplicas a mano y el API solo suma imagenes exporta. **Redimensionar** un diseno existente a otro formato es otra accion API (suele requerir **Pro/Enterprise**).

**Prompt ejemplo para Jarvis (si tienes brand templates):**  
*“Con Composio Canva: lista mis brand templates, muestra el dataset de la plantilla [nombre o ID], y si los campos encajan con el post de Corral X, ejecuta autofill con titular=…, subtitulo=…, logo=… (asset id o URL segun pida la herramienta).”*

---

## Flujo combinado: guion + diseno + publicacion

```
carousel-ops (guion)
       |
       v
  +----+----+
  |         |
  v         v
open-carrusel    Canva/Composio
(local PNG)      (API remota, agente)
  |              |
  v              v
Archivos PNG    URL de descarga / design_id
  |              |
  +------+-------+
         |
         v
  AG-03 solo si PUBLICAR en IG
  (aprobacion CEO)
         |
         v
  Publicacion en IG
```

1. **Jarvis / mkt-content** ejecuta `carousel-ops` y, si aplica, **Canva/Composio en la misma sesion** (sin pasos humanos entre guion y export).
2. **open-carrusel** solo si no hay API o se pide control local explicito.
3. **AG-03** unicamente al **publicar** en la red; el export/borrador en Canva puede ser totalmente automatico.

---

## Lo que se desecha definitivamente

- App open-carrusel **dentro** del monorepo (Next.js, Puppeteer, Chromium, Claude CLI).
- Submodulo o fork en `clawvis-openclaw/`.
- Job de CI que levante esa stack.

## Tabla comparativa: vias Canva disponibles

| Via | Tipo | Herramientas clave | Plan Canva | Estado |
|-----|------|-------------------|------------|--------|
| **A. open-carrusel** | Local (HTML/PNG) | Export pixel-perfect, sin API | N/A | Opcional en `~/tools/` |
| **B. Composio** | MCP remoto | ~32 acciones Canva via tool calling | Gratis (limitado) | Activa (OAuth OK) |
| **C. Canva Connect directo** | OAuth + REST | `canva.sh`: designs, export, autofill, upload | Gratis (limitado) | Skill `canva` instalado |
| **D. MCP oficial Canva** | MCP remoto | 30+ tools: `generate-design`, editing transactions, resize | Free/Pro/Enterprise | Pendiente registro |

**Proyectos de referencia estudiados:**

1. [`coolmanns/canva-connect`](https://github.com/openclaw/skills/tree/main/skills/coolmanns/canva-connect) — skill OpenClaw, Connect API directa (base del skill C).
2. [Canva MCP oficial](https://www.canva.dev/docs/mcp/) — servidor remoto con generacion IA y edicion en lienzo.
3. [`canva-design-assets`](https://mcpmarket.com/tools/skills/canva-design-assets) — skill MCPMarket, patron bulk social media.
4. [`canva-sdks/canva-gemini-extension`](https://github.com/canva-sdks/canva-gemini-extension) — extension MCP oficial de Canva para Gemini.
5. [Composio toolkit Canva](https://composio.dev/toolkits/canva) — integracion ya activa en el ecosistema.
6. **Canva MCP Connector (intake)** — Formulario oficial: [Canva MCP Connector Intake Form](https://docs.google.com/forms/d/e/1FAIpQLSdtsKA9LSmY-JEf_nF5QYBdjxfnXbgqvlKzd8obKGSPSK_eOA/viewform). Canva documenta alli el servidor MCP remoto `https://mcp.canva.com/mcp`, ejemplo cliente con `npx -y mcp-remote@latest https://mcp.canva.com/mcp`, y que el **OAuth Redirect URI** que usaras debe declararse en el formulario. Capacidades citadas como disponibles: autofill con lenguaje natural, buscar disenos, explorar contenido del diseno, crear desde imagen, importar disenos, comentarios, redimensionar, exportar, crear desde brand template, generar disenos nuevos desde el contexto del chat.

**Herramientas MCP oficial por plan (referencia [canva.dev/docs/mcp/tools](https://www.canva.dev/docs/mcp/tools/)):**

| Herramienta | Free | Pro | Enterprise |
|-------------|------|-----|------------|
| `generate-design` | Si | Si | Si |
| `export-design` | Standard | Pro quality | Pro quality |
| `start/perform/commit-editing-transaction` | Si | Si | Si |
| `resize-design` | No | Si | Si |
| `autofill-design` | No | No | Si |
| `search-brand-templates` / `list-brand-kits` | No | No | Si |
| `upload-asset-from-url` | Si | Si | Si |

### Documentacion oficial Canva MCP (enlaces)

| Tema | Enlace |
|------|--------|
| Vision general (servidor remoto `https://mcp.canva.com/mcp`, DCR, planes) | [Canva Model Context Protocol (MCP)](https://www.canva.dev/docs/mcp/) |
| Herramientas MCP y limites por minuto / plan | [MCP tools and rate limits](https://www.canva.dev/docs/mcp/tools/) |
| **Design edit handoff:** devolver `edit_url` o `https://www.canva.com/design/{design_id}/edit` tras crear/listar/editar | [Design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/) |
| Timeouts (`generate-design` hasta ~60s), registro manual OAuth, sin auth a nivel organizacion, dominios `canva.com` / `canva.ai` | [Troubleshooting](https://www.canva.dev/docs/mcp/troubleshooting/) |
| Politica de uso para integradores (UX, datos, Brand Kit, agentes compartidos) | [Usage policy](https://www.canva.dev/docs/mcp/usage-policy/) |
| Usos prohibidos (extraccion masiva, competencia, entrenar modelos con datos Canva) | [Prohibited use](https://www.canva.dev/docs/mcp/prohibited-use/) |

Jarvis y `mkt-*` deben respetar **handoff** (enlace de edicion al usuario) y las politicas anteriores si integran el MCP oficial.

---

## Resumen

| Pregunta | Respuesta |
|----------|-----------|
| Jarvis necesita open-carrusel instalado? | **No** — opcional en `~/tools/`. |
| Jarvis necesita Canva? | **Opcional** — via Composio, skill directo o MCP oficial. |
| Que necesita el ecosistema como minimo? | Skill `carousel-ops` + gobierno (dossier, Trello, AG-03). |
| Donde estan los PNG? | Donde el humano los exporte (open-carrusel local o Canva export). |
| Cual es la via mas potente? | MCP oficial (D) — pero requiere registro y espera 5-7 dias. |
