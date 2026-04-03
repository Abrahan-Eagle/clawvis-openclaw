# Subir cambios a GitHub (manual)

El commit local ya está hecho en la rama `main`. Si `git push` falla por credenciales, en tu máquina:

```bash
cd ~/clawvis-openclaw
# Opción A — GitHub CLI
gh auth login
git push origin main

# Opción B — HTTPS con token (PAT) guardado en credential helper
git push https://github.com/Abrahan-Eagle/clawvis-openclaw.git main
```

Hacer el repo **privado** antes si incluyes secretos: GitHub → repo → Settings → Danger zone → Change visibility → Private.
