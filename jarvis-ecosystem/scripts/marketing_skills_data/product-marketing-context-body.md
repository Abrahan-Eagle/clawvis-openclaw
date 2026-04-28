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
