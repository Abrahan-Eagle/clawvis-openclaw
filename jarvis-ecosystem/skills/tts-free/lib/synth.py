#!/usr/bin/env python3
"""
tts-free / synth.py — synthesizer wrapper para edge-tts.

Comandos:
  python lib/synth.py synthesize --text "..." --voice es-ES-AlvaroNeural --out out.mp3
  python lib/synth.py voices [--lang es] [--gender Female]

Soporta --with-subs para emitir <out>.srt con marcas word-level.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import edge_tts


def _fmt_srt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


async def list_voices(lang: str | None, gender: str | None) -> None:
    voices = await edge_tts.list_voices()
    out = []
    for v in voices:
        short = v.get("ShortName", "")
        loc = v.get("Locale", "")
        g = v.get("Gender", "")
        if lang and not loc.lower().startswith(lang.lower()):
            continue
        if gender and g.lower() != gender.lower():
            continue
        out.append({"name": short, "locale": loc, "gender": g, "style": v.get("VoiceTag", {}).get("ContentCategories", [])})
    out.sort(key=lambda x: x["locale"])
    for o in out:
        print(f"{o['name']:35s} {o['locale']:10s} {o['gender']:8s} {','.join(o['style']) if o['style'] else ''}")


async def synthesize(text: str, voice: str, out: Path, rate: str, pitch: str, volume: str, with_subs: bool) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate or "+0%",
        pitch=pitch or "+0Hz",
        volume=volume or "+0%",
    )

    if not with_subs:
        await communicate.save(str(out))
        return

    submaker = edge_tts.SubMaker()
    with out.open("wb") as fh:
        async for chunk in communicate.stream():
            t = chunk["type"]
            if t == "audio":
                fh.write(chunk["data"])
            elif t in ("WordBoundary", "SentenceBoundary"):
                try:
                    submaker.feed(chunk)
                except ValueError:
                    pass

    srt_path = out.with_suffix(out.suffix + ".srt")
    srt_text = submaker.get_srt()
    srt_path.write_text(srt_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="tts-free — Edge TTS wrapper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_voices = sub.add_parser("voices")
    p_voices.add_argument("--lang", default=None)
    p_voices.add_argument("--gender", default=None, choices=["Male", "Female"])

    p_syn = sub.add_parser("synthesize")
    p_syn.add_argument("--text", required=True)
    p_syn.add_argument("--voice", required=True)
    p_syn.add_argument("--out", required=True)
    p_syn.add_argument("--rate", default="+0%")
    p_syn.add_argument("--pitch", default="+0Hz")
    p_syn.add_argument("--volume", default="+0%")
    p_syn.add_argument("--with-subs", action="store_true")

    args = parser.parse_args()
    if args.cmd == "voices":
        asyncio.run(list_voices(args.lang, args.gender))
    elif args.cmd == "synthesize":
        asyncio.run(
            synthesize(
                args.text,
                args.voice,
                Path(args.out),
                args.rate,
                args.pitch,
                args.volume,
                args.with_subs,
            )
        )
        print(args.out)


if __name__ == "__main__":
    main()
