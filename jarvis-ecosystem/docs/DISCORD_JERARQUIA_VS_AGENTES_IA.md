# Discord: jerarquía humana (CEO / supervisor / equipo) vs agentes OpenClaw

**Problema que resuelve:** En Discord solo ves **un bot** (p. ej. `Bot_Jarvis`) y no “varios empleados IA” con cuentas distintas. Eso **no contradice** el modelo de gobierno de [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md): la jerarquía CEO → supervisor → equipo es **organizacional y de trazabilidad** (Trello, canales, roles humanos). Los **agentes OpenClaw** (`jarvis`, `mkt-social`, etc.) son **otra capa**: qué modelo y qué `workspace` atiende cada conversación.

**Última revisión:** abril 2026.

---

## 1. Qué ves en Discord (una sola cara de bot)

| Hecho | Implicación |
|-------|-------------|
| Una **aplicación** de Discord = un **bot** con un nombre y avatar | No aparecen “3 IA” como 3 usuarios distintos salvo que registres **varias aplicaciones** de Discord (no recomendado salvo necesidad fuerte). |
| OpenClaw elige **qué agente** (`agentId`) responde según **`bindings`** en `~/.openclaw/openclaw.json` | Si todo el servidor cae en `agentId: "jarvis"`, **siempre** responde el agente Jarvis (mismo bot). |
| El **workspace** del agente (p. ej. `agents/jarvis` vs `agents/marketing`) define **contexto de archivos** (AGENTS.md, skills), no el nombre del bot en Discord | Para que “suene a marketing” hace falta **routing** a `mkt-social` o **instrucciones** en el prompt. |

---

## 2. Tu configuración típica (todo Discord → Jarvis)

Si tienes algo equivalente a:

```json
{
  "agentId": "jarvis",
  "match": { "channel": "discord", "guildId": "*" }
}
```

entonces **cualquier canal** del servidor usa el agente **jarvis**. Eso es coherente con “Jarvis orquesta”, pero **no** separa automáticamente el trabajo al agente de marketing: **no verás otro bot**, solo el mismo respondiendo con el contexto de Jarvis.

---

## 3. Cómo alinear gobierno documentado con la técnica (tres niveles)

### Nivel A — Gobierno humano + trazabilidad (sin cambiar agentes)

- **Roles Discord** (CEO, Supervisor, Equipo) y **canales** según [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md).
- **Trello** con `dossier_id` y convención de tableros ([CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md)).
- La IA puede ser **una sola voz** (Jarvis) que **documenta** en el mensaje quién sería el responsable humano de cada pieza.

Aquí **no** “ves” agentes distintos en Discord; ves **proceso** y **canales**.

### Nivel B — Un solo agente (`jarvis`), handoff **simulado** en el texto

Pides explícitamente secciones firmadas, por ejemplo:

- `Jarvis (orquestación): …`
- `CEO Marketing (síntesis): …`
- `Supervisor (estrategia / Trello): …`
- `Equipo contenido (borrador IG/FB): …`

Es **un** modelo generando **varias etiquetas lógicas**; sirve para demos y para no tocar `openclaw.json`.

### Nivel C — Routing OpenClaw: canales distintos → `agentId` distinto

OpenClaw resuelve rutas por `bindings`; el **primer match gana** (ver documentación upstream de OpenClaw: `match.peer`, `match.guildId`, etc.).

Puedes añadir **antes** del comodín `guildId: "*"` una entrada **más específica** que envíe, por ejemplo, `#social` o `#marketing` al agente `mkt-social` (workspace de marketing).

Ejemplo **esquemático** (debes sustituir `GUILD_ID` y `CHANNEL_ID` reales; activar modo desarrollador en Discord → copiar ID):

```json
{
  "agentId": "mkt-social",
  "match": {
    "channel": "discord",
    "guildId": "GUILD_ID",
    "peer": { "kind": "channel", "id": "CHANNEL_ID_DEL_CANAL_MARKETING" }
  }
},
{
  "agentId": "jarvis",
  "match": { "channel": "discord", "guildId": "*" }
}
```

- El canal con ID concreto → **mkt-social** (lee `agents/marketing`, skills de redes).
- El resto del Discord → **jarvis** (orquestación).

Tras editar: reiniciar el gateway (`systemctl --user restart openclaw-gateway` o equivalente).

**Nota:** Si no creas canales dedicados o no rellenas IDs, seguirás viendo solo el comportamiento “todo Jarvis”.

---

## 4. Cómo saber “quién trabajó” en la práctica

| Pregunta | Respuesta |
|----------|-----------|
| ¿El mensaje lo escribió “marketing” o “Jarvis”? | Mira **`agentId`** de la sesión en logs de OpenClaw o la configuración de **bindings** del canal. Si no hay routing, fue **Jarvis** (aunque el texto hable de marketing). |
| ¿Los CEO/supervisor “existen” como IA? | En el modelo actual son **roles humanos** o **simulación en prompt**; no hay obligación de tener un `agentId` por rol. |
| ¿La captura con `HTTP 401: User not found`? | Suele ser un aviso de API Discord/OpenClaw al resolver un usuario; **no** indica por sí solo qué agente generó el texto. Revisa logs del gateway si persiste. |

---

## 5. Enlaces

- [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md) — jerarquía y principios.
- [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) — bindings y rutas de dossiers.
- Referencia OpenClaw (instalación local): `docs/gateway/configuration-reference.md` → sección **Binding match fields**.
