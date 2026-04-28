---
name: product-marketing-context
description: "Crea y mantiene el documento de contexto de marketing (producto, audiencia, posicionamiento) que el resto de skills debe leer primero. EN: marketing context, ICP, positioning, set up context"
metadata:
  version: "1.1.0"
  jarvis_ecosystem: "2026-04-28"
  upstream_version: "1.1.0"
---

> Adaptado de [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Atribución preservada.

## Resumen

Crea y mantiene el documento de contexto de marketing (producto, audiencia, posicionamiento) que el resto de skills debe leer primero.

### Cuándo usarla (disparadores)

- **ES:** `contexto de marketing`, `ICP`, `posicionamiento`, `marketing-context.md`, `antes de copy`
- **EN:** `marketing context`, `ICP`, `positioning`, `set up context`


### Contexto obligatorio (dossier-first)

1. Cliente con dossier: `client-dossiers/<dossier_id>/marketing-context.md`.
2. Sin cliente: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Crear/actualizar contexto con [`product-marketing-context`](../product-marketing-context/SKILL.md) si falta.

**No** uses rutas legacy fuera de `client-dossiers/` o `.agents/` como fuente canónica del contexto de marketing.


### Variante rápida en Jarvis (`*-ops`)

No hay `*-ops` homónima en Jarvis para esta skill; usa la skill completa y skills globales (`brand-kit`, `carousel-render`, …).

## Frameworks / metodología

## Contexto obligatorio (dossier-first)

1. **Cliente con dossier**: documento canónico `client-dossiers/<dossier_id>/marketing-context.md`.
2. **Sin cliente (holding Jarvis)**: `jarvis-ecosystem/.agents/product-marketing-context.md`.
3. Plantilla vacía: [`.agents/product-marketing-context.md.template`](../../../../.agents/product-marketing-context.md.template).

**No** uses rutas legacy fuera del dossier o de `.agents/` para el contexto canónico; migra cualquier borrador antiguo al dossier o a `.agents/product-marketing-context.md`.

Snippet de comprobación:

```bash
cd jarvis-ecosystem
ls -la client-dossiers/<dossier_id>/marketing-context.md 2>/dev/null || true
ls -la .agents/product-marketing-context.md 2>/dev/null || true
grep -n "marketing-context" client-dossiers/*/marketing-context.md 2>/dev/null | head
```

## Flujo de trabajo

1. Detectar si ya existe contexto (dossier o `.agents/`).
2. Si existe: resume secciones cubiertas y pregunta qué actualizar.
3. Si no: (a) auto-borrador desde README / dossier / `brand.json` o (b) entrevista guiada por secciones.

## Plantilla embebida (resumen)

Usa la plantilla del repo para no omitir campos; las 12 secciones detalladas están en el bloque siguiente (y en la plantilla `.template`).


## Las 12 secciones (detalle operativo)

### 1) Producto — visión en una frase

- **One-liner**: qué es y para quién en una línea.
- **Categoría** del producto y vecinos cercanos (para positioning).
- **Modelo de negocio** (SaaS usage-based, seat-based, marketplace take rate…).

### 2) Audiencia — ICP y JTBD

- **ICP ideal** vs rangos aceptables (tamaño, sector, madurez tech).
- **Jobs-to-be-done** funcionales y emocionales.
- **Quién decide** vs quién usa día a día en B2B.

### 3) Personas B2B (si aplica)

Por rol: objetivos, KPIs, objeciones típicas, vocabulario que resuenan.

### 4) Dolores — problema real

Antes/después, costes del status quo, errores frecuentes del cliente.

### 5) Competencia — mapa

Directos, indirectos, alternativas DIY/hoja de cálculo. Qué reclaman vs qué demuestran.

### 6) Diferenciación y prueba

Pillares defensibles; evidencias (métricas, diseño, velocidad, soporte). Evitar adjetivos sin prueba.

### 7) Objeciones y anti-persona

Fricciones de compra (precio, seguridad, tiempo de setup). Anti-persona: quién **no** debe comprar.

### 8) Switching dynamics — cuatro fuerzas

Push del status quo, pull del producto, hábitos que frenan, ansiedad del cambio.

### 9) Lenguaje del cliente (verbatim)

Frases reales de llamadas/emails/support (sin inventar). Glosario prohibido vs palabras que sí usan.

### 10) Voz de marca

Tono (directo/técnico/cálido), ritmo de frase, nivel de humor, lista negra de clichés.

### 11) Proof points

Logos (si hay), testimonios anonimizables, benchmarks internos, certificaciones.

### 12) Metas y conversión principal

North-star para marketing (pipeline SQL, activación, revenue). **Una** conversión principal por vista cuando aplique.

## Ejemplos por tipo de cliente

### B2B SaaS

Enfatiza proceso de compra multi-stakeholder, seguridad, evidencias de ROI, ciclo de pilotos.

### B2C / prosumer

Enfatiza beneficio emocional rápido, prueba social masiva, políticas claras (envíos, garantías).

### E‑commerce / marketplace

Enfatiza confianza (pagos, stock, SLA), políticas de devolución, prueba en PDP y checkout.

## Snippet dossier-first (bash)

```bash
DOSSIER_ID=\"cli-DEMO-rrss\"
CTX=\"client-dossiers/${DOSSIER_ID}/marketing-context.md\"
test -f \"$CTX\" && echo \"OK: $CTX\" || echo \"FALTA: crear $CTX con esta skill\"
```

### Hooks al pipeline Jarvis

| Skill / doc | Rol |
|-------------|-----|
| [`brand-kit`](../../../../skills/brand-kit/SKILL.md) | Identidad `brand.json` del dossier |
| [`activity-log`](../../../../skills/global/activity-log/SKILL.md) | Traza de tareas/eventos |
| [`handoff`](../../../../skills/global/handoff/SKILL.md) | Pass entregables entre agentes |


## Puertas de aprobación

- Sin gates extra por defecto; ante reputación/pagos/datos sensibles revisa [`docs/APPROVAL_GATES.md`](../../../../docs/APPROVAL_GATES.md).

## Coordinación (comandos reales)

Ejecutar desde la raíz del repo `jarvis-ecosystem/` (ajusta rutas si tu cwd es otro).

**1) Iniciar tarea**

```bash
bash skills/global/activity-log/bin/activity-log start \
  --agent marketing \
  --title "Brief / entrega skill" \
  --dossier <DOSSIER_ID> \
  --ref marketing-context
```

**2) Registrar hito / artefacto**

```bash
bash skills/global/activity-log/bin/activity-log event \
  --task <TASK_ID> \
  --agent marketing \
  --kind milestone \
  --note "Descripción breve del entregable"
```

**3) Handoff al siguiente rol**

```bash
bash skills/global/handoff/bin/handoff create \
  --from marketing \
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

- [`copywriting`](../copywriting/SKILL.md)
- [`page-cro`](../page-cro/SKILL.md)
- [`customer-research`](../customer-research/SKILL.md)


## Referencias

- Texto upstream original (inglés): [`references/upstream-en.md`](references/upstream-en.md).
- Herramientas documentadas upstream: [`docs/upstream-marketingskills/tools/`](../../../../docs/upstream-marketingskills/tools/).
