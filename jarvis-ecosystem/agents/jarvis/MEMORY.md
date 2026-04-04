# MEMORY.md - Long-term memory

Solo lectura/escritura en sesion principal con el humano (ver `AGENTS.md`).

---

## Holding / empresas

Registro completo: [../../COMPANIES.md](../../COMPANIES.md).

**CEO / Supervisor (Fase 1):** [../../docs/ASIGNACION_ROLES.md](../../docs/ASIGNACION_ROLES.md). Nombres de **ejemplo** por empresa (no el superusuario); ver tabla en ese archivo.

| Empresa | Estado | Notas rapidas |
|---------|--------|---------------|
| marketing | Activa | Workspace `agents/marketing/`. Agentes: mkt-content, mkt-social, mkt-analytics, mkt-ads, mkt-email. |
| ventas | Activa | Workspace `agents/ventas/`. Agentes: sales-hunter, sales-closer, sales-account. |
| dev-agency | Planificada | Sin workspace aun. |
| legal | Planificada | Sin workspace aun. |
| contadores | Planificada | Sin workspace aun. |

Gobierno operativo: [../../docs/GOBIERNO_JARVIS_V2.md](../../docs/GOBIERNO_JARVIS_V2.md).

**Operacion post gobierno (indice):** [../../docs/OPERACION_POST_GOBIERNO.md](../../docs/OPERACION_POST_GOBIERNO.md).

**Archivos en disco (entregables, medios):** solo bajo `~/Documents/JARVIS-DOCUMENTS/` (carpeta **`Documents`**, no `Documentos`) — arbol por empresa y cliente. Especificacion completa: [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md).

**Integraciones OpenClaw (Trello, Discord, Telegram):** ya configuradas en el gateway — ver [../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md). No proponer reinstalar salvo orden del superusuario.

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
Integracion OpenClaw: **configurada** ([../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](../../docs/INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)). Credenciales API: solo `~/.openclaw/.env` (`TRELLO_API_KEY`, `TRELLO_TOKEN`).

**Esqueleto (tableros + listas):** guía paso a paso y script — [../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md), script [../../scripts/trello-bootstrap-boards.sh](../../scripts/trello-bootstrap-boards.sh). Si la API devuelve `401`, el token actual es **solo lectura**: crear tableros a mano o regenerar token con escritura en [trello.com/app-key](https://trello.com/app-key).

| Empresa | Board (nombre) | Board ID | Listas / notas |
|---------|----------------|----------|----------------|
| *(legacy)* | Mi tablero de Trello | `69d0a352e4fed9476a5f6cec` | Puede quedar como sandbox; preferir tableros `Empresa-*` para operacion |
| `marketing` | Empresa-marketing - Operaciones | *(rellenar tras crear)* | Backlog → En curso → Revisión supervisor → Bloqueado → Hecho |
| `ventas` | Empresa-ventas - Operaciones | *(rellenar tras crear)* | Idem |

---

## Discord (Fase 4)

Integracion OpenClaw: **configurada** (Discord como canal del gateway). Referencia organizativa: [../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md](../../docs/DISCORD_ESTRUCTURA_CHECKLIST.md), [../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md](../../docs/PLANTILLA_DISCORD_TELEGRAM_EMPRESA.md). Verificacion documental: [../../docs/VERIFICACION_DISCORD_FASE4.md](../../docs/VERIFICACION_DISCORD_FASE4.md).

**Esqueleto de canales (servidor Jarvis):** lista concreta en [../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md](../../docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md) sección 2 — crear categorías/canales en la app Discord (no automatizable sin bot con permisos).

Telegram: mismo gateway OpenClaw; no repetir integracion desde el repo.

*(Opcional: anotar aqui IDs de servidor/categoria solo si el superusuario quiere que Jarvis los referencie en sesion; evitar secretos.)*

---

## Reportes supervisor → CEO (Fase 5)

Formato: [../../docs/SUPERVISOR_CEO_REPORTE.md](../../docs/SUPERVISOR_CEO_REPORTE.md).  
Plantilla copiable: [../../docs/plantillas/REPORTE_SUPERVISOR_CEO.md](../../docs/plantillas/REPORTE_SUPERVISOR_CEO.md).

---

## Decisiones de gobierno (log)

- **2026-04-04:** Modelo de gobierno v2 formalizado. Jarvis es agente maestro; cada empresa con CEO + supervisor + equipo; clientes como dossiers de contexto; solo el superusuario dialoga con Jarvis.
- **2026-04-04:** Cliente de prueba `cli-20260404-cliente-tests-redes` (Instagram + Facebook, empresa marketing) para depurar ecosistema; brief en `client-dossiers/BRIEF_CLIENTE_TESTS_REDES.md`.
- **2026-04-04:** Documentado en repo que Trello, Discord y Telegram ya estan integrados en OpenClaw (`INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md`); plantilla Fase 5 y verificacion Discord Fase 4 añadidas.
- **2026-04-04:** Unificada convencion de ruta: carpeta del sistema **`Documents`** (`~/Documents/`), explicitamente no `documentos` / `Documentos` / `~/Documentos/` salvo excepcion en WORKSPACE_POLICY.
- **2026-04-04:** Añadidos `BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md` y `scripts/trello-bootstrap-boards.sh`. API Trello en este entorno rechazo escritura (401); esqueleto de tableros/canales manual o token con permiso de escritura.
