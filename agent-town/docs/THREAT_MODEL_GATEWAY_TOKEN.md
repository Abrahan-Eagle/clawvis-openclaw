# Threat model — `NEXT_PUBLIC_GATEWAY_TOKEN`

## Contexto

Agent Town puede pasar un token de gateway al cliente vía:

- `process.env.NEXT_PUBLIC_GATEWAY_TOKEN` (embebido en el bundle del navegador)
- `localStorage` (panel Connection / persistencia)

El proxy servidor (`lib/ws-proxy.ts`) además lee la **identidad del dispositivo** desde `~/.openclaw/identity/` e inyecta firma + `deviceToken` en el handshake `connect`. Esa clave **no** se envía al navegador.

## Modelo de amenaza (loopback / operador único)

| Activo | Exposición | Riesgo aceptable si… |
|--------|-----------|----------------------|
| Token en `NEXT_PUBLIC_*` | Cualquiera que abra la UI | Gateway solo en `127.0.0.1`, `gateway.auth.mode: none` o token de bajo privilegio, sin exposición a LAN/Internet |
| Device PEM en HOME | Solo proceso Node del proxy | HOME del mismo usuario que corre Agent Town; no versionar `identity/` |
| Operator deviceToken | Solo proxy → upstream | No loguear frames `connect` completos |

## Decisiones

1. **Hoy (MVP local):** se acepta `NEXT_PUBLIC_GATEWAY_TOKEN` vacío o de desarrollo **solo** con gateway en loopback.
2. **No hacer:** publicar Agent Town a Internet con un token real en `NEXT_PUBLIC_*`.
3. **Mejora futura (P2+):** token solo server-side (cookie httpOnly / sesión) y UI sin secretos; el browser siempre habla a `/api/gateway` same-origin.

## Controles actuales

- `checkOrigin` / `isAllowedWsOrigin` en upgrade WS
- Device auth inyectada solo en el servidor
- CSP `connect-src` acotada a localhost (ver `next.config.ts`)

Ver también: [INFORME_FORENSE_360_2026-07.md](../../docs/INFORME_FORENSE_360_2026-07.md) (H-13).
