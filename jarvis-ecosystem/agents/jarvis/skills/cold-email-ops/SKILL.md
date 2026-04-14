# Cold Email Ops

*Adaptado de marketingskills/cold-email para el ecosistema Jarvis (sales-hunter)*

## Trigger

Usar este skill cuando el agente necesite:
- Escribir un email frio a un prospect o lead de Workana
- Crear un follow-up para un prospect que no respondio
- Redactar la primera respuesta a un proyecto publicado en un portal
- Preparar templates de outreach para campanas de prospeccion

## Prerequisito obligatorio

**ANTES de escribir cualquier email, leer:**
`jarvis-ecosystem/.agents/product-marketing-context.md`

Extraer: servicios que ofrecemos, diferenciadores, voz de marca, objeciones.

## Principios de cold email

1. **Corto** -- maximo 150 palabras en el primer email. El prospect no te conoce.
2. **Sobre ellos, no sobre ti** -- 80% habla de su problema, 20% de como puedes ayudar.
3. **Un solo CTA** -- una pregunta o accion. No dos. No tres.
4. **Sin adjuntos** -- nunca en el primer contacto.
5. **Personalizacion real** -- mencionar algo especifico del prospect o su proyecto.

## Estructura del primer email

```
Linea 1: Observacion personalizada (algo de su proyecto/empresa)
Linea 2-3: Problema que probablemente tiene
Linea 4-5: Como lo hemos resuelto (sin detalles tecnicos)
Linea 6: CTA simple (pregunta)
```

**Ejemplo para Workana:**

```
Hola [nombre],

Vi tu proyecto de [tipo] en Workana. Entiendo que necesitas
[resultado esperado] y que el tiempo es clave.

Trabajo con un equipo que entrega [tipo de entregable] en
[timeframe]. Hemos hecho proyectos similares con [resultado breve].

¿Te parece si hablamos 15 min para ver si encajamos?

[Firma corta]
```

## Subject lines (asuntos)

| Tipo | Ejemplo |
|------|---------|
| Directo | "Re: tu proyecto de [tipo]" |
| Pregunta | "Pregunta rapida sobre [proyecto]" |
| Resultado | "[Resultado] en [tiempo]" |

**Evitar:** emojis en asunto, mayusculas excesivas, promesas exageradas.

## Secuencia de follow-up

| Dia | Email | Enfoque |
|-----|-------|---------|
| 0 | Email 1 | Presentacion + valor |
| 3 | Email 2 | Agregar un dato nuevo o prueba social |
| 7 | Email 3 | Cambiar angulo (otro beneficio) |
| 14 | Email 4 | Breakup: "¿sigo buscandote o cierro?" |

Maximo 4 emails. Despues de eso, mover a "frio" en el pipeline.

## Signal-Based Selling

No enviar outreach sin una razon por la que el prospect deberia importarle AHORA. Las senales de compra multiplican la tasa de respuesta 4-8x vs outreach generico.

### Tiers de senales

**Tier 1 -- Intent activo (prioridad maxima)**
- Proyecto publicado en Workana/portal (senal mas directa)
- Perfil del cliente buscando servicio especifico
- Actualizacion reciente del brief con urgencia

**Tier 2 -- Cambio organizacional**
- Empresa recien fundada o en expansion
- Nuevo puesto de decision publicado (buscan CTO, head of marketing)
- Lanzamiento de producto o pivote visible

**Tier 3 -- Senales tecnicas y de comportamiento**
- Stack tecnologico visible que podemos complementar
- Actividad en LinkedIn/redes sobre temas que resolvemos
- Contenido publicado sobre problemas que atacamos

**Velocidad critica:** actuar dentro de las primeras 24h de la senal. Despues de 72h, un competidor ya tuvo la conversacion.

## ICP (Ideal Customer Profile)

Un ICP que no excluye empresas no es un ICP. Definir:

**Filtros firmograficos**
- Industria (2-4 verticales especificas)
- Tamaño (PYME, startup, 1-50 personas)
- Presupuesto estimado (puede pagar nuestras tarifas)

**Calificadores de comportamiento**
- Que evento los convierte en comprador ahora
- Que dolor resolvemos que no pueden ignorar
- Cual es su workaround actual

**Descalificadores (igual de importantes)**
- Busca lo mas barato posible (sin margen)
- Proyecto requiere presencia fisica constante
- Historial de no pagar o no contratar en Workana

## Secuencia multicanal (10 touches en 28 dias)

| Dia | Touch | Canal | Enfoque |
|-----|-------|-------|---------|
| 1 | 1 | Email/Workana | Senal + valor + CTA suave |
| 3 | 2 | LinkedIn | Conexion con nota personalizada (sin pitch) |
| 5 | 3 | Email | Dato nuevo o prueba social |
| 8 | 4 | Telefono/WhatsApp | Referencia al email, voicemail si no contesta |
| 10 | 5 | LinkedIn | Interactuar con su contenido |
| 14 | 6 | Email | Caso de estudio de situacion similar + CTA claro |
| 17 | 7 | Video/Loom | 60 seg personalizado mostrando algo especifico |
| 21 | 8 | Email | Nuevo angulo -- dolor diferente o perspectiva |
| 24 | 9 | Telefono | Ultimo intento de contacto |
| 28 | 10 | Email | Breakup: "¿sigo o cierro?" honesto y breve |

Cada touch debe agregar un angulo nuevo. Repetir el mismo ask con diferentes palabras no es una secuencia, es acoso.

## Benchmarks de reply rate

| Nivel de personalizacion | Reply rate esperado |
|--------------------------|---------------------|
| Generico, sin targeting | 1-3% |
| Personalizado por rol/industria | 5-8% |
| Signal-based + research | 12-25% |
| Warm intro o referido | 30-50% |

## Adaptacion a Workana

- El "email" en Workana es la propuesta + mensaje inicial
- Subject line = primera linea visible de la propuesta
- Incluir precio y plazo en la propuesta (requerido por la plataforma)
- Personalizar mencionando detalles especificos del brief del cliente
- Para propuestas estructuradas, usar `proposal-ops`

## Checklist antes de enviar

- [ ] Lei product-marketing-context.md
- [ ] El email tiene menos de 150 palabras
- [ ] Hay personalizacion real (no generica)
- [ ] Solo hay un CTA
- [ ] No hay adjuntos ni links sospechosos
- [ ] El tono es profesional pero cercano (brand voice)
- [ ] Si es Workana: precio y plazo incluidos

## Output esperado

Entregar:
- Email/propuesta completo listo para enviar
- Subject line sugerido
- Notas de personalizacion (que investigar del prospect)
- Siguiente paso si responde / si no responde
