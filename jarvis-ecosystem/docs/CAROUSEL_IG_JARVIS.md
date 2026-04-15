# Carruseles Instagram y disenos para redes — ecosistema Jarvis

## Que queda en el repo (lo necesario)

- **Skill [`carousel-ops`](../agents/jarvis/skills/carousel-ops/SKILL.md):** guion por slides, dimensiones IG, reglas de diseno legibles, caption/hashtags, cumplimiento **AG-03**.
- Referencia en [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) §2.9 y §2.10.

Con eso Jarvis y `mkt-*` pueden **planificar y redactar** carruseles sin instalar nada mas.

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
| **Quien lo opera** | El agente (via tool calling); el humano aprueba publicacion (AG-03). |

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
(local PNG)      (API remota)
  |              |
  v              v
Archivos PNG    URL de descarga
  |              |
  +------+-------+
         |
         v
  AG-03 (aprobacion CEO)
         |
         v
  Publicacion en IG
```

1. **Jarvis / mkt-content** genera el guion con `carousel-ops`.
2. El operador elige herramienta:
   - **open-carrusel** para control total local (HTML custom).
   - **Canva** para usar templates de marca y edicion visual rapida.
3. El resultado visual pasa por **AG-03** antes de publicar.

---

## Lo que se desecha definitivamente

- App open-carrusel **dentro** del monorepo (Next.js, Puppeteer, Chromium, Claude CLI).
- Submodulo o fork en `clawvis-openclaw/`.
- Job de CI que levante esa stack.

## Resumen

| Pregunta | Respuesta |
|----------|-----------|
| Jarvis necesita open-carrusel instalado? | **No** — opcional en `~/tools/`. |
| Jarvis necesita Canva? | **Opcional** — via plugin Composio si se quiere diseno desde chat. |
| Que necesita el ecosistema como minimo? | Skill `carousel-ops` + gobierno (dossier, Trello, AG-03). |
| Donde estan los PNG? | Donde el humano los exporte (open-carrusel local o Canva export). |
