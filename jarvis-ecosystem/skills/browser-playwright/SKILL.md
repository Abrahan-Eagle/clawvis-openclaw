# browser-playwright

> Inspiración: automatización vía navegador como [actions/browser_control.py](https://github.com/FatihMakes/Jarvis-MK37/blob/main/actions/browser_control.py) — **código original** (Node + Playwright), no se copia el proyecto MK37.

## Setup

```bash
cd skills/browser-playwright
npm install
chmod +x bin/browser-playwright
```

**Navegador:** si `npx playwright install chromium` falla (p. ej. host Linux no soportado para el binario descargado), el runtime usa **Chrome o Edge ya instalados en el sistema** vía `PLAYWRIGHT_CHANNEL` (por defecto `chrome`). Comprobar: `which google-chrome` o `which microsoft-edge`. Opcional: `npx playwright install chrome` solo confirma que el canal está disponible.

Variables útiles:

| Variable | Efecto |
|----------|--------|
| `PLAYWRIGHT_CHANNEL` | `chrome` (defecto), `msedge`, o dejar vacío/`bundled` para intentar Chromium del caché de Playwright |
| `PLAYWRIGHT_USER_DATA` | Perfil persistente (default `~/.openclaw/playwright-profile/`) |

Perfil aislado (sin cookies del Chrome del usuario normal): directorio anterior es **solo para el bot**; no lee tu perfil personal.

## Allowlist (obligatorio)

Solo se navega a hosts en `BROWSER_PLAYWRIGHT_ALLOW` (coma-separada). Default incluye `localhost`, `127.0.0.1`, `open-meteo.com`, `example.com`.

**Añadir un dominio de producción (CRM, banco, portal fiscal)** → revisión y aprobación del CEO: [APPROVAL_GATES.md](../../docs/APPROVAL_GATES.md) (p. ej. `AG-09` instalación, `AG-10` acciones sensibles, `AG-08` datos de clientes).

## Uso

```bash
./bin/browser-playwright go-to --url=https://example.com/
./bin/browser-playwright get-text --url=https://example.com/
./bin/browser-playwright screenshot --url=https://example.com/ --path=/tmp/x.png
```

## Salida

JSON en stdout (errores con `error` y pistas de aprobación).

## Limitaciones (v1)

- Subcomandos: `go-to`, `get-text`, `screenshot`, `close` (cierre = salir del proceso; no hay hot-reload de sesión larga). Type/click/scroll se pueden añadir siguiendo el mismo allowlist.
- `headless: true` — para depurar, cambiar a `headless: false` en `src/run.mjs` (solo con confianza).
