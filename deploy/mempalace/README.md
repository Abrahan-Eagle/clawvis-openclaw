# Deploy — MemPalace (Jarvis ecosystem)

Archivos para **replicar** auto-mine, KG y plantillas sin depender solo de la memoria del host.

| Archivo | Uso |
|---------|-----|
| `restore.env.example` | Copiar a `~/.config/mempalace/restore.env`; definir `JARVIS_ECOSYSTEM`. |
| `mempalace-auto-mine.sh` | Copiar a `~/.openclaw/hooks/`; ejecutable. |
| `mempalace-auto-mine.service` / `.timer` | Copiar a `~/.config/systemd/user/`; ajustar rutas; `daemon-reload` + `enable --now`. |
| `kg-populate-ecosystem.py` + `.sh` | Poblar Knowledge Graph; requiere Python del venv pipx de mempalace. |
| `templates/` | `config.json`, `wing_config.json`, `identity.txt` → `~/.mempalace/` (editar rutas). |

Documentación de cierre: `jarvis-ecosystem/docs/MODULO_MEMPALACE_CIERRE.md`.
