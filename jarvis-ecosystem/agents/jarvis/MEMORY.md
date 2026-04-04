# MEMORY.md - Long-term memory

Solo lectura/escritura en sesion principal con el humano (ver `AGENTS.md`).

---

## Holding / empresas

Registro completo: [../../COMPANIES.md](../../COMPANIES.md).

**CEO / Supervisor (Fase 1):** [../../docs/ASIGNACION_ROLES.md](../../docs/ASIGNACION_ROLES.md).

| Empresa | Estado | Notas rapidas |
|---------|--------|---------------|
| marketing | Activa | Workspace `agents/marketing/`. Agentes: mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email. |
| ventas | Activa | Workspace `agents/ventas/`. Agentes: sales-hunter, sales-closer, sales-account. |
| dev-agency | Planificada | Sin workspace aun. |
| legal | Planificada | Sin workspace aun. |
| contadores | Planificada | Sin workspace aun. |

Gobierno operativo: [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).

**Operacion post gobierno (indice):** [../../docs/OPERACION_POST_GOBIERNO.md](../../docs/OPERACION_POST_GOBIERNO.md).

---

## Clientes activos (dossiers)

Directorio: [../../client-dossiers/](../../client-dossiers/).  
Plantilla vacia: [../../client-dossiers/cli-PLANTILLA-vacio.json](../../client-dossiers/cli-PLANTILLA-vacio.json).

| dossier_id | Cliente | Empresa asignada | Estado |
|------------|---------|------------------|--------|
| `cli-20260404-ejemplo` | ACME Ferreteria C.A. (ejemplo) | marketing | Ejemplo de documentacion |
| `cli-20260404-cliente-tests-redes` | Cliente TESTS (IG + FB) | marketing | **Cliente prueba** — depuracion ecosistema; ver [BRIEF_CLIENTE_TESTS_REDES.md](../../client-dossiers/BRIEF_CLIENTE_TESTS_REDES.md) |

---

## Trello (referencia por empresa — Fase 3)

Convencion: [../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md).  
Credenciales: solo `~/.openclaw/.env` (`TRELLO_API_KEY`, `TRELLO_TOKEN`).

| Empresa | Board (nombre) | Board ID | Listas / notas |
|---------|----------------|----------|----------------|
| *(legacy)* | Mi tablero de Trello | `69d0a352e4fed9476a5f6cec` | Migrar a convencion por empresa cuando aplique |
| `marketing` | *(rellenar)* | *(rellenar)* | Backlog / En curso / Revision supervisor / Bloqueado / Hecho |
| `ventas` | *(rellenar)* | *(rellenar)* | Idem |

---

## Discord (Fase 4)

Checklist: [../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md](../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md).  
Plantilla: [../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md).

*(Opcional: anotar aqui IDs de servidor/categoria solo si el superusuario quiere que Jarvis los referencie en sesion; evitar secretos.)*

---

## Reportes supervisor → CEO (Fase 5)

Formato: [../../docs/SUPERVISOR_CEO_REPORTE.md](../../docs/SUPERVISOR_CEO_REPORTE.md).

---

## Decisiones de gobierno (log)

- **2026-04-04:** Modelo de gobierno v2 formalizado. Jarvis es agente maestro; cada empresa con CEO + supervisor + equipo; clientes como dossiers de contexto; solo el superusuario dialoga con Jarvis.
- **2026-04-04:** Cliente de prueba `cli-20260404-cliente-tests-redes` (Instagram + Facebook, empresa marketing) para depurar ecosistema; brief en `client-dossiers/BRIEF_CLIENTE_TESTS_REDES.md`.
