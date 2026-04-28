# carousel-render — orquestador de carruseles RRSS

**Tipo:** skill local.
**Bin:** `skills/carousel-render/bin/carousel-render`.
**Estado:** v1 (Fase 3 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Orquesta un carrusel completo a partir de `carousel.json`:

1. Lee `brand_id` -> resuelve a `client-dossiers/<brand_id>/brand.json` o flat.
2. Itera cada slide; si `bg_prompt`, llama [`image-ai-free`](../image-ai-free/SKILL.md) para fondo cacheado.
3. Llama [`image-render slide`](../image-render/SKILL.md) por slide.
4. Emite `out/<brand_id>/<slug>/<NN>.png` + `index.json` con manifiesto.
5. Opcional: registra `activity-log event` y devuelve handoff payload `copy-to-design` validado.

## Schema `carousel.json`

```json
{
  "id": "cli-DEMO-rrss-c001",
  "brand_id": "cli-DEMO-rrss",
  "format": "1080x1350",
  "slug": "5-errores-marketing",
  "title": "5 errores en marketing organico",
  "slides": [
    {
      "type": "hook",
      "title": "El error #1 que cuesta clientes",
      "subtitle": "Y como evitarlo en 7 pasos",
      "bg_prompt": "abstract gradient soft blue minimal"
    },
    {
      "type": "step",
      "n": 1,
      "title": "Escucha primero",
      "body": "Antes de proponer, entiende el problema real."
    }
  ],
  "ai_assets": false
}
```

Si algun slide tiene `bg_prompt`, `ai_assets` debe ponerse en `true` y el caller debe haber pasado AG-13.

## Comandos

```bash
carousel-render render --in carousel.json [--out-dir out/]   # generar todos los slides
carousel-render validate --in carousel.json                  # validar JSON sin renderizar
carousel-render preview --in carousel.json                   # listar slides + bg planeados (dry-run)
```

## Flags `render`

| Flag | Default | Detalle |
|---|---|---|
| `--in` | (req) | Path del `carousel.json` |
| `--out-dir` | `out/<brand_id>/<slug>/` | Donde escribir PNGs e `index.json` |
| `--task-id` | `""` | Si se da, se loggea `activity-log event` |
| `--no-ai` | off | Ignora `bg_prompt`, no llama Pollinations |
| `--seed` | `42` | Seed pasado a `image-ai-free` |

## Output

```
out/cli-DEMO-rrss/5-errores-marketing/
├── 01.png
├── 02.png
├── 03.png
├── ...
└── index.json
```

`index.json` contiene metadatos (timestamp, brand_id, format, slides count, sha de cada PNG, asset_used si fue Pollinations).

## Limites honestos

- Cada `bg_prompt` Pollinations cuesta ~5-30s. Un carrusel de 10 slides con todos `bg_prompt` puede tardar 1-5 min. Cache `state/cache/images/` ayuda en re-renders.
- El stack tipografico depende del sistema. Si la fuente no existe, cae a DejaVu. Para identidad fuerte poner las TTF en `assets/fonts/`.
- No hay anti-aliasing avanzado: bordes nitidos pero servible para RRSS.

## Ejemplo end-to-end

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
skills/carousel-render/bin/carousel-render render \
  --in templates/carousels/cli-DEMO-rrss/5-errores-marketing.json \
  --task-id task-2026-04-27-rrss
```
