# error-recovery

> Inspiración: [agent/error_handler.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/agent/error_handler.py) — **heurística en bash+Python** (el MK37 usaba un prompt LLM; aquí v1 es local y rápida).

## Uso

```bash
./bin/error-recovery "HTTP 429 rate limit"
echo "ETIMEDOUT" | ./bin/error-recovery
```

## Decisiones

- `RETRY` — posible intermitencia / rate limit
- `REPLAN` — credenciales / permisos
- `SKIP` — 404 o recurso inexistente
- `ABORT` — resto (escalar; revisar [APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md))

Para criterios con LLM, añade una capa en el agente o una segunda implementación vía `summarize` sin sustituir esta heurística básica.
