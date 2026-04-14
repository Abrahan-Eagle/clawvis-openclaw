# Graphify — Mapa estructural del ecosistema (integrado abr 2026)

Graphify convierte el repositorio en un **grafo de conocimiento consultable**: nodos (archivos, secciones), aristas (referencias entre docs), comunidades (clusters de temas relacionados). Complementa a MemPalace sin reemplazarlo.

## Convención: Graphify vs MemPalace

| Capa | Herramienta | Qué hace |
|------|-------------|----------|
| **Mapa estructural** | Graphify | Relaciones entre archivos/secciones del repo. God nodes, comunidades, conexiones. Regenerable desde el repo. |
| **Memoria semántica** | MemPalace | Búsqueda por significado, Knowledge Graph de decisiones/clientes/empresas. Datos acumulativos. |

No mezclar: Graphify es el **mapa**; MemPalace es la **memoria**.

---

## Qué genera

Todo en `graphify-out/` (gitignored, regenerable):

| Archivo | Qué es |
|---------|--------|
| `GRAPH_REPORT.md` | Reporte: god nodes, comunidades, conexiones sorprendentes, preguntas sugeridas |
| `graph.json` | Grafo persistente (NetworkX serializado). Se consulta sin releer el repo |
| `graph.html` | Visualización interactiva (click nodos, buscar, filtrar por comunidad) |

## God nodes actuales

Los nodos más conectados del ecosistema (conceptos centrales):

- **README**, **AGENTS** (docs de workspace de cada agente)
- **OPERACION_POST_GOBIERNO** (índice de fases operativas)
- **GOBIERNO_JARVIS_V2** (modelo de gobierno)
- **CONVENCION_TRELLO_EMPRESA_CLIENTE** (convención Trello)
- **MEMORY** (memoria de largo plazo de Jarvis)

Estos son los documentos que **más otros documentos referencian**. Si algo cambia en un god node, el impacto se propaga.

---

## Comandos útiles

```bash
# Consultar el grafo (sin LLM, desde terminal)
graphify query "qué conecta a ventas con marketing"
graphify query "cómo funciona el gobierno" --budget 3000

# Ruta más corta entre dos nodos
graphify path "AGENTS" "GOBIERNO_JARVIS_V2"

# Explicar un nodo
graphify explain "MEMORY"

# Actualizar el grafo tras cambios en código (AST, sin LLM)
graphify update .

# Reconstruir clusters sin re-extraer
graphify cluster-only .
```

## Actualización del grafo

El grafo se actualiza de dos formas:

1. **Manual**: correr el script de build (ver sección siguiente) cuando hay cambios significativos en la documentación
2. **Automático**: `graphify update .` para cambios de código (AST, sin coste de API)

El caché SHA256 (`graphify-out/cache/`) evita reprocesar archivos sin cambios.

## MCP Server

Registrado en `~/.openclaw/openclaw.json` bajo `mcp.servers.graphify`. Herramientas disponibles:

- `query_graph` -- buscar en el grafo
- `get_node` -- obtener un nodo y sus atributos
- `get_neighbors` -- nodos vecinos
- `shortest_path` -- ruta más corta entre dos nodos
- `god_nodes` -- los nodos más conectados

## Always-on en Cursor y OpenClaw

- **Cursor**: `.cursor/rules/graphify.mdc` (alwaysApply: true) — lee GRAPH_REPORT.md antes de responder preguntas de arquitectura
- **OpenClaw**: `AGENTS.md` en raíz del repo — mismas reglas

## Instalación (referencia)

```bash
pipx install graphifyy    # v0.4.13
graphify cursor install   # Cursor rules
graphify claw install     # OpenClaw AGENTS.md
```

---

**Repo fuente:** [safishamsi/graphify](https://github.com/safishamsi/graphify) (26.4k stars, MIT)
