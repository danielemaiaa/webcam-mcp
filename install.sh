#!/bin/bash
set -e

echo "============================================"
echo " Instalador - Webcam MCP para Claude Desktop"
echo " macOS / Linux"
echo "============================================"
echo ""

# Detecta OS
OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
    OS_NAME="macOS"
elif [ "$OS" = "Linux" ]; then
    OS_NAME="Linux"
else
    echo "Sistema operacional não suportado: $OS"
    exit 1
fi
echo "[INFO] Sistema detectado: $OS_NAME"

# Verifica Python
if ! command -v python3 &>/dev/null; then
    echo ""
    echo "ERRO: python3 não encontrado."
    if [ "$OS" = "Darwin" ]; then
        echo "Instale via Homebrew: brew install python"
    else
        echo "Instale via apt: sudo apt install python3 python3-pip"
    fi
    exit 1
fi
echo "[OK] $(python3 --version) encontrado."

# Linux: verifica dependência de câmera
if [ "$OS" = "Linux" ]; then
    if ! python3 -c "import cv2" &>/dev/null; then
        echo ""
        echo "[INFO] No Linux, opencv-python precisa de libGL."
        echo "       Instalando: sudo apt-get install -y libgl1 libglib2.0-0"
        sudo apt-get install -y libgl1 libglib2.0-0 2>/dev/null || \
            echo "[AVISO] Não foi possível instalar automaticamente. Instale manualmente se der erro."
    fi
fi

# Instala dependências Python
echo ""
echo "Instalando dependências (opencv + mcp)..."
pip3 install -r "$(dirname "$0")/requirements.txt"

echo ""
echo "[OK] Dependências instaladas."
echo ""

# Caminhos absolutos
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_PATH="$SCRIPT_DIR/server.py"
PYTHON_PATH="$(which python3)"

# Caminho do config do Claude Desktop por OS
if [ "$OS" = "Darwin" ]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
else
    CONFIG_DIR="$HOME/.config/Claude"
fi
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

echo "============================================"
echo " ÚLTIMO PASSO: Configurar o Claude Desktop"
echo "============================================"
echo ""

# Tenta criar/atualizar o config automaticamente
mkdir -p "$CONFIG_DIR"

if [ -f "$CONFIG_FILE" ]; then
    echo "[AVISO] Arquivo de config já existe: $CONFIG_FILE"
    echo "        Adicione o bloco 'webcam' manualmente ao 'mcpServers' existente."
    echo ""
else
    cat > "$CONFIG_FILE" <<EOF
{
  "mcpServers": {
    "webcam": {
      "command": "$PYTHON_PATH",
      "args": ["$SERVER_PATH"]
    }
  }
}
EOF
    echo "[OK] Config criado automaticamente em:"
    echo "     $CONFIG_FILE"
fi

echo ""
echo "Bloco para adicionar ao claude_desktop_config.json caso precise:"
echo ""
echo "{"
echo "  \"mcpServers\": {"
echo "    \"webcam\": {"
echo "      \"command\": \"$PYTHON_PATH\","
echo "      \"args\": [\"$SERVER_PATH\"]"
echo "    }"
echo "  }"
echo "}"
echo ""
echo "Após salvar, REINICIE o Claude Desktop."
echo "Procure o ícone de martelo (🔨) na janela de chat para confirmar."
echo ""
echo "============================================"
