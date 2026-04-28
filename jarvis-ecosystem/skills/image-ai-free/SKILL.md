# image-ai-free — generacion de imagen IA gratis (Pollinations)

**Tipo:** skill local.
**Bin:** `skills/image-ai-free/bin/image-ai-free`.
**Estado:** v1 (Fase 3 de [docs/PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Wrapper bash + curl sobre [Pollinations.ai](https://pollinations.ai/) (API gratis sin API key). Genera fondos / ilustraciones para usar como `--bg` en `image-render` o como B-roll para `video-short`.

URL base usada: `https://image.pollinations.ai/prompt/<prompt>?width=W&height=H&nologo=true&seed=N`.

## Por que Pollinations

- **Gratis sin registro.** Pareja API publica, modelos: Flux, DALL-E, Stable Diffusion (segun parametro `model=`).
- Suficiente calidad para fondos, texturas y assets ambient. Para hero-shot fotorealista buscar otra cosa.
- Sujeto a rate limits no documentados. El skill tolera 429 y reintenta con backoff.

## Comandos

```bash
image-ai-free generate \
  --prompt "abstract gradient soft blue and amber, minimal" \
  --aspect 4:5 \
  --out state/cache/images/bg-cli-DEMO-rrss-001.png \
  [--seed 42] [--model flux] [--no-cache]

image-ai-free clean    # vaciar cache si supera 500MB
image-ai-free models   # listar modelos publicos comunes
```

## Aspect ratios soportados

| Aspect | Resolucion (default) |
|---|---|
| `1:1` | 1024x1024 |
| `4:5` | 1024x1280 |
| `9:16` | 1080x1920 |
| `16:9` | 1920x1080 |
| `3:2` | 1200x800 |

Usa `--width WxH` para override completo.

## Cache

Por default, antes de descargar, calcula `sha1(prompt+aspect+seed+model)` y cachea en `state/cache/images/<sha>.png`. Si existe, lo reusa. Pasa `--no-cache` para forzar nueva descarga.

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `JARVIS_STATE_DIR` | `<repo>/state` | Donde vive `cache/images/` |
| `IMAGE_AI_TIMEOUT` | `60` | Timeout curl (s) |
| `IMAGE_AI_RETRIES` | `3` | Reintentos en 429/5xx |

## AG-13

Cualquier asset publicado que use IA generativa requiere **AG-13** + nota en el manifiesto del carrusel/reel. Detalle: [APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md).

## Limites honestos

- Pollinations puede tardar 5-30s por imagen. Si falla, reintenta con backoff y, si sigue fallando, devuelve codigo 5 y mensaje claro (el caller decide fallback a generar imagen plana sin fondo).
- No hay garantia de calidad uniforme: misma prompt da resultados distintos sin seed fijo. Para reproducibilidad usa `--seed`.
- TOS publicos pero implicitos: no pedir contenido ofensivo; respetar copyright (no nombrar marcas o personajes registrados).

## Tests rapidos

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/image-ai-free/bin/image-ai-free
$bin models
$bin generate --prompt "minimal abstract gradient blue amber" --aspect 4:5 --out /tmp/bg.png --seed 42
file /tmp/bg.png
```
