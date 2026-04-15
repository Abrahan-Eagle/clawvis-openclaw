# Seguridad del gateway OpenClaw

## Autenticación (`gateway.auth`)

Si en la configuración efectiva aparece **`auth` deshabilitado o modo permisivo** mientras el gateway escucha **solo en loopback** (`127.0.0.1`), el riesgo es acotado al usuario local.

**Antes de exponer el puerto del gateway a LAN o Internet** (cambio de `bind`, reverse proxy, túnel):

1. Activar **autenticación** acorde a la documentación actual de OpenClaw (token, OAuth, u otra opción soportada).
2. Restringir con **firewall** quién puede llegar al puerto.
3. Preferir **VPN o SSH tunnel** antes que abrir el servicio al mundo.

El snapshot en `config/openclaw-home/` puede mostrar `auth` relajado por comodidad en desarrollo; **no copies ese patrón** a despliegues expuestos.

## Plugins y canales

Ver aviso **`plugins.allow`** en el [README.md](../../README.md) del monorepo: una lista restrictiva sin los IDs de canal necesarios desactiva plugins aunque `channels.*.enabled` sea `true`.

## Referencias

- [RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](../../docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md)
- [COHERENCIA_RUNTIME_REPO.md](./COHERENCIA_RUNTIME_REPO.md)
