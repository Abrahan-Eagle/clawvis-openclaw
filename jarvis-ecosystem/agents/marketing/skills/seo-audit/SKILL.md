---
name: seo-audit
description: "Auditoría SEO técnica, on-page y de contenido con priorización accionable. EN: SEO audit, technical SEO"
metadata:
  version: "1.2.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.2.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Auditoría SEO técnica, on-page y de contenido con priorización accionable.

### Cuándo usarla (disparadores)

- **ES:** `auditoría SEO`, `Search Console`, `indexación`
- **EN:** `SEO audit`, `technical SEO`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

Variante corta **ops**: [`seo-audit-ops`](../../../jarvis/skills/seo-audit-ops/SKILL.md). Usa **esta skill completa** con dossier/brief formal.

## Frameworks / metodología

### Marco de trabajo (SEO audit)

#### Alcance

- Técnico: HTTPS, indexación, CWV, sitemap, robots.
- On-page: title, meta, H1, enlazado interno coherente con intención.
- Contenido: intención de búsqueda y canibalización (resolver antes de escalar).

#### Variante rápida

[seo-audit-ops](../../../jarvis/skills/seo-audit-ops/SKILL.md).


### Hooks al pipeline Jarvis

| Skill / doc | Rol |
|-------------|-----|
| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |
| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |
| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |


## Puertas de aprobación

- **AG-11**: automatizar dominio nuevo en Playwright / scraping → aprobación antes de `BROWSER_PLAYWRIGHT_ALLOW`.

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent mkt-seo \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref seo
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent mkt-seo \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from mkt-seo \
  --to mkt-content \
  --schema research-to-strategy \
  --task <TASK_ID> \
  --payload-file /tmp/handoff-payload.json
```

**4) Cerrar**

```bash
bash skills/global/activity-log/bin/activity-log end \
  --task <TASK_ID> \
  --note "Listo para revisión CEO/cliente"
```

Lista de schemas: `bash skills/global/handoff/bin/handoff schemas`.


### Skills relacionadas (mapa local)

- [`ai-seo`](../ai-seo/SKILL.md)
- [`site-architecture`](../site-architecture/SKILL.md)
- [`schema-markup`](../schema-markup/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
