# MEMORY.md - Long-term memory

Solo lectura/escritura en sesion principal con el humano (ver `AGENTS.md`).

---

## Holding / empresas

Registro completo: [../../COMPANIES.md](../../COMPANIES.md).

| Empresa | Estado | Notas rapidas |
|---------|--------|---------------|
| marketing | Activa | Workspace `agents/marketing/`. Agentes: mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email. |
| ventas | Activa | Workspace `agents/ventas/`. Agentes: sales-hunter, sales-closer, sales-account. |
| dev-agency | Planificada | Sin workspace aun. |
| legal | Planificada | Sin workspace aun. |
| contadores | Planificada | Sin workspace aun. |

Gobierno operativo: [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).

---

## Clientes activos (dossiers)

Directorio: [../../client-dossiers/](../../client-dossiers/).

| dossier_id | Cliente | Empresa asignada | Estado |
|------------|---------|------------------|--------|
| `cli-20260404-ejemplo` | ACME Ferreteria C.A. (ejemplo) | marketing | Ejemplo de documentacion |

Al agregar un cliente real, actualizar esta tabla como indice rapido.

---

## Trello (referencia rapida)

IDs utiles para la API (`curl` / skill **trello**). Actualiza con `GET /1/boards/{boardId}/lists` si anades listas.

| Recurso | Nombre | ID |
|---------|--------|-----|
| Tablero | Mi tablero de Trello | `69d0a352e4fed9476a5f6cec` |
| Lista | (rellenar) | — |

Convencion de tableros por empresa: [../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md](../../docs/CONVENCION_TRELLO_EMPRESA_CLIENTE.md).

**Nota:** credenciales solo en `~/.openclaw/.env` (`TRELLO_API_KEY`, `TRELLO_TOKEN`), no en este archivo.

---

## Decisiones de gobierno (log)

- **2026-04-04:** Modelo de gobierno v2 formalizado. Jarvis es agente maestro; cada empresa con CEO + supervisor + equipo; clientes como dossiers de contexto; solo el superusuario dialoga con Jarvis.
