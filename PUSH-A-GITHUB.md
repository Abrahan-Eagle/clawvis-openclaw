# Publicar cambios en GitHub

Procedimiento breve; el detalle de qué entra en el repo está en [README.md](README.md) (sección *Qué queda en GitHub y qué no*).

## Desde la raíz del repositorio

```bash
cd /ruta/al/clawvis-openclaw
git status
git add -A
git commit -m "Descripción clara del cambio en una frase."
git push origin main
```

- Usa rama `main` u otra según tu remoto; ajusta si trabajas con `git worktree` o ramas de feature.
- **No** subas `~/.openclaw/.env`, tokens de bots ni claves API; el `openclaw.json` completo con secretos no debe versionarse como copia íntegra salvo política explícita del equipo (ver README).

## Si el remoto rechaza el push

- Revisa autenticación (`ssh -T git@github.com` o credencial HTTPS).
- Confirma que el repositorio remoto sea **privado** si contiene material sensible (README lo recuerda).
