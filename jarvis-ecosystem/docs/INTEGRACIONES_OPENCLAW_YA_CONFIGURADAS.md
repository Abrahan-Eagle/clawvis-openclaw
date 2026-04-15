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

## Canva (vía Composio + OpenClaw)

**No** es una integración nativa “Canva ↔ OpenClaw” sin intermediario: el camino oficial documentado es **Composio** (MCP + toolkit Canva). Guía upstream: [How to integrate Canva MCP with OpenClaw](https://composio.dev/toolkits/canva/framework/openclaw) (Composio). En el ecosistema Jarvis: [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) **§2.10**, [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md) (límites API, brand templates, Telegram/`messaging`).

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
7. **Verificación:** `openclaw composio doctor` (debe listar herramientas Composio y estado healthy).

**CLI Composio (opcional):** `curl -fsSL https://composio.dev/install | bash` y `composio login ...` — útil para pruebas desde terminal; el agente Jarvis usa el **plugin OpenClaw**, no sustituye el paso del consumer key en `openclaw.json`.

**Nota:** cuenta **Canva gratis** suele no exponer **brand templates** a la API (`items: []`); autofill avanzado suele requerir flujos de equipo/Enterprise — ver [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md).

---

## Historial

- **2026-04-15:** Sección **Canva (vía Composio + OpenClaw)** — enlace oficial Composio, checklist (`consumerKey`, plugin, `plugins.allow`, `tools.alsoAllow` `COMPOSIO_*`, OAuth Canva, `composio doctor`), nota cuenta gratis y [CAROUSEL_IG_JARVIS.md](CAROUSEL_IG_JARVIS.md).
- **2026-04-07:** Enlace a [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) (inventario forense comunidad OpenClaw). Ampliación: ancla `#marketing-openclaw-forense`, §2 marketing + Claude y mapeo `mkt-*` en el párrafo del catálogo.
- **2026-04-04:** [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md) — norma obligatoria de trabajo en Trello para agentes y subagentes.
- **2026-04-04:** Enlace a [DISCORD_JERARQUIA_VS_AGENTES_IA.md](DISCORD_JERARQUIA_VS_AGENTES_IA.md) (un bot, bindings por canal, handoff simulado).
- **2026-04-04:** Sección **Client dossiers (rutas en disco)** — `~/Documents/client-dossiers`, symlinks en repo y en `~/jarvis-ecosystem`, ruta relativa desde `agents/jarvis`.
- **2026-04-04:** Documento añadido para alinear el ecosistema Jarvis con el estado real de integraciones OpenClaw.
- **2026-04-04:** Enlace a [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md) (token Trello escritura, `exec`, Discord).
