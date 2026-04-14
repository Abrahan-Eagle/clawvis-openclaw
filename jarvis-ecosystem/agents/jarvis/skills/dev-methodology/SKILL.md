---
name: dev-methodology
description: "Metodologia de desarrollo de software para cuando se escriban scripts, automatizaciones o codigo del ecosistema, y para cuando se active dev-agency. TDD, planes detallados, code review, subagentes."
---

# Metodologia de desarrollo

Inspirado en superpowers: test-driven-development, writing-plans, subagent-driven-development, requesting-code-review. Para uso cuando se escriba codigo en el ecosistema o cuando dev-agency este activa.

## Cuando se activa

- Crear o modificar scripts en `scripts/`
- Crear o modificar ClawFlows YAML en `automations/`
- Escribir codigo para career-ops o cualquier herramienta
- Cualquier tarea de dev-agency (cuando se active)
- Modificar configuracion compleja (openclaw.json con muchos cambios)

## 1. TDD — Test-Driven Development

### Ley de hierro

```
NO HAY CODIGO DE PRODUCCION SIN UN TEST QUE FALLE PRIMERO
```

Escribiste codigo antes del test? Borralo. Empieza de nuevo.

### Ciclo Red-Green-Refactor

1. **RED** — Escribir un test minimal que muestre lo que deberia pasar
2. **Verificar RED** — Ejecutar test, confirmar que FALLA por la razon correcta
3. **GREEN** — Escribir el codigo MINIMO para que el test pase
4. **Verificar GREEN** — Ejecutar test, confirmar que PASA. Otros tests siguen pasando.
5. **REFACTOR** — Limpiar, eliminar duplicacion. Mantener tests verdes.
6. **Repetir** — Siguiente test para siguiente funcionalidad.

### Excepciones (preguntar al CEO)

- Prototipos desechables
- Archivos de configuracion YAML/JSON
- Scripts de una sola vez para migracion

### Racionalizaciones comunes

| Excusa | Realidad |
|--------|----------|
| "Muy simple para testear" | Codigo simple se rompe. El test toma 30 segundos. |
| "Testeo despues" | Tests que pasan inmediatamente no prueban nada. |
| "TDD me hace lento" | TDD es mas rapido que debuggear despues. |
| "Ya lo probe manualmente" | Manual != sistematico. No hay registro, no es repetible. |

## 2. Planes detallados (writing-plans)

Cuando una tarea de desarrollo tiene mas de 3 pasos:

### Estructura de tarea

```markdown
### Tarea N: [Nombre del componente]

**Archivos:**
- Crear: `ruta/exacta/al/archivo.sh`
- Modificar: `ruta/existente.yaml:lineas 10-20`
- Test: `ruta/al/test.sh`

- [ ] Paso 1: Escribir test que falle
- [ ] Paso 2: Ejecutar test, verificar que falla
- [ ] Paso 3: Escribir implementacion minimal
- [ ] Paso 4: Ejecutar test, verificar que pasa
- [ ] Paso 5: Commit
```

### Reglas de planes

- **Tareas bite-sized** — cada paso es una accion de 2-5 minutos
- **Rutas exactas** — siempre paths completos
- **Codigo completo** — cada paso que cambia codigo muestra el codigo
- **Sin placeholders** — nada de "TBD", "TODO", "implementar despues"
- **YAGNI** — no agregar features que no se pidieron
- **DRY** — no duplicar logica

## 3. Code review entre tareas

Despues de cada tarea completada, antes de pasar a la siguiente:

### Revision en 2 fases

1. **Cumplimiento de spec** — El codigo hace lo que la tarea pidio? Ni mas ni menos?
2. **Calidad de codigo** — Es limpio? Tiene tests? Maneja errores?

### Checklist de revision

- [ ] Toda funcion nueva tiene test
- [ ] Tests pasan
- [ ] Output limpio (sin errores, sin warnings)
- [ ] Codigo minimal (no over-engineered)
- [ ] Edge cases cubiertos

## 4. Subagentes para desarrollo

Cuando hay multiples tareas independientes:

### Principio

Un subagente fresco por tarea + revision en 2 fases = alta calidad, iteracion rapida.

### Proceso

1. Leer plan, extraer todas las tareas
2. Por cada tarea: dispatch subagente con contexto completo
3. Subagente implementa, testea, commitea
4. Revisor de spec: cumple lo pedido?
5. Revisor de calidad: codigo limpio?
6. Marcar tarea como completada
7. Siguiente tarea

### Seleccion de modelo

- **Tareas mecanicas** (1-2 archivos, spec clara): modelo rapido/barato
- **Integracion** (multiples archivos, coordinacion): modelo estandar
- **Arquitectura y revision**: modelo mas capaz disponible

## 5. Git workflow

- **Nunca trabajar en main sin consentimiento** del CEO
- **Commits frecuentes** — despues de cada test verde
- **Mensajes descriptivos** — que cambiaste y por que
- **Verificar antes de push** — todos los tests pasan, lint limpio

## Banderas rojas

- Codigo antes de test
- Test que pasa inmediatamente
- Plan sin rutas exactas de archivos
- Saltarse code review "porque es simple"
- Multiples cambios no relacionados en un commit
- "Ya lo probe manualmente" como excusa para no escribir test
- Subagente falla y se reintenta sin cambiar nada

## Referencia: skill Superpowers completo

Para el workflow completo de Superpowers (brainstorming -> plan -> worktree -> subagent-driven -> code review -> finish branch), el plugin esta instalado en Cursor en `~/.cursor/plugins/local/superpowers/`. Usarlo directamente al programar con Cursor.
