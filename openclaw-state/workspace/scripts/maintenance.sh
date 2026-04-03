#!/bin/bash
# maintenance.sh - Automation for Jarvis Ecosystem
# Path: /home/will/.openclaw/workspace/scripts/maintenance.sh

DOCS_DIR="/home/will/.openclaw/workspace/docs/openclaw"
REPO_URL="https://github.com/openclaw/openclaw.git"

update_docs() {
    echo "Starting monthly documentation refresh..."
    if [ -d "$DOCS_DIR/.git" ]; then
        cd "$DOCS_DIR" && git pull
    else
        # If not a git repo, re-clone it
        rm -rf "$DOCS_DIR"
        mkdir -p "$DOCS_DIR"
        git clone --depth 1 "$REPO_URL" /tmp/openclaw_refresh
        cp -r /tmp/openclaw_refresh/* "$DOCS_DIR/"
        rm -rf /tmp/openclaw_refresh
    fi
    echo "Documentation updated successfully."
}

weekly_review() {
    echo "Triggering weekly ecosystem review prompt..."
    openclaw agent --agent main --message "Jarvis, es sábado por la mañana. Por favor, realiza tu revisión semanal del ecosistema. Investiga en internet nuevas ideas de optimización para las agencias de Abrahan y propón mejoras basadas en la documentación actualizada." --deliver
}

case "$1" in
    --docs) update_docs ;;
    --review) weekly_review ;;
    *) echo "Usage: $0 {--docs|--review}" ;;
esac
