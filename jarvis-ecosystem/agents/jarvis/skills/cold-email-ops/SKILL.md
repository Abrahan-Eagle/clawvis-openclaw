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

## Adaptacion a Workana

- El "email" en Workana es la propuesta + mensaje inicial
- Subject line = primera linea visible de la propuesta
- Incluir precio y plazo en la propuesta (requerido por la plataforma)
- Personalizar mencionando detalles especificos del brief del cliente

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
