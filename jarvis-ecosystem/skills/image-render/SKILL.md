# image-render — composicion de imagenes con Pillow

**Tipo:** skill local.
**Bin:** `skills/image-render/bin/image-render`.
**Estado:** v1 (Fase 3 de [docs/PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Renderiza una imagen final 1080x1080 / 1080x1350 / 1080x1920 / 1200x630 a partir de:

- un brand kit (`client-dossiers/<id>/brand.json`),
- un slide JSON con `type` y campos (`title`, `subtitle`, `body`, `text`, `bullets`, `n`, etc.),
- opcional: un fondo (PNG/JPG local o URL local cacheada por `image-ai-free`).

No genera imagen IA por si solo: para eso usa `image-ai-free`. Esta capa es deterministica y sin red.

## Setup (una vez)

```bash
cd skills/image-render
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
chmod +x bin/image-render
```

## Comandos

```bash
image-render slide \
  --brand client-dossiers/cli-DEMO-rrss/brand.json \
  --slide /tmp/slide.json \
  --format 1080x1350 \
  --out /tmp/01.png \
  [--bg /tmp/bg.png] \
  [--template minimal|editorial|listicle|before-after]
```

Tipos soportados de slide:

| `type` | Campos | Layout |
|---|---|---|
| `hook` | title, subtitle | Titular grande centrado, subtitulo abajo |
| `step` | n, title, body | Numero grande superior, titulo, cuerpo |
| `body` | title, body | Titulo + cuerpo en bloque |
| `quote` | text, author | Comillas grandes, texto centrado, autor abajo |
| `bullet` | title, bullets[] | Titulo + lista con viñetas |
| `cta` | title, subtitle | CTA con paleta acento |
| `cover` | title, subtitle | Portada con logo |

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `IMAGE_RENDER_VENV` | `<self>/.venv` | venv autodetectado |
| `IMAGE_RENDER_FONT_DIR` | `<repo>/assets/fonts` | Donde buscar fuentes registradas |

## Limites

- Si la fuente declarada en brand.json no existe en `assets/fonts/` ni en el sistema, usa `DejaVu Sans` (siempre disponible en Linux).
- No procesa SVG: si necesitas un logo SVG, conviertelo a PNG antes (`rsvg-convert` o `inkscape`).
- No hace lay-out fluido tipo CSS: las plantillas son cajas predefinidas. Calidad agencia con limites claros.

## Ejemplo

```bash
echo '{"type":"hook","title":"El error #1 que cuesta clientes","subtitle":"Y como evitarlo en 7 pasos"}' > /tmp/s.json
image-render slide \
  --brand client-dossiers/cli-DEMO-rrss/brand.json \
  --slide /tmp/s.json \
  --format 1080x1350 \
  --out /tmp/hook.png
```
