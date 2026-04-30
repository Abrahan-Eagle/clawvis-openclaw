# JMC Chat — buzón `jmc-inbox` (contrato + flujo Jarvis)

Fuente de verdad en disco bajo `state/jmc-inbox/` (o `JMC_CHAT_INBOX_DIR`). Jarvis **no** es un daemon: las respuestas aparecen cuando alguien escribe los ficheros de reply.

## Estructura de directorios

```
state/jmc-inbox/
  conv-YYYY-MM-DD-xxxxxx/
    meta.json
    msg-YYYY-MM-DD-HHMMSS-xxxxxx.json
    msg-YYYY-MM-DD-HHMMSS-xxxxxx.attachments/
      archivo.pdf
    msg-YYYY-MM-DD-HHMMSS-xxxxxx.reply.json
  _archived/
    conv-…/
```

- `conv_id`: `conv-<fecha-UTC>-<6 hex minúsculas>`.
- `msg_id`: `msg-<fecha-UTC>-<HHMMSS>-<6 hex minúsculas>`.

## `meta.json`

```json
{
  "conv_id": "conv-2026-04-29-a1b2c3",
  "title": "Chat",
  "created_at": "2026-04-29T12:00:00Z",
  "archived": false
}
```

## `msg-*.json` (mensaje CEO)

| Campo | Tipo | Notas |
|--------|------|--------|
| `id` | string | Igual al stem del fichero (`msg-…`). |
| `role` | string | Siempre `ceo` en mensajes creados por JMC. |
| `text` | string | Cuerpo (acotado en servidor). |
| `ts` | string | ISO-8601 UTC con sufijo `Z`. |
| `attachments` | array | Metadatos `{ stored_name, original_name, size_bytes, content_type }`. |
| `mirror_channel` | string? | `telegram` o `discord` si el usuario pidió espejo. |
| `mirror_result` | object? | Resultado de `openclaw message send` (`ok`, `warning`, `error`, etc.). |

## `msg-*.reply.json` (respuesta Jarvis)

Mismo esquema general que el mensaje, con:

- `role`: `jarvis`
- `text`: respuesta visible en JMC
- `ts`: momento de la respuesta
- `attachments`: opcional (si Jarvis deja ficheros en el directorio `.attachments` del mismo prefijo; la UI v1 prioriza texto + adjuntos del mensaje CEO)

Ejemplo mínimo:

```json
{
  "id": "msg-2026-04-29-143015-d4e5f6",
  "role": "jarvis",
  "text": "Listo: revisé el PDF y dejé el resumen en skills/…",
  "ts": "2026-04-29T14:35:00Z",
  "attachments": []
}
```

## Activity log

Tras escribir el mensaje, el adapter invoca el mismo mecanismo que otros eventos (`activity-log event`):

- `kind`: `jmc_inbox`
- `agent`: `ceo`
- `task`: `jmc-chat-<conv_id>`
- `payload`: `{ "conv_id", "msg_id", "attachment_count", "mirror"? }`

Para una respuesta escrita a mano por Jarvis, se recomienda añadir una línea coherente (mismo `task` o `jarvis` + nota) con `kind: jmc_reply` si tu instalación lo estandariza; v1 del adapter solo emite `jmc_inbox` en el POST del CEO.

## Workflow sugerido (Jarvis en Cursor/CLI)

1. Listar conversaciones: leer directorios bajo `jmc-inbox/` que casen el patrón `conv-*`.
2. Abrir `msg-*.json` sin `.reply.json` pendientes de respuesta (o donde falte reply).
3. Leer adjuntos en `msg-….attachments/`.
4. Escribir `msg-….reply.json` con el JSON de respuesta.
5. (Opcional) Registrar en `state/activity-log.jsonl` vía `skills/global/activity-log/bin/activity-log` o equivalente.

## API (resumen)

| Método | Ruta |
|--------|------|
| GET | `/v1/chat/options` |
| GET / POST | `/v1/chat/conversations` |
| GET | `/v1/chat/conversations/{conv_id}` |
| POST | `/v1/chat/conversations/{conv_id}/messages` (multipart: `text`, `files[]`, `mirror_channel`) |
| GET | `/v1/chat/conversations/{conv_id}/messages/{msg_id}/attachments/{filename}` |
| POST | `/v1/chat/conversations/{conv_id}/archive` |

Todas requieren `Authorization: Bearer <JMC_BEARER_TOKEN>`.

## Adjuntos y seguridad

- Tope por fichero: `JMC_CHAT_MAX_FILE_BYTES` (mínimo efectivo 1024 bytes en código).
- Cantidad: `JMC_CHAT_MAX_FILES_PER_MSG` (máx. 10).
- Extensiones bloqueadas por defecto: `.sh`, `.bat`, `.cmd`, `.exe`, `.dll`, `.so`, `.ps1`, etc.; hace falta **extensión** explícita en el nombre.
- Nombres con `/`, `\` o subcadena `..` se rechazan en la ruta de descarga.

## Espejo OpenClaw

Solo texto (y nombres de adjuntos en una línea de contexto) se envían al canal. Requiere binario resuelto por `JMC_OPENCLAW_BIN` y `JMC_CHAT_MIRROR_ENABLED=1`.
