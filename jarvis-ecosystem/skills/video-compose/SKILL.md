# video-compose — wrapper ffmpeg para Reels/TikToks

**Tipo:** skill local (bash + ffmpeg).
**Bin:** `skills/video-compose/bin/video-compose`.
**Estado:** v1 (Fase 4 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Wrapper bash sobre ffmpeg que orquesta:

1. Lee `reel.json`: lista de slides (PNGs ya renderizados por [`image-render`](../image-render/SKILL.md) o [`carousel-render`](../carousel-render/SKILL.md)) con duraciones, transiciones, audio y subtitulos.
2. Compone video MP4 H.264 + AAC, 1080x1920 30fps (o el formato que se especifique).
3. Quema subtitulos ASS opcionalmente para garantizar que se vean en cualquier reproductor.
4. Emite manifiesto `index.json` y opcional handoff `producer-to-publisher`.

## `reel.json` (input)

```json
{
  "id": "cli-DEMO-rrss-r001",
  "brand_id": "cli-DEMO-rrss",
  "format": "1080x1920",
  "fps": 30,
  "duration_sec": 45,
  "slug": "5-errores-marketing-reel",
  "slides": [
    { "image": "out/cli-DEMO-rrss/5-errores-marketing/01.png", "duration": 3.0, "transition": "fade" },
    { "image": "out/cli-DEMO-rrss/5-errores-marketing/02.png", "duration": 6.0 },
    { "image": "out/cli-DEMO-rrss/5-errores-marketing/03.png", "duration": 6.0 }
  ],
  "audio": {
    "voice": "out/audio/reel.mp3",
    "music": "assets/music/upbeat-loop.mp3",
    "music_volume": 0.15
  },
  "subtitles": {
    "ass": "out/audio/reel.ass",
    "burn": true
  },
  "ai_assets": false
}
```

Sumando `duration` de cada slide debe coincidir con la longitud del audio de voz (o quedar dentro de `duration_sec`).

## Comandos

```bash
video-compose validate --in reel.json
video-compose render   --in reel.json [--out-dir out/<brand>/<slug>/] [--task-id ...]
video-compose probe    --in some.mp4
```

## Pipeline ffmpeg

Por dentro hace:

1. Crea un concat-friendly intermediate: cada slide se convierte a `.ts` (MPEG-TS) con `-loop 1 -t <dur> -i img.png -vf scale=...,setsar=1`.
2. Concatena con `concat:` o `-f concat -i list.txt`.
3. Mezcla audio: voz + musica de fondo (con `volume` aplicado), `-shortest` para empatar.
4. Si `subtitles.burn`, quema ASS via `-vf subtitles=foo.ass` o `-vf ass=foo.ass`.
5. Salida final: `out/<brand>/<slug>/reel.mp4` con CRF 23, preset medium.

## Transiciones

| Modo | Como | Costo |
|---|---|---|
| `cut` (default) | corte directo | barato |
| `fade` | xfade entre clips | un poco mas pesado |
| `slide-left` | xfade=slideleft | medio |
| `dissolve` | xfade=dissolve | medio |

xfade requiere ffmpeg >= 4.3.

## Limites honestos

- **Sin animaciones complejas**: text-on-screen animado, kinetic typography, particle FX, etc no se pueden hacer solo con ffmpeg. Para eso, `video-short` (Remotion) es mejor — pendiente Fase 4.5.
- **Loudness**: no normaliza audio. Para evitar saltos de volumen, hacer pre-procesamiento manual (`ffmpeg -af loudnorm`).
- **Calidad subtitulos quemados**: depende de la fuente declarada en el ASS. Si la fuente no esta instalada, ffmpeg cae a default sans-serif.
- **Tiempo de render**: ~real-time en CPU sin GPU. Un reel de 45s tarda ~30-60s.

## Approval Gates

| Gate | Cuando |
|---|---|
| **AG-12** | Antes de publicar el reel |
| **AG-13** | Si `ai_assets: true` (voz IA via tts-free, fondos via Pollinations, etc) |

`index.json` declara `ai_used`.

## Test rapido

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
# Con un reel.json de prueba:
skills/video-compose/bin/video-compose render --in /tmp/reel.json
ffprobe out/cli-DEMO-rrss/<slug>/reel.mp4
```
