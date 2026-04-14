---
name: proposal-ops
description: "Escribir propuestas que persuadan, no que solo cumplan. Win themes, narrativa en 3 actos, executive summary. Para Workana y prospeccion directa."
---

# Proposal Ops

Adaptado de agency-agents:Proposal Strategist para el ecosistema Jarvis (sales-hunter).

## Trigger

Usar este skill cuando el agente necesite:
- Escribir una propuesta formal para un proyecto de Workana
- Preparar una propuesta para un cliente directo
- Responder un RFP o brief de proyecto
- Redactar un pitch de servicios

## Prerequisitos obligatorios

**ANTES de escribir cualquier propuesta:**
1. Leer `jarvis-ecosystem/.agents/product-marketing-context.md`
2. Si hay dossier del cliente: leerlo (`client-dossiers/`)
3. Si el pedido es vago: ejecutar `deep-interview-ops` primero
4. Si ya hay datos del lead: revisar resultado de `lead-research-ops`

## Win Themes

Cada propuesta necesita 2-3 win themes: afirmaciones centradas en el cliente que conectan nuestra solucion con su dolor especifico.

Un win theme fuerte:
- Nombra el reto **especifico** del cliente, no un problema generico de la industria
- Conecta una capacidad concreta con un resultado medible
- Diferencia sin mencionar competidores
- Es demostrable con evidencia o metodologia

| Debil | Fuerte |
|-------|--------|
| "Tenemos amplia experiencia en desarrollo web" | "Nuestro equipo entrega MVPs funcionales en 3-4 semanas, con iteraciones semanales para que valides antes de invertir mas" |
| "Somos expertos en marketing digital" | "Optimizamos landing pages con un framework de 7 dimensiones que identifica exactamente donde se pierden visitantes" |

### Plantilla de win themes

```
Win Theme 1: [Afirmacion centrada en el cliente]
- Necesidad del cliente: [del brief o entrevista]
- Nuestra capacidad: [que hacemos concretamente]
- Evidencia: [proyecto similar, metrica, metodologia]

Win Theme 2: [Afirmacion centrada en el cliente]
- Necesidad del cliente: [...]
- Nuestra capacidad: [...]
- Evidencia: [...]
```

## Narrativa en 3 actos

### Acto I: Entender el reto

Demostrar que entendemos el mundo del cliente mejor de lo que esperaba. Usar su lenguaje, sus restricciones, su contexto.

**La mayoria de propuestas perdedoras saltan este acto o lo llenan con texto generico.**

```
"Entiendo que necesitas [resultado] para [fecha/contexto].
El reto principal es [problema concreto del brief], y lo que
lo complica es [restriccion o contexto que eleva la dificultad]."
```

### Acto II: La solucion como recorrido

No un listado de features. Un viaje guiado donde cada capacidad resuelve un problema del Acto I.

```
Paso 1: [Accion concreta] -> resuelve [problema X del brief]
Paso 2: [Accion concreta] -> resuelve [problema Y]
Paso 3: [Entregable final] -> resultado medible
```

### Acto III: El estado transformado

Pintar una imagen especifica del futuro del cliente despues de trabajar con nosotros.

```
"Al finalizar, tendras [entregable concreto] funcionando.
Eso significa [beneficio 1] y [beneficio 2].
El siguiente paso natural seria [expansion o mantenimiento]."
```

## Executive Summary (para propuestas largas)

Si la propuesta tiene mas de una pagina, incluir un resumen ejecutivo al inicio. Es el argumento de cierre, puesto al principio.

```
1. Espejo del problema (1-2 oraciones en su lenguaje)
2. Tension (que pasa si no se resuelve)
3. Nuestra tesis (como lo resolvemos, win themes aqui)
4. Prueba (1 dato concreto: proyecto similar, metrica, experiencia)
5. Estado transformado (que cambia para ellos)
```

Maximo una pagina. Cada oracion debe ganarse su lugar.

## Adaptacion a Workana

En Workana la "propuesta" es un campo de texto corto + precio + plazo. Adaptar:

- **Primera linea** = hook (equivalente al subject line del email)
- **Parrafo 1** = Acto I comprimido (entiendo tu problema)
- **Parrafo 2** = Acto II comprimido (asi lo resuelvo, en X pasos)
- **Parrafo 3** = Acto III comprimido (resultado + siguiente paso)
- **Precio y plazo** = obligatorios; anclar en valor, no en costo
- **Maximo 200 palabras** total (el cliente tiene 50 propuestas que leer)

## Reglas de calidad

1. **Nunca generico** -- si puedes cambiar el nombre del cliente sin que la propuesta cambie, esta perdiendo
2. **Sin adjetivos vacios** -- "robusto", "innovador", "world-class" son ruido. Reemplazar con datos
3. **Cada claim necesita evidencia** -- una metrica, un proyecto similar, o un paso concreto del proceso
4. **Precio despues de valor** -- construir el caso de ROI antes de que el cliente vea el numero
5. **No atacar competidores** -- diferenciar por fortaleza propia, no por debilidad ajena

## Checklist antes de enviar

- [ ] Lei product-marketing-context.md
- [ ] La propuesta tiene 2-3 win themes especificos al cliente
- [ ] Sigue la narrativa en 3 actos (entender -> solucionar -> transformar)
- [ ] La primera linea engancha (no "Hola, somos...")
- [ ] Cada claim tiene evidencia
- [ ] Precio y plazo incluidos (si aplica)
- [ ] Tono profesional pero cercano (brand voice)
- [ ] Maximo 200 palabras para Workana; 1 pagina para propuestas directas
- [ ] No hay adjetivos vacios ni texto generico

## Output esperado

Entregar:
- Propuesta completa lista para enviar
- Win themes documentados (para reutilizar si el lead avanza)
- Notas de personalizacion usadas
- Siguiente paso si acepta / si no responde
