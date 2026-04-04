# Política de rutas en esta PC (Jarvis)

Edita este archivo para definir **dónde puede trabajar Jarvis por defecto** y **qué zonas están vetadas**. El agente debe leerlo al inicio de sesión (junto con `AGENTS.md`).

## Principio

- **Por defecto:** solo tocar proyectos y carpetas que tú listes abajo como permitidas.
- **Si el humano ordena explícitamente** una ruta concreta (“edita `/ruta/archivo`”, “haz backup de X en Y”): **hazlo** salvo que sea obviamente destructivo o ilegal; en ese caso confirma una frase antes.

## Entregas en disco: `~/Documents/JARVIS-DOCUMENTS/` (obligatorio leer)

- **Convención canónica:** [../../docs/JARVIS_DOCUMENTS_ON_DISK.md](../../docs/JARVIS_DOCUMENTS_ON_DISK.md) — carpeta del sistema **`Documents`** (inglés), ruta `~/Documents/JARVIS-DOCUMENTS/` por empresa, cliente (`dossier_id`) y estados (borradores → publicados). No confundir con `documentos` / `Documentos` / `~/Documentos/` salvo excepción anotada aquí.
- En esta máquina la ruta absoluta equivalente está listada abajo en **Rutas permitidas**.

## Rutas permitidas (trabajo habitual)

**Esta PC (usuario `aipp`):**

- `/var/www/clawvis-openclaw/jarvis-ecosystem/` — ecosistema Jarvis (workspace y repo `clawvis-openclaw`)
- `/home/aipp/Documents/JARVIS-DOCUMENTS/` — entregables y medios del holding (ver sección “Entregas en disco” arriba)

**Otras máquinas:** sustituir por el usuario y la ruta del clon; mantener la convención `~/Documents/JARVIS-DOCUMENTS/`.

- _(añade aquí más proyectos: `~/proyectos/foo`, etc.)_

## Rutas restringidas o prohibidas (no tocar sin orden expresa)

Ejemplos típicos (ajusta a tu máquina):

- `/etc/`, `/boot/`, `/sys/` — sistema
- `~/.ssh/` — claves privadas (solo lectura si el humano lo pide para una tarea concreta)
- Carpetas de otros usuarios sin permiso
- _(añade: backups ajenos, discos de red sensibles, etc.)_

## Excepciones

- Si el humano **nombra una ruta concreta** en el mensaje, esa orden tiene prioridad sobre “prohibido por defecto”, salvo riesgo claro (borrar disco, enviar secretos, etc.).

## Navegador (solo OpenClaw)

En `~/.openclaw/openclaw.json` está fijado **un solo binario** para la herramienta de navegador de OpenClaw: **Chromium snap** (`/snap/bin/chromium`; el wrapper `chromium-browser` apunta al mismo), con **`headless: true`**, **`noSandbox: true`** (necesario en Linux con snap) y flags para bajar uso de RAM. El perfil de usuario CDP no puede vivir bajo `~/.openclaw/...` con el snap por confinamiento: **`~/.openclaw/browser/openclaw/user-data` es un enlace simbólico** a `~/snap/chromium/common/openclaw-cdp`. OpenClaw **no** usa Firefox ni otros navegadores salvo que cambies esa config o añadas perfiles CDP remotos.

Si algo falla con el Chromium snap, prueba la ruta de Chrome solo para diagnosticar; la política deseada sigue siendo **solo Chromium**.

## Nota técnica

OpenClaw puede usar **sandbox** (contenedores) para aislar más el filesystem; ahora mismo las sesiones de Jarvis pueden ejecutarse **sin sandbox de archivos** (`sandboxed: false`). Esta política es la capa de **reglas explícitas** hasta que actives sandbox en la documentación de OpenClaw si lo necesitas.
