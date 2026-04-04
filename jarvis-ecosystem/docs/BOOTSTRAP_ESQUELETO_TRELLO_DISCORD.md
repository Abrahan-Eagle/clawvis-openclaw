# Esqueleto operativo — Trello + Discord (primera pasada)

**Objetivo:** alinear tu tablero Trello y el servidor Discord **Jarvis** con [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md) y [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md).

**Nota API Trello:** si `scripts/trello-bootstrap-boards.sh` devuelve `401` / `unauthorized permission requested`, el token en `~/.openclaw/.env` **no tiene permiso de escritura**. Genera un token nuevo en [trello.com/app-key](https://trello.com/app-key) (misma clave) con permisos de **lectura y escritura**, actualiza `TRELLO_TOKEN`, reinicia el gateway y vuelve a ejecutar el script — o crea tableros/listas **a mano** siguiendo la sección 1.

---

## 1. Trello — tableros por empresa (manual si la API falla)

### Opción A — Dos tableros (recomendado)

1. **Crear tablero** `Empresa-marketing - Operaciones` (o `Empresa-marketing — Operaciones`).
2. **Crear tablero** `Empresa-ventas - Operaciones`.
3. En **cada** tablero, borra listas por defecto si no las quieres y crea **en este orden** (izquierda → derecha):

| Orden | Nombre de lista |
|-------|-----------------|
| 1 | Backlog |
| 2 | En curso |
| 3 | Revisión supervisor |
| 4 | Bloqueado |
| 5 | Hecho |

4. (Opcional) Etiqueta global de color para `dossier_id`: texto tipo `dossier:cli-XXXX` según [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md).

5. Copia la **URL** de cada tablero; el ID corto está en la URL (`/b/XXXXXX/...`) o en **Menú del tablero → Más → Copiar enlace**.

6. Pega **Board ID** (id largo de 24 hex) en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md) tabla Trello (o pide a Jarvis que lo actualice tras leer la API `members/me/boards`).

### Opción B — Un solo tablero (transición)

Si prefieres seguir en **Mi tablero de Trello** un tiempo: añade las **cinco listas** anteriores y usa prefijo `[marketing]` / `[ventas]` en títulos hasta separar tableros.

---

## 2. Discord — servidor **Jarvis** (una pasada en la app)

Crea **categorías** y **canales de texto** (ajusta permisos: CEO/supervisor de ejemplo son roles futuros; por ahora solo tú y el bot).

| Categoría | Canales de texto | Notas |
|-----------|------------------|--------|
| **Dirección** | `#ceo`, `#supervisor-interno` | `#supervisor-interno` puede ser privado (solo tu rol + CEO cuando exista). |
| **Operación** | `#daily`, `#bloqueos`, `#trello-sync` | Resúmenes de tablero y bloqueos. |
| **Clientes** | `#cliente-cli-20260404-cliente-tests-redes` | Cliente de prueba; en descripción del canal: enlace al dossier en el repo y al tablero Trello marketing. |

**Voz (opcional):** categoría **Voz** con `Sala equipo`.

**Regla:** el hilo **superusuario ↔ Jarvis** (Telegram/OpenClaw) **no** es este servidor para clientes; no invites clientes a canales internos.

---

## 3. Después de crear

1. Marca checkboxes en [VERIFICACION_DISCORD_FASE4.md](VERIFICACION_DISCORD_FASE4.md).
2. Actualiza **MEMORY.md** (tabla Trello y nota Discord).
3. Si regeneraste token Trello con escritura, prueba [../scripts/trello-bootstrap-boards.sh](../scripts/trello-bootstrap-boards.sh).

---

## Historial

- **2026-04-04:** Guía añadida; API Trello en este entorno respondió 401 en escritura — bootstrap manual o token con scope de escritura.
