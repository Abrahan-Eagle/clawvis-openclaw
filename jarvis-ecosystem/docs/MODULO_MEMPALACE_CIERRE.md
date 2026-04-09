# Módulo MemPalace — documentación de cierre (abr 2026)

**Estado:** módulo **cerrado** a nivel documentación y artefactos en repo.  
**Objetivo:** poder **replicar** el stack en otra máquina o **recuperar** tras imprevisto, combinando **git + pasos de sistema + datos locales opcionales**.

---

## 1. Qué incluye este módulo

| Capa | Función |
|------|---------|
| **OpenClaw `memory-core`** | Embeddings locales (**Ollama** `nomic-embed-text`), búsqueda híbrida sobre `MEMORY.md` / `memory/*.md`, hook **session-memory**, **memoryFlush** antes de compactar. |
| **MemPalace** | ChromaDB en `~/.mempalace/palace/` (drawers por wing/room), **Knowledge Graph** SQLite (`~/.mempalace/knowledge_graph.sqlite3`), **MCP** `mempalace_*` en OpenClaw. |
| **Auto-mine** | Script + timer systemd (~30 min) para re-indexar ecosistema y sesiones JSONL. |

**No incluye:** enrutado automático de LLM por dificultad (eso es Cursor/OpenClaw/model-router, no MemPalace). **No sustituye** Trello ni los Markdown como fuente de verdad humana.

---

## 2. Qué queda versionado en Git (clonable)

| Ruta en repo | Contenido |
|--------------|-----------|
| `jarvis-ecosystem/mempalace.yaml` | Taxonomía rooms/wing tras `mempalace init` sobre el ecosistema. |
| `jarvis-ecosystem/docs/MEMORIA_MEMPALACE.md` | Referencia técnica (arquitectura, comandos, herramientas MCP). |
| **Este archivo** | Cierre, restore completo, checklist. |
| `jarvis-ecosystem/docs/OPERACION_POST_GOBIERNO.md` | Índice operativo (enlace a memoria avanzada). |
| `docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md` | Respaldo de config OpenClaw (sección MemPalace). |
| `config/openclaw-home/openclaw.json` | **Plantilla** de config (memorySearch, hooks, mcp, compaction). **Rutas de ejemplo:** ajustar usuario y rutas al clonar. |
| `deploy/mempalace/` | Scripts, units systemd, plantillas, ejemplo `restore.env`. |

---

## 3. Qué no va en Git (o se regenera)

| Elemento | Notas |
|----------|--------|
| `~/.mempalace/palace/` | Base ChromaDB; **se regenera** con `mempalace mine`. Opcional: backup `tar` para no re-embeddar. |
| `~/.mempalace/knowledge_graph.sqlite3` | **Se regenera** con `deploy/mempalace/kg-populate-ecosystem.sh` (o triples vía MCP). |
| `~/.openclaw/openclaw.json` (real) | Vive en HOME; la copia “oficial” para documentar es `config/openclaw-home/openclaw.json`. |
| `pipx`, Ollama, modelos | Instalación en el host. |
| `entities.json` (si existe) | Generado por `mempalace init`; puede commitearse o ignorarse según política del repo. |

---

## 4. Checklist: nueva máquina desde cero

### 4.1 Prerrequisitos

- Node.js + OpenClaw instalado (`openclaw` en PATH).
- **Ollama** escuchando en `127.0.0.1:11434` y modelo **`nomic-embed-text`** (`ollama pull nomic-embed-text`).
- **Python 3.9+** y **pipx**: `pipx install mempalace` (versión acordada, p. ej. 3.0.0).

### 4.2 Repositorio

```bash
git clone <url-del-repo> clawvis-openclaw
cd clawvis-openclaw/jarvis-ecosystem   # o la ruta donde esté el ecosistema
```

Asegurar que exista `mempalace.yaml` en la raíz del árbol que se va a minar (incluido en git).

### 4.3 Directorios MemPalace en HOME

```bash
mkdir -p ~/.mempalace/palace ~/.config/mempalace
cp deploy/mempalace/templates/config.json ~/.mempalace/config.json
cp deploy/mempalace/templates/wing_config.json ~/.mempalace/wing_config.json
cp deploy/mempalace/templates/identity.txt ~/.mempalace/identity.txt
# Editar config.json: sustituir /home/TU_USUARIO por tu HOME real.
```

### 4.4 Primera indexación (ecosistema + opcional sesiones)

```bash
export PATH="${HOME}/.local/bin:${PATH}"
mempalace mine /ruta/al/clon/jarvis-ecosystem --wing jarvis --agent jarvis
# Sesiones: copiar *.jsonl activos a un tmp con mempalace.yaml mínimo; ver MEMORIA_MEMPALACE.md
```

### 4.5 Knowledge Graph (hechos del holding)

```bash
cd /ruta/al/clon
chmod +x deploy/mempalace/kg-populate-ecosystem.sh
./deploy/mempalace/kg-populate-ecosystem.sh
```

Editar `deploy/mempalace/kg-populate-ecosystem.py` si el holding cambia (empresas, clientes, fechas).

### 4.6 OpenClaw

1. Copiar `config/openclaw-home/openclaw.json` → `~/.openclaw/openclaw.json` (o fusionar bloques).
2. **Sustituir en todo el archivo:**
   - `/home/aipp` → tu `$HOME` o usuario real.
   - Rutas `workspace` de agentes → donde clonaste `jarvis-ecosystem` (p. ej. `/home/usuario/clawvis-openclaw/jarvis-ecosystem/...`).
3. Bloques imprescindibles del módulo:
   - `agents.defaults.memorySearch` (provider `ollama`, model `nomic-embed-text`).
   - `hooks.internal.entries["session-memory"].enabled`: `true`.
   - `agents.defaults.compaction.memoryFlush.enabled`: `true` (y `postIndexSync` si se desea).
   - `mcp.servers.mempalace`: **command** = Python del venv pipx de mempalace; **env** `MEMPALACE_PALACE` = `~/.mempalace/palace`.

Obtener ruta del intérprete pipx:

```bash
pipx runpip mempalace list  # comprobar entorno
# Típico Linux:
# ~/.local/share/pipx/venvs/mempalace/bin/python3
```

4. Reindexar memoria OpenClaw:

```bash
openclaw memory index --agent jarvis
openclaw memory status --agent jarvis
```

5. Reiniciar gateway: `systemctl --user restart openclaw-gateway` (o el método que uses).

### 4.7 Auto-mine (opcional pero recomendado)

```bash
mkdir -p ~/.openclaw/hooks
cp deploy/mempalace/mempalace-auto-mine.sh ~/.openclaw/hooks/
chmod +x ~/.openclaw/hooks/mempalace-auto-mine.sh
cp deploy/mempalace/restore.env.example ~/.config/mempalace/restore.env
# Editar restore.env: JARVIS_ECOSYSTEM=/ruta/absoluta/al/clon/jarvis-ecosystem
cp deploy/mempalace/mempalace-auto-mine.service ~/.config/systemd/user/
cp deploy/mempalace/mempalace-auto-mine.timer ~/.config/systemd/user/
# Editar .service si el script no está en ~/.openclaw/hooks/
systemctl --user daemon-reload
systemctl --user enable --now mempalace-auto-mine.timer
```

---

## 5. Verificación rápida

```bash
mempalace status
mempalace search "ventas workana"
~/.local/share/pipx/venvs/mempalace/bin/python3 -c "from mempalace.knowledge_graph import KnowledgeGraph; print(KnowledgeGraph().stats())"
openclaw memory status --agent jarvis
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' | \
  ~/.local/share/pipx/venvs/mempalace/bin/python3 -m mempalace.mcp_server 2>/dev/null | head -1
```

---

## 6. Backup ante imprevistos (fuera de git)

- `tar czf mempalace-backup-$(date +%F).tar.gz ~/.mempalace ~/.config/mempalace/restore.env`
- Copia cifrada opcional de `~/.openclaw/openclaw.json` (sin secretos en git; secretos en `~/.openclaw/.env`).

---

## 7. Checklist antes de `git push` (mantenedor)

- [ ] `jarvis-ecosystem/docs/MODULO_MEMPALACE_CIERRE.md` actualizado si cambia el procedimiento.
- [ ] `deploy/mempalace/` refleja el script y units vigentes.
- [ ] `config/openclaw-home/openclaw.json` sin secretos; rutas marcadas como ejemplo o usuario de referencia.
- [ ] `mempalace.yaml` en `jarvis-ecosystem/` coherente con la estructura del repo.
- [ ] Probar en limpio (VM o otro usuario) al menos: `mempalace mine` + `openclaw memory index` + MCP arranca.

---

## 8. Referencias cruzadas

- Técnica detallada: [MEMORIA_MEMPALACE.md](MEMORIA_MEMPALACE.md)
- Respaldo OpenClaw: [../../docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](../../docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md)
- Artefactos deploy: [../../deploy/mempalace/README.md](../../deploy/mempalace/README.md)

---

**Última revisión documental:** 2026-04-08. Módulo considerado **cerrado** para el alcance definido en el plan de integración (P0–P5).
