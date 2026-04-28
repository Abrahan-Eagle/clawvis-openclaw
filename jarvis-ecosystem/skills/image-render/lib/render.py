#!/usr/bin/env python3
"""
image-render — composicion de imagenes con Pillow para el pipeline RRSS.

Lee brand.json + slide.json + formato, devuelve PNG.

Uso:
  python lib/render.py slide --brand brand.json --slide slide.json \
      --format 1080x1350 --out out.png [--bg bg.png] [--template minimal]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------- helpers ----------

DEFAULT_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEFAULT_FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FORMATS = {
    "1080x1080": (1080, 1080),
    "1080x1350": (1080, 1350),
    "1080x1920": (1080, 1920),
    "1200x630": (1200, 630),
}


def hex_to_rgb(s: str) -> Tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def find_font_file(name: str, font_dirs: list[Path]) -> str:
    """Busca por nombre primero en font_dirs locales, luego deja a Pillow caer al default."""
    if not name:
        return DEFAULT_FONT
    candidates_local = []
    for fd in font_dirs:
        if fd.is_dir():
            for ext in (".ttf", ".otf"):
                candidates_local.append(fd / f"{name}{ext}")
                candidates_local.append(fd / f"{name.replace(' ', '-')}{ext}")
                candidates_local.append(fd / f"{name.replace(' ', '_')}{ext}")
    for c in candidates_local:
        if c.is_file():
            return str(c)
    # fc-match si existe
    try:
        import subprocess
        out = subprocess.check_output(["fc-match", "-f", "%{file}", name], stderr=subprocess.DEVNULL)
        path = out.decode().strip()
        if path and Path(path).is_file():
            return path
    except Exception:
        pass
    return DEFAULT_FONT


def font(file_path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(file_path, size=size)
    except Exception:
        return ImageFont.truetype(DEFAULT_FONT, size=size)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    if not text:
        return []
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        cand = (cur + " " + w).strip()
        if text_size(draw, cand, fnt)[0] <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_block(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    fnt: ImageFont.FreeTypeFont,
    cx: int,
    top_y: int,
    color: Tuple[int, int, int],
    line_spacing: float = 1.25,
) -> int:
    line_h = int(fnt.size * line_spacing)
    y = top_y
    for ln in lines:
        w, _ = text_size(draw, ln, fnt)
        draw.text((cx - w // 2, y), ln, font=fnt, fill=color)
        y += line_h
    return y


def draw_left_block(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    fnt: ImageFont.FreeTypeFont,
    x: int,
    top_y: int,
    color: Tuple[int, int, int],
    line_spacing: float = 1.25,
) -> int:
    line_h = int(fnt.size * line_spacing)
    y = top_y
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += line_h
    return y


def make_canvas(size: Tuple[int, int], bg_color, bg_image: Path | None) -> Image.Image:
    canvas = Image.new("RGB", size, bg_color)
    if bg_image and bg_image.is_file():
        try:
            bg = Image.open(bg_image).convert("RGB")
            bg = bg.resize(size, Image.LANCZOS)
            # Suavizar para que el texto encima sea legible
            bg = bg.filter(ImageFilter.GaussianBlur(radius=1))
            # Mezclar con un overlay del bg color al 35% para legibilidad
            overlay = Image.new("RGB", size, bg_color)
            canvas = Image.blend(bg, overlay, 0.35)
        except Exception as e:
            print(f"WARN: no se pudo cargar bg {bg_image}: {e}", file=sys.stderr)
    return canvas


def overlay_logo(canvas: Image.Image, brand: dict) -> Image.Image:
    logo = brand.get("logo", {})
    p = logo.get("path")
    pad = int(logo.get("padding", 40))
    if not p:
        return canvas
    p = Path(p)
    if not p.is_absolute():
        # Relativo al repo root
        repo = Path(__file__).resolve().parents[3]
        p = repo / p
    if not p.is_file():
        return canvas
    try:
        l = Image.open(p).convert("RGBA")
        max_w = canvas.size[0] // 6
        scale = max_w / l.size[0]
        new_size = (max_w, int(l.size[1] * scale))
        l = l.resize(new_size, Image.LANCZOS)
        canvas_rgba = canvas.convert("RGBA")
        canvas_rgba.alpha_composite(l, dest=(pad, canvas.size[1] - new_size[1] - pad))
        return canvas_rgba.convert("RGB")
    except Exception as e:
        print(f"WARN: no se pudo poner logo: {e}", file=sys.stderr)
        return canvas


# ---------- layouts ----------

def layout_hook(canvas, draw, slide, brand, fonts, fmt):
    W, H = canvas.size
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    fg = hex_to_rgb(brand["palette"]["fg"])
    accent = hex_to_rgb(brand["palette"].get("accent", brand["palette"]["primary"]))

    title_size = int(W * 0.085)
    sub_size = int(W * 0.04)
    title_font = font(fonts["heading"], title_size)
    sub_font = font(fonts["body"], sub_size)

    pad = int(W * 0.08)
    max_w = W - pad * 2
    title_lines = wrap_text(draw, title, title_font, max_w)
    sub_lines = wrap_text(draw, subtitle, sub_font, max_w)

    title_h = len(title_lines) * int(title_font.size * 1.2)
    sub_h = len(sub_lines) * int(sub_font.size * 1.3)
    block_h = title_h + (int(W * 0.04) if subtitle else 0) + sub_h
    top = (H - block_h) // 2

    cx = W // 2
    y = draw_centered_block(draw, title_lines, title_font, cx, top, fg, 1.2)
    if subtitle:
        y += int(W * 0.04)
        draw_centered_block(draw, sub_lines, sub_font, cx, y, accent, 1.3)


def layout_step(canvas, draw, slide, brand, fonts, fmt):
    W, H = canvas.size
    n = slide.get("n", "")
    title = slide.get("title", "")
    body = slide.get("body", "")
    fg = hex_to_rgb(brand["palette"]["fg"])
    accent = hex_to_rgb(brand["palette"].get("accent", brand["palette"]["primary"]))
    primary = hex_to_rgb(brand["palette"]["primary"])

    pad = int(W * 0.08)
    n_size = int(W * 0.18)
    title_size = int(W * 0.06)
    body_size = int(W * 0.038)

    n_font = font(fonts["heading"], n_size)
    title_font = font(fonts["heading"], title_size)
    body_font = font(fonts["body"], body_size)

    y = pad
    if str(n):
        n_str = f"{n:02d}" if isinstance(n, int) else str(n)
        draw.text((pad, y), n_str, font=n_font, fill=accent)
        y += int(n_font.size * 1.05)

    if title:
        title_lines = wrap_text(draw, title, title_font, W - pad * 2)
        y = draw_left_block(draw, title_lines, title_font, pad, y, primary, 1.2)
        y += int(W * 0.025)

    if body:
        body_lines = wrap_text(draw, body, body_font, W - pad * 2)
        draw_left_block(draw, body_lines, body_font, pad, y, fg, 1.4)


def layout_body(canvas, draw, slide, brand, fonts, fmt):
    layout_step(canvas, draw, {"n": "", **slide}, brand, fonts, fmt)


def layout_quote(canvas, draw, slide, brand, fonts, fmt):
    W, H = canvas.size
    text = slide.get("text", "")
    author = slide.get("author", "")
    fg = hex_to_rgb(brand["palette"]["fg"])
    muted = hex_to_rgb(brand["palette"].get("muted", brand["palette"]["fg"]))
    accent = hex_to_rgb(brand["palette"].get("accent", brand["palette"]["primary"]))

    pad = int(W * 0.08)
    quote_size = int(W * 0.065)
    author_size = int(W * 0.035)
    quote_font = font(fonts["heading"], quote_size)
    big_quote = font(fonts["heading"], int(W * 0.22))
    author_font = font(fonts["body"], author_size)

    draw.text((pad, pad - int(W * 0.02)), '"', font=big_quote, fill=accent)

    lines = wrap_text(draw, text, quote_font, W - pad * 2)
    line_h = int(quote_font.size * 1.25)
    block_h = len(lines) * line_h
    top = (H - block_h) // 2
    cx = W // 2
    y = draw_centered_block(draw, lines, quote_font, cx, top, fg, 1.25)

    if author:
        y += int(W * 0.05)
        a_lines = wrap_text(draw, f"— {author}", author_font, W - pad * 2)
        draw_centered_block(draw, a_lines, author_font, cx, y, muted, 1.3)


def layout_bullet(canvas, draw, slide, brand, fonts, fmt):
    W, H = canvas.size
    title = slide.get("title", "")
    bullets = slide.get("bullets", [])
    fg = hex_to_rgb(brand["palette"]["fg"])
    accent = hex_to_rgb(brand["palette"].get("accent", brand["palette"]["primary"]))
    primary = hex_to_rgb(brand["palette"]["primary"])

    pad = int(W * 0.08)
    title_size = int(W * 0.07)
    body_size = int(W * 0.04)
    title_font = font(fonts["heading"], title_size)
    body_font = font(fonts["body"], body_size)

    y = pad
    if title:
        title_lines = wrap_text(draw, title, title_font, W - pad * 2)
        y = draw_left_block(draw, title_lines, title_font, pad, y, primary, 1.2)
        y += int(W * 0.04)

    bullet_indent = int(W * 0.08)
    for b in bullets:
        b_text = b if isinstance(b, str) else (b.get("text") or "")
        if not b_text:
            continue
        # punto/numerito accent
        bullet_font = font(fonts["heading"], body_size)
        draw.text((pad, y), "•", font=bullet_font, fill=accent)
        b_lines = wrap_text(draw, b_text, body_font, W - pad - bullet_indent - int(W * 0.04))
        for i, ln in enumerate(b_lines):
            draw.text((pad + bullet_indent, y if i == 0 else y), ln, font=body_font, fill=fg)
            y += int(body_font.size * 1.4)
        y += int(W * 0.015)


def layout_cta(canvas, draw, slide, brand, fonts, fmt):
    W, H = canvas.size
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    accent = hex_to_rgb(brand["palette"].get("accent", brand["palette"]["primary"]))
    primary = hex_to_rgb(brand["palette"]["primary"])
    bg = hex_to_rgb(brand["palette"]["bg"])

    # Banda accent inferior
    band_h = int(H * 0.5)
    draw.rectangle([(0, H - band_h), (W, H)], fill=accent)

    pad = int(W * 0.08)
    title_size = int(W * 0.085)
    sub_size = int(W * 0.04)
    title_font = font(fonts["heading"], title_size)
    sub_font = font(fonts["body"], sub_size)

    title_lines = wrap_text(draw, title, title_font, W - pad * 2)
    sub_lines = wrap_text(draw, subtitle, sub_font, W - pad * 2)

    title_h = len(title_lines) * int(title_font.size * 1.2)
    sub_h = len(sub_lines) * int(sub_font.size * 1.3)
    block_h = title_h + (int(W * 0.04) if subtitle else 0) + sub_h
    top = H - band_h + (band_h - block_h) // 2

    cx = W // 2
    y = draw_centered_block(draw, title_lines, title_font, cx, top, bg, 1.2)
    if subtitle:
        y += int(W * 0.04)
        draw_centered_block(draw, sub_lines, sub_font, cx, y, bg, 1.3)


def layout_cover(canvas, draw, slide, brand, fonts, fmt):
    layout_hook(canvas, draw, slide, brand, fonts, fmt)


LAYOUTS = {
    "hook": layout_hook,
    "step": layout_step,
    "body": layout_body,
    "quote": layout_quote,
    "bullet": layout_bullet,
    "cta": layout_cta,
    "cover": layout_cover,
}


# ---------- main ----------

def render_slide(brand_path: Path, slide: dict, fmt: str, out: Path,
                 bg: Path | None, template: str) -> None:
    if fmt not in FORMATS:
        raise SystemExit(f"Formato no soportado: {fmt}. Validos: {list(FORMATS.keys())}")
    size = FORMATS[fmt]

    brand = json.loads(brand_path.read_text(encoding="utf-8"))
    pal = brand["palette"]
    bg_color = hex_to_rgb(pal["bg"])

    repo = Path(__file__).resolve().parents[3]
    font_dirs = [
        repo / "assets/fonts",
        Path(os.environ.get("IMAGE_RENDER_FONT_DIR", "/dev/null")),
    ]
    fonts = {
        "heading": find_font_file(brand["fonts"].get("heading", ""), font_dirs),
        "body": find_font_file(brand["fonts"].get("body", ""), font_dirs),
    }

    canvas = make_canvas(size, bg_color, bg)
    draw = ImageDraw.Draw(canvas)

    s_type = slide.get("type", "body")
    layout = LAYOUTS.get(s_type, layout_body)
    layout(canvas, draw, slide, brand, fonts, fmt)

    canvas = overlay_logo(canvas, brand)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="image-render — composicion de imagenes")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_slide = sub.add_parser("slide", help="Renderizar un slide")
    p_slide.add_argument("--brand", required=True)
    p_slide.add_argument("--slide", required=True)
    p_slide.add_argument("--format", required=True)
    p_slide.add_argument("--out", required=True)
    p_slide.add_argument("--bg", default=None)
    p_slide.add_argument("--template", default="minimal")

    args = parser.parse_args()
    if args.cmd == "slide":
        slide = json.loads(Path(args.slide).read_text(encoding="utf-8"))
        bg = Path(args.bg) if args.bg else None
        render_slide(Path(args.brand), slide, args.format, Path(args.out), bg, args.template)
        print(args.out)


if __name__ == "__main__":
    main()
