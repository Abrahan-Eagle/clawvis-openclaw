# tts-free — voces gratis con Microsoft Edge TTS

**Tipo:** skill local con venv Python.
**Bin:** `skills/tts-free/bin/tts-free`.
**Estado:** v1 (Fase 4 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Wrapper sobre [`edge-tts`](https://pypi.org/project/edge-tts/), libreria Python que usa la API publica de voces de Microsoft Edge / Azure (la misma que usa el lector "leer en voz alta" del navegador). Es **gratis**, **no requiere API key**, y produce **WAV/MP3 con voces neuronales** de buena calidad en es-ES, es-AR, es-MX, en-US, etc.

> No confundir con Azure Cognitive Services (de pago). El endpoint que usa `edge-tts` es el mismo que el navegador y no tiene costo.

## Setup (una vez)

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem/skills/tts-free
python3 -m venv .venv
.venv/bin/pip install --quiet -r requirements.txt
```

## Comandos

```bash
tts-free synthesize \
  --text "Hola, soy Jarvis." \
  --voice es-ES-AlvaroNeural \
  --out out/audio/intro.mp3 \
  [--rate "+0%"] [--pitch "+0Hz"] [--volume "+0%"]

tts-free synthesize-file \
  --text-file script.txt \
  --voice es-AR-ElenaNeural \
  --out out/audio/reel.mp3

tts-free voices --lang es      # listar voces es-*
tts-free voices --gender Female # listar voces femeninas
```

## Voces recomendadas

| Voz | Idioma | Estilo |
|---|---|---|
| `es-ES-AlvaroNeural` | España (M) | natural, neutro |
| `es-ES-ElviraNeural` | España (F) | calida, broadcast |
| `es-AR-TomasNeural` | Argentina (M) | local sutil |
| `es-AR-ElenaNeural` | Argentina (F) | local |
| `es-MX-DaliaNeural` | Mexico (F) | comercial |
| `es-MX-JorgeNeural` | Mexico (M) | autoritario |
| `en-US-GuyNeural` | EN-US (M) | broadcast |
| `en-US-JennyNeural` | EN-US (F) | conversacional |

`tts-free voices --lang es` lista la lista completa actualizada.

## Salida

- Por default: MP3 (configurable a WAV con `--format wav`).
- 24kHz mono. Para Reels/TikToks alcanza con eso.
- Genera tambien `<out>.srt` si se pasa `--with-subs` (subtitulos word-level).

## Limites honestos

- Internet requerido (igual que un navegador comun).
- Velocidad: ~real-time (1 minuto de audio = ~10-30s).
- No soporta clonacion de voz (eso requiere modelos locales tipo XTTS / Coqui, no incluidos en este skill).
- Microsoft puede cambiar el endpoint sin aviso. Si pasa, este skill rompe; en ese caso, fallback a `pyttsx3` (offline, calidad robotica) o instalar Coqui XTTS local.

## AG-13

Voz IA en contenido publicado requiere **AG-13** y debe declararse en el manifiesto del reel/video. Detalle: [APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md).

## Test rapido

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/tts-free/bin/tts-free
$bin voices --lang es | head -20
$bin synthesize --text "Hola, soy Jarvis. Esta es una prueba de voz." --voice es-ES-AlvaroNeural --out /tmp/test.mp3
file /tmp/test.mp3
ffprobe -v error -show_format /tmp/test.mp3
```
