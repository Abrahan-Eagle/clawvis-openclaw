#!/usr/bin/env bash
# Sirve graphify-out/graph.html en localhost sin 404 de favicon y sin escuchar en todas las interfaces.
# Uso (desde cualquier cwd):
#   ./jarvis-ecosystem/scripts/graphify-serve-local.sh
# Variables opcionales: PORT=8765 BIND=127.0.0.1

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUT="$REPO_ROOT/graphify-out"

if [[ ! -d "$OUT" ]] || [[ ! -f "$OUT/graph.html" ]]; then
  echo "ERROR: falta $OUT/graph.html. Ejecuta desde la raiz del repo: graphify update ." >&2
  exit 1
fi

# Python SimpleHTTPRequestHandler pide /favicon.ico; un fichero vacio devuelve 200 y evita ruido 404 en logs.
:>"$OUT/favicon.ico"

# Chrome DevTools suele pedir esta ruta al abrir la consola; JSON minimo evita 404 en logs del servidor.
mkdir -p "$OUT/.well-known/appspecific"
printf '%s\n' '{}' >"$OUT/.well-known/appspecific/com.chrome.devtools.json"

BIND="${BIND:-127.0.0.1}"
START_PORT="${PORT:-8765}"

# Si el puerto pedido esta ocupado (p. ej. otro `python3 -m http.server`), usar el siguiente libre.
FREE_PORT="$(python3 -c "
import socket
bind = '${BIND}'
start = int('${START_PORT}')
for p in range(start, start + 40):
    s = socket.socket()
    try:
        s.bind((bind, p))
        s.close()
        print(p)
        break
    except OSError:
        pass
else:
    raise SystemExit('no free port in range')
")" || {
  echo "ERROR: no hay puerto libre entre ${START_PORT} y $((START_PORT + 39)). Cierra el proceso anterior, p. ej.:" >&2
  echo "  fuser -k ${START_PORT}/tcp   # o: ss -ltnp | grep ${START_PORT}" >&2
  exit 1
}

if [[ "$FREE_PORT" != "$START_PORT" ]]; then
  echo "Aviso: puerto ${START_PORT} ocupado; uso ${FREE_PORT} -> http://${BIND}:${FREE_PORT}/graph.html" >&2
fi

cd "$OUT"
exec python3 -m http.server "$FREE_PORT" --bind "$BIND"
