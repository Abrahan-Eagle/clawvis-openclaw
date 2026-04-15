---
name: dual-retrieval-ops
description: "Patrones de recuperacion inspirados en LightRAG (HKUDS): busqueda local + global, hechos con citas, descomposicion de preguntas mixtas — usando MemPalace, Graphify y dossiers. No requiere instalar lightrag-hku."
---

# Dual retrieval ops (patrones LightRAG en Jarvis)

Inspiracion: [LightRAG](https://github.com/HKUDS/LightRAG) (paper EMNLP 2025, arXiv:2410.05779) — RAG con recuperacion en dos niveles (detalle local + contexto global) y grafo de conocimiento sobre el corpus. **En este ecosistema no desplegamos el servidor LightRAG**; replicamos las **habilidades operativas** que mejor encajan con OpenClaw:

| Idea LightRAG | Equivalente Jarvis |
|---------------|-------------------|
| Recuperacion "local" (fragmentos especificos) | `mempalace_search` acotado, lectura de `client-dossiers/`, `memory/*.md`, tarjeta Trello citada |
| Recuperacion "global" (temas amplios) | `mempalace_kg_query` / timeline, `graphify` MCP o `GRAPH_REPORT.md` para mapa del repo |
| Grafo inducido del texto | KG MemPalace (hechos de negocio) + enlaces entre docs vía Graphify |
| Consultas mixtas | Descomponer en sub-preguntas (local vs global) antes de sintetizar |
| Reranking (ordenar candidatos) | Tras buscar, priorizar por recencia, `dossier_id`, y rol del holding |

## Cuando activar

- Preguntas que mezclan **hechos concretos** (fechas, montos, nombres) con **contexto amplio** ("como encaja esto en el holding").
- Respuestas que deben ser **defendibles ante cliente o CEO** (citar fuente).
- Investigacion sobre un **cliente o entrega** sin inventar: obligatorio anclar a dossier + memoria.

No usar para mensajes triviales de un paso.

## Secuencia (orden sugerido)

1. **Acotar entidades** — ¿Cliente? ¿Empresa del holding? ¿Proyecto? Si falta, preguntar o leer `COMPANIES.md` / dossier.
2. **Local primero** — Busqueda semantica en MemPalace con query concreta; abrir fragmentos relevantes del dossier en `client-dossiers/` si aplica.
3. **Global despues** — Consultar KG (`mempalace_kg_query`, timeline) para relaciones y decisiones pasadas; si el tema es **codigo o docs del repo**, usar Graphify (`graphify query` o MCP) para no adivinar dependencias.
4. **Preguntas mixtas** — Partir en 2+ sub-preguntas, responder cada una con su fuente, luego sintesis.
5. **Salida** — Lista de **afirmaciones** con **citacion** (archivo, drawer, triple KG, URL interna). Si no hay fuente: decirlo explicitamente.

## Plantilla de citacion (obligatoria en respuestas sensibles)

```
- [Afirmacion]: fuente — (ruta o herramienta, p. ej. client-dossiers/foo.md §3; mempalace_search; graphify)
```

## Limites

- No sustituye [APPROVAL_GATES.md](../../../../docs/APPROVAL_GATES.md) ni Trello.
- Si el corpus son PDFs masivos solo en disco del cliente, valorar pipeline externo; este skill cubre **lo que ya esta en workspace + MemPalace + repo**.
- Ver [RECURSOS_COMUNIDAD_OPENCLAW.md](../../../../docs/RECURSOS_COMUNIDAD_OPENCLAW.md) §2.8 para relacion con upstream HKUDS.

## Referencias

- MemPalace: [MEMORIA_MEMPALACE.md](../../../../docs/MEMORIA_MEMPALACE.md)
- Graphify: [GRAPHIFY_INTEGRACION.md](../../../../docs/GRAPHIFY_INTEGRACION.md)
- Paper LightRAG (contexto teorico): [arXiv:2410.05779](https://arxiv.org/abs/2410.05779)
