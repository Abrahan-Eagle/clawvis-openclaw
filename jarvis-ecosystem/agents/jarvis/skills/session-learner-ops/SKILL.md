---
name: session-learner-ops
description: "Despues de completar tareas significativas: extraer patrones reutilizables, lecciones concretas, y proponer mejoras. Solo patrones reproducibles, no generalidades."
---

# Session Learner Ops

Adaptado de oh-my-claudecode:learner. Para mejora continua del ecosistema Jarvis.

## Cuando se activa

- Despues de completar un proyecto de cliente (propuesta enviada, entrega hecha)
- Despues de resolver un problema operativo complejo
- Despues de un modulo forense (como este)
- Cuando un proceso fallo y se corrigio (la correccion es el patron)
- Al cierre de semana/sprint si hubo trabajo significativo

NO activar para tareas rutinarias o triviales.

## Que extraer

### Patrones reutilizables

Algo que funciono y se puede repetir en situaciones similares.

```
Buen patron:
"Cuando el cliente no responde en 3 dias, enviar follow-up con nuevo
angulo (beneficio diferente). Tasa de respuesta mejora ~40%."

Mal patron (demasiado generico):
"La comunicacion es importante."
```

### Lecciones concretas

Algo que aprendimos que NO sabiamos antes.

```
Buena leccion:
"Workana rechaza propuestas sin precio explicito, incluso si el brief
dice 'presupuesto a convenir'. Siempre incluir rango de precio."

Mala leccion (obvia):
"Hay que leer el brief antes de responder."
```

### Mejoras propuestas

Cambios concretos al ecosistema basados en lo aprendido.

```
Buena propuesta:
"Agregar campo 'presupuesto_min' al template de propuesta en cold-email-ops."

Mala propuesta (vaga):
"Mejorar el proceso de ventas."
```

## Quality gates

Un aprendizaje solo se documenta si cumple TODOS estos criterios:

1. **Concreto** -- describe una situacion especifica, no un principio abstracto
2. **Reproducible** -- si la situacion se repite, el patron aplica igual
3. **Accionable** -- alguien puede actuar basandose en esto
4. **Nuevo** -- no es algo que ya estaba documentado en un skill existente

Si no cumple los 4, no documentar. Mejor pocos patrones buenos que muchos genericos.

## Proceso

### Paso 1: Revisar la tarea completada

- Que se hizo
- Que funciono como esperado
- Que no funciono y como se corrigio
- Cuanto tiempo tomo vs lo estimado

### Paso 2: Extraer candidatos

Para cada hallazgo, evaluar contra los 4 quality gates.

### Paso 3: Clasificar

| Tipo | Donde documentar | Ejemplo |
|------|------------------|---------|
| **Patron de proceso** | `memory/learnings.md` del agente | "Follow-up dia 3 con nuevo angulo" |
| **Leccion de plataforma** | `memory/learnings.md` del agente | "Workana requiere precio explicito" |
| **Mejora a skill existente** | Issue / nota en MEMORY.md | "Agregar campo X a cold-email-ops" |
| **Skill nuevo propuesto** | Nota en MEMORY.md para CEO | "Crear skill de proposal-template-ops" |
| **Bug o workaround** | `memory/learnings.md` + tarjeta en Trello | "OpenClaw timeout en X; workaround: Y" |

### Paso 4: Documentar

Formato para `memory/learnings.md`:

```markdown
## [YYYY-MM-DD] <titulo corto>

**Contexto:** <que tarea se estaba haciendo>
**Hallazgo:** <que descubrimos>
**Patron/Leccion:** <regla extraida>
**Accion:** <que cambiar o que tener en cuenta>
```

### Paso 5: Proponer cambios (si aplica)

Si el patron justifica un cambio al ecosistema:
1. Documentar la propuesta en MEMORY.md seccion "Propuestas pendientes"
2. Esperar aprobacion del CEO antes de implementar
3. Si se aprueba, usar brainstorming-ops + task-pipeline-ops

## Checklist

- [ ] Revise la tarea completada
- [ ] Extraje candidatos evaluados contra los 4 quality gates
- [ ] Solo documente patrones concretos, reproducibles, accionables y nuevos
- [ ] Clasifique cada hallazgo en el tipo correcto
- [ ] Documente en el lugar correcto (memory/learnings.md o MEMORY.md)
- [ ] Si hay propuesta de cambio, esta en MEMORY.md esperando aprobacion

## Anti-patrones

- Documentar todo "por si acaso" -> ruido, nadie lo lee
- Lecciones tipo "hay que comunicar mejor" -> demasiado vago
- Proponer skills nuevos para cada leccion -> inflacion de skills
- No revisar learnings anteriores -> se repiten patrones ya documentados
