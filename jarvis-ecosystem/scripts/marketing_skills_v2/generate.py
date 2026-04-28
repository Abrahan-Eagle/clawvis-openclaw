#!/usr/bin/env python3
"""Genera agents/marketing/skills/<slug>/SKILL.md (adaptación v2, ES)."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

from .coordination import render_coordination
from .manifest import SKILL_INDEX, SkillRecord, all_slugs
from .templates import render_framework

ECOSYSTEM = Path(__file__).resolve().parents[2]
YAML_DIR = ECOSYSTEM / "scripts" / "marketing_skills_data"
UPSTREAM = Path("/tmp/marketingskills-upstream/skills")
OUT_SKILLS = ECOSYSTEM / "agents" / "marketing" / "skills"

ATTRIBUTION = """> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.
"""

AG13 = {"image", "ad-creative", "video", "social-content"}
AG12 = {
    "social-content",
    "email-sequence",
    "paid-ads",
    "directory-submissions",
    "referral-program",
    "launch-strategy",
}
AG11 = {"competitor-profiling", "customer-research", "seo-audit", "programmatic-seo"}

OPS_DUAL = {
    "page-cro": "../../../jarvis/skills/page-cro-ops/SKILL.md",
    "copywriting": "../../../jarvis/skills/copywriting-ops/SKILL.md",
    "cold-email": "../../../jarvis/skills/cold-email-ops/SKILL.md",
    "seo-audit": "../../../jarvis/skills/seo-audit-ops/SKILL.md",
    "customer-research": "../../../jarvis/skills/deep-interview-ops/SKILL.md",
}
OPS_DERIVED = {
    "marketing-ideas": "../../../jarvis/skills/brainstorming-ops/SKILL.md",
    "launch-strategy": "../../../jarvis/skills/strategic-briefing-ops/SKILL.md",
    "sales-enablement": "../../../jarvis/skills/proposal-ops/SKILL.md",
}


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), text[m.end() :]


def inject_jarvis_into_fm(fm_raw: str, ecosystem_tag: str = "2026-04-28") -> str:
    if "jarvis_ecosystem:" in fm_raw:
        return fm_raw.rstrip() + "\n"
    lines = fm_raw.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and re.match(r"\s*version:\s*", line):
            out.append(f'  jarvis_ecosystem: "{ecosystem_tag}"')
            inserted = True
    if not inserted:
        if any(line.strip() == "metadata:" for line in out):
            out.append(f'  jarvis_ecosystem: "{ecosystem_tag}"')
        else:
            out.append("metadata:")
            out.append(f'  jarvis_ecosystem: "{ecosystem_tag}"')
    return "\n".join(out) + "\n"


def fix_upstream_relative_links(body: str) -> str:
    """Enlaces relativos upstream skills/ -> carpeta local."""

    def sibling_repl(m: re.Match[str]) -> str:
        seg = m.group(1)
        if seg == "references":
            return m.group(0)
        return f"(../{seg}/"

    body = re.sub(r"\(\./([a-z0-9-]+)/", sibling_repl, body)
    body = body.replace("](../../tools/", "](../../../../docs/upstream-marketingskills/tools/")
    body = body.replace("](../tools/", "(../../../docs/upstream-marketingskills/tools/")
    return body


def strip_leading_h1(body: str) -> str:
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return body


def build_ag_block(skill: str) -> str:
    lines: list[str] = []
    if skill in AG13:
        lines.append(
            "- **AG-13**: IA generativa en assets que se entreguen o publiquen → [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md)."
        )
    if skill in AG12:
        lines.append(
            "- **AG-12**: publicar en canales externos o piezas listas para difusión masiva → aprobación previa."
        )
    if skill in AG11:
        lines.append(
            "- **AG-11**: automatizar dominio nuevo en Playwright / scraping → aprobación antes de `BROWSER_PLAYWRIGHT_ALLOW`."
        )
    if not lines:
        lines.append(
            "- Sin gates extra por defecto; ante reputación/pagos/datos sensibles revisa [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md)."
        )
    return "\n".join(lines)


def build_ops_short(record: SkillRecord) -> str:
    s = record.slug
    if s in OPS_DUAL:
        p = OPS_DUAL[s]
        label = Path(p).parent.name  # p.ej. copywriting-ops (evitar anchor literal SKILL.md)
        return f"Variante corta **ops**: [`{label}`]({p}). Usa **esta skill completa** con dossier/brief formal."
    if s in OPS_DERIVED:
        p = OPS_DERIVED[s]
        label = Path(p).parent.name
        return f"Workflow **ops** relacionado: [`{label}`]({p}) (nombre distinto en Jarvis)."
    return "No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …)."


def build_description_es_en(record: SkillRecord) -> str:
    es = record.summary_es.strip()
    en_bits = ", ".join(record.triggers_en[:10])
    raw = f"{es} EN: {en_bits}"
    if len(raw) <= 500:
        return raw
    return raw[:497].rstrip() + "…"


def render_hooks_table(record: SkillRecord) -> str:
    if record.hooks_override:
        lines = ["| Hook |", "|------|"]
        for line in record.hooks_override:
            lines.append(f"| {line} |")
        return "### Hooks al pipeline Jarvis\n\n" + "\n".join(lines) + "\n"
    common = [
        "| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |",
        "| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |",
        "| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |",
    ]
    extra: list[str] = []
    if record.slug in {"image", "social-content"}:
        extra.append("| [`carousel-render`](../../../../skills/carousel-render/SKILL.md) | Slides/carruseles |")
        extra.append("| [`image-ai-free`](../../../../skills/image-ai-free/SKILL.md) | IA gratuita (AG-13) |")
    if record.slug == "video":
        extra.extend(
            [
                "| [`tts-free`](../../../../skills/tts-free/SKILL.md) | Voz TTS |",
                "| [`video-compose`](../../../../skills/video-compose/SKILL.md) | Montaje ffmpeg |",
            ]
        )
    lines = ["| Skill / doc | Rol |", "|-------------|-----|"] + common + extra
    return "### Hooks al pipeline Jarvis\n\n" + "\n".join(lines) + "\n"


def render_related(record: SkillRecord) -> str:
    lines: list[str] = []
    for r in record.related_local:
        if r == record.slug:
            continue
        lines.append(f"- [`{r}`](../{r}/SKILL.md)")
    if not lines:
        return "### Skills relacionadas (mapa local)\n\n- _(ninguna enlazada; revisa upstream-en)_\n"
    return "### Skills relacionadas (mapa local)\n\n" + "\n".join(lines) + "\n"


def render_triggers(record: SkillRecord) -> str:
    es = ", ".join(f"`{t}`" for t in record.triggers_es)
    en = ", ".join(f"`{t}`" for t in record.triggers_en)
    return f"""### Cuándo usarla (disparadores)

- **ES:** {es}
- **EN:** {en}
"""


def render_context_block() -> str:
    return """### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.
"""


def assemble_skill_md(record: SkillRecord, upstream_version: str | None) -> str:
    framework = render_framework(record.template_key, dict(record.ctx))
    md_ver = upstream_version or "unknown"
    description = build_description_es_en(record)
    fm = (
        "---\n"
        f"name: {record.slug}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "metadata:\n"
        f"  version: {json.dumps(md_ver)}\n"
        '  jarvis_ecosystem: "2026-04-28"\n'
        f"  upstream_version: {json.dumps(md_ver)}\n"
        "---\n"
    )
    parts = [
        fm.rstrip(),
        "",
        ATTRIBUTION.strip(),
        "",
        f"## Resumen\n\n{record.summary_es}",
        "",
        render_triggers(record),
        "",
        render_context_block(),
        "",
        "### Variante rápida en Jarvis (`*-ops`)\n\n" + build_ops_short(record),
        "",
        "## Frameworks / metodología\n",
        framework,
        "",
        render_hooks_table(record),
        "",
        "## Puertas de aprobación\n\n" + build_ag_block(record.slug),
        "",
        render_coordination(record.coord_category),
        "",
        render_related(record),
        "",
        "## Referencias\n\n"
        "- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).\n"
        "- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).",
        "",
    ]
    return "\n".join(parts).rstrip() + "\n"


def upstream_version_for(skill: str) -> str | None:
    src = UPSTREAM / skill / "SKILL.md"
    if not src.is_file():
        return None
    fm_raw, _ = split_frontmatter(src.read_text(encoding="utf-8"))
    if not fm_raw:
        return None
    for line in fm_raw.splitlines():
        m = re.match(r"\s*version:\s*(.+)", line)
        if m:
            return m.group(1).strip().strip('"')
    return None


def write_upstream_reference(skill: str, out_dir: Path) -> None:
    src = UPSTREAM / skill / "SKILL.md"
    ref_dir = out_dir / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)
    if not src.is_file():
        stub = (
            "# Upstream no disponible localmente\n\n"
            f"Clona el repo upstream y coloca `skills/{skill}/SKILL.md` en "
            "`/tmp/marketingskills-upstream/skills/`; vuelve a ejecutar "
            "`scripts/generate_marketing_skills.py`.\n"
        )
        (ref_dir / "upstream-en.md").write_text(stub, encoding="utf-8")
        return
    raw = src.read_text(encoding="utf-8")
    fm_raw, body = split_frontmatter(raw)
    body_fixed = fix_upstream_relative_links(body)
    body_use = strip_leading_h1(body_fixed)
    header = ""
    if fm_raw:
        header = "## Frontmatter upstream (YAML)\n\n```yaml\n" + fm_raw.rstrip() + "\n```\n\n---\n\n"
    (ref_dir / "upstream-en.md").write_text(
        header + "## Contenido upstream completo\n\n" + body_use,
        encoding="utf-8",
    )


def copy_upstream_refs(skill: str, out_dir: Path) -> None:
    ref_dir = UPSTREAM / skill / "references"
    if not ref_dir.is_dir():
        return
    dst = out_dir / "references"
    # merge: copytree requires dst not exist or we merge manually
    dst.mkdir(parents=True, exist_ok=True)
    for child in ref_dir.iterdir():
        if child.name == "upstream-en.md":
            continue
        target = dst / child.name
        if child.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)


def generate_one(skill: str) -> None:
    record = SKILL_INDEX[skill]
    out_dir = OUT_SKILLS / skill
    out_dir.mkdir(parents=True, exist_ok=True)
    uv = upstream_version_for(skill)
    md = assemble_skill_md(record, uv)
    (out_dir / "SKILL.md").write_text(md, encoding="utf-8")
    write_upstream_reference(skill, out_dir)
    copy_upstream_refs(skill, out_dir)


def export_skill_yaml_files() -> None:
    """Fichas YAML por skill (Adaptación v2) — fuente declarativa paralela al manifiesto Python."""

    def block_indent(prefix: str, lines: tuple[str, ...]) -> list[str]:
        out = [prefix]
        for line in lines:
            out.append(f"  - {line}")
        return out

    YAML_DIR.mkdir(parents=True, exist_ok=True)
    for slug, rec in SKILL_INDEX.items():
        lines: list[str] = [
            f"# Auto-generado por scripts/generate_marketing_skills.py — no editar a mano salvo saber que se sobrescribe.",
            f"slug: {slug}",
            f"template_key: {rec.template_key}",
            "summary_es: |",
        ]
        lines.append("  " + rec.summary_es.strip().replace("\n", "\n  "))
        lines.extend(block_indent("triggers_es:", rec.triggers_es))
        lines.extend(block_indent("triggers_en:", rec.triggers_en))
        lines.append(f"coord_category: {rec.coord_category}")
        lines.extend(block_indent("related_local:", rec.related_local))
        if rec.hooks_override:
            lines.extend(block_indent("hooks_override:", tuple(rec.hooks_override)))
        lines.append("body_sections_note: >-")
        lines.append(
            "  El cuerpo largo se renderiza desde scripts/marketing_skills_v2/templates.py"
            " + manifest.py (plantilla por template_key)."
        )
        (YAML_DIR / f"{slug}.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not UPSTREAM.is_dir():
        print("WARN: upstream ausente en", UPSTREAM, "- generando solo desde manifiesto.", file=sys.stderr)
    OUT_SKILLS.mkdir(parents=True, exist_ok=True)
    for s in sorted(all_slugs()):
        generate_one(s)
    export_skill_yaml_files()
    print(f"OK marketing skills v2 -> {OUT_SKILLS} ({len(all_slugs())} skills); YAML -> {YAML_DIR}")


if __name__ == "__main__":
    main()
