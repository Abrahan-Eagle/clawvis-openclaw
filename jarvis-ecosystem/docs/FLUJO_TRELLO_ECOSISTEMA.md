# Flujo de trabajo Trello — obligatorio para el ecosistema Jarvis

**Estado:** **norma operativa**. Aplica a **todas** las tareas que deban ejecutar **Jarvis**, **agentes por empresa** (`mkt-*`, `sales-*`, etc.) y **subagentes** cuando realicen trabajo que represente entregables, seguimiento o responsabilidad frente a un cliente del holding.

**Última revisión:** abril 2026.  
**Convención de nombres y `dossier_id`:** [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md).  
**Gobierno (CEO / supervisor / equipo):** [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md).

---

## 1. Regla madre

| Regla | Texto |
|-------|--------|
| **Trello como fuente de verdad del flujo** | Si el trabajo es **formal** (tiene cliente o `dossier_id`, o afecta entregables del holding), debe existir **al menos una tarjeta** que lo represente, o quedar **explícitamente enlazado** a una tarjeta existente (comentario con ID). |
| **Trazabilidad** | Toda tarjeta relevante debe llevar **`dossier_id` visible** (prefijo en título y/o etiqueta `dossier:...`), salvo tareas puramente internas del superusuario acordadas por escrito. |
| **Sin tarjeta = no cuenta como flujo cerrado** | Discord, chat o voz **no sustituyen** el registro en tablero para auditoría y priorización. Excepciones solo con **orden expresa del superusuario** documentada (p. ej. incidente crítico). |

Los agentes **crean, comentan o mueven** tarjetas **solo** dentro de los límites que este documento y [OPENCLAW_PERMISOS_AUTOMATIZACION.md](OPENCLAW_PERMISOS_AUTOMATIZACION.md) permitan (API + `exec`). **Prioridad y cierre de calidad** siguen al **supervisor humano** y al **CEO** según empresa.

---

## 2. Listas del tablero (Kanban mínimo)

Orden lógico **izquierda → derecha**. Los nombres pueden traducirse; la **función** debe conservarse.

| Lista | Función |
|-------|---------|
| **Entrada / Inbox** | Peticiones sin clasificar o recién capturadas. |
| **Triaje / Prioridad** | El supervisor (humano) o el proceso acordado ordena urgencia, fecha y responsable. Jarvis puede **proponer** orden. |
| **Cola** | Trabajo **aprobado** para ejecutar, ordenado. |
| **En progreso** | Está activo ahora (una persona o rol tomó la tarjeta). |
| **En revisión** | Entregable listo para revisión de calidad / alineación con brief. |
| **Listo / Entregado** | Cumple el [criterio de salida](#5-definición-de-hecho-done). |
| **Bloqueado** (opcional) | Falta input externo; exige comentario con motivo. |

Tableros pequeños pueden fusionar **Entrada + Cola** al inicio; no se elimina la idea de **estado visible**.

---

## 3. Formato obligatorio de tarjeta

- **Título:** `[dossier_id] Descripción breve` — ejemplo: `[cli-20260404-cliente-tests-redes] Post IG — oferta fin de semana`.
- **Descripción:** objetivo, alcance, enlace o referencia al brief/dossier; plazo si aplica; marca **BORRADOR** o **NO PUBLICAR** cuando no haya publicación real.
- **Etiquetas:** según [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md) (`dossier:...`, `empresa:marketing`, etc.).
- **Comentarios:** un hilo breve por hito (propuesta Jarvis, cambio de lista, bloqueo, aprobación).

---

## 4. Quién hace qué (Jarvis, subagentes, humanos)

| Acción | Jarvis / agente IA | Supervisor humano | CEO |
|--------|---------------------|-------------------|-----|
| Crear tarjeta desde encargo | Sí | Revisa coherencia | Oversight |
| Priorizar entre clientes | Propone | **Decide** | Estrategia |
| Mover Cola → En progreso | Solo si el superusuario definió regla explícita; si no, **comentar** y pedir | Normalmente **sí** | Si aplica |
| Mover a En revisión / Listo | Puede proponer o mover si convención del tablero lo permite | Valida calidad | Según empresa |
| Desbloquear | Comentar causas y opciones | **Coordina** | Escalación |

**Subagentes** (cuando OpenClaw los lance): el mismo criterio — **toda salida** que sea entregable debe **reflejarse** en Trello (tarjeta nueva o comentario en tarjeta madre con ID y resumen).

---

## 5. Definición de hecho (Done)

Una tarjeta pasa a **Listo / Entregado** cuando:

1. Cumple el **brief** o el alcance descrito en la tarjeta.  
2. El entregable es **usable** (copy final, archivo, decisión documentada), salvo que el estado sea explícitamente “solo propuesta”.  
3. No hay **bloqueos** abiertos sin plan.  
4. La **aprobación** requerida por el cliente o por supervisor interno está **registrada** (comentario o checklist marcado).

---

## 6. Discord y Trello

- **Discord:** coordinación, avisos, hilos (“revisar tarjeta X”).  
- **Trello:** estado y responsabilidad.  
Mensaje en Discord que cierre un trabajo debe **referenciar** enlace corto de tarjeta o `shortLink` cuando sea posible.

---

## 7. Excepciones

| Caso | Tratamiento |
|------|-------------|
| Micro-tarea &lt; 5 min sin impacto en cliente | Puede no crear tarjeta si el superusuario lo indica **en esa sesión**; dejar constancia en `memory` o comentario del día. |
| Solo lectura / consulta | No exige tarjeta nueva; si afecta decisión de cliente, enlazar a tarjeta existente o crear **Seguimiento**. |

---

## 8. Referencias cruzadas

- [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md) — credenciales y rutas.  
- [../../docs/TRELLO_OPENCLAW.md](../../docs/TRELLO_OPENCLAW.md) — uso de API desde OpenClaw.  
- [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) — canales alineados a proyectos.
