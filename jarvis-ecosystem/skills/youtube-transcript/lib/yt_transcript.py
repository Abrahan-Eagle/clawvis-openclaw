#!/usr/bin/env python3
"""Transcripción de YouTube (idea similar a MK37 youtube_video — sin copiar su código)."""
import re
import sys
import json


def video_id_from_arg(arg: str) -> str:
    s = arg.strip()
    m = re.search(r"(?:v=|/shorts/|youtu\.be/)([a-zA-Z0-9_-]{11})", s)
    if m:
        return m.group(1)
    m = re.search(r"^([a-zA-Z0-9_-]{11})$", s)
    if m:
        return m.group(1)
    raise ValueError("No se pudo extraer el video ID de la URL o cadena.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: yt_transcript.py <url_o_id> [lenguaje]", file=sys.stderr)
        sys.exit(2)
    vid = video_id_from_arg(sys.argv[1])
    lang = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as e:
        print(
            json.dumps(
                {
                    "error": "missing_dependency",
                    "hint": "pip install -r requirements.txt (en este directorio o venv)",
                }
            )
        )
        sys.exit(1)
    try:
        if lang:
            tr = YouTubeTranscriptApi.get_transcript(vid, languages=[lang])
        else:
            tr = YouTubeTranscriptApi.get_transcript(vid)
    except Exception as e:
        print(json.dumps({"error": str(e), "video_id": vid}))
        sys.exit(1)
    text = " ".join(segment.get("text", "") for segment in tr)
    print(
        json.dumps(
            {
                "video_id": vid,
                "lang": lang or "auto",
                "text": text,
                "char_count": len(text),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
