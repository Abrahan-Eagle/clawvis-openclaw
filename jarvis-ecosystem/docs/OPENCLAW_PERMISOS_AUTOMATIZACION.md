# Permisos para que OpenClaw / Jarvis automatice (Trello, herramientas, Discord)

**Objetivo:** que el gateway pueda **crear y editar** en Trello vía API, ejecutar `curl`/`jq` (skill Trello), y que sepas qué falta para **Discord** (bot con permisos en el servidor).

**No** se versionan secretos: todo vive en `~/.openclaw/.env` y `~/.openclaw/openclaw.json` en tu máquina.

---

## 1. OpenClaw — herramienta `exec` (obligatoria para Trello vía shell)

La skill Trello usa **`curl`**; el agente necesita la herramienta **`exec`** permitida.

1. Abre **`~/.openclaw/openclaw.json`** (el que usa el gateway, no solo la copia del repo).
2. En **`tools`**, asegura algo equivalente a:

```json
"tools": {
  "alsoAllow": [
    "exec",
    "lobster"
  ]
}
```

- **No** dupliques claves `allow` y `alsoAllow` en el mismo bloque (comportamiento indefinido).
3. Reinicia el gateway: `systemctl --user restart openclaw-gateway`.

Referencia: [../../docs/TRELLO_OPENCLAW.md](../../docs/TRELLO_OPENCLAW.md).

---

## 2. Trello — token con permiso de **escritura** (crear tableros, listas, tarjetas)

Si la API responde **`401`** / **`unauthorized permission requested`** al hacer `POST` (crear tablero o lista), el **`TRELLO_TOKEN` actual no tiene alcance de escritura** o no empareja la clave.

### Pasos recomendados

1. Abre [https://trello.com/app-key](https://trello.com/app-key) (sesión Trello iniciada).
2. Copia la **API key** (`TRELLO_API_KEY`). Debe ser la **misma** que usarás en `.env`.
3. Pulsa el enlace **Token** (o “manually generate a Token”) en **esa misma página**.
4. En la pantalla de autorización, **acepta todos los permisos** que Trello ofrezca (lectura y escritura sobre tableros, etc.).
5. Copia el **token** largo → `TRELLO_TOKEN` en `~/.openclaw/.env`:

```bash
TRELLO_API_KEY=tu_clave_32_chars
TRELLO_TOKEN=tu_token_largo
```

6. **Revoca** tokens viejos si sospechas mezcla Camino A (Power-Up) vs Camino B (app-key): [Cuenta Trello → Aplicaciones](https://trello.com/account) / ajustes de desarrollador.
7. Reinicia el gateway para cargar el `.env`.

### Verificación de escritura (desde terminal)

```bash
set -a && source ~/.openclaw/.env && set +a
curl -sS -X POST "https://api.trello.com/1/boards" \
  -d "name=TEST-Permisos-Jarvis-BORRAR" \
  -d "defaultLists=false" \
  -d "key=$TRELLO_API_KEY" \
  -d "token=$TRELLO_TOKEN" | jq '{id,name,url}'
```

- Si ves **`id`** y **`name`**: escritura OK. Borra el tablero de prueba en la web Trello o por API.
- Si ves **`unauthorized permission requested`**: repite generación del token en `app-key` o revisa que no estés mezclando clave de un Power-Up con token de otra fuente.

### Automatizar tableros del holding

Con escritura OK:

```bash
/var/www/clawvis-openclaw/jarvis-ecosystem/scripts/trello-bootstrap-boards.sh
```

Luego pega los **Board ID** en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md).

---

## 3. Discord — qué puede y qué no puede OpenClaw “solo”

- **OpenClaw** en tu setup ya **envía/recibe** en canales configurados en `openclaw.json` (bot existente).
- **Crear categorías/canales** vía API requiere un **bot de Discord** con token en `.env` y permisos en el servidor: **Gestionar canales**, **Gestionar roles** (según lo que quieras automatizar).

### Si quieres que el bot cree el esqueleto de canales

1. [Portal de desarrolladores Discord](https://discord.com/developers/applications) → tu aplicación → **Bot** → token (solo en `.env`, nunca en Git).
2. Activa **Privileged Gateway Intents** solo si tu librería los necesita (mensajes: suele bastar **Message Content Intent** si aplica).
3. **URL de invitación** con permisos calculados, por ejemplo `Manage Channels` (0x10), `View Channels`, `Send Messages`: genera enlace OAuth2 con `bot` + `applications.commands` si usas comandos.
4. Invita el bot al servidor **Jarvis** con ese enlace.
5. Sube el bot en la jerarquía por debajo del dueño; asigna rol con permisos en categoría **Dirección / Operación / Clientes**.

Documentación de nombres de canales: [BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) §2.

*(Automatizar creación por script Python/Node queda fuera de este repo salvo que añadas tarea explícita.)*

---

## 4. Telegram

Ya enlazado por OpenClaw; permisos típicos: bot con permisos de envío en los chats configurados en `bindings`. Sin cambios extra para “hacer todo” salvo nuevos canales/grupos.

---

## 5. Checklist rápido

| Comprobación | Dónde |
|--------------|--------|
| `exec` en `alsoAllow` | `~/.openclaw/openclaw.json` |
| `TRELLO_*` con token de escritura | `~/.openclaw/.env` + reinicio gateway |
| POST tablero de prueba OK | Comando §2 |
| Script bootstrap Trello | `jarvis-ecosystem/scripts/trello-bootstrap-boards.sh` |
| Discord canales por bot | Portal Discord + permisos servidor |

---

## Historial

- **2026-04-04:** Documento añadido para alinear permisos Trello/OpenClaw y guía Discord bot.
