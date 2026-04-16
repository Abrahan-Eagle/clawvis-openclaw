---
name: scenario-analysis-ops
description: "Analisis de escenarios what-if para decisiones estrategicas del holding. Semilla -> contexto -> variables -> escenarios -> informe iterativo con matriz de riesgos y acciones Trello."
---

# Scenario Analysis Ops

Inspirado en el patron semilla-a-informe de simuladores multi-agente (MiroFish et al.), adaptado al ecosistema Jarvis sin motor de simulacion ni dependencias externas. Produce informes de escenarios estructurados e iterables.

## Cuando se activa

- Decisiones estrategicas que afectan mas de una empresa del holding
- Evaluar expansion a nuevo servicio, mercado o cliente grande
- Cambios de pricing o modelo de negocio
- Evaluar riesgos operativos (dependencia de proveedor, cambio de plataforma, contratacion)
- Comparar inversiones alternativas (publicidad vs contenido organico, Workana vs outbound directo)
- Cualquier situacion donde el CEO necesite ver "que pasa si X cambia"

NO usar para:
- Tareas operativas del dia a dia (usar `task-pipeline-ops`)
- Propuestas a clientes (usar `proposal-ops`)
- Brainstorming de ideas (usar `brainstorming-ops`)

## Relacion con otros skills

```
deep-interview-ops  (si el pedido es vago)
        |
        v
scenario-analysis-ops  (este skill)
        |
        v
brainstorming-ops  (para disenar la ejecucion del escenario elegido)
        |
        v
task-pipeline-ops  (para ejecutar)
```

## Prerequisitos obligatorios

**ANTES de analizar:**
1. Leer `GOALS.md` — los escenarios deben evaluarse contra los goals activos
2. Leer `LESSONS.md` — evitar repetir errores documentados
3. Si hay cliente involucrado: leer su dossier en `client-dossiers/`
4. Si hay datos recientes relevantes: consultar MemPalace (`mempalace_search`)
5. Si el tema toca codigo/infra del ecosistema: consultar Graphify

## El proceso

### Fase 1: Definir la semilla

La semilla es la pregunta o situacion que dispara el analisis. Debe ser una frase concreta, no un tema vago.

| Semilla debil | Semilla fuerte |
|---------------|----------------|
| "Mejorar ventas" | "Que pasa si duplicamos el presupuesto de outbound y reducimos Workana a 50%?" |
| "Expandir el holding" | "Que impacto tiene activar dev-agency en Q3 con 2 desarrolladores freelance?" |
| "Competencia" | "Si un competidor ofrece carruseles IG a mitad de precio, como afecta a marketing?" |

Si la semilla es vaga, activar `deep-interview-ops` para acotar antes de continuar.

### Fase 2: Inyeccion de contexto

Recopilar automaticamente:

```
Contexto = {
  goals:     GOALS.md (goals activos de las empresas involucradas),
  pipeline:  Estado actual del pipeline (Trello o ultimo health check),
  dossiers:  Clientes relevantes al escenario,
  memoria:   Decisiones y lecciones recientes (MEMORY.md + LESSONS.md),
  externo:   Si aplica, last30days-openclaw para pulso de mercado
}
```

Documentar el contexto usado en el informe — todo claim debe ser trazable.

### Fase 3: Identificar variables clave

Extraer 3-6 variables que determinan el resultado del escenario. Cada variable necesita:

```
| Variable | Valor actual | Rango posible | Unidad | Controlable? |
|----------|-------------|---------------|--------|--------------|
| Presupuesto outbound | $500/mes | $0 - $2000 | USD | Si |
| Leads Workana / semana | 8 | 2 - 15 | leads | Parcial |
| Win rate propuestas | 18% | 10% - 35% | % | Si (mejorando propuestas) |
| Timeline activacion dev-agency | N/A | Q3 - Q4 2026 | trimestre | Si |
```

**Variables controlables** = las que el holding puede cambiar con una decision.
**Variables parciales** = dependen de factores externos pero se pueden influenciar.
**Variables externas** = fuera de control (mercado, competencia, regulacion).

### Fase 4: Construir escenarios

Minimo 3 escenarios. Cada uno es una combinacion especifica de valores de las variables.

#### Escenario Base (continuidad)

Que pasa si todo sigue como esta. Usar valores actuales de todas las variables.

#### Escenario Optimista

Que pasa si las variables controlables se mueven a favor y las externas son neutrales.

#### Escenario Pesimista

Que pasa si las variables externas se mueven en contra y las controlables tienen el impacto minimo esperado.

#### Escenarios adicionales (opcional)

Si hay una combinacion especifica que el CEO quiere evaluar, agregarla como escenario nombrado.

**Tabla de escenarios:**

```
| Escenario | Var 1 | Var 2 | Var 3 | Resultado estimado | Confianza |
|-----------|-------|-------|-------|--------------------|-----------|
| Base | actual | actual | actual | [resultado] | Alta |
| Optimista | +X | +Y | neutral | [resultado] | Media |
| Pesimista | -X | neutral | -Z | [resultado] | Media |
| [Nombrado] | valor | valor | valor | [resultado] | Baja-Media |
```

**Confianza:** Alta = basado en datos reales; Media = proyeccion razonable; Baja = supuesto sin datos.

### Fase 5: Matriz de riesgos

Para cada escenario, identificar los 3-5 riesgos principales.

```
| Riesgo | Probabilidad | Impacto | Escenario | Mitigacion |
|--------|-------------|---------|-----------|------------|
| [descripcion] | Alta/Media/Baja | Alto/Medio/Bajo | Optimista | [accion concreta] |
| [descripcion] | ... | ... | Pesimista | [accion concreta] |
```

Riesgos con Probabilidad Alta + Impacto Alto = **deal-breakers** que deben resolverse antes de proceder.

### Fase 6: Resumen ejecutivo

Escribir PRIMERO (antes de presentar el informe completo). 5-7 oraciones que responden:

1. Que se analizo (semilla)
2. Que escenario recomiendas y por que
3. Cual es el riesgo principal
4. Que decision necesita el CEO
5. Que goal del holding se avanza

**El resumen ejecutivo va AL INICIO del informe, no al final.**

### Fase 7: Acciones recomendadas

Para el escenario recomendado, listar acciones concretas:

```
| # | Accion | Responsable | Goal | Plazo | Trello |
|---|--------|-------------|------|-------|--------|
| 1 | [accion concreta] | [agente o empresa] | G-XXX | [dias/semana] | Crear tarjeta |
| 2 | ... | ... | ... | ... | ... |
```

Si requiere aprobacion: indicar el gate (`AG-XX`) de `APPROVAL_GATES.md`.

## Protocolo de iteracion

Este es el patron clave que diferencia scenario-analysis de un brainstorming one-shot:

**Cuando el CEO dice "y si cambio X?":**

1. Identificar que variable(s) cambiaron
2. Recalcular SOLO los escenarios afectados (no todo el informe)
3. Actualizar matriz de riesgos si cambian probabilidades
4. Regenerar resumen ejecutivo y acciones
5. Marcar la iteracion:

```
--- Iteracion 2 (variable: presupuesto outbound = $1500) ---
[Nuevo resumen ejecutivo]
[Escenarios actualizados]
[Nuevas acciones si cambian]
```

**Maximo 5 iteraciones** antes de tomar decision. Si despues de 5 iteraciones no hay claridad, escalar: el problema probablemente necesita mas datos, no mas escenarios.

## Plantilla de informe completo

```markdown
# Analisis de Escenarios: [titulo corto]

**Fecha:** YYYY-MM-DD
**Semilla:** [la pregunta original]
**Iteracion:** 1 de N
**Goals relacionados:** G-XXX, G-YYY

## Resumen ejecutivo

[5-7 oraciones: que se analizo, recomendacion, riesgo principal, decision requerida]

## Contexto

- Goals: [cuales aplican]
- Pipeline: [estado relevante]
- Clientes: [dossiers consultados]
- Datos externos: [si se uso last30days u otra fuente]
- Lecciones previas: [si aplican de LESSONS.md]

## Variables clave

| Variable | Valor actual | Rango | Controlable? |
|----------|-------------|-------|--------------|
| ... | ... | ... | ... |

## Escenarios

### Base
[Descripcion + resultado]

### Optimista
[Descripcion + resultado]

### Pesimista
[Descripcion + resultado]

## Tabla comparativa

| Escenario | Var 1 | Var 2 | ... | Resultado | Confianza |
|-----------|-------|-------|-----|-----------|-----------|
| ... | ... | ... | ... | ... | ... |

## Matriz de riesgos

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|-------------|---------|------------|
| ... | ... | ... | ... |

## Acciones recomendadas

| # | Accion | Responsable | Goal | Plazo | Gate |
|---|--------|-------------|------|-------|------|
| ... | ... | ... | ... | ... | ... |

## Decision requerida

[Que necesita decidir el CEO para avanzar]
```

## Donde guardar el informe

- **Trello:** Crear tarjeta en el tablero de la empresa principal involucrada, columna "Review"
- **Disco:** Si el informe es largo o tiene multiples iteraciones: `~/Documents/JARVIS-DOCUMENTS/[empresa]/scenarios/YYYY-MM-DD-[slug].md`
- **Memoria:** Anotar la decision final en `MEMORY.md` una vez que el CEO decida

## Checklist

- [ ] Semilla concreta (no vaga)
- [ ] Contexto inyectado con fuentes citadas
- [ ] 3-6 variables identificadas con valores y rangos
- [ ] Minimo 3 escenarios con tabla comparativa
- [ ] Matriz de riesgos con mitigaciones
- [ ] Resumen ejecutivo AL INICIO
- [ ] Acciones con responsable, goal y plazo
- [ ] Decision requerida explicita para el CEO
- [ ] Si es iteracion: marcada con numero y variable cambiada

## Output esperado

Entregar:
- Informe completo usando la plantilla
- Tabla comparativa de escenarios
- Matriz de riesgos
- Lista de acciones con Trello
- Nota clara de que decision necesita el CEO
- Listo para iterar si el CEO cambia una variable
