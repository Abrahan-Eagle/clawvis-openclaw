---
name: deep-interview-ops
description: "Cuestionamiento socratico estructurado ANTES de ejecutar tareas complejas. Expone supuestos ocultos, mide claridad, y bloquea ejecucion hasta que los requisitos superen el umbral de ambiguedad."
metadata:
  version: "1.0.0"
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

## Frameworks de venta (para sales-hunter)

Cuando la entrevista es con un prospect o cliente, usar estos 3 frameworks complementarios. Cada uno ilumina una dimension diferente del problema del comprador.

### SPIN Selling

Secuencia de preguntas que va de contexto a impacto:

**S - Situation** (contexto, usar con moderacion -- investigar antes)
- "Como maneja su equipo [proceso] actualmente?"
- "Que herramientas usa para [funcion]?"

**P - Problem** (superficie del dolor)
- "Donde se rompe ese proceso?"
- "Que es lo mas frustrante de como funciona hoy?"

**I - Implication** (expandir el dolor -- aqui se ganan los deals)
- "Cuando eso falla, cual es el impacto en [equipo/metrica]?"
- "Si esto sigue asi 6 meses mas, que le cuesta?"
- "Quien mas en la organizacion siente los efectos?"

**N - Need-Payoff** (el comprador articula el valor)
- "Si pudiera resolver eso, que se desbloquea para su equipo?"
- "Como cambiaria su capacidad de lograr [meta]?"

Las preguntas de Implicacion son las mas importantes y las que mas se saltan.

### Gap Selling

La venta es el gap entre el estado actual y el estado deseado. Mientras mas grande y preciso el gap, mas urgencia.

```
ESTADO ACTUAL (donde estan)
├── Herramientas y procesos actuales
├── Que esta roto, lento o faltante
├── Impacto medible (revenue, costo, riesgo, personas)
└── Causa raiz (POR QUE existe el problema)

ESTADO FUTURO (donde quieren estar)
├── Como se ve "resuelto" en terminos concretos
├── Que metricas cambian y cuanto
└── Timeline para necesitarlo

EL GAP (la venta)
├── Distancia entre actual y futuro
├── Costo de quedarse como estan
└── Pueden cerrar el gap sin nosotros? (si si, no hay deal)
```

La pregunta de **causa raiz** es la mas importante y la mas ignorada. Problemas superficiales no crean urgencia; causas raiz si.

### Sandler Pain Funnel

3 niveles de profundidad, cada uno mas profundo:

**Nivel 1 -- Dolor tecnico/funcional**
- "Cuentame mas sobre eso"
- "Dame un ejemplo"
- "Hace cuanto tiempo pasa esto?"

**Nivel 2 -- Impacto de negocio (cuantificable)**
- "Cuanto le ha costado al negocio?"
- "Que han intentado y por que no funciono?"

**Nivel 3 -- Stakes personales/emocionales**
- "Como afecta esto a tu equipo dia a dia?"
- "Que pasa con [tu meta/iniciativa] si esto no se resuelve?"

La mayoria de vendedores nunca llegan al Nivel 3. Pero las decisiones de compra son emocionales con justificaciones racionales.

## Manejo de objeciones: Framework AECR

Las objeciones son informacion diagnostica, no ataques.

**A - Acknowledge** (validar sin estar de acuerdo)
- "Es una preocupacion valida."

**E - Empathize** (mostrar que entiendes por que lo sienten)
- "Si yo estuviera en tu lugar y hubiera tenido una mala experiencia con [similar], tambien seria esceptico."

**C - Clarify** (preguntar para entender la objecion real)
- "Que especificamente te preocupa de [tema]?"
- "Cuando dices que el timing no es bueno, es tema de presupuesto, de bandwidth, o de otra cosa?"

**R - Reframe** (ofrecer nueva perspectiva basada en lo aprendido)
- "Lo que escucho es [preocupacion real]. Asi lo han manejado otros equipos en tu situacion..."

| Objecion | Frecuencia | Lo que realmente significa |
|----------|------------|--------------------------|
| Presupuesto/valor | ~48% | "No estoy convencido del ROI" o "no controlo el presupuesto" |
| Timing | ~32% | "No es prioridad ahora" o "estoy saturado" |
| Competencia | ~20% | "Necesito justificar por que no [alternativa]" |

## Regla 60/40

El comprador debe hablar 60%+ del tiempo. Si tu hablas mas del 40%, estas haciendo pitch, no discovery. El silencio despues de una pregunta dificil es una herramienta -- la primera respuesta es la superficial, la que viene despues de la pausa es la real.

## Adaptacion por agente

### sales-hunter (calificacion de cliente)

Dimensiones prioritarias: alcance, restricciones (presupuesto/tiempo), criterio de exito.
Usar SPIN + Gap Selling. Preguntas extra:
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
