# Convención Trello por empresa y vínculo con dossier de cliente

**Objetivo:** que cada unidad del holding tenga tableros **predecibles** y que cada tarjeta de trabajo pueda enlazarse al **`dossier_id`** del cliente para trazabilidad y contexto de Jarvis.

**Última revisión:** abril 2026.  
**API / credenciales:** ver [../../docs/TRELLO_OPENCLAW.md](../../docs/TRELLO_OPENCLAW.md).

**Flujo operativo obligatorio (listas, Done, roles):** todo agente y subagente debe cumplir [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md) además de esta convención.

---

## 1. Estructura recomendada por empresa

| Nivel | Convención | Notas |
|-------|------------|--------|
| **Workspace Trello** | Un workspace por holding o **uno por empresa** si el volumen es alto. | Facilita permisos por CEO/supervisor. |
| **Board** | Nombre: `Empresa-<NombreCorto> — Operaciones` o `Empresa-<NombreCorto> — <Año>`. | Un board principal por empresa; boards extra para programas grandes opcional. |
| **Listas** | Backlog \| En curso \| Revisión supervisor \| Bloqueado \| Hecho (ajustar a Kanban interno). | El **supervisor** mueve tarjetas y mantiene coherencia con Discord. |

---

## 2. Vínculo `dossier_id` ↔ Trello

Cada cliente con dossier debe ser **identificable** en Trello de una de estas formas (elige una y sé consistente):

| Método | Cómo | Ventaja |
|--------|------|---------|
| **A. Lista por cliente** | Lista llamada `Cliente: <nombre>` o `CLI-<dossier_id>`; las tarjetas del cliente viven ahí. | Vista rápida por cliente. |
| **B. Etiqueta (label)** | Color por tipo de servicio; **etiqueta de texto** `dossier:cli-20260404-acme` en todas las tarjetas de ese cliente. | Mezcla listas funcionales (En curso) con filtro por cliente. |
| **C. Prefijo en título** | Título de tarjeta: `[cli-20260404-acme] Diseño banner Q2`. | Visible en notificaciones y búsqueda sin depender de labels. |

**Recomendación:** **B + C** (etiqueta + prefijo corto) cuando un mismo tablero mezcla varios clientes en “En curso”.

---

## 3. Tarjeta madre (opcional)

Para clientes grandes, crear **una tarjeta índice** por cliente:

- **Título:** `[DOSSIER] cli-20260404-acme — Nombre comercial`
- **Descripción:** enlace al dossier (Notion, archivo Markdown, JSON), contacto, enlaces Discord del proyecto.
- **Checklist:** hitos alineados a `planificacion_resumen` del dossier.

El supervisor mantiene esta tarjeta cuando cambia el alcance acordado.

---

## 4. Encargos cruzados (otra empresa del holding)

| Situación | Convención |
|-----------|-------------|
| Empresa A delega trabajo a Empresa B | Tarjeta en **board de A** con etiqueta `delegado-a:B` y comentario con enlace a **tarjeta espejo** en board de B (o mismo `dossier_id` en ambos). |
| Seguimiento único | Un solo `dossier_id` del cliente; la tarjeta en B replica el mismo prefijo `[dossier_id]` en el título. |

---

## 5. Campos personalizados (si usas Trello Power-Ups)

Si están disponibles, campos útiles:

- `dossier_id` (texto)
- `empresa_interna` (lista: marketing, dev_agency, …)
- `supervisor` (miembro)

---

## 6. Rol del supervisor

- Crear/ajustar listas y etiquetas según esta convención.
- Revisar que ninguna tarjeta de cliente quede sin `dossier_id` visible (etiqueta o título).
- Sincronizar **estados** con Discord (mensaje en `#trello-sync` o hilo del proyecto cuando cambie Bloqueado/Hecho).

---

## 7. Referencias

- [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md) — norma obligatoria de flujo para Jarvis, agentes y subagentes.
- [CLIENT_DOSSIER_SCHEMA.md](CLIENT_DOSSIER_SCHEMA.md) — campos del dossier.
- [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md) — flujo supervisor → CEO y solo superusuario ↔ Jarvis.
- [PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md) — canales alineados a proyectos cliente.
