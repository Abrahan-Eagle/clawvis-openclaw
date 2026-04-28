# Pipeline de contenido para redes sociales — stack 100% gratis

**Fecha:** abril 2026
**Estado:** v1 — implementado en Fases 3 y 4 de [PROPUESTA_MEJORA_JARVIS_V2.md](PROPUESTA_MEJORA_JARVIS_V2.md)
**Aplica a:** mkt-content, mkt-social, jarvis (orquestacion)

---

## 1. Objetivo

Producir contenido de marketing **listo para publicar** en Instagram, Facebook y TikTok desde un brief estructurado:

- Carruseles IG (10 slides, 1080x1350).
- Stories y Reels verticales (1080x1920).
- Reels / TikToks de 30 a 60 segundos con voz y subtitulos.

Sin gastar dinero, sin GPU, sin servicios propietarios cerrados.

---

## 2. Stack adoptado

| Capa | Tecnologia | Tipo | Por que |
|---|---|---|---|
| Brand kit | JSON local | Manual | Paleta, fuentes, logo, voice, claim por marca |
| Imagen plantilla | Python + Pillow | Local | Sin red, deterministico, tipografias del cliente |
| Imagen generativa fondo | Pollinations.ai | API gratis sin key | Fondos ilustrados, ambient, abstract |
| Imagen fallback | HuggingFace Inference free | API gratis con token free | Cuando Pollinations cae |
| Carrusel | `carousel-render` propio | Local | Une plantillas + brand kit + slides |
| Voz TTS | edge-tts (Microsoft Edge) | API gratis | Voces es-ES, es-MX, es-AR, es-VE de calidad alta |
| Voz fallback | piper local | Local | Si edge-tts no responde |
| Subtitulos | SRT desde guion + opcional whisper.cpp | Local | Quemados o como pista |
| Video corto | Remotion (React + Node) | Local CPU | Plantillas vertical 9:16 deterministicas |
| Composicion video | ffmpeg | Local | Mux audio + video + subs + musica |
| Musica libre | Pixabay / Mixkit / YouTube Audio Library | Manual | Sin automatizacion para evitar TOS |

---

## 3. Formatos soportados

| Red | Formato | Resolucion | Aspect | Comentario |
|---|---|---|---|---|
| IG Feed | Carrusel | 1080x1080 o 1080x1350 | 1:1 / 4:5 | 10 slides max |
| IG Stories / Reels | Vertical | 1080x1920 | 9:16 | 5-90s |
| Facebook Feed | Imagen | 1200x630 o 1080x1080 | varies | Reusa carrusel |
| Facebook Reels | Vertical | 1080x1920 | 9:16 | 5-90s |
| TikTok | Vertical | 1080x1920 | 9:16 | 9-60s recomendado |

---

## 4. Estructura de input (lo que llena el copy/estratega)

### 4.1 `brand.json` por cliente

`client-dossiers/<id>/brand.json`:

```json
{
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

### 4.2 Brief del carrusel `carousel.json`

```json
{
  "format": "carousel_ig_1080x1350",
  "slides": [
    { "type": "hook", "title": "El error #1 que cuesta clientes", "subtitle": "Y como evitarlo en 7 pasos" },
    { "type": "step",  "n": 1, "title": "Escucha primero", "body": "Antes de proponer, entiende el problema real." },
    { "type": "step",  "n": 2, "title": "Mide lo importante", "body": "Tres KPIs basta. Mas es ruido." },
    { "type": "quote", "text": "El cliente no compra una funcion, compra un cambio en su vida." },
    { "type": "cta",   "title": "Hablemos", "subtitle": "DM o link en bio" }
  ]
}
```

### 4.3 Brief del reel `reel.json`

```json
{
  "format": "reel_1080x1920",
  "duration_sec": 45,
  "voice": "es-ES-ElviraNeural",
  "music": "assets/music/upbeat-corporate.mp3",
  "scenes": [
    { "t": 0, "type": "hook", "text": "Si vendes y no te responden, mira esto.", "bg_image": "auto" },
    { "t": 4, "type": "body", "bullets": [
        "El 80% no contesta al primer mensaje",
        "El 50% lo hace al tercer toque",
        "El 90% nunca contesta despues de 14 dias"
      ]},
    { "t": 24, "type": "body", "text": "Cambia el guion: pregunta, no vendas." },
    { "t": 35, "type": "cta", "text": "Comenta METODO y te paso la plantilla.", "bg_image": "auto" }
  ]
}
```

---

## 5. Pipeline ejecutable

### 5.1 Carrusel

```bash
# 1. Generar fondos opcionales con IA
image-ai-free generate \
  --prompt "abstract gradient, soft blue and amber" \
  --out state/cache/images/bg-cli-DEMO-rrss-001.png \
  --aspect 4:5

# 2. Renderizar carrusel
carousel-render \
  --brand client-dossiers/cli-DEMO-rrss/brand.json \
  --slides /tmp/carousel.json \
  --out out/carousel-cli-DEMO-rrss/
# Salida: 01.png ... 10.png + manifest.json
```

### 5.2 Reel 30-60s

```bash
# 1. Voz desde guion
tts-free say \
  --text "Si vendes y no te responden, mira esto. ..." \
  --voice es-ES-ElviraNeural \
  --out /tmp/voice.mp3

# 2. Subtitulos SRT (sincronizados al guion)
subtitles from-script \
  --script /tmp/scenes.json \
  --audio /tmp/voice.mp3 \
  --out /tmp/subs.srt

# 3. Render Remotion (vertical 9:16)
video-short render \
  --script /tmp/scenes.json \
  --brand client-dossiers/cli-DEMO-rrss/brand.json \
  --voice /tmp/voice.mp3 \
  --subs /tmp/subs.srt \
  --music assets/music/upbeat-corporate.mp3 \
  --out out/reel-cli-DEMO-rrss.mp4

# Alternativa simple sin Remotion (slideshow Ken Burns con ffmpeg)
video-compose slideshow \
  --images out/carousel-cli-DEMO-rrss/*.png \
  --voice /tmp/voice.mp3 \
  --music assets/music/upbeat-corporate.mp3 \
  --subs /tmp/subs.srt \
  --duration 45 \
  --out out/reel-quick.mp4
```

---

## 6. Plantillas iniciales

### 6.1 Carrusel

| Plantilla | Uso |
|---|---|
| `minimal` | Tipografica, paleta neutra, ideal pensamiento / cita |
| `editorial` | Cards con foto + headline; estilo magazine |
| `listicle` | "5 cosas que…" numeradas |
| `before-after` | Mitad antes / mitad despues |

### 6.2 Reel

| Plantilla | Uso | Estructura |
|---|---|---|
| `hook-listicle` | "3 errores que…", "5 trucos…" | Hook 3s + lista 30-50s + CTA 5s |
| `tutorial-3steps` | Tutorial corto | Hook + paso1 + paso2 + paso3 + CTA |
| `before-after` | Transformacion | Antes 10s + despues 30s + CTA 5s |
| `ugc-talking-head` | Talking head con texto motion | Hook + cuerpo + CTA |

---

## 7. Calidad y limites honestos

**Lo que el stack puede hacer bien:**
- Carruseles con tipografia consistente, paleta de marca, layouts limpios.
- Reels con voz humana de calidad alta (Edge TTS), subtitulos quemados, slideshow con motion (Ken Burns), B-roll desde Pollinations, transiciones suaves.
- Plantillas reutilizables y reproducibles.

**Lo que NO hace este stack:**
- Generar clips fotorrealistas de cero tipo Sora / Veo / Seedance / Kling. Esos son APIs propietarias de pago.
- Generar avatar talking-head con lip-sync animado (necesita HeyGen / D-ID / SadTalker — los dos primeros son de pago, el tercero requiere GPU).
- Aplicar efectos VFX cinematograficos (After Effects no es gratis y no esta automatizable).

**Cuando se necesite calidad cinematica:** AG-13 + decision del CEO sobre pagar API o conseguir GPU. Esto queda **fuera** de v1.

---

## 8. Approval gates aplicables

- `AG-03` — publicar contenido en plataforma (ya existia, sigue vigente).
- `AG-12` — publicar carrusel o reel generado por este pipeline (nuevo).
- `AG-13` — uso de imagen / voz / video con IA generativa (Pollinations, Edge TTS) (nuevo).

Detalle: [APPROVAL_GATES.md](APPROVAL_GATES.md).

---

## 9. Roadmap

- v1 (hoy): carrusel + reel 30-60s con stack gratis local.
- v1.1: plantillas adicionales (quote, story, anuncio).
- v1.2: integracion con `canva` skill para tomar plantillas de marca cuando el cliente tenga Canva Brand Kit.
- v1.3: skill stub `video-gen-local` que detecte GPU NVIDIA y, si existe, instale Wan 2.2 / LTX-Video bajo AG-13.
- v2: si hay presupuesto, integraciones con Ideogram (texto en imagen perfecto) y Suno (musica) bajo AG-13.
