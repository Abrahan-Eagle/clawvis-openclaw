---
name: task-pipeline-ops
description: "Secuencia estandar para tareas multi-paso: Plan -> Spec -> Exec -> Verify -> Fix. Formaliza como Jarvis coordina trabajo complejo a traves de agentes."
---

# Task Pipeline Ops

Adaptado del Team pipeline de oh-my-claudecode (plan -> prd -> exec -> verify -> fix). Secuencia de referencia para que Jarvis coordine tareas multi-paso de forma consistente.

## Cuando se activa

- Cualquier tarea que involucre mas de 3 pasos
- Trabajo que cruza mas de un agente o empresa del holding
- Proyectos de cliente (propuesta a entrega)
- Cambios operativos al ecosistema (nuevas integraciones, migraciones)

NO usar para tareas simples de 1-2 pasos (responder un mensaje, mover una tarjeta).

## El pipeline

```
PLAN -> SPEC -> EXEC -> VERIFY -> FIX (loop max 3)
                                    |
                                    v
                                 COMPLETE / ESCALATE
```

### Fase 1: PLAN

**Que:** Descomponer la tarea en pasos concretos y asignar responsables.

**Skills que se activan:** `brainstorming-ops` (si la tarea es compleja), `deep-interview-ops` (si los requisitos son vagos).

**Entregable:** Lista de pasos numerados con responsable y estimacion.

**Criterio de salida:** El CEO o agente coordinador aprueba el plan.

```
Ejemplo:
1. [sales-hunter] Investigar lead -> 30 min
2. [sales-hunter] Escribir propuesta -> 1h
3. [jarvis] Revisar y aprobar propuesta -> 15 min
4. [sales-hunter] Enviar propuesta -> 5 min
5. [jarvis] Verificar envio -> 5 min
```

### Fase 2: SPEC

**Que:** Definir criterio de exito y entregables concretos para cada paso.

**Entregable:** Tabla de acceptance criteria.

**Criterio de salida:** Cada paso tiene un "done when" medible.

```
| Paso | Done when |
|------|-----------|
| Investigar lead | Ficha de lead con scoring >= 3.0 |
| Escribir propuesta | Propuesta con precio, plazo, scope |
| Revisar propuesta | CEO aprueba o pide cambios |
| Enviar propuesta | Confirmacion de envio en plataforma |
| Verificar envio | Screenshot o URL de la propuesta enviada |
```

### Fase 3: EXEC

**Que:** Ejecutar cada paso en orden. Si hay pasos independientes, ejecutar en paralelo.

**Reglas:**
- Seguir el orden del plan salvo que los pasos sean explicitamente independientes
- Si un paso falla, no saltar al siguiente; ir a FIX
- Documentar progreso en Trello o `memory/`

**Criterio de salida:** Todos los pasos tienen entregable.

### Fase 4: VERIFY

**Que:** Verificar que cada entregable cumple su criterio de exito.

**Skills que se activan:** `verification-before-completion`

**Reglas:**
- Verificar con evidencia fresca (no cache, no "deberia funcionar")
- Si un entregable no pasa, documentar que fallo

**Entregable:** Tabla de verificacion con pass/fail por paso.

```
| Paso | Criterio | Resultado | Evidencia |
|------|----------|-----------|-----------|
| Investigar lead | Scoring >= 3.0 | PASS | Ficha: 4.2/5 |
| Escribir propuesta | Precio + plazo + scope | PASS | Doc completo |
| Enviar propuesta | Confirmacion | FAIL | Error de plataforma |
```

### Fase 5: FIX

**Que:** Corregir los pasos que fallaron en VERIFY.

**Reglas:**
- Maximo 3 intentos por paso
- Si despues de 3 intentos sigue fallando: **ESCALATE** al CEO
- Cada intento debe cambiar algo (no repetir lo mismo esperando resultado diferente)
- Despues de fix, volver a VERIFY para ese paso

**Criterio de salida:** Todos los pasos en PASS, o escalado documentado.

## Estados terminales

| Estado | Significado |
|--------|-------------|
| **COMPLETE** | Todos los pasos verificados con evidencia |
| **ESCALATE** | Un paso fallo 3 veces; requiere decision del CEO |
| **CANCELLED** | El CEO o el cliente cancelo la tarea |

## Cuando NO usar el pipeline completo

| Situacion | Que hacer |
|-----------|-----------|
| Tarea de 1-2 pasos | Ejecutar directamente + verification-before-completion |
| Respuesta rapida a cliente | Ejecutar directamente |
| Consulta informativa | Responder directamente |
| Emergencia (sistema caido) | Actuar primero, documentar despues |

## Integracion con Trello

- Crear tarjeta al inicio del pipeline
- Mover entre columnas segun fase: Backlog -> En progreso -> Review -> Done
- Si se escala: mover a columna "Bloqueado" con nota de por que

## Checklist de cierre

- [ ] Todos los pasos del plan estan en PASS o ESCALATE
- [ ] Evidencia de verificacion documentada
- [ ] Tarjeta de Trello en estado correcto
- [ ] Lecciones aprendidas (si hubo FIX) documentadas en memory/
