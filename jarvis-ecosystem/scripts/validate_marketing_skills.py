#!/usr/bin/env python3
"""Valida SKILL.md bajo agents/marketing/skills/ (adaptación v2)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "agents" / "marketing" / "skills"

OPS_DUAL_SLUGS = {"page-cro", "copywriting", "cold-email", "seo-audit", "customer-research"}

# Patrones típicos del upstream sin reapuntar al dossier (fallar si aparecen en el cuerpo)
FORBIDDEN_UPSTREAM_SNIPPETS = (
    "(or `.claude/product-marketing-context.md`",
    "`.agents/product-marketing-context.md` also use when",
)


def extract_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), text[m.end() :]


def fm_description_length(fm_raw: str) -> int | None:
    for line in fm_raw.splitlines():
        if line.startswith("description:"):
            rest = line[len("description:") :].strip()
            if rest.startswith('"'):
                end = rest.rfind('"')
                if end > 0:
                    inner = rest[1:end]
                    return len(inner)
            return len(rest)
    return None


def main() -> int:
    errors = 0
    md_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if len(md_files) != 40:
        print(f"ERROR: esperaba 40 SKILL.md, hay {len(md_files)}", file=sys.stderr)
        errors += 1

    for skill_md in md_files:
        slug = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        fm_raw, body = extract_frontmatter(text)
        if fm_raw is None:
            print(f"ERROR: sin frontmatter: {skill_md}", file=sys.stderr)
            errors += 1
            fm_raw = ""

        if "jarvis_ecosystem:" not in text:
            print(f"ERROR: falta jarvis_ecosystem: {skill_md}", file=sys.stderr)
            errors += 1
        if "coreyhaines31/marketingskills" not in text:
            print(f"ERROR: falta atribucion upstream: {skill_md}", file=sys.stderr)
            errors += 1

        # Estructura v2
        if "## Resumen" not in text:
            print(f"ERROR: falta seccion Resumen: {skill_md}", file=sys.stderr)
            errors += 1
        if "## Coordinación" not in text and "## Coordinacion" not in text:
            print(f"ERROR: falta bloque Coordinacion: {skill_md}", file=sys.stderr)
            errors += 1
        if "activity-log" not in text or "handoff" not in text:
            print(f"ERROR: falta mencionar activity-log y/o handoff: {skill_md}", file=sys.stderr)
            errors += 1

        desc_len = fm_description_length(fm_raw)
        if desc_len is not None and desc_len > 500:
            print(f"ERROR: description frontmatter >500 chars ({desc_len}): {skill_md}", file=sys.stderr)
            errors += 1

        lowered = body.lower()
        if "client-dossiers/" not in body and "marketing-context.md" not in body:
            print(f"ERROR: cuerpo sin dossier/marketing-context obligatorio: {skill_md}", file=sys.stderr)
            errors += 1

        for snippet in FORBIDDEN_UPSTREAM_SNIPPETS:
            if snippet in body:
                print(f"ERROR: mencion prohibida upstream legacy ({snippet}): {skill_md}", file=sys.stderr)
                errors += 1

        if "_sin Related Skills_" in text or "(sin Related Skills" in text:
            print(f"ERROR: marcador prohibido Related Skills: {skill_md}", file=sys.stderr)
            errors += 1

        # Anchors mal formados: texto del enlace literal SKILL.md
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            label = m.group(1).strip()
            if label == "SKILL.md":
                print(f"ERROR: anchor prohibido [SKILL.md](...) en {skill_md}", file=sys.stderr)
                errors += 1

        # Hooks image / video
        if slug == "image":
            for needle in ("image-render", "image-ai-free", "carousel-render", "brand-kit"):
                if needle not in text:
                    print(f"ERROR: skill image sin hook {needle}: {skill_md}", file=sys.stderr)
                    errors += 1
        if slug == "video":
            for needle in ("video-compose", "tts-free", "subtitles"):
                if needle not in text:
                    print(f"ERROR: skill video sin hook {needle}: {skill_md}", file=sys.stderr)
                    errors += 1

        # DUAL: enlace explícito a *-ops en jarvis
        if slug in OPS_DUAL_SLUGS:
            ops_folder = f"{slug}-ops" if slug != "customer-research" else "deep-interview-ops"
            expected = f"jarvis/skills/{ops_folder}/SKILL.md"
            if expected not in text:
                print(f"ERROR: skill dual sin enlace esperado a {expected}: {skill_md}", file=sys.stderr)
                errors += 1

        base = skill_md.parent
        for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
            url = m.group(2).strip()
            if url.startswith("http://") or url.startswith("https://") or url.startswith("#"):
                continue
            if url.startswith("mailto:"):
                continue
            if url.startswith("/") and not url.startswith("//"):
                continue
            path_part = url.split("#")[0]
            if not path_part:
                continue
            target = (base / path_part).resolve()
            if not target.exists():
                print(f"ERROR: enlace roto en {skill_md}: ({path_part})", file=sys.stderr)
                errors += 1

        upstream_ref = base / "references" / "upstream-en.md"
        if not upstream_ref.is_file():
            print(f"ERROR: falta references/upstream-en.md: {skill_md}", file=sys.stderr)
            errors += 1

    if errors == 0:
        print(f"OK: {len(md_files)} skills validadas en {SKILLS_DIR}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
