# Lead Research Ops

*Adaptado de awesome-claude-skills/lead-research-assistant para el ecosistema Jarvis (sales-hunter)*

## Trigger

Usar este skill cuando el agente necesite:
- Investigar un lead o prospect antes de contactarlo
- Evaluar si un proyecto de Workana vale la pena
- Calificar leads del pipeline para priorizar esfuerzo
- Preparar un dossier de cliente antes de una reunion

## Prerequisito obligatorio

**ANTES de investigar cualquier lead, leer:**
`jarvis-ecosystem/.agents/product-marketing-context.md`

Extraer: servicios, audiencia objetivo, diferenciadores. Para saber si el lead encaja con lo que ofrecemos.

## Paso 0 (opcional): intel reciente con last30days-openclaw

Cuando el lead es **Hot/Warm** o el tema del proyecto depende de **stack, herramienta o persona publica**, considerar ejecutar el skill **last30days-openclaw** para pulso de comunidad (Reddit, HN, GitHub, X, etc.) en los ultimos dias. No sustituye Workana/LinkedIn; **complementa** con lenguaje y dolores recientes.

- Skill: `agents/jarvis/skills/last30days-openclaw/SKILL.md`
- Guia: `jarvis-ecosystem/docs/LAST30DAYS_INTEGRACION.md`
- Si el skill no esta instalado en la maquina: `openclaw skills install last30days-openclaw` (o usar la copia versionada en el repo + `setup_openclaw_env.sh`).

Integrar en la ficha del lead: 2-4 bullets de "que dice la comunidad ahora" solo si aportan al angulo de contacto o a la propuesta.

## Ideal Customer Profile (ICP)

Un lead es ideal si cumple 3+ de estos criterios:

| Criterio | Descripcion |
|----------|-------------|
| Necesidad real | Tiene un problema concreto que resolvemos (dev, marketing, web) |
| Presupuesto | Puede pagar nuestras tarifas (no busca lo mas barato posible) |
| Urgencia | Necesita resultados en semanas, no en "algun dia" |
| Tamaño | PYME o startup (1-50 personas) |
| Comunicacion | Responde mensajes, tiene claro lo que quiere |
| Repetibilidad | Potencial de relacion a largo plazo (no solo un encargo) |

## Proceso de investigacion

### Paso 1: Recopilar datos

Para cada lead, buscar:
- **Nombre y empresa** (si aplica)
- **Proyecto/necesidad** (descripcion del brief o solicitud)
- **Presupuesto indicado** (o rango estimado)
- **Plazo** (cuando necesita resultados)
- **Historial** (en Workana: reviews, proyectos previos, tasa de contratacion)
- **Presencia online** (web, redes, LinkedIn)

### Paso 2: Scoring

| Factor | Peso | Puntaje (1-5) |
|--------|------|----------------|
| Fit con servicios | 25% | |
| Presupuesto adecuado | 25% | |
| Urgencia / timeline | 20% | |
| Potencial recurrente | 15% | |
| Historial del cliente | 15% | |
| **Total ponderado** | 100% | **/5.0** |

**Clasificacion:**
- 4.0+ = **Hot** -- contactar inmediatamente
- 3.0-3.9 = **Warm** -- contactar esta semana
- 2.0-2.9 = **Cold** -- monitorear, no priorizar
- <2.0 = **Skip** -- no invertir tiempo

### Paso 3: Estrategia de contacto

Para leads Hot y Warm, preparar:
- **Angulo de entrada** (que aspecto del proyecto destacar)
- **Personalizacion** (dato especifico del lead para el email)
- **Propuesta de valor** (diferenciador relevante para este lead)
- **Precio sugerido** (basado en alcance y presupuesto del lead)
- **Siguiente paso** (propuesta formal, call, demo)

## Fuentes de datos

| Fuente | Que buscar |
|--------|-----------|
| Workana (perfil del cliente) | Reviews, proyectos publicados, tasa de contratacion |
| LinkedIn | Empresa, rol, tamaño |
| Web del prospect | Servicios, stack, presencia digital |
| Redes sociales | Actividad, engagement, necesidades expresadas |

## Checklist antes de entregar

- [ ] Lei product-marketing-context.md
- [ ] (Opcional) last30days-openclaw si el lead/tema lo justifica — ver Paso 0
- [ ] Complete los datos basicos del lead
- [ ] Hice scoring con todos los factores
- [ ] El lead esta clasificado (Hot/Warm/Cold/Skip)
- [ ] Para Hot/Warm: hay estrategia de contacto
- [ ] No estoy gastando tiempo en leads Skip

## Output esperado

Entregar:
- Ficha del lead (datos basicos)
- Scorecard con puntaje ponderado
- Clasificacion (Hot/Warm/Cold/Skip)
- Estrategia de contacto (si aplica)
- Notas de personalizacion para cold-email-ops
