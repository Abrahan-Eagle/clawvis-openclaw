# Trello + OpenClaw (skill REST)

**Ámbito:** usar la API REST de Trello desde el agente OpenClaw mediante la skill **trello** (ejemplos con `curl` + `jq`), sin webhooks ni canal propio.

**Última revisión:** abril 2026.

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Skill | Incluida en el paquete OpenClaw (`skills/trello/SKILL.md`) y en el workspace Jarvis: `jarvis-ecosystem/agents/jarvis/skills/trello/SKILL.md`. |
| Binario | `jq` en el `PATH` del proceso del gateway (p. ej. `/usr/bin/jq`). |
| Variables | `TRELLO_API_KEY` y `TRELLO_TOKEN` visibles para el gateway. |
| Herramienta | El perfil `messaging` **no** incluye shell; añade `exec` vía `tools.alsoAllow` en `openclaw.json` (junto a otros como `lobster` si aplica). **No** mezclar `allow` y `alsoAllow` en el mismo bloque. |

---

## Credenciales

La API REST exige una **pareja válida** `key` + `token` en la query. El token queda **ligado a la clave** con la que se generó: no mezcles una clave de un sitio con el token de otro.

### Secreto del Power-Up no es el token

En la administración de un Power-Up verás **Clave de API**, **Secreto** y a veces **Orígenes permitidos**. Para los `curl` de la skill solo se usan **`TRELLO_API_KEY`** (la clave visible) y **`TRELLO_TOKEN`** (generado con el enlace de token de **esa misma** pantalla o de `app-key`). El **Secreto** sirve para otros flujos (OAuth/servidor); **no** lo pongas en `TRELLO_TOKEN`.

### Camino A: Power-Up (p. ej. Jarvis)

1. Abre la integración en Trello: `trello.com/power-ups/<id>/edit/api-key` (o el menú del Power-Up → Clave de API).
2. Copia la **Clave de API** del Power-Up (32 caracteres).
3. Usa el enlace de **token manual** que describe la página (pruebas locales / autorización) y copia el **token** resultante.
4. Esa clave y ese token son la pareja para `~/.openclaw/.env`.

### Camino B: clave global de desarrollador

1. [trello.com/app-key](https://trello.com/app-key) → **Developer API Key**.
2. Enlace **Token** en la **misma** página → autoriza y copia el token.

No mezcles Camino A y B.

Definir en `~/.openclaw/.env` (el servicio user suele cargarlo con `EnvironmentFile=-%h/.openclaw/.env`):

```bash
TRELLO_API_KEY=tu_clave
TRELLO_TOKEN=tu_token
```

Sin comillas innecesarias ni espacios al final de línea.

Reiniciar el gateway tras cambios: `systemctl --user restart openclaw-gateway`.

---

## Verificación rápida

Primero comprueba código HTTP y cuerpo (si falla, `jq` mostrará error de parseo porque la API devuelve texto plano, p. ej. `invalid key`):

```bash
set -a && source ~/.openclaw/.env && set +a
curl -sS -w "\nHTTP:%{http_code}\n" "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

Con **HTTP 200** y JSON (array), entonces:

```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

- **HTTP 200** y JSON de tableros: OK.
- **401** y cuerpo `invalid key`: la pareja key+token no es válida (origen mezclado, token generado con otra clave, o Secreto usado como token). Vuelve a generar **clave y token en la misma página** (Camino A o B) y actualiza `.env`.

### Seguridad

Si expusiste clave o Secreto en capturas o chats, rota credenciales en Trello y actualiza `.env`.

---

## Uso con el agente

Pedir al agente que aplique la skill **trello** (listar tableros, listas, tarjetas, comentarios, etc.) según los ejemplos del `SKILL.md`. El modelo ejecutará `curl`/`jq` vía la herramienta **exec**.

### Workspace: `jarvis-ecosystem` en repo vs en `$HOME`

OpenClaw suele apuntar el agente `jarvis` a `~/jarvis-ecosystem/agents/jarvis`, mientras el clon del repo puede vivir en otra ruta (p. ej. `/var/www/clawvis-openclaw/jarvis-ecosystem`). Si solo editas el repo, el agente puede **no ver** `skills/trello/` hasta que sincronices.

**Opción recomendada:** enlace simbólico a la skill canónica del repo (ajusta la ruta si tu clon es distinto):

```bash
mkdir -p ~/jarvis-ecosystem/agents/jarvis/skills
ln -sfn /var/www/clawvis-openclaw/jarvis-ecosystem/agents/jarvis/skills/trello \
  ~/jarvis-ecosystem/agents/jarvis/skills/trello
```

Alternativa: `rsync -a --delete` desde el repo al árbol en `$HOME` (más pesado; revisa antes de `--delete`).

**Agente `main`** (`workspace` = `~/.openclaw/workspace`): por defecto no incluye skills; puedes enlazar la misma carpeta:

```bash
mkdir -p ~/.openclaw/workspace/skills
ln -sfn /var/www/clawvis-openclaw/jarvis-ecosystem/agents/jarvis/skills/trello \
  ~/.openclaw/workspace/skills/trello
```

### `maxTokens` del agente `jarvis`

Para salidas largas (JSON de tableros/listas), conviene un `maxTokens` alto en `~/.openclaw/openclaw.json` para el agente `jarvis` (p. ej. `4096`), o usar el agente `jarvis-deep` en OpenClaw para tareas pesadas.

---

## Fuera de alcance aquí

- **Webhooks** Trello → OpenClaw (eventos entrantes): requiere endpoint HTTP dedicado y validación.
- **MCP** solo-Trello: alternativa si se quiere evitar `exec`; no es necesaria para el flujo con skill.
