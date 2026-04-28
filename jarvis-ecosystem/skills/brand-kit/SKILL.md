# brand-kit — lector y validador de brand.json por cliente

**Tipo:** skill global.
**Bin:** `skills/brand-kit/bin/brand-kit`.
**Estado:** v1 (Fase 3 de [docs/PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Skill bash + jq que lee `client-dossiers/<id>/brand.json` y expone los campos de marca (paleta, fuentes, logo, voz, claim) al resto del pipeline (image-render, carousel-render, video-short).

## Convenio de ubicacion

Los dossiers de cliente conviven en dos formatos:

1. **JSON plano canonico** (registro del cliente): `client-dossiers/<id>.json` — campos del cliente.
2. **Directorio de assets** (opcional, lo crea `brand-kit init`): `client-dossiers/<id>/` con:
   - `brand.json` — paleta, fuentes, logo, voz.
   - `assets/logo.png`, `assets/<otros>` — recursos.
   - `assets/templates/` — plantillas custom del cliente.

`brand-kit` busca primero `<id>/brand.json`; fallback a `<id>.brand.json` (caso single-file).

## Estructura esperada de `brand.json`

```json
{
  "id": "cli-DEMO-rrss",
  "name": "Marca demo",
  "voice": {
    "tone": "claro, cercano, evita tecnicismos",
    "banned_words": ["sinergia", "innovador"]
  },
  "palette": {
    "primary": "#0F172A",
    "secondary": "#22D3EE",
    "accent": "#F59E0B",
    "bg": "#FFFFFF",
    "fg": "#0F172A",
    "muted": "#64748B"
  },
  "fonts": {
    "heading": "Inter-Bold",
    "body": "Inter-Regular",
    "fallback": "DejaVu Sans"
  },
  "logo": {
    "path": "client-dossiers/cli-DEMO-rrss/assets/logo.png",
    "padding": 40
  },
  "claim": "Marca demo: lo que importa, simple"
}
```

Campos minimos para que el pipeline funcione: `name`, `palette.primary`, `palette.bg`, `palette.fg`, `fonts.heading`, `fonts.body`.

## Comandos

```bash
brand-kit show --dossier cli-DEMO-rrss
brand-kit get --dossier cli-DEMO-rrss --field palette.primary
brand-kit validate --dossier cli-DEMO-rrss
brand-kit init --dossier cli-DEMO-rrss --name "Marca X"  # crea brand.json minimo
```

`validate` chequea presencia de campos minimos y devuelve codigo 0 si valido, 3 si invalido.

## Variables de entorno

| Variable | Default | Proposito |
|---|---|---|
| `JARVIS_DOSSIERS_DIR` | `<repo>/client-dossiers` | Donde buscar brand.json |

## Limites

- No descarga fuentes: si `fonts.heading` apunta a una fuente que no esta en `assets/fonts/` ni en el sistema, `image-render` cae a `fonts.fallback` ("DejaVu Sans" por defecto).
- No valida que la paleta tenga buen contraste; eso es trabajo del estratega.
