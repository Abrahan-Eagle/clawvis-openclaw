#!/usr/bin/env bash
# Instala JMC como servicio systemd para arranque automático al reiniciar el equipo.
# Uso:
#   sudo ./scripts/jmc-systemd-install.sh              # servicio system (recomendado en servidor)
#   ./scripts/jmc-systemd-install.sh --user          # servicio user (sin sudo; requiere linger para arranque en boot)
#
# uvicorn se resuelve en este orden:
#   1) Variable de entorno JMC_UVICORN_BIN al invocar este script
#   2) Si existe el fichero de entorno del servicio y define JMC_UVICORN_BIN= (ruta ejecutable)
#   3) jarvis-ecosystem/.venv-jmc/bin/uvicorn
#   4) jarvis-ecosystem/venv/bin/uvicorn
#   5) $VIRTUAL_ENV/bin/uvicorn
#   6) primer uvicorn en PATH (aviso: mejor .venv-jmc con dependencias del adapter)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$ROOT"
ADAPTER="$REPO/jmc/adapter"
MODE="system"
KEEP_UNIT=0
FORCE_OVERWRITE=0

for arg in "$@"; do
  case "$arg" in
    --user) MODE="user" ;;
    --keep-unit) KEEP_UNIT=1 ;;
    --force) FORCE_OVERWRITE=1 ;;
    -h|--help)
      echo "Uso: $0 [--user] [--keep-unit] [--force]"
      echo "  --user        Servicio systemd de usuario (sin sudo)."
      echo "  --keep-unit   No sobrescribe jmc-adapter.service si ya existe."
      echo "  --force       Omite aviso si la unidad generada difiere de la instalada."
      echo "Opcional: export JMC_UVICORN_BIN=/ruta/absoluta/a/uvicorn"
      exit 0
      ;;
  esac
done

if [[ "$MODE" == "system" ]]; then
  ENV_FILE_PREVIEW="/etc/jmc/jmc-adapter.env"
else
  ENV_FILE_PREVIEW="${HOME}/.config/jmc/jmc-adapter.env"
fi

# Resuelve ruta absoluta al binario uvicorn (stdout: ruta; stderr: avisos)
resolve_uvicorn() {
  local repo="$1"
  local env_file="${2:-}"
  if [[ -n "${JMC_UVICORN_BIN:-}" && -x "${JMC_UVICORN_BIN}" ]]; then
    printf '%s\n' "${JMC_UVICORN_BIN}"
    return 0
  fi
  if [[ -n "$env_file" && -f "$env_file" ]]; then
    local line val
    line="$(grep -E '^[[:space:]]*JMC_UVICORN_BIN=' "$env_file" 2>/dev/null | tail -1 || true)"
    if [[ -n "$line" ]]; then
      val="${line#*=}"
      val="${val//$'\r'/}"
      val="${val//\"/}"
      while [[ "$val" == [[:space:]]* ]]; do val="${val#?}"; done
      while [[ "$val" == *[[:space:]] ]]; do val="${val%?}"; done
      if [[ -n "$val" && -x "$val" ]]; then
        printf '%s\n' "$val"
        return 0
      fi
    fi
  fi
  local c
  for c in "$repo/.venv-jmc/bin/uvicorn" "$repo/venv/bin/uvicorn"; do
    if [[ -x "$c" ]]; then
      printf '%s\n' "$c"
      return 0
    fi
  done
  if [[ -n "${VIRTUAL_ENV:-}" && -x "${VIRTUAL_ENV}/bin/uvicorn" ]]; then
    printf '%s\n' "${VIRTUAL_ENV}/bin/uvicorn"
    return 0
  fi
  local w
  w="$(command -v uvicorn 2>/dev/null || true)"
  if [[ -n "$w" && -x "$w" ]]; then
    echo "WARN: usando uvicorn del PATH: $w — recomendado: python3 -m venv $repo/.venv-jmc && .venv-jmc/bin/pip install -e $repo/jmc/adapter" >&2
    printf '%s\n' "$w"
    return 0
  fi
  return 1
}

UVICORN="$(resolve_uvicorn "$REPO" "$ENV_FILE_PREVIEW" || true)"
if [[ -z "${UVICORN:-}" ]]; then
  echo "ERROR: no se encontró uvicorn ejecutable." >&2
  echo "  Crear venv en el repo: cd \"$REPO\" && python3 -m venv .venv-jmc && .venv-jmc/bin/pip install -e jmc/adapter" >&2
  echo "  O exportar: JMC_UVICORN_BIN=/ruta/a/uvicorn antes de ejecutar este script." >&2
  echo "  O añadir en $ENV_FILE_PREVIEW la línea: JMC_UVICORN_BIN=/ruta/a/uvicorn" >&2
  exit 1
fi

gen_token() { openssl rand -hex 32; }

# Lee KEY=value del fichero de entorno (última coincidencia); default si falta.
_jmc_env_kv() {
  local f="$1" key="$2" def="$3"
  local line val
  if [[ ! -f "$f" ]]; then
    printf '%s\n' "$def"
    return
  fi
  line="$(grep -E "^[[:space:]]*${key}=" "$f" 2>/dev/null | tail -1 || true)"
  if [[ -z "$line" ]]; then
    printf '%s\n' "$def"
    return
  fi
  val="${line#*=}"
  val="${val//$'\r'/}"
  val="${val//\"/}"
  while [[ "$val" == [[:space:]]* ]]; do val="${val#?}"; done
  while [[ "$val" == *[[:space:]] ]]; do val="${val%?}"; done
  if [[ -z "$val" ]]; then
    printf '%s\n' "$def"
  else
    printf '%s\n' "$val"
  fi
}

# Entre comillas si la ruta tiene espacios (systemd ExecStart / WorkingDirectory).
_sd_quote() {
  local s="$1"
  if [[ "$s" != *[[:space:]]* ]]; then
    printf '%s' "$s"
    return
  fi
  s="${s//\"/\\\"}"
  printf '"%s"' "$s"
}

if [[ "$MODE" == "system" ]]; then
  if [[ "${EUID:-0}" -ne 0 ]]; then
    echo "ERROR: modo system requiere sudo: sudo $0" >&2
    exit 1
  fi
  RUN_AS="${SUDO_USER:-${USER:-root}}"
  PRIMARY_GROUP="$(id -gn "$RUN_AS" 2>/dev/null || echo "$RUN_AS")"
  if [[ "$RUN_AS" == "root" ]]; then
    echo "WARN: El servicio correría como root. Mejor: sudo -u tu_usuario o ejecutar sudo desde tu usuario normal." >&2
  fi
  ENV_DIR="/etc/jmc"
  ENV_FILE="$ENV_DIR/jmc-adapter.env"
  UNIT_PATH="/etc/systemd/system/jmc-adapter.service"

  mkdir -p "$ENV_DIR"
  if [[ ! -f "$ENV_FILE" ]]; then
    install -m 0600 /dev/null "$ENV_FILE"
    {
      echo "JMC_BEARER_TOKEN=$(gen_token)"
      echo "JMC_REPO_ROOT=$REPO"
      echo "JMC_BIND=127.0.0.1"
      echo "JMC_PORT=8765"
      echo "# Opcional: ruta absoluta a uvicorn (sobrescribe detección al reinstalar)"
      echo "# JMC_UVICORN_BIN=$UVICORN"
      echo "# Chat: espejo opcional a Telegram/Discord (openclaw message send); requiere reinicio del servicio"
      echo "# JMC_CHAT_MIRROR_ENABLED=1"
      echo "# JMC_OPENCLAW_BIN=/ruta/al/binario/openclaw"
    } >> "$ENV_FILE"
    chown root:root "$ENV_FILE"
    echo "Creado $ENV_FILE (token nuevo). Guárdalo en un gestor seguro; la UI lo necesita."
  else
    echo "Usando $ENV_FILE existente (no se sobrescribe)."
  fi

  BIND_EFF="$(_jmc_env_kv "$ENV_FILE" JMC_BIND "127.0.0.1")"
  PORT_EFF="$(_jmc_env_kv "$ENV_FILE" JMC_PORT "8765")"
  UVQ="$(_sd_quote "$UVICORN")"
  WDQ="$(_sd_quote "$ADAPTER")"
  UNIT_TMP="$(mktemp)"
  {
    cat <<EOF
[Unit]
Description=Jarvis Mission Control adapter (API + UI; escritura acotada a modo)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=120
StartLimitBurst=5

[Service]
Type=simple
User=$RUN_AS
Group=$PRIMARY_GROUP
WorkingDirectory=$WDQ
EnvironmentFile=$ENV_FILE
ExecStart=$UVQ app.main:app --host $BIND_EFF --port $PORT_EFF --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
  } >"$UNIT_TMP"

  if [[ "$KEEP_UNIT" -eq 1 && -f "$UNIT_PATH" ]]; then
    echo "Se mantiene la unidad existente (--keep-unit): $UNIT_PATH"
    rm -f "$UNIT_TMP"
  else
    if [[ -f "$UNIT_PATH" && "$FORCE_OVERWRITE" -ne 1 ]] && ! cmp -s "$UNIT_TMP" "$UNIT_PATH" 2>/dev/null; then
      echo "WARN: la unidad generada difiere de $UNIT_PATH (se sobrescribe). Usa --keep-unit para conservar la actual o --force para omitir este aviso." >&2
    fi
    mv -f "$UNIT_TMP" "$UNIT_PATH"
  fi

  chmod 644 "$UNIT_PATH"
  systemctl daemon-reload
  systemctl enable jmc-adapter.service
  systemctl restart jmc-adapter.service
  systemctl --no-pager --full status jmc-adapter.service || true
  echo ""
  echo "OK: jmc-adapter habilitado al arranque. Estado: systemctl status jmc-adapter"
  echo "Token Bearer (solo si acabas de crear el env): sudo grep JMC_BEARER_TOKEN $ENV_FILE"
  echo ""
  echo "Tras cada reinicio de la PC, systemd arranca JMC solo (no hace falta levantar uvicorn a mano)."
  echo "Vuelve a ejecutar este script solo si cambias venv, ruta del repo o quieres regenerar la unidad."
else
  # --user
  RUN_AS="${USER}"
  ENV_DIR="${HOME}/.config/jmc"
  ENV_FILE="$ENV_DIR/jmc-adapter.env"
  UNIT_DIR="${HOME}/.config/systemd/user"
  UNIT_PATH="$UNIT_DIR/jmc-adapter.service"

  mkdir -p "$ENV_DIR" "$UNIT_DIR"
  if [[ ! -f "$ENV_FILE" ]]; then
    {
      echo "JMC_BEARER_TOKEN=$(gen_token)"
      echo "JMC_REPO_ROOT=$REPO"
      echo "JMC_BIND=127.0.0.1"
      echo "JMC_PORT=8765"
      echo "# Opcional: ruta absoluta a uvicorn"
      echo "# JMC_UVICORN_BIN=$UVICORN"
      echo "# Chat: espejo opcional (reiniciar servicio tras activar)"
      echo "# JMC_CHAT_MIRROR_ENABLED=1"
      echo "# JMC_OPENCLAW_BIN=/ruta/al/binario/openclaw"
    } > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo "Creado $ENV_FILE"
  else
    echo "Usando $ENV_FILE existente."
  fi

  BIND_EFF="$(_jmc_env_kv "$ENV_FILE" JMC_BIND "127.0.0.1")"
  PORT_EFF="$(_jmc_env_kv "$ENV_FILE" JMC_PORT "8765")"
  UVQ="$(_sd_quote "$UVICORN")"
  WDQ="$(_sd_quote "$ADAPTER")"
  UNIT_TMP="$(mktemp)"
  {
    cat <<EOF
[Unit]
Description=Jarvis Mission Control adapter (API + UI; escritura acotada a modo)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=120
StartLimitBurst=5

[Service]
Type=simple
WorkingDirectory=$WDQ
EnvironmentFile=$ENV_FILE
ExecStart=$UVQ app.main:app --host $BIND_EFF --port $PORT_EFF --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
  } >"$UNIT_TMP"

  if [[ "$KEEP_UNIT" -eq 1 && -f "$UNIT_PATH" ]]; then
    echo "Se mantiene la unidad existente (--keep-unit): $UNIT_PATH"
    rm -f "$UNIT_TMP"
  else
    if [[ -f "$UNIT_PATH" && "$FORCE_OVERWRITE" -ne 1 ]] && ! cmp -s "$UNIT_TMP" "$UNIT_PATH" 2>/dev/null; then
      echo "WARN: la unidad generada difiere de $UNIT_PATH (se sobrescribe). Usa --keep-unit para conservar la actual o --force para omitir este aviso." >&2
    fi
    mv -f "$UNIT_TMP" "$UNIT_PATH"
  fi

  systemctl --user daemon-reload
  systemctl --user enable jmc-adapter.service
  systemctl --user restart jmc-adapter.service
  systemctl --user --no-pager --full status jmc-adapter.service || true
  echo ""
  echo "OK: servicio de usuario instalado."
  echo "Para que arranque al reiniciar SIN tener sesión gráfica iniciada:"
  echo "  loginctl enable-linger $RUN_AS"
  echo "Token: grep JMC_BEARER_TOKEN $ENV_FILE"
  echo ""
  echo "Con 'loginctl enable-linger' hecho una vez, JMC sube al arrancar el equipo sin pasos manuales."
  echo "Sin linger, el servicio user arranca al iniciar sesión gráfica (también sin uvicorn manual)."
fi
