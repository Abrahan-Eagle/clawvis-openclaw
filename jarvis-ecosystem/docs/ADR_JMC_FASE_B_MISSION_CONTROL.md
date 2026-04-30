# ADR: posible Fase B — acercamiento a Mission Control o convivencia

**Estado:** propuesta — **no implementada** en el código actual de JMC.  
**Contexto:** [`JMC_DESIGN.md`](JMC_DESIGN.md) define JMC como read-only sin DB; [`JMC_VS_MISSION_CONTROL.md`](JMC_VS_MISSION_CONTROL.md) contrasta con [openclaw-mission-control](https://github.com/abhi1693/openclaw-mission-control).

## Problema

Operadores pueden pedir **paridad funcional** con Mission Control (tableros con escritura, CRUD de tags, multi-usuario, persistencia centralizada). Implementarlo dentro del adapter actual rompería los límites explícitos del diseño (sin escritura desde UI, sin DB).

## Opciones consideradas

1. **Mantener JMC solo lectura** y desplegar Mission Control como **segunda aplicación** cuando haga falta operación pesada; definir una única fuente de verdad para tareas (archivos vs servidor).
2. **Ampliar JMC con POST acotados** alineados a [`JMC_DESIGN.md`](JMC_DESIGN.md) v2.1 (p. ej. disparar AG / colas externas) sin convertir JMC en Mission Control.
3. **Nuevo servicio** con DB y API de escritura; JMC quedaría como cliente de solo lectura o se deprecaría parcialmente.

## Decisión recomendada hasta nueva orden

No iniciar Fase B sin **ADR de producto** firmado: alcance, seguridad, hosting y modelo de datos. Hasta entonces, las mejoras de UX permisibles siguen siendo **derivadas en cliente** y **GET** en el adapter.

## Consecuencias

- Evitar dependencias que obliguen a escritura desde `jmc/ui` sin política clara de tokens y auditoría.
- Cualquier POST futuro debe documentarse en `JMC_DESIGN.md` y versionarse (p. ej. v2.x).
