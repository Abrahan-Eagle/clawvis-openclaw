---
name: structured-commits-ops
description: "Commits con trailers de decision: Constraint, Rejected, Directive, Confidence, Scope-risk. Crea un log de decisiones dentro del historial git."
---

# Structured Commits Ops

Adaptado de oh-my-claudecode git trailers. Para commits en el ecosistema Jarvis.

## Cuando se activa

- Commits que involucran decisiones de diseno o arquitectura
- Cambios a configuracion del ecosistema (openclaw.json, AGENTS.md, etc.)
- Nuevos skills, ClawFlows o integraciones
- Cualquier cambio donde se eligio una opcion sobre otra
- Obligatorio para dev-agency cuando se active

NO usar para commits triviales (typos, formato, actualizacion de docs sin decision).

## Formato

```
<tipo>(<scope>): <descripcion corta>

<cuerpo opcional: contexto, razon del cambio>

Constraint: <restriccion activa que moldeo esta decision>
Rejected: <alternativa considerada> | <razon de rechazo>
Directive: <advertencia o instruccion para futuros modificadores>
Confidence: high | medium | low
Scope-risk: narrow | moderate | broad
Not-tested: <escenario no cubierto por verificacion>
```

## Trailers disponibles

| Trailer | Cuando usarlo | Ejemplo |
|---------|---------------|---------|
| `Constraint:` | Restriccion que forzo la decision | `Constraint: Workana no permite adjuntos en propuestas` |
| `Rejected:` | Alternativa descartada + razon | `Rejected: Scraping automatico \| viola TOS de Workana` |
| `Directive:` | Advertencia para quien toque este codigo despues | `Directive: No cambiar el formato sin revisar APPROVAL_GATES` |
| `Confidence:` | Nivel de certeza en la decision | `Confidence: medium` |
| `Scope-risk:` | Cuanto abarca el cambio | `Scope-risk: broad` (toca 3+ agentes) |
| `Not-tested:` | Que no se verifico | `Not-tested: Heartbeat con timezone diferente a America/Caracas` |

## Reglas

1. **Incluir trailers solo cuando apliquen** -- no forzar trailers en commits triviales
2. **Minimo para commits con decision:** `Confidence:` + `Scope-risk:`
3. **Si rechazaste una alternativa:** incluir `Rejected:` siempre (es el mas valioso)
4. **Subject line:** conventional commits (`feat`, `fix`, `docs`, `refactor`, `chore`)
5. **Scope:** empresa o area (`ventas`, `marketing`, `jarvis`, `ecosystem`, `config`)

## Ejemplos

### Cambio operativo

```
feat(ventas): agregar scoring de leads al pipeline

Lead-research-ops evalua leads con ICP y 5 factores ponderados.
Clasificacion Hot/Warm/Cold/Skip para priorizar esfuerzo.

Constraint: Solo usar datos publicos de Workana (perfil, reviews)
Rejected: Scraping automatico de perfiles | viola TOS
Rejected: Scoring manual sin formula | inconsistente entre sesiones
Directive: Si Workana cambia la estructura del perfil, revisar lead-research-ops
Confidence: high
Scope-risk: narrow
```

### Cambio de configuracion

```
fix(config): corregir timezone de heartbeats a America/Caracas

Heartbeats estaban usando UTC, causando activaciones fuera de horario.

Constraint: Todos los agentes operan en horario de Venezuela (UTC-4)
Rejected: Dejar en UTC y ajustar las horas | confuso para el CEO
Confidence: high
Scope-risk: moderate
Not-tested: Cambio de horario de verano (Venezuela no usa DST)
```

### Nuevo skill

```
feat(ecosystem): agregar deep-interview-ops skill

Cuestionamiento socratico antes de tareas complejas.
6 dimensiones, gate de claridad >= 3.5/5.

Constraint: No bloquear tareas simples con entrevista innecesaria
Rejected: Fusionar con brainstorming-ops | responsabilidades distintas
Directive: deep-interview va ANTES de brainstorming-ops en la secuencia
Confidence: high
Scope-risk: narrow
```

## Checklist antes de commit

- [ ] Subject line sigue conventional commits
- [ ] Si hubo decision: hay al menos Confidence + Scope-risk
- [ ] Si se descarto alternativa: hay Rejected con razon
- [ ] Directive presente si alguien podria romper algo al modificar
- [ ] No hay secretos ni tokens en el mensaje
