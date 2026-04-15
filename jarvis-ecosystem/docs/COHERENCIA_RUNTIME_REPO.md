# Coherencia: runtime (`~/.openclaw`) vs repositorio

Evita la **deriva** entre tres sitios que suelen contener “verdad” distinta si no se disciplina.

## Las tres ubicaciones

| Ubicación | Rol |
|-----------|-----|
| `~/.openclaw/` | **Fuente de verdad en ejecución** del gateway: `openclaw.json`, sesiones, plugins. |
| `~/.jarvis-ecosystem` → symlink al repo | Workspace Jarvis que OpenClaw usa para skills y prompts (ver [README.md](../../README.md) raíz del monorepo). |
| `config/openclaw-home/` en el monorepo | **Instantánea sanitizada** (sin secretos) para Git y revisión. |

## Reglas prácticas

1. **Symlink:** `ln -sfn /ruta/al/clon/jarvis-ecosystem ~/.jarvis-ecosystem` — un solo árbol editado.
2. Tras cambiar **`~/.openclaw/openclaw.json`**, si quieres reflejarlo en Git sin secretos, sigue el procedimiento del README raíz hacia `config/openclaw-home/`.
3. No edites solo el snapshot en Git esperando que el gateway “lo lea”; el gateway lee **`~/.openclaw`**.

## Historial y secretos

Si alguna vez se commiteó `jarvis-ecosystem/.env` u otro secreto **antes** de las reglas en `.gitignore`, conviene **rotar credenciales** y, si hace falta, usar `git log -p -- path` o herramientas tipo `gitleaks` / `trufflehog` sobre el historial local (no automatizado en este repo).

## Informe forense

Brechas relacionadas: síntesis [INFORME_FORENSE_ECOSISTEMA_JARVIS.md](../../docs/INFORME_FORENSE_ECOSISTEMA_JARVIS.md) (sección S.3).
