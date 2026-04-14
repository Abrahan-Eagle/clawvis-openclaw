# Forense Skills Repos — Resumen

*Modulo completado: abril 2026*

## Repos analizados

| Repo | Stars | Foco |
|------|-------|------|
| [anthropics/skills](https://github.com/anthropics/skills) | 117k | Skills oficiales Anthropic: documentos, MCP builder, brand guidelines, webapp testing. Especificacion Agent Skills. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 53.8k | Coleccion curada: lead-research, competitive-ads, content-research, twitter-optimizer, +78 automatizaciones SaaS via Composio. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 21.1k | 35+ skills de marketing: CRO, copywriting, SEO audit, cold email, paid ads, pricing, referral. Patron central: product-marketing-context. |

## Patron clave adoptado: Product Marketing Context

`marketingskills` tiene un patron donde un archivo central (`product-marketing-context`) define producto, audiencia, diferenciacion, voz, objeciones y customer language. **Todos los demas skills lo leen primero.** Esto garantiza coherencia y evita que cada skill pregunte lo mismo.

Implementado en: `.agents/product-marketing-context.md` (raiz del jarvis-ecosystem).

## Que se adopto

| Skill | Fuente | Ubicacion | Agentes que lo usan |
|-------|--------|-----------|---------------------|
| **product-marketing-context** | marketingskills | `.agents/product-marketing-context.md` | Todos (ventas + marketing) |
| **copywriting-ops** | marketingskills | `agents/jarvis/skills/copywriting-ops/SKILL.md` | mkt-content, sales-hunter |
| **cold-email-ops** | marketingskills | `agents/jarvis/skills/cold-email-ops/SKILL.md` | sales-hunter |
| **page-cro-ops** | marketingskills | `agents/jarvis/skills/page-cro-ops/SKILL.md` | mkt-content, mkt-analytics |
| **lead-research-ops** | awesome-claude-skills | `agents/jarvis/skills/lead-research-ops/SKILL.md` | sales-hunter |
| **seo-audit-ops** | marketingskills | `agents/jarvis/skills/seo-audit-ops/SKILL.md` | mkt-content, mkt-analytics |

## Que NO se adopto (y por que)

| Patron | Fuente | Razon |
|--------|--------|-------|
| Composio / 78 SaaS automations | awesome-claude-skills | Requiere API key de Composio + dependencia externa fuerte |
| Document skills (docx/pdf/pptx) | anthropics/skills | Pesados; no necesarios en esta fase |
| Dev tools (MCP builder, webapp testing) | anthropics/skills + awesome-claude-skills | No aplican hasta que dev-agency este activa |
| twitter-algorithm-optimizer | awesome-claude-skills | Solo util cuando haya cuenta X activa del holding |
| paid-ads, pricing-strategy, ab-test-setup | marketingskills | Buenos pero no prioritarios; adoptables luego |

## Archivos creados / modificados

**Creados:**
- `.agents/product-marketing-context.md` — contexto central de producto, audiencia, voz, objeciones
- `agents/jarvis/skills/copywriting-ops/SKILL.md` — copy para landing, homepage, redes, propuestas
- `agents/jarvis/skills/cold-email-ops/SKILL.md` — emails frios, propuestas Workana, follow-ups
- `agents/jarvis/skills/page-cro-ops/SKILL.md` — framework 7 dimensiones para CRO
- `agents/jarvis/skills/lead-research-ops/SKILL.md` — scoring de leads, ICP, estrategia de contacto
- `agents/jarvis/skills/seo-audit-ops/SKILL.md` — checklist SEO tecnico + on-page
- `docs/FORENSE_SKILLS_REPOS_RESUMEN.md` — este archivo

**Modificados:**
- `agents/ventas/AGENTS.md` — seccion "Skills de marketing y ventas" (cold-email, lead-research, copywriting)
- `agents/marketing/AGENTS.md` — seccion "Skills de marketing y ventas" (copywriting, page-cro, seo-audit)
- `agents/jarvis/MEMORY.md` — log de decisiones
- `docs/OPERACION_POST_GOBIERNO.md` — enlace al modulo
- `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md` — seccion de respaldo

## Impacto en el ecosistema

1. **Coherencia de marca:** todos los agentes de ventas y marketing leen el mismo product-marketing-context antes de actuar.
2. **Outreach estructurado:** sales-hunter tiene framework para emails frios + scoring de leads.
3. **Contenido optimizado:** mkt-content puede escribir copy con formulas probadas y auditar SEO/CRO.
4. **Escalable:** cuando se activen nuevos skills (paid-ads, pricing, etc.), siguen el mismo patron de leer product-marketing-context primero.
