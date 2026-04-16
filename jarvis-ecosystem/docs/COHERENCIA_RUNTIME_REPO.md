# Coherencia: runtime (`~/.openclaw`) vs repositorio

Evita la **deriva** entre tres sitios que suelen contener “verdad” distinta si no se disciplina.

## Las tres ubicaciones

| Ubicación | Rol |
|-----------|-----|
| `~/.openclaw/` | **Fuente de verdad en ejecución** del gateway: `openclaw.json`, sesiones, plugins. |
| Arbol **`jarvis-ecosystem`** en el PC del operador (p. ej. `/home/aipp/jarvis-ecosystem` o `~/jarvis-ecosystem`) | Debe coincidir con el repo para skills y prompts. El snapshot [config/openclaw-home/openclaw.json](../../config/openclaw-home/openclaw.json) usa `workspace: .../jarvis-ecosystem/agents/jarvis` (ruta explicita bajo `$HOME`). **No** confundir con `~/.jarvis-ecosystem` (nombre con punto): si usas ese nombre, el `workspace` en `openclaw.json` debe apuntar ahi, no a otra copia desactualizada. |
| `config/openclaw-home/` en el monorepo | **Instantánea sanitizada** (sin secretos) para Git y revisión. |

## Reglas prácticas

1. **Una sola copia:** idealmente `jarvis-ecosystem` del usuario es **symlink** al clon Git, p. ej. `ln -sfn /var/www/clawvis-openclaw/jarvis-ecosystem /home/aipp/jarvis-ecosystem` (si ya existe carpeta, respaldala y eliminala antes). Asi `skills/carousel-ops/` nunca se queda atras.
2. Tras cambiar **`~/.openclaw/openclaw.json`**, si quieres reflejarlo en Git sin secretos, sigue el procedimiento del README raíz hacia `config/openclaw-home/`.
3. No edites solo el snapshot en Git esperando que el gateway “lo lea”; el gateway lee **`~/.openclaw`**.

## Skills en el workspace del agente (carousel-ops “no existe”)

OpenClaw apunta el `workspace` de Jarvis a una ruta del host (p. ej. `/home/aipp/jarvis-ecosystem/agents/jarvis` en `openclaw.json`). Ese arbol **debe** contener lo mismo que el repo en `jarvis-ecosystem/agents/jarvis/`, incluida **`skills/carousel-ops/SKILL.md`**.

Si el agente informa que **no hay** `skills/carousel-ops/` pero en Git **sí** existe, el directorio del gateway esta **desactualizado** (copia vieja, otro clone, o nunca se sincronizo).

**Comprobar en el host:** sustituye por tu ruta de `workspace`:

```bash
ls /home/aipp/jarvis-ecosystem/agents/jarvis/skills/carousel-ops/SKILL.md
```

**Sincronizar skills** (sin sustituir todo el home tree):

```bash
JARVIS_WORKSPACE_BASE=/home/aipp/jarvis-ecosystem \
  /var/www/clawvis-openclaw/jarvis-ecosystem/scripts/sync-jarvis-skills-from-repo.sh
```

(ajusta ambas rutas a tu usuario y clon). Script: [../scripts/sync-jarvis-skills-from-repo.sh](../scripts/sync-jarvis-skills-from-repo.sh).

O sustituir `jarvis-ecosystem` del usuario por **symlink** al repo (regla 1 arriba) y reiniciar el gateway.

**Alternativa dev:** en `~/.openclaw/openclaw.json`, `agents.list[].workspace` puede apuntar **directamente** al clon, p. ej. `/var/www/clawvis-openclaw/jarvis-ecosystem/agents/jarvis`, para evitar duplicados (solo si esa ruta existe en la misma maquina que el gateway).

## Historial y secretos

Si alguna vez se commiteó `jarvis-ecosystem/.env` u otro secreto **antes** de las reglas en `.gitignore`, conviene **rotar credenciales** y, si hace falta, usar `git log -p -- path` o herramientas tipo `gitleaks` / `trufflehog` sobre el historial local (no automatizado en este repo).

## Informe forense

Brechas relacionadas: síntesis [INFORME_FORENSE_ECOSISTEMA_JARVIS.md](../../docs/INFORME_FORENSE_ECOSISTEMA_JARVIS.md) (sección S.3).
