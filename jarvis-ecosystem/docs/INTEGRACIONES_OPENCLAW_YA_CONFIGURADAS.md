# Integraciones ya configuradas en OpenClaw

**Estado:** Trello, Discord y Telegram **ya están enlazados al gateway OpenClaw** (`~/.openclaw/openclaw.json`, variables en `~/.openclaw/.env` según cada integración). Jarvis **no** debe asumir que hay que “instalar desde cero” esas conexiones; la fuente operativa es la configuración del gateway.

---

## Qué implica para el agente

1. **No** proponer reconfigurar credenciales salvo que el superusuario lo pida.
2. Para **Trello** (API / skill): credenciales y uso con `curl`/`jq` — [../../docs/TRELLO_OPENCLAW.md](../../docs/TRELLO_OPENCLAW.md).
3. **Discord y Telegram:** canales y bindings los define OpenClaw; las plantillas de organización ([PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md)) son referencia de **roles y nombres**, no un checklist de integración técnica pendiente.
4. **Un solo bot en Discord vs varios agentes OpenClaw** (CEO/supervisor/equipo “visibles”): [DISCORD_JERARQUIA_VS_AGENTES_IA.md](DISCORD_JERARQUIA_VS_AGENTES_IA.md).
5. Convención de negocio tableros/clientes: [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md).
6. **Flujo Trello obligatorio** para Jarvis, agentes y subagentes: [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md).

---

## Client dossiers (rutas en disco)

- **Ubicación visible (Documentos):** `~/Documents/client-dossiers` — un JSON por cliente (`cli-*.json`) y briefs opcionales (`BRIEF_*.md`).
- **Repo:** `jarvis-ecosystem/client-dossiers` es un **enlace simbólico** a esa carpeta (sin duplicar archivos en el clon).
- **OpenClaw (home):** `~/jarvis-ecosystem/client-dossiers` enlaza al mismo destino para que el gateway y el explorador vean los mismos ficheros.
- **Desde el workspace del agente** (`~/jarvis-ecosystem/agents/jarvis`): ruta relativa `../../client-dossiers/`.
- Resumen en memoria del agente: [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md) (copia en home usada por OpenClaw).

---

## Seguridad

- **No** commitear tokens, `openclaw.json` completo con secretos, ni contenido de `.env`.
- Tablas de referencia en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md) pueden listar IDs públicos de tablero Trello si el superusuario lo desea; no pegar API keys.

## Permisos para automatizar (Trello escritura, exec, Discord bot)

Checklist y comandos de verificación: [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md).

**Catálogo comunidad (skills/repos externos, no confundir con integraciones ya hechas):** [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md#marketing-openclaw-forense) — inventario forense (incluye **§2** marketing + Claude, mapeo `mkt-*`, criterios de adopción); el ancla lleva al bloque principal; el documento completo lista también núcleo, skills y patrones.

---

## Canva (tres vias configuradas)

Tres caminos para usar Canva desde el ecosistema Jarvis, de mas inmediato a mas potente:

| Via | Estado | Descripcion |
|-----|--------|-------------|
| **B. Composio** | Activa (OAuth OK) | Plugin `@composio/openclaw-plugin` + `consumerKey` + 7 herramientas `COMPOSIO_*` en `alsoAllow`. Tool calling desde chat. |
| **C. Canva Connect directo** | Skill instalado | Skill `canva` de ClawHub (`openclaw skills install canva`). OAuth directo, scripts CLI (`canva.sh`), sin intermediario. |
| **D. MCP oficial Canva** | Pendiente registro | Servidor remoto `https://mcp.canva.com/mcp`. Antes de acceso: completar [Canva MCP Connector Intake Form](https://docs.google.com/forms/d/e/1FAIpQLSdtsKA9LSmY-JEf_nF5QYBdjxfnXbgqvlKzd8obKGSPSK_eOA/viewform) (OAuth Redirect URI obligatorio; volumen estimado, caso de uso, etc.). Cliente tipico: `npx -y mcp-remote@latest https://mcp.canva.com/mcp` — ver [canva.dev/docs/mcp](https://www.canva.dev/docs/mcp/). |

Guia upstream Composio: [How to integrate Canva MCP with OpenClaw](https://composio.dev/toolkits/canva/framework/openclaw). **Documentacion oficial Canva MCP:** [Overview](https://www.canva.dev/docs/mcp/) · [Tools y rate limits](https://www.canva.dev/docs/mcp/tools/) · [Design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/) · [Troubleshooting](https://www.canva.dev/docs/mcp/troubleshooting/) · [Usage policy](https://www.canva.dev/docs/mcp/usage-policy/) · [Prohibited use](https://www.canva.dev/docs/mcp/prohibited-use/). En el ecosistema Jarvis: [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) **§2.10**, [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) (tabla de enlaces MCP, limites API, brand templates, Telegram/`messaging`).

### Checklist de configuración (host donde corre el gateway)

1. **Cuenta Composio** — [dashboard.composio.dev](https://dashboard.composio.dev); crear cliente **OpenClaw** y copiar **consumer key** (`ck_...`) desde la pestaña del cliente OpenClaw (Plugin / API Key).
2. **Instalar plugin** (si no está):
   ```bash
   openclaw plugins install --dangerously-force-unsafe-install @composio/openclaw-plugin
   ```
   (OpenClaw puede bloquear la instalación sin este flag por patrones “peligrosos” en el paquete; es decisión consciente del operador.)
3. **Configurar la clave y habilitar el plugin** en `~/.openclaw/openclaw.json`:
   - `plugins.entries.composio.enabled`: `true`
   - `plugins.entries.composio.config.consumerKey`: `"ck_..."` (no commitear)
   - `plugins.allow`: incluir `"composio"`
4. **Perfil `tools.profile: "messaging"`** (Telegram, etc.): añadir en `tools.alsoAllow` las siete herramientas genéricas `COMPOSIO_*` además de `lobster` / `browser`, para que el agente pueda invocar Composio en canales de mensajería — ver [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) (snapshot en [config/openclaw-home/openclaw.json](../../config/openclaw-home/openclaw.json)).
5. **Reiniciar gateway:** `openclaw gateway restart` (o `systemctl --user restart openclaw-gateway` si aplica).
6. **Conectar Canva** en Composio: [Connect Apps](https://dashboard.composio.dev) → autorizar OAuth de Canva con la cuenta deseada.
7. **Verificación:** `openclaw composio doctor` (debe listar herramientas Composio y estado **healthy**). Si al final aparece `MCP client connection failed: fetch failed`, **no** reinstalar OAuth por defecto: el criterio de éxito es que el **gateway** pueda usar `COMPOSIO_*` en chat — ver [TROUBLESHOOTING_COMPOSIO_OPENCLAW.md](TROUBLESHOOTING_COMPOSIO_OPENCLAW.md). Script opcional: [../scripts/composio-diagnose.sh](../scripts/composio-diagnose.sh).

**CLI Composio (opcional):** `curl -fsSL https://composio.dev/install | bash` y `composio login ...` — útil para pruebas desde terminal; el agente Jarvis usa el **plugin OpenClaw**, no sustituye el paso del consumer key en `openclaw.json`.

**Nota:** cuenta **Canva gratis** suele no exponer **brand templates** a la API (`items: []`); autofill avanzado suele requerir flujos de equipo/Enterprise — ver [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md).

---

## Historial

- **2026-04-16:** [TROUBLESHOOTING_COMPOSIO_OPENCLAW.md](TROUBLESHOOTING_COMPOSIO_OPENCLAW.md) — `fetch failed` tras `composio doctor`, criterio de éxito (runtime gateway), proxy/`NODE_USE_ENV_PROXY`, Inspector, escalación upstream; script [../scripts/composio-diagnose.sh](../scripts/composio-diagnose.sh).
- **2026-04-16:** Enlaces oficiales Canva MCP en documentacion: [Overview](https://www.canva.dev/docs/mcp/), [Tools](https://www.canva.dev/docs/mcp/tools/), [Design edit handoff](https://www.canva.dev/docs/mcp/workflows/design-edit/), [Troubleshooting](https://www.canva.dev/docs/mcp/troubleshooting/), [Usage policy](https://www.canva.dev/docs/mcp/usage-policy/), [Prohibited use](https://www.canva.dev/docs/mcp/prohibited-use/) — tabla en [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md).
- **2026-04-16:** URL canonica del intake MCP: [Canva MCP Connector Intake Form](https://docs.google.com/forms/d/e/1FAIpQLSdtsKA9LSmY-JEf_nF5QYBdjxfnXbgqvlKzd8obKGSPSK_eOA/viewform) (`/d/e/1FAIpQLSdtsKA9...`); OAuth Redirect URI obligatorio; contenido alineado al texto publico del formulario.
- **2026-04-16:** Via **D (MCP oficial)** — alineacion con *Canva MCP Connector Intake Form*: descripcion del conector SDK+MCP y nota de verificar enlace al repo en el formulario; enlaces en [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) y [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md).
- **2026-04-15:** Seccion **Canva (tres vias configuradas)** — tabla comparativa Composio / Canva Connect directo / MCP oficial, skill `canva` de ClawHub, formulario de intake MCP.
- **2026-04-15:** Seccion **Canva (via Composio + OpenClaw)** (version inicial) — enlace oficial Composio, checklist (`consumerKey`, plugin, `plugins.allow`, `tools.alsoAllow` `COMPOSIO_*`, OAuth Canva, `composio doctor`), nota cuenta gratis y [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md).
- **2026-04-07:** Enlace a [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) (inventario forense comunidad OpenClaw). Ampliación: ancla `#marketing-openclaw-forense`, §2 marketing + Claude y mapeo `mkt-*` en el párrafo del catálogo.
- **2026-04-04:** [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md) — norma obligatoria de trabajo en Trello para agentes y subagentes.
- **2026-04-04:** Enlace a [DISCORD_JERARQUIA_VS_AGENTES_IA.md](DISCORD_JERARQUIA_VS_AGENTES_IA.md) (un bot, bindings por canal, handoff simulado).
- **2026-04-04:** Sección **Client dossiers (rutas en disco)** — `~/Documents/client-dossiers`, symlinks en repo y en `~/jarvis-ecosystem`, ruta relativa desde `agents/jarvis`.
- **2026-04-04:** Documento añadido para alinear el ecosistema Jarvis con el estado real de integraciones OpenClaw.
- **2026-04-04:** Enlace a [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md) (token Trello escritura, `exec`, Discord).
