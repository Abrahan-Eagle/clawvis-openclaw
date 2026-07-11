# Memoria avanzada — MemPalace (integrado abr 2026)

**Cierre del módulo, restore desde Git y checklist:** [MODULO_MEMPALACE_CIERRE.md](MODULO_MEMPALACE_CIERRE.md) — leer antes de replicar en otra máquina.

Sistema de memoria complementario a `memory-core` de OpenClaw. Aporta busqueda semantica local (ChromaDB), Knowledge Graph temporal (SQLite) y estructura jerarquica (Wings/Rooms/Drawers).

**No reemplaza** la memoria nativa de OpenClaw (`MEMORY.md`, `memory/*.md`, session-memory hook). Es un **complemento** que agrega recall semantico y grafo de conocimiento.

### `agents.defaults.memorySearch` (plantilla OpenClaw)

En `config/openclaw-home/openclaw.json` la plantilla deja **`memorySearch.enabled: false`** por defecto. Motivo: el índice vectorial nativo exige Ollama + modelo `nomic-embed-text` y sync; activarlo sin ese runtime satura CPU o falla en silencio.

| Capa | Estado en plantilla | Notas |
|------|---------------------|-------|
| `memoryFlush` pre-compaction | **enabled** | Persistencia a `memory/` antes de compactar |
| `memorySearch` (vector nativo) | **disabled** | Activar solo tras verificar Ollama + embed; gate AG-07 si se toca runtime |
| MemPalace MCP | Complementario | Independiente de `memorySearch` |
| `memory-store` (`memory.json`) | Activo en repo | Session Startup: `format-prompt` |

Cuando el CEO active búsqueda vectorial nativa: poner `enabled: true`, `sync.onSessionStart` según carga, y documentar en este archivo.

**Patrones tipo LightRAG (sin instalar LightRAG):** el skill [`dual-retrieval-ops`](../agents/jarvis/skills/dual-retrieval-ops/SKILL.md) usa MemPalace + dossiers como capa “local” y KG + Graphify como capa “global”. No es otro producto de memoria; es metodología. Detalle: [DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md](DUAL_RETRIEVAL_LIGHTRAG_PATTERNS.md) y [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) §2.8.

---

## Arquitectura

```
OpenClaw gateway
  ├── memory-core (nativo)
  │     ├── MEMORY.md + memory/*.md
  │     ├── session-memory hook (activado)
  │     ├── memoryFlush pre-compaction (activado)
  │     └── Vector index: Ollama nomic-embed-text → SQLite-vec
  │
  └── MemPalace MCP Server (complementario)
        ├── ChromaDB local (~/.mempalace/palace/)
        │     ├── Wing: jarvis (agents, docs, automations, scripts)
        │     └── Wing: jarvis_sessions (transcripts OpenClaw)
        ├── Knowledge Graph (~/.mempalace/knowledge_graph.sqlite3)
        │     └── 54 triples: empresas, agentes, clientes, decisiones, tech stack
        └── Auto-mine timer (systemd, cada 30 min)
```

---

## Ubicaciones en disco

| Componente | Ruta |
|-----------|------|
| Palace (ChromaDB) | `~/.mempalace/palace/` |
| Knowledge Graph | `~/.mempalace/knowledge_graph.sqlite3` |
| Config | `~/.mempalace/config.json` |
| Wing config | `~/.mempalace/wing_config.json` |
| Identity (L0) | `~/.mempalace/identity.txt` |
| Auto-mine script | `~/.openclaw/hooks/mempalace-auto-mine.sh` |
| Auto-mine log | `~/.mempalace/auto-mine.log` |
| Systemd timer | `~/.config/systemd/user/mempalace-auto-mine.timer` |
| MCP Server config | `~/.openclaw/openclaw.json` → `mcp.servers.mempalace` |

---

## Comandos utiles

```bash
# Estado del palace
mempalace status

# Busqueda semantica
mempalace search "que decidimos sobre ventas"

# Minar archivos nuevos manualmente
mempalace mine /var/www/clawvis-openclaw/jarvis-ecosystem --wing jarvis --agent jarvis

# Minar sesiones OpenClaw
# (copiar .jsonl activos a un dir temporal con mempalace.yaml, luego)
mempalace mine /tmp/sessions-dir --mode convos --wing jarvis_sessions --agent jarvis

# Verificar timer
systemctl --user status mempalace-auto-mine.timer

# Ejecutar auto-mine manual
~/.openclaw/hooks/mempalace-auto-mine.sh

# Knowledge Graph: consultar entidad
python3 -c "
from mempalace.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
for r in kg.query_entity('ventas'): print(r)
"

# KG: timeline completo
python3 -c "
from mempalace.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
for r in kg.timeline(): print(r)
"
```

**Nota:** el binario Python de mempalace esta en el venv de pipx: `/home/aipp/.local/share/pipx/venvs/mempalace/bin/python3`. Para scripts que importen `mempalace` directamente, usar ese interprete.

---

## MCP Server (herramientas disponibles)

El server MCP expone estas herramientas a agentes OpenClaw y Cursor:

| Herramienta | Descripcion |
|------------|------------|
| `mempalace_status` | Vision general del palace |
| `mempalace_search` | Busqueda semantica en drawers |
| `mempalace_list_wings` | Listar wings con conteo |
| `mempalace_list_rooms` | Listar rooms de un wing |
| `mempalace_get_taxonomy` | Taxonomia completa |
| `mempalace_kg_query` | Consultar relaciones de una entidad |
| `mempalace_kg_add` | Agregar triple al KG |
| `mempalace_kg_invalidate` | Marcar hecho como expirado |
| `mempalace_kg_timeline` | Timeline cronologico |
| `mempalace_kg_stats` | Estadisticas del KG |
| `mempalace_add_drawer` | Agregar contenido al palace |
| `mempalace_traverse` | Navegar grafo del palace |
| `mempalace_find_tunnels` | Conexiones entre wings |

---

## Mantenimiento

- **Actualizaciones:** `pipx upgrade mempalace`. Verificar compatibilidad de schema ChromaDB antes de actualizar (pinear version si es critico).
- **Backup:** copiar `~/.mempalace/` completo (palace + KG + config).
- **Re-mine completo:** borrar `~/.mempalace/palace/`, recrear con `mempalace init`, minar de nuevo.
- **Issue #110 (MemPalace upstream):** shell injection en hooks. No activar hooks automaticos de MemPalace directamente; nuestro auto-mine usa script propio controlado.

---

## Lo que NO se usa de MemPalace (y por que)

- **AAAK (compresion lossy):** regresa en benchmarks (84.2% vs 96.6% recall); sin beneficio a esta escala.
- **Specialist Agents / diarios AAAK:** Jarvis ya tiene agentes (`sales-hunter`, etc.) con estructura superior.
- **Contradiction detection:** no conectada al KG en upstream; esperar correccion.

---

**Documentos relacionados:**
- [`RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md`](../../docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md)
- [`agents/jarvis/AGENTS.md`](../agents/jarvis/AGENTS.md)
- [`agents/ventas/AGENTS.md`](../agents/ventas/AGENTS.md)
