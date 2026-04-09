# Flujo de trabajo Ventas — prospección, conversación y cierre

**Empresa:** Ventas (workspace `agents/ventas/`).  
**Última revisión:** abril 2026.

**Normas que este flujo respeta:** [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md), [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md), [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md).  
**Dossiers y entregables en disco:** [JARVIS_DOCUMENTS_ON_DISK.md](JARVIS_DOCUMENTS_ON_DISK.md).

---

## 1. Idea central

1. **Conseguir trabajo** = oportunidades **capturadas, evaluadas y priorizadas** (no solo “ver chats”).
2. **Hablar con el cliente** = conversación **en el canal del negocio** (Workana, email, reunión acordada), con **registro en Trello**.
3. **Cerrar** = **alcance, precio y siguiente paso** por escrito; el agente **propone**, el **humano** (CEO) **aprueba** precios y compromisos.

Telegram/Discord personales **no** sustituyen el tablero ni el historial con el cliente en la plataforma donde negociás.

---

## 2. Etapas del embudo (una línea cada una)

| Etapa | Qué es | Salida |
|-------|--------|--------|
| **1. Captura** | Entra un lead (Workana, referido, formulario, LinkedIn). | Datos mínimos + enlace en tarjeta Trello **Inbox/Entrada**. |
| **2. Calificación** | ¿Encaja ICP, plazo, presupuesto probable? | Decisión: **seguir** / **archivar** / **delegar** (con comentario). |
| **3. Diagnóstico** | Preguntas que cierran necesidad (problema, éxito, restricciones). | Notas en tarjeta + enlace a **dossier** si existe o se crea. |
| **4. Propuesta** | Alcance, entregables, plazo, inversión (borrador). | Documento o mensaje marcado **BORRADOR** hasta aprobación humana. |
| **5. Negociación** | Ajustes de alcance, forma de pago, hitos. | Comentarios en tarjeta; **sin promesas finales** sin OK del CEO. |
| **6. Cierre** | Aceptación explícita (contrato, aceptación en plataforma, firma). | Tarjeta → **Listo** con evidencia (enlace, captura en carpeta acordada). |
| **7. Entrega / postventa** | Ejecución y seguimiento; upsell solo si encaja. | Nuevas tarjetas por hito o sub-proyecto. |

---

## 3. Roles de agentes OpenClaw (orientativo)

| Agente | Enfoque en este flujo |
|--------|------------------------|
| **sales-hunter** | Ayuda a **encontrar y filtrar** oportunidades (listas, búsquedas, primer scrape de info pública), **borradores** de primer contacto. |
| **sales-closer** | Ayuda a **estructurar propuesta, manejar objeciones, checklist de cierre**; no fija precio solo. |
| **sales-account** | **Seguimiento**, renovación, satisfacción, próximos pasos después del primer cierre. |

Jarvis (agente maestro) puede **orquestar** y **asignar** tareas; el **CEO** decide prioridad y cierre comercial.

---

## 4. Mapeo a Trello (listas del tablero Ventas)

Alineá las listas del [Kanban mínimo](FLUJO_TRELLO_ECOSISTEMA.md#2-listas-del-tablero-kanban-mínimo) con el embudo:

| Embudo | Lista típica |
|--------|----------------|
| Captura | **Entrada / Inbox** |
| Calificación + diagnóstico | **Triaje / Prioridad** → **Cola** |
| Propuesta + negociación | **En progreso** (una tarjeta por oportunidad seria) |
| Revisión interna | **En revisión** |
| Cierre acordado | **Listo / Entregado** (con criterio de “Done” del flujo Trello) |

**Bloqueado:** solo con comentario (qué falta: cliente, pago, legal).

---

## 5. Workana (freelance) — particularidades

| Paso | Acción |
|------|--------|
| Descubrimiento | Búsqueda en la plataforma + alertas; URLs relevantes pueden pasar por **career-ops** como evaluación de encaje (`agents/ventas/career-ops/`). |
| Primer mensaje | Corto: problema del cliente + plan en 3 puntos + enlace portfolio; **revisión humana** antes de enviar. |
| Chat | Mantener **tono profesional** y **límites de alcance**; lo acordado por Workana queda como trazabilidad. |
| Cierre | Aceptación del proyecto en la plataforma o acuerdo por hitos según reglas de Workana; reflejar en Trello + dossier. |

No automatizar envíos masivos ni violar ToS de la plataforma.

---

## 6. Frases tipo para pedir ayuda a Jarvis (copiar y adaptar)

- «Nueva oportunidad: [enlace o texto]. Calificá encaje con nuestro ICP y sugerí siguientes preguntas al cliente.»
- «Redactá un borrador de propuesta para [alcance] con entregables y supuestos; **no incluyas precio final** hasta que yo lo confirme.»
- «Lista de objeciones probables para este tipo de proyecto y respuestas cortas.»
- «Resumen para Trello: título de tarjeta con `[dossier_id]`, descripción en tres bullets y siguiente paso.»

---

## 7. Líneas rojas (sin excepción informal)

- **Precios, descuentos y plazos contractuales:** fuente = CEO o documento aprobado; el agente no inventa ([AGENTS.md](../agents/ventas/AGENTS.md)).
- **Datos de clientes:** solo canales y repos autorizados.
- **“Cerrado” en Trello:** solo con evidencia acordada en la sección [Done](FLUJO_TRELLO_ECOSISTEMA.md#5-definición-de-hecho-done).

---

## 8. Cadencia sugerida (humano + sistema)

| Frecuencia | Actividad |
|------------|-----------|
| **Diaria (15 min)** | Revisar **Inbox** Trello + mensajes en **canales de negocio** (Workana, email). |
| **2–3× semana** | Bloque de **prospección** (nuevas oportunidades, actualizar `portals`/búsquedas). |
| **Semanal** | Revisar embudo completo, una pasada de **seguimiento** a propuestas abiertas. |

---

*Este documento es la referencia de flujo para Ventas; ajustá nombres de listas si tu tablero ya existe con otra nomenclatura, manteniendo la **función** de cada etapa.*
