# SEO Audit Ops

*Adaptado de marketingskills/seo-audit para el ecosistema Jarvis*

## Trigger

Usar este skill cuando el agente necesite:
- Auditar el SEO de una pagina web propia (Aiblock, landing de servicios)
- Auditar el SEO de la pagina de un cliente (como parte de un servicio)
- Evaluar oportunidades SEO antes de una propuesta comercial
- Revisar cambios en una pagina antes de publicarla

## Prerequisito obligatorio

**ANTES de auditar, leer:**
`jarvis-ecosystem/.agents/product-marketing-context.md`

Extraer: servicios, audiencia, palabras que usan los clientes. Esto define las keywords target.

## Checklist SEO

### A. SEO Tecnico

| Item | Verificar | Prioridad |
|------|-----------|-----------|
| HTTPS activo | El sitio carga con https:// sin errores de certificado | Alta |
| Mobile-friendly | Responsive, texto legible sin zoom, botones tapables | Alta |
| Velocidad | Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1 | Alta |
| Sitemap XML | Existe, esta actualizado, enviado a Search Console | Media |
| Robots.txt | No bloquea paginas importantes | Media |
| URLs limpias | Sin parametros innecesarios, descriptivas, con guiones | Media |
| Canonical tags | Paginas con contenido duplicado tienen canonical correcto | Media |
| 404 / broken links | No hay links rotos internos ni externos | Baja |
| Structured data | Schema.org basico: Organization, Service, FAQ | Baja |

### B. SEO On-Page

| Item | Verificar | Prioridad |
|------|-----------|-----------|
| Title tag | 50-60 chars, keyword principal, unico por pagina | Alta |
| Meta description | 150-160 chars, CTA implicito, keyword incluida | Alta |
| H1 | Uno solo por pagina, contiene keyword principal | Alta |
| Jerarquia de headings | H2 > H3 logicos, sin saltos | Media |
| Alt text en imagenes | Descriptivo, con keyword si es natural | Media |
| Internal linking | Las paginas importantes estan enlazadas entre si | Media |
| Keyword density | Natural (1-2%), sin keyword stuffing | Media |
| Content length | Minimo 300 palabras por pagina indexable | Baja |
| Open Graph tags | Title, description, image para social sharing | Baja |

### C. Contenido y Keywords

| Item | Verificar | Prioridad |
|------|-----------|-----------|
| Keyword research | Hay lista de keywords target basada en customer language | Alta |
| Search intent | El contenido responde lo que el usuario busca | Alta |
| Contenido actualizado | La informacion es vigente | Media |
| Blog / recursos | Hay contenido que atrae trafico informacional | Baja |

## Scorecard

```
| Seccion         | Items OK | Items Total | Score |
|-----------------|----------|-------------|-------|
| SEO Tecnico     |          | 9           |       |
| SEO On-Page     |          | 9           |       |
| Contenido       |          | 4           |       |
| **Total**       |          | **22**      |       |
```

## Prioridades de accion

Ordenar hallazgos por:
1. **Alta prioridad + rapido de arreglar** -- hacer esta semana
2. **Alta prioridad + requiere desarrollo** -- planificar sprint
3. **Media/baja prioridad** -- backlog

## Herramientas sugeridas

- Google Search Console (indexacion, errores, queries)
- PageSpeed Insights (Core Web Vitals)
- Google Rich Results Test (structured data)
- Screaming Frog o similar (crawl tecnico)

## Checklist antes de entregar

- [ ] Lei product-marketing-context.md
- [ ] Verifique todos los items del checklist tecnico
- [ ] Verifique todos los items on-page
- [ ] Evalúe contenido y keywords
- [ ] El scorecard esta completo
- [ ] Las recomendaciones estan priorizadas
- [ ] Incluyo keywords target basadas en customer language

## Output esperado

Entregar:
- Scorecard completo
- Top-5 hallazgos priorizados con recomendacion
- Lista de keywords target sugeridas
- Proximos pasos concretos
