# youtube-transcript

> Inspiración: capacidad de resumen/transcripción de [actions/youtube_video.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/actions/youtube_video.py) en Jarvis-MK37 — **código propio** (`lib/yt_transcript.py`).

## Setup (una vez)

```bash
cd skills/youtube-transcript
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
chmod +x bin/youtube-transcript
```

Opcional: `export YOUTUBE_TRANSCRIPT_VENV=/ruta/al/.venv`

## Uso

```bash
./bin/youtube-transcript transcript "https://www.youtube.com/watch?v=VIDEO_ID"
./bin/youtube-transcript transcript VIDEO_ID en
./bin/youtube-transcript trending-hint
```

## Resumen con LLM

No genera resumen aquí: pipea el JSON `text` al agente o a skill `summarize` en la misma sesión.

## Notas

- Depende de subtítulos disponibles en YouTube; si no hay, fallará.
- Cumplimiento de ToS: uso razonable; no scrapear a gran volumen.
