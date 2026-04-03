#!/bin/bash
# 🦞 Jarvis Reset Tool - AIBlock
# Este script limpia procesos colgados y archivos de bloqueo (.lock)

echo "🛡️ Iniciando limpieza de emergencia del Ecosistema Jarvis..."

# 1. Matar procesos de OpenClaw y Node que puedan estar colgados
echo "🔸 Terminando procesos de OpenClaw/Node..."
pkill -f openclaw
pkill -f node

# 2. Limpiar archivos de bloqueo (.lock) que impiden que Jarvis inicie
echo "🔸 Limpiando archivos de bloqueo (.lock)..."
rm -f /home/will/.openclaw/agents/*/sessions/*.lock 2>/dev/null

# 3. Reiniciar Ollama (Opcional, pero recomendado en 4GB RAM)
# echo "🔸 Reiniciando Ollama..."
# systemctl restart ollama || sudo systemctl restart ollama

echo "✅ Sistema desbloqueado. Ahora puedes volver a correr: openclaw agent --agent jarvis --local"
