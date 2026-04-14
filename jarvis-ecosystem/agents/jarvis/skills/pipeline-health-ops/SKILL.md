---
name: pipeline-health-ops
description: "Monitorear la salud del pipeline de ventas: metricas, forecasting, alertas de deals estancados. Para sales-hunter heartbeat semanal."
---

# Pipeline Health Ops

Adaptado de agency-agents:Pipeline Analyst para el ecosistema Jarvis (sales-hunter + jarvis).

## Trigger

Usar este skill cuando el agente necesite:
- Hacer el health check semanal del pipeline (heartbeat de sales-hunter)
- Evaluar si hay suficientes leads para cumplir metas del mes
- Identificar deals estancados que necesitan accion
- Reportar metricas de ventas al CEO
- Decidir donde invertir tiempo de prospeccion

## Prerequisitos obligatorios

1. Leer `jarvis-ecosystem/.agents/product-marketing-context.md`
2. Tener acceso al estado actual del pipeline (Trello, archivo de deals, o memoria)

## Metricas core

### Volumen

| Metrica | Que mide | Target minimo |
|---------|----------|---------------|
| Leads nuevos / semana | Flujo de entrada al funnel | 10+ |
| Propuestas enviadas / semana | Conversion de lead a propuesta | 5+ |
| Propuestas aceptadas / mes | Deals cerrados | 2+ |

### Velocidad

| Metrica | Formula | Target |
|---------|---------|--------|
| Lead-to-proposal (dias) | Fecha propuesta - Fecha lead | < 48h |
| Proposal-to-response (dias) | Fecha respuesta - Fecha propuesta | < 7 dias |
| Deal velocity | (# Deals x Win Rate x Avg Deal Size) / Avg Sales Cycle | Crecer MoM |

### Calidad

| Metrica | Que mide | Target |
|---------|----------|--------|
| Reply rate | % prospects que responden | > 10% |
| Win rate | % propuestas aceptadas | > 20% |
| Avg deal size | Ingreso promedio por deal cerrado | Crecer QoQ |
| Churn de pipeline | % deals que mueren sin decision | < 40% |

## Pipeline Health Check (semanal)

Ejecutar cada heartbeat semanal de sales-hunter.

### Paso 1: Snapshot del funnel

```
| Etapa | # Deals | Valor total | Antigüedad promedio | Deals estancados |
|-------|---------|-------------|---------------------|------------------|
| Nuevo lead | | | | |
| Contacto hecho | | | | |
| Propuesta enviada | | | | |
| Negociacion | | | | |
| Cerrado/ganado | | | | |
| Cerrado/perdido | | | | |
```

### Paso 2: Pipeline Coverage Ratio

```
Pipeline Coverage = Valor total pipeline / Meta de revenue del mes
```

| Coverage | Interpretacion | Accion |
|----------|---------------|--------|
| > 3x | Saludable | Enfocarse en cerrar, no en prospectar |
| 2-3x | Adecuado | Balance entre prospeccion y cierre |
| 1-2x | Riesgoso | Aumentar prospeccion urgente |
| < 1x | Critico | Alarma: no hay suficiente pipeline para cumplir meta |

### Paso 3: Identificar deals estancados

Un deal esta estancado si:
- Lead sin contacto por > 48h
- Propuesta enviada sin respuesta por > 7 dias
- Negociacion abierta por > 14 dias sin movimiento
- Follow-up pendiente vencido

Para cada deal estancado, definir:
- Ultima accion realizada
- Razon probable del estancamiento
- Siguiente accion recomendada
- Deadline para actuar o descartar

### Paso 4: Alertas automaticas

| Condicion | Severidad | Accion |
|-----------|-----------|--------|
| Coverage < 2x | ALTA | Notificar a jarvis; duplicar prospeccion |
| > 3 deals estancados | MEDIA | Review individual de cada deal |
| Win rate < 15% en ultimo mes | ALTA | Revisar calidad de propuestas (usar proposal-ops) |
| Reply rate < 5% | ALTA | Revisar outreach (usar cold-email-ops) |
| 0 propuestas enviadas esta semana | CRITICA | Escalar a CEO |

## Forecasting basico

### Forecast conservador (bottom-up)

```
Revenue forecast = Sum(deals en negociacion x probabilidad de cierre)
```

| Etapa | Probabilidad default |
|-------|---------------------|
| Propuesta enviada | 20% |
| Negociacion activa | 50% |
| Acuerdo verbal | 80% |

### Tendencia MoM

```
| Mes | Leads | Propuestas | Win Rate | Revenue | Tendencia |
|-----|-------|------------|----------|---------|-----------|
| M-2 | | | | | |
| M-1 | | | | | |
| M actual | | | | | ↑/↓/→ |
```

Si tendencia es ↓ por 2+ meses consecutivos, escalar con diagnostico de causa raiz.

## Integracion con otros skills

- **cold-email-ops**: si reply rate baja, revisar targeting y personalizacion
- **proposal-ops**: si win rate baja, revisar calidad de propuestas
- **deep-interview-ops**: si deals mueren en negociacion, calificar mejor al inicio
- **lead-research-ops**: si leads son de baja calidad, ajustar ICP

## Cadencia

| Reporte | Frecuencia | Destinatario |
|---------|------------|-------------|
| Pipeline snapshot | Semanal (heartbeat) | sales-hunter auto-check |
| Health check completo | Quincenal | jarvis -> CEO |
| Forecast update | Mensual | jarvis -> CEO |

## Checklist del health check

- [ ] Lei product-marketing-context.md
- [ ] Pipeline snapshot actualizado con todos los deals activos
- [ ] Coverage ratio calculado
- [ ] Deals estancados identificados con siguiente accion
- [ ] Alertas evaluadas y escaladas si aplica
- [ ] Forecast actualizado
- [ ] Tendencia MoM documentada

## Output esperado

Entregar:
- Pipeline snapshot table
- Coverage ratio con interpretacion
- Lista de deals estancados con proxima accion y deadline
- Alertas activas
- Forecast conservador del mes
- Recomendacion: donde invertir tiempo esta semana (prospectar vs cerrar vs mejorar propuestas)
