"""Cuerpo principal (marcos ES) por plantilla — sin coordinación ni referencia upstream (añade generate.py)."""
from __future__ import annotations

from pathlib import Path

from typing import Any

_ECOSYSTEM = Path(__file__).resolve().parents[2]  # jarvis-ecosystem/


def _load_foundation_extra() -> str:
    p = _ECOSYSTEM / "scripts" / "marketing_skills_data" / "product-marketing-context-body.md"
    if p.is_file():
        return p.read_text(encoding="utf-8").strip()
    return ""


def tpl_foundation(_: dict[str, Any]) -> str:
    extra = _load_foundation_extra()
    base = """## Contexto obligatorio (dossier-first)

1. **Cliente con dossier**: documento canónico `client-dossiers/<dossier_id>/marketing-context.md`.
2. **Sin cliente (holding Jarvis)**: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Plantilla vacía: [`.agents/product-marketing-context.md.template`](../../../../.agents/product-marketing-context.md.template).

**No** uses rutas legacy fuera del dossier o de `.agents/` para el contexto canónico; migra cualquier borrador antiguo al dossier o a `.agents/product-marketing-context.md`.

Snippet de comprobación:

```bash
cd jarvis-ecosystem
ls -la client-dossiers/<dossier_id>/marketing-context.md 2>/dev/null || true
ls -la .agents/product-marketing-context.md 2>/dev/null || true
grep -n \"marketing-context\" client-dossiers/*/marketing-context.md 2>/dev/null | head
```

## Flujo de trabajo

1. Detectar si ya existe contexto (dossier o `.agents/`).
2. Si existe: resume secciones cubiertas y pregunta qué actualizar.
3. Si no: (a) auto-borrador desde README / dossier / `brand.json` o (b) entrevista guiada por secciones.

## Plantilla embebida (resumen)

Usa la plantilla del repo para no omitir campos; las 12 secciones detalladas están en el bloque siguiente (y en la plantilla `.template`).
"""
    if extra:
        return base + "\n\n" + extra
    return base


def tpl_cro_dual(ctx: dict[str, Any]) -> str:
    titulo = ctx.get("titulo", "CRO")
    ops_name = ctx.get("ops_name", "page-cro-ops")
    ops_path = ctx.get("ops_path", "../../../jarvis/skills/page-cro-ops/SKILL.md")
    focus = ctx.get("focus", "mejorar conversión")
    return f"""### Marco de trabajo ({titulo})

**Objetivo:** {focus}.

#### Principios (adaptación Jarvis)

- Claridad del mensaje en <5 s (hero).
- Propuesta de valor específica vs genérica.
- Prueba social creíble cerca del CTA.
- Una acción primaria por vista; repetir CTA en puntos de decisión.
- Fricción mínima: campos necesarios, rendimiento, sin distracciones que compitan con la meta.

#### Variante rápida (`*-ops`)

Para iteración corta en chat sin brief formal: [{ops_name}]({ops_path}).

#### Contexto de cliente

Parte siempre de `client-dossiers/<dossier_id>/marketing-context.md` (ICP, objeciones, lenguaje del cliente).
"""


def tpl_cro(ctx: dict[str, Any]) -> str:
    titulo = ctx.get("titulo", "CRO")
    focus = ctx.get("focus", "optimizar flujo")
    return f"""### Marco de trabajo ({titulo})

**Objetivo:** {focus}.

#### Enfoque

1. Mapear pasos del flujo y punto de conversión principal.
2. Medir fricción por paso (campos, copy, errores, tiempo).
3. Hipótesis priorizadas (impacto × facilidad).
4. Si hay datos: validar con experimentos (`ab-test-setup`).

#### Contexto dossier-first

`marketing-context.md` define idioma del cliente y objeciones.
"""


def tpl_copy_dual(ctx: dict[str, Any]) -> str:
    ops = ctx.get("ops_path", "../../../jarvis/skills/copywriting-ops/SKILL.md")
    ops_label = ctx.get("ops_label", "copywriting-ops")
    return f"""### Marco de trabajo (copywriting / mensajes)

#### Principios

- Claridad > creatividad; beneficios > features; prueba > adjetivos.
- Una idea por bloque; CTA explícito con siguiente paso.
- Vocabulario del cliente (del dossier), no jerga interna.

#### Variante rápida

[{ops_label}]({ops}) para iteraciones sin dossier completo.

#### Dossier-first

Audiencia, tono, objeciones y pruebas desde `client-dossiers/<dossier_id>/marketing-context.md`.
"""


def tpl_copy(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (edición de copy)

#### Objetivo

Mejorar claridad, ritmo y conversión sin cambiar hechos ni promesas no respaldadas.

#### Checklist

- Titulares específicos; cortar passive voice y redundancia.
- Un solo CTA siguiente por bloque.
- Alinear con voz de marca del dossier.
"""


def tpl_cold_dual(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (cold email)

#### Reglas

- Corto (<150 palabras primer touch); personalización demostrable; un CTA.
- Sin adjuntos en primer email salvo que el prospect lo pida.

#### Variante rápida

[cold-email-ops](../../../jarvis/skills/cold-email-ops/SKILL.md).
"""


def tpl_email_sequences(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (secuencias de email)

#### Diseño

- Objetivo por correo (educar / probar / siguiente micro-compromiso).
- Cadencia y límites anti-spam; valor nuevo en cada touch cuando aplique.
- Coherencia con voz de marca del dossier.
"""


def tpl_pipeline_social(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (contenido social)

#### Pipeline RRSS gratis (Jarvis)

1. [`brand-kit`](../../../../skills/brand-kit/SKILL.md) — validar `brand.json` del dossier.
2. Copy / guion — esta skill + [`copywriting`](../copywriting/SKILL.md).
3. Carruseles estáticos: [`carousel-render`](../../../../skills/carousel-render/SKILL.md); IA opcional: [`image-ai-free`](../../../../skills/image-ai-free/SKILL.md) (**AG-13**).
4. Variante corta de slides: [`carousel-ops`](../../../jarvis/skills/carousel-ops/SKILL.md).

Documentación: [`docs/CAROUSEL_PIPELINE_FREE.md`](../../../../docs/CAROUSEL_PIPELINE_FREE.md), [`docs/REELS_TIKTOK_PIPELINE_FREE.md`](../../../../docs/REELS_TIKTOK_PIPELINE_FREE.md).
"""


def tpl_pipeline_image(_: dict[str, Any]) -> str:
    return """### Enfoques de producción (ecosistema Jarvis)

| Enfoque | Cuándo | Skill local |
|---------|--------|-------------|
| Render determinista | Carruseles OG, layouts | [`image-render`](../../../../skills/image-render/SKILL.md) |
| IA gratuita (online) | Variaciones creativas sin presupuesto | [`image-ai-free`](../../../../skills/image-ai-free/SKILL.md) — **AG-13** |
| Carrusel multi-slide | Varias slides coherentes | [`carousel-render`](../../../../skills/carousel-render/SKILL.md) |
| Identidad | Tipografía/color | [`brand-kit`](../../../../skills/brand-kit/SKILL.md) |

#### Workflow ejemplo (carrusel + marca)

1. `brand-kit validate --dossier <id>`
2. `carousel-render` / `image-render` según docs RRSS.
3. Registrar artefacto con `activity-log`.

#### Nota sobre upstream

El texto upstream puede mencionar herramientas comerciales (Midjourney, APIs de pago). En este holding **prioriza** el stack local/documentado salvo aprobación explícita (**AG-13** / presupuesto).
"""


def tpl_pipeline_video(_: dict[str, Any]) -> str:
    return """### Enfoques de video (ecosistema Jarvis)

| Enfoque | Skill local |
|---------|---------------|
| Voz + subs + montaje | [`tts-free`](../../../../skills/tts-free/SKILL.md) → [`subtitles`](../../../../skills/subtitles/SKILL.md) → [`video-compose`](../../../../skills/video-compose/SKILL.md) |
| Plantilla animada | [`video-short`](../../../../skills/video-short/SKILL.md) |

#### Workflow reel corto (vertical)

1. Frames 9:16 con `image-render` si aplica.
2. `tts-free synthesize --with-subs`
3. `subtitles` (SRT/ASS) al estilo marca.
4. `video-compose render` → MP4 en `out/`.

Doc: [`docs/REELS_TIKTOK_PIPELINE_FREE.md`](../../../../docs/REELS_TIKTOK_PIPELINE_FREE.md).
"""


def tpl_seo_dual(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (SEO audit)

#### Alcance

- Técnico: HTTPS, indexación, CWV, sitemap, robots.
- On-page: title, meta, H1, enlazado interno coherente con intención.
- Contenido: intención de búsqueda y canibalización (resolver antes de escalar).

#### Variante rápida

[seo-audit-ops](../../../jarvis/skills/seo-audit-ops/SKILL.md).
"""


def tpl_seo(ctx: dict[str, Any]) -> str:
    tema = ctx.get("tema", "SEO")
    return f"""### Marco de trabajo ({tema})

Prioriza impacto: intención + autoridad temática + experiencia de página. Usa datos (Search Console) cuando existan.

#### Dossier-first

Keywords y lenguaje del cliente en `client-dossiers/<dossier_id>/marketing-context.md`.
"""


def tpl_paid(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (paid media)

#### Estructura

- Objetivo de negocio → KPI → hipótesis y experimentos.
- Creatividades alineadas con landing (`page-cro`, `copywriting`).
- Medición verificable (`analytics-tracking`).
"""


def tpl_meas(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (medición / experimentos)

#### Principios

- Un evento = una decisión de producto; nombres estables.
- Validar en staging antes de producción.
- Para A/B: tamaño de muestra razonable (`ab-test-setup`).
"""


def tpl_retention(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (retención / churn)

#### Enfoque

- Motivos de cancelación por segmento.
- Flujos save honestos (sin dark patterns).
- Emails transaccionales y recuperación de pagos medidos.
"""


def tpl_growth(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (growth engineering)

#### Principios

- Hipótesis → MVP barato → medición.
- Herramientas gratuitas / contenido evergreen cuando el presupuesto es cero.
"""


def tpl_strat(ctx: dict[str, Any]) -> str:
    nombre = ctx.get("nombre", "Estrategia")
    return f"""### Marco de trabajo ({nombre})

Conecta objetivos de negocio con hipótesis priorizadas y canales. Usa el marketing-context del dossier como fuente de verdad.
"""


def tpl_strat_derived(ctx: dict[str, Any]) -> str:
    label = ctx.get("ops_label", "brainstorming-ops")
    path = ctx.get("ops_path", "../../../jarvis/skills/brainstorming-ops/SKILL.md")
    return f"""### Marco de trabajo (estrategia / ideas)

#### Variante rápida relacionada

[{label}]({path}) — nombre distinto; úsala para sesiones cortas en chat.
"""


def tpl_sales_derived(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (sales enablement)

#### Variante relacionada

[proposal-ops](../../../jarvis/skills/proposal-ops/SKILL.md) para propuestas estructuradas.
"""


def tpl_revops(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (RevOps)

#### Alcance

- Definición de etapas lead → oportunidad → cliente.
- Reglas de routing y SLA entre marketing y ventas.
- Datos mínimos en CRM para decisiones.
"""


def tpl_research_dual(_: dict[str, Any]) -> str:
    return """### Marco de trabajo (investigación de clientes)

#### Modos

1. **Activos existentes**: entrevistas, tickets, encuestas → VOC.
2. **Desk research**: fuentes públicas; automatización web puede requerir **AG-11**.

#### Variante rápida

[deep-interview-ops](../../../jarvis/skills/deep-interview-ops/SKILL.md).
"""


TEMPLATES: dict[str, Any] = {
    "foundation": tpl_foundation,
    "cro_dual": tpl_cro_dual,
    "cro": tpl_cro,
    "copy_dual": tpl_copy_dual,
    "copy": tpl_copy,
    "cold_dual": tpl_cold_dual,
    "email_sequences": tpl_email_sequences,
    "pipeline_social": tpl_pipeline_social,
    "pipeline_image": tpl_pipeline_image,
    "pipeline_video": tpl_pipeline_video,
    "seo_dual": tpl_seo_dual,
    "seo": tpl_seo,
    "paid": tpl_paid,
    "meas": tpl_meas,
    "retention": tpl_retention,
    "growth": tpl_growth,
    "strat": tpl_strat,
    "strat_derived": tpl_strat_derived,
    "sales_derived": tpl_sales_derived,
    "revops": tpl_revops,
    "research_dual": tpl_research_dual,
}


def render_framework(template_key: str, ctx: dict[str, Any]) -> str:
    fn = TEMPLATES[template_key]
    return fn(ctx)
