---
name: brainstorming-ops
description: "OBLIGATORIO antes de cualquier tarea compleja: propuestas comerciales, campanas de marketing, features, scripts, integraciones. Explora contexto, pregunta, propone alternativas, presenta diseno y obtiene aprobacion antes de ejecutar."
---

# Brainstorming operativo

Inspirado en superpowers:brainstorming. Adaptado para operaciones de negocio, no solo codigo.

NO ejecutes ninguna accion hasta presentar un diseno y obtener aprobacion del CEO o del agente coordinador.

## Cuando se activa

- Propuesta comercial a un cliente
- Campana de marketing nueva
- Nuevo script o automatizacion
- Cambio en la configuracion del ecosistema (openclaw.json, integraciones)
- Cualquier tarea que toque mas de un agente o empresa del holding

## Anti-patron: "Esto es muy simple para pensarlo"

Toda tarea pasa por este proceso. Una propuesta de 2 parrafos, un post para redes, un script de 10 lineas. "Simple" es donde las suposiciones no examinadas causan mas trabajo desperdiciado. El diseno puede ser corto (2-3 oraciones para cosas triviales), pero DEBES presentarlo y obtener aprobacion.

## Checklist

1. **Explorar contexto** — revisar dossier del cliente, Trello, MEMORY.md, docs relevantes
2. **Preguntas clarificadoras** — una a la vez, entender proposito, restricciones, criterio de exito
3. **Proponer 2-3 alternativas** — con trade-offs y tu recomendacion
4. **Presentar diseno** — en secciones proporcionales a la complejidad, validar cada seccion
5. **Documentar diseno** — en la tarjeta de Trello o en `memory/` segun corresponda
6. **Obtener aprobacion** — del CEO si aplica Approval Gate (ver `docs/APPROVAL_GATES.md`)
7. **Transicion a ejecucion** — descomponer en tareas bite-sized si es necesario

## Proceso por tipo de tarea

### Propuesta comercial (ventas)

1. Leer dossier del cliente (`client-dossiers/`)
2. Preguntar: Que necesita exactamente? Presupuesto? Timeline? Competencia?
3. Proponer 2-3 enfoques de propuesta (precio, alcance, diferenciador)
4. Presentar borrador al CEO para aprobacion (AG-01)
5. Solo despues de aprobacion: enviar

### Campana de marketing

1. Revisar goals de marketing (G-M01, G-M02)
2. Preguntar: Objetivo de la campana? Audiencia? Canal? KPIs?
3. Proponer alternativas de contenido/canal
4. Presentar plan al CEO para aprobacion (AG-03)
5. Solo despues de aprobacion: ejecutar

### Script o automatizacion

1. Revisar CLAWFLOWS.md y scripts/ existentes
2. Preguntar: Que problema resuelve? Con que frecuencia? Que datos necesita?
3. Proponer alternativa simple vs robusta
4. Presentar diseno (pseudocodigo o esquema)
5. Implementar con verificacion (ver skill verification-before-completion)

## Principios

- **Una pregunta a la vez** — no abrumar con multiples preguntas
- **Multiple choice cuando sea posible** — mas facil de responder
- **YAGNI** — eliminar funcionalidades innecesarias de todo diseno
- **Explorar alternativas siempre** — proponer 2-3 antes de decidir
- **Validacion incremental** — presentar diseno, obtener aprobacion, luego avanzar

## Senales de que lo estas haciendo mal

- Saltar directamente a ejecutar sin preguntar
- Enviar propuesta sin revisar dossier del cliente
- Crear campana sin definir KPIs
- Escribir script sin revisar si ya existe algo similar
- "Ya se lo que necesita" sin verificar con el CEO
