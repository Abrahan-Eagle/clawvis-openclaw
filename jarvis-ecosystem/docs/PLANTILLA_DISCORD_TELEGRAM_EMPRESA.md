# Plantilla Discord y Telegram por empresa

**Objetivo:** misma **estructura lógica** en cada unidad del holding (CEO, supervisor, equipo) con **separación clara**: los clientes **no** tienen canal directo a Jarvis; el único diálogo humano↔IA es el del **superusuario**.

**Última revisión:** abril 2026.

---

## Principios

| Principio | Implementación |
|-----------|----------------|
| Un servidor Discord (o espacio equivalente) **por empresa**, o categorías claramente nombradas en un servidor único. | Evita mezclar permisos y notificaciones entre unidades. |
| **Jarvis** solo en canales que el superusuario use o que estén explícitamente enlazados al agente (Telegram bot, etc.). | No añadir clientes a esos hilos como “usuarios de Jarvis”. |
| **CEO** y **supervisor** con roles distinguibles; el supervisor **mantiene** la organización de canales según acuerdo interno. | Ver [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md). |

---

## Discord — roles sugeridos (por servidor o por categoría)

| Rol | Permisos típicos | Notas |
|-----|------------------|--------|
| `CEO` | Ver todos los canales de gestión; administración opcional según confianza. | No requiere hablar con Jarvis. |
| `Supervisor` | Gestionar canales de proyecto, anclar mensajes, moderar hilos operativos. | Responsable de alinear Discord con Trello. |
| `Equipo` | Canales de trabajo y voz según proyecto. | Sin acceso a canales solo-CEO si existen. |
| `Cliente` (opcional) | Solo canales **proyecto-cliente** acordados: entregas, revisiones, **sin** enlace al bot de Jarvis. | Si el cliente no debe ver internals, usar categoría aparte o solo email/WhatsApp comercial. |

**No** crear un canal “hablar con Jarvis” para clientes ni para CEOs si el modelo acordado es solo superusuario ↔ Jarvis.

---

## Discord — categorías y canales (plantilla)

Ajusta nombres al idioma de la empresa; la **estructura** es lo reutilizable.

| Categoría | Canales sugeridos | Propósito |
|-----------|-------------------|-----------|
| **Dirección** | `#ceo`, `#supervisor-interno` (opcional privado CEO+supervisor) | Decisiones, reportes supervisor→CEO. |
| **Operación** | `#daily`, `#bloqueos`, `#trello-sync` (o anuncios de estado) | Coordinación diaria; el supervisor puede postear resumen de tablero. |
| **Por cliente o proyecto** | `#cliente-<dossier_id>-nombre` | Trabajo y entregas; en descripción del canal: enlace al dossier y al tablero Trello. |
| **Voz** | `Sala equipo`, `Sala cliente` (si aplica) | Llamadas; no sustituye registro escrito en dossier/Trello. |

---

## Telegram (OpenClaw / Jarvis)

| Uso | Recomendación |
|-----|----------------|
| **Superusuario ↔ Jarvis** | Bot principal en chat 1:1 o grupo **exclusivo** del superusuario + Jarvis (sin clientes). |
| **Alertas a CEO/supervisor** | Opcional: canal o grupo **solo lectura** con resúmenes generados (sin exponer el token del bot a clientes). |
| **Clientes** | Grupos comerciales **sin** el bot de Jarvis, o solo canal humano. |

La configuración viva está en `~/.openclaw/openclaw.json` (`bindings`, `channels`). No versionar secretos.

---

## Checklist al dar de alta una empresa nueva

1. Crear servidor Discord (o categoría) con roles CEO / Supervisor / Equipo.
2. Confirmar que **ningún** cliente tiene acceso al chat Telegram/Discord donde opera Jarvis para el superusuario.
3. Documentar IDs de servidor/canal críticos en el dossier interno de la empresa (no en repo público con secretos).
4. Alinear nombres de canal proyecto con `dossier_id` y [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md).
