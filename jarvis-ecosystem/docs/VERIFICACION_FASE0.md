# Verificacion Fase 0 — Post gobierno Jarvis

**Objetivo:** confirmar que el workspace de Jarvis en disco coincide con el repo y que el gateway OpenClaw esta operativo.

**Ultima ejecucion (automatica):** 2026-04-04 (entorno de desarrollo).

---

## Comandos y resultados

| Comando | Resultado |
|---------|-----------|
| `readlink -f ~/.jarvis-ecosystem` | `/var/www/clawvis-openclaw/jarvis-ecosystem` |
| `readlink -f <repo>/jarvis-ecosystem` | `/var/www/clawvis-openclaw/jarvis-ecosystem` |
| `systemctl --user is-active openclaw-gateway` | `active` |

**Interpretacion:** el enlace simbolico `~/.jarvis-ecosystem` apunta al mismo arbol que el clon en `/var/www/clawvis-openclaw/jarvis-ecosystem`. El gateway de usuario esta **activo**.

---

## Re-ejecutar en tu maquina

```bash
readlink -f ~/.jarvis-ecosystem
readlink -f "$(git -C /ruta/al/clawvis-openclaw rev-parse --show-toplevel 2>/dev/null)/jarvis-ecosystem"
systemctl --user is-active openclaw-gateway
openclaw channels status 2>/dev/null || true
```

Si `openclaw-gateway` no esta `active`, revisar logs: `journalctl --user -u openclaw-gateway -n 50`.
