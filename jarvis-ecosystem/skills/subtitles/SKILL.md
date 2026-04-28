# subtitles — generador y normalizador de SRT/ASS

**Tipo:** skill local (bash + jq + python).
**Bin:** `skills/subtitles/bin/subtitles`.
**Estado:** v1 (Fase 4 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)).

---

## Que es

Tres modos de uso:

1. **`from-script`**: a partir de un `script.json` con bloques de texto y duraciones, emite un SRT.
2. **`split-words`**: toma un SRT existente y lo re-segmenta en chunks word-level (3-5 palabras por linea), util para Reels/TikToks que requieren subtitulos animados.
3. **`to-ass`**: convierte SRT a formato ASS para ffmpeg con estilos basados en `brand.json` (color, fuente, outline).

> Para subtitulos automaticos a partir de audio (forced alignment), tts-free ya emite SRT al pasar `--with-subs`. Si el caller necesita transcribir un audio externo, usar `whisper.cpp` (no incluido en este skill por peso, ver doc).

## Comandos

```bash
subtitles from-script --in script.json --out out.srt
subtitles split-words --in voice.srt --out voice.words.srt --max-words 4
subtitles to-ass --in voice.srt --out voice.ass --brand cli-DEMO-rrss
```

## `script.json` (input para `from-script`)

```json
{
  "blocks": [
    { "text": "Hola, soy Jarvis.", "start": 0.0, "end": 2.0 },
    { "text": "Esta es una prueba.", "start": 2.0, "end": 4.5 }
  ]
}
```

Si no se conocen tiempos, usar [`tts-free synthesize --with-subs`](../tts-free/SKILL.md), que emite SRT directamente con marcas reales del TTS.

## `to-ass` y branding

Lee `brand.json` (vía [`brand-kit`](../brand-kit/SKILL.md)) y genera un encabezado ASS con:

- `Fontname`: brand.fonts.heading
- `PrimaryColour`: brand.palette.bg (texto)
- `OutlineColour`: brand.palette.fg (borde)
- `Outline`: 3px (default)
- `Shadow`: 0
- `Alignment`: 2 (centrado abajo)
- `MarginV`: 120 (suficiente para safe-area de Reels/TikTok)

## Limites honestos

- `from-script` confia en los timestamps del caller. Si vienen mal, el SRT esta mal sincronizado.
- `split-words` distribuye linealmente por largo de texto: en idiomas con palabras compuestas (alemán) puede sobre-segmentar.
- `to-ass` no soporta animaciones karaoke ni `\fad` por simplicidad. Para eso, editar el ASS manualmente.

## Test rapido

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
bin=skills/subtitles/bin/subtitles
echo '{"blocks":[{"text":"Hola","start":0,"end":1.5},{"text":"Adios","start":1.5,"end":3}]}' > /tmp/s.json
bash $bin from-script --in /tmp/s.json --out /tmp/s.srt
cat /tmp/s.srt
```
