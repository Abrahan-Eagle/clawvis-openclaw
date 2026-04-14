---
name: deep-interview-ops
description: "Cuestionamiento socratico estructurado ANTES de ejecutar tareas complejas. Expone supuestos ocultos, mide claridad, y bloquea ejecucion hasta que los requisitos superen el umbral de ambiguedad."
---

# Deep Interview Ops

Adaptado de oh-my-claudecode:deep-interview (Socratic questioning + ambiguity gating). Para operaciones de negocio del ecosistema Jarvis.

## Cuando se activa

- **sales-hunter**: Antes de escribir una propuesta a un cliente nuevo o un proyecto complejo
- **mkt-content**: Antes de lanzar una campana nueva o redisenar presencia digital
- **jarvis**: Antes de cambios operativos que tocan mas de un agente/empresa
- Cualquier tarea donde el pedido sea vago, amplio, o tenga multiples interpretaciones

## Relacion con brainstorming-ops

`brainstorming-ops` propone alternativas y pide aprobacion. `deep-interview-ops` va ANTES: asegura que entendemos el problema antes de proponer soluciones. Secuencia correcta:

```
deep-interview-ops -> brainstorming-ops -> ejecucion
```

Si el pedido ya es claro y especifico, saltar directo a brainstorming-ops.

## Gate de ejecucion

```
NO EJECUTAR SI CLARIDAD < 3.5 / 5.0
```

Si al terminar la entrevista la claridad promedio de las dimensiones es menor a 3.5, NO proceder. Hacer mas preguntas o escalar al CEO.

## Las 6 dimensiones

Evaluar cada dimension con puntaje 1-5 despues de la entrevista.

### 1. Alcance

- Que se incluye y que NO se incluye
- Limites claros del entregable
- Pregunta tipo: "Si tuviera que decir 'esto NO es parte del trabajo', que diria?"

### 2. Criterio de exito

- Como sabremos que esta terminado
- Metricas o indicadores concretos
- Pregunta tipo: "Si entrego esto manana, que revisaria para decir 'esta bien'?"

### 3. Restricciones

- Presupuesto, tiempo, herramientas, plataformas
- Que NO podemos hacer (politica, tecnico, legal)
- Pregunta tipo: "Hay algo que definitivamente NO debo hacer o usar?"

### 4. Dependencias

- Que necesitamos de otros (cliente, otro agente, herramienta externa)
- Que bloquea el arranque
- Pregunta tipo: "Que necesito que me entreguen antes de empezar?"

### 5. Riesgos

- Que puede salir mal
- Plan B si falla el enfoque principal
- Pregunta tipo: "Cual es el peor escenario? Que hariamos?"

### 6. Contexto oculto

- Supuestos no dichos
- Historia relevante (intentos anteriores, relacion con el cliente)
- Pregunta tipo: "Hay algo que deberia saber pero que no es obvio?"

## Scorecard

```
| Dimension         | Puntaje (1-5) | Supuesto detectado | Pregunta pendiente |
|-------------------|---------------|--------------------|--------------------|
| Alcance           |               |                    |                    |
| Criterio de exito |               |                    |                    |
| Restricciones     |               |                    |                    |
| Dependencias      |               |                    |                    |
| Riesgos           |               |                    |                    |
| Contexto oculto   |               |                    |                    |
| **Promedio**      | **/5.0**      |                    |                    |
```

**Umbrales:**
- 4.0+ = Proceder con confianza
- 3.5-3.9 = Proceder con precaucion; documentar supuestos
- < 3.5 = NO proceder; hacer mas preguntas o escalar

## Reglas de entrevista

1. **Una pregunta a la vez** -- no bombardear. Esperar respuesta antes de la siguiente.
2. **Preguntas abiertas** -- "que", "como", "por que", no "si/no".
3. **Resumir antes de seguir** -- "Entonces lo que entiendo es X. Correcto?"
4. **No asumir** -- si algo no se dijo, preguntar. No rellenar con suposiciones.
5. **Documentar** -- anotar cada respuesta; esto alimenta la propuesta/campana/plan.

## Adaptacion por agente

### sales-hunter (calificacion de cliente)

Dimensiones prioritarias: alcance, restricciones (presupuesto/tiempo), criterio de exito.
Preguntas extra:
- "Cual es su presupuesto aproximado?"
- "Cuando necesita esto funcionando?"
- "Ha trabajado con freelancers antes? Que funciono y que no?"
- "Quien toma la decision final?"

### mkt-content (planificacion de campana)

Dimensiones prioritarias: criterio de exito, alcance, contexto oculto.
Preguntas extra:
- "Que queremos que haga la audiencia despues de ver esto?"
- "Hay contenido anterior que funciono bien? Que no funciono?"
- "Cuanto contenido necesitamos y para cuando?"

### jarvis (cambios operativos)

Dimensiones prioritarias: dependencias, riesgos, alcance.
Preguntas extra:
- "Que agentes se ven afectados?"
- "Se puede revertir si algo sale mal?"
- "Hay ventana de mantenimiento o se hace en caliente?"

## Checklist antes de proceder

- [ ] Evalúe las 6 dimensiones con puntaje
- [ ] Promedio >= 3.5
- [ ] Supuestos detectados estan documentados
- [ ] No hay preguntas criticas sin responder
- [ ] El resultado de la entrevista esta en Trello/memory segun corresponda

## Output esperado

Entregar:
- Scorecard con puntajes por dimension
- Lista de supuestos detectados
- Resumen de requisitos claros (input para brainstorming-ops)
- Decision: proceder / mas preguntas / escalar
