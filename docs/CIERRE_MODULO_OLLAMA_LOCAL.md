# Cierre de módulo — Ollama como fallback local (OpenClaw / Jarvis)

**Estado:** cerrado (operativo en host de referencia, abril 2026).  
**Alcance:** instalar y operar **Ollama en la misma máquina** que el Gateway OpenClaw, con modelos acotados a la VRAM/RAM disponible, y enlazarlos en `openclaw.json` para que Jarvis responda aunque fallen claves o límites de proveedores cloud.

---

## Objetivo cumplido

- Respuestas del agente vía **Ollama** en `127.0.0.1:11434`.
- **Servicio persistente** (systemd usuario), no dependencia manual de terminal.
- **Dos niveles de coste/latencia:** agente ligero (`jarvis-auto-light`) con modelo mini conversacional; agente principal (`jarvis`) con modelo un poco mayor.
- **Canales** (Telegram/Discord) validados con `openclaw channels status --probe` en estado **works** tras la integración.

---

## Hardware de referencia (máquina donde se cerró)

| Recurso | Valor orientativo |
|--------|-------------------|
| CPU | AMD Ryzen 5 7535HS (12 hilos) |
| RAM | ~19 GiB |
| GPU | NVIDIA GeForce RTX 2050, **4 GiB VRAM** |

Con esa capacidad se priorizaron modelos **pequeños** (orden ~0.5B–3B parámetros en cuantización estándar de Ollama), no modelos 7B+ en GPU 4GB sin ajustes agresivos.

---

## Artefactos en el host (rutas ejemplo: usuario `aipp`)

| Qué | Dónde |
|-----|--------|
| Binario Ollama (extracción local, sin `sudo`) | `$HOME/ollama-local/bin/ollama` |
| Modelos en disco | `$HOME/.ollama/models` |
| Config OpenClaw viva | `$HOME/.openclaw/openclaw.json` |
| Log append del servicio Ollama | `$HOME/.openclaw/ollama-local.log` (si se configuró `StandardOutput`/`StandardError` en la unit) |
| Unit systemd usuario | `$HOME/.config/systemd/user/ollama-local.service` |

**No versionar** en git: `auth-profiles.json`, `.env`, tokens de bots.

---

## Servicio systemd (usuario)

- **Unit:** `ollama-local.service`
- **Comando:** `ExecStart=$HOME/ollama-local/bin/ollama serve`
- **Variables útiles:** `HOME=$HOME`, `OLLAMA_HOST=http://127.0.0.1:11434`, `OLLAMA_MODELS=$HOME/.ollama/models`, `OLLAMA_KEEP_ALIVE=30m` (mantener modelo caliente más tiempo).

Comandos habituales:

```bash
systemctl --user daemon-reload
systemctl --user enable --now ollama-local.service
systemctl --user restart ollama-local.service
```

Tras cambiar modelos en `openclaw.json`, reiniciar también el Gateway:

```bash
systemctl --user restart openclaw-gateway
```

---

## Modelos instalados (referencia)

| Modelo Ollama | Rol |
|----------------|-----|
| `qwen2.5:3b` | Principal razonable para `jarvis` en esta GPU |
| `qwen2.5:0.5b` | Rápido / barato en tokens para `jarvis-auto-light` |
| `qwen2.5-coder:0.5b` | Fallback opcional (sesgo “código”; no ideal solo para charla casual) |

Listar en el host: `ollama list` (usando el binario de `$HOME/ollama-local/bin/ollama`).

---

## Configuración OpenClaw (resumen conceptual)

- **`agents.defaults.model`:** `primary` apuntando a `ollama/...` y `fallbacks` con más `ollama/...` y luego proveedores cloud si aplica.
- **`jarvis-auto-light`:** `model.primary` = modelo mini conversacional (`ollama/qwen2.5:0.5b`), fallbacks hacia `ollama/qwen2.5:3b` y cloud.
- **Bootstrap:** se redujeron `bootstrapMaxChars` / `bootstrapTotalMaxChars` para bajar tokens de sistema; **sigue habiendo truncado** de `AGENTS.md` grande — es esperable.
- **`contextTokens`:** debe permanecer **≥ 16000** en esta versión de OpenClaw; valores menores **bloquean** todos los candidatos con error de “context window too small”.

Los fragmentos JSON históricos en [`MODELOS_JARVIS_OPENCLAW.md`](MODELOS_JARVIS_OPENCLAW.md) pueden quedar desactualizados respecto a la config viva en `~/.openclaw/openclaw.json`; la fuente de verdad es siempre el archivo local del Gateway.

---

## Verificación mínima post-cierre

```bash
curl -s http://127.0.0.1:11434/api/tags
openclaw agent --agent jarvis --message "hola" --json
openclaw agent --agent jarvis-auto-light --message "hola" --json
openclaw channels status --probe
```

En la salida JSON del agente, comprobar `result.meta.agentMeta.provider` = `ollama` y `model` acorde.

---

## Riesgos y límites aceptados

- Modelos **muy pequeños** pueden dar respuestas raras o “formato herramienta” en algunos turnos; el tier “fuerte” sigue siendo cloud u otro agente si lo configuras.
- **TPM / rate limits** de Groq u otros no se “arreglan” solo con Ollama: el local reduce dependencia, no sustituye políticas de API.
- **OpenRouter 401** u otras claves inválidas siguen siendo fallos de credencial hasta rotar la key en `auth-profiles` / entorno.

---

## Próximos pasos opcionales (fuera de este cierre)

- Binding Telegram DM → `jarvis-auto-light` y grupos / tareas largas → `jarvis` (requiere revisar `bindings` y política de canales).
- Enlazar WhatsApp (`openclaw channels login`) si se desea el mismo stack en ese canal.
- Alinear documentación de tiers en `MODELOS_JARVIS_OPENCLAW.md` con el despliegue real Ollama+cloud en tu `openclaw.json`.

---

**Última actualización:** 3 abril 2026
