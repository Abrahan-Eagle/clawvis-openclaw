# Patrones LightRAG portados a Jarvis (sin servidor LightRAG)

**Proposito:** documentar como las **habilidades** del proyecto [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) (recuperacion dual, KG + vectores, consultas mixtas) se implementan **en Jarvis** mediante el skill **`dual-retrieval-ops`** y las herramientas ya existentes — **sin** instalar `lightrag-hku`, Docker del servidor LightRAG ni duplicar Ollama.

| En LightRAG upstream | En jarvis-ecosystem |
|----------------------|---------------------|
| Indexado con extraccion entidad-relacion (LLM dedicado) | MemPalace (`mempalace_kg_add`, auto-mine) + decisiones humanas en dossiers |
| Almacenamiento vectorial + KV + grafo | Chroma + KG MemPalace + Graphify para mapa del repo |
| API / Web UI | MCP MemPalace, Graphify, lectura de `client-dossiers/` |
| Modo mixto + reranker | Skill `dual-retrieval-ops`: descomponer query, priorizar fuentes |

**Skill:** [../agents/jarvis/skills/dual-retrieval-ops/SKILL.md](../agents/jarvis/skills/dual-retrieval-ops/SKILL.md)

**Criterio de negocio** para desplegar algun dia el **servidor** LightRAG aparte (corpus documental enorme fuera del palace): ver [RECURSOS_COMUNIDAD_OPENCLAW.md](RECURSOS_COMUNIDAD_OPENCLAW.md) §2.8 — solo con aprobacion explicita y host acotado.
