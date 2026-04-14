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
| Seccion              | Items OK | Items Total | Score |
|----------------------|----------|-------------|-------|
| SEO Tecnico          |          | 9           |       |
| SEO On-Page          |          | 9           |       |
| Contenido            |          | 4           |       |
| Canibalizacion       |          | 3           |       |
| Keyword Clusters     |          | 2           |       |
| Link Building / EEAT |          | 2           |       |
| **Total**            |          | **29**      |       |
```

## D. Cannibalization Audit (BLOQUEANTE)

**OBLIGATORIO antes de optimizar cualquier pagina.** Si dos paginas compiten por la misma keyword, optimizar una empeora la otra.

### Paso 1: Cross-Page Query Map

Para cada keyword target, verificar en Search Console (dimensions: page + query) cuantas paginas rankean para ella.

```
| Query | Pagina A | Pos A | Clicks A | Pagina B | Pos B | Clicks B | Conflicto? |
|-------|----------|-------|----------|----------|-------|----------|------------|
```

### Paso 2: Asignar ownership

Para cada conflicto, asignar UNA pagina duena basandose en:
- Cual tiene mas clicks/impresiones para esa query
- Cual es el match semantico mas cercano
- Cual es el pilar/satelite designado para ese tema

### Paso 3: Resolver

- Eliminar/reducir contenido competidor de la pagina no-duena
- Agregar internal links DESDE la no-duena HACIA la duena
- Asegurar que title tags y H1s no se superpongan en keywords primarias
- Verificar que canonical tags son self-referencing

**Si hay canibalizacion activa (2+ paginas en top 20 para la misma query con clicks divididos), resolver ANTES de crear contenido nuevo o optimizar.**

## E. Keyword Cluster Framework

Organizar keywords en clusters (pilar + satelites) para evitar canibalizacion y maximizar autoridad tematica.

```
PILLAR PAGE: [keyword principal, alto volumen]
├── Satelite 1: [long-tail informacional] -> blog post
├── Satelite 2: [long-tail comercial] -> pagina de servicio
├── Satelite 3: [long-tail transaccional] -> landing page
└── Satelite 4: [pregunta PAA] -> seccion FAQ
```

Cada satelite enlaza al pilar. El pilar enlaza a todos los satelites. Nunca dos paginas del cluster comparten keyword principal.

### Intent mapping

| Keyword | Volumen | Intent | URL target | Tipo contenido |
|---------|---------|--------|------------|----------------|
| [head term] | Alto | Informacional | /pilar | Guia completa |
| [long-tail 1] | Medio | Comercial | /servicio | Pagina de servicio |
| [long-tail 2] | Bajo | Transaccional | /landing | Landing page |

## F. Link Building Plan

### Tacticas por tipo

| Tipo | Links/mes target | DR minimo | Approach |
|------|------------------|-----------|----------|
| Digital PR | 3-5 | 50+ | Datos originales, comentario experto |
| Content-led | 5-10 | 40+ | Guias definitivas, herramientas, casos de estudio |
| Outreach | 3-5 | 40+ | Broken links, menciones sin enlace, resource pages |

### E-E-A-T (obligatorio)

Todo contenido debe demostrar:
- **Experience**: experiencia real con el tema
- **Expertise**: conocimiento tecnico demostrable
- **Authoritativeness**: reconocimiento externo (backlinks, menciones)
- **Trustworthiness**: precision, fuentes citadas, HTTPS, politica de privacidad

## Prioridades de accion

Ordenar hallazgos por:
1. **Canibalizacion activa** -- resolver PRIMERO
2. **Alta prioridad + rapido de arreglar** -- hacer esta semana
3. **Alta prioridad + requiere desarrollo** -- planificar sprint
4. **Media/baja prioridad** -- backlog

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
- [ ] Complete cannibalization audit (es BLOQUEANTE)
- [ ] Defini keyword clusters (pilar + satelites)
- [ ] Revise E-E-A-T compliance
- [ ] El scorecard esta completo (29 items)
- [ ] Las recomendaciones estan priorizadas (canibalizacion primero)
- [ ] Incluyo keywords target basadas en customer language

## Output esperado

Entregar:
- Scorecard completo (29 items)
- Cannibalization report con ownership y resoluciones
- Keyword cluster map (pilar + satelites por tema)
- Top-5 hallazgos priorizados con recomendacion
- Link building plan mensual
- Proximos pasos concretos
