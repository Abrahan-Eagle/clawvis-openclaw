# task-queue

> Inspiración: [agent/task_queue.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/agent/task_queue.py) — **persistencia mínima en JSONL**.

## Archivo

`~/.openclaw/jarvis-queue.jsonl` o `JARVIS_QUEUE_FILE=/ruta/archivo.jsonl`

## Uso

```bash
./bin/task-queue path
./bin/task-queue submit '{"goal":"briefing test","priority":"NORMAL"}'
./bin/task-queue list
```

Un ejecutor (humano o `executor` skill) debería consumir y vaciar/rotar el archivo; v1 deja el archivo como log append-only.
