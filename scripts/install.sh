#!/bin/bash
# 🦙 Instalador de Nexo Llama para Linux/macOS

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🦙  INSTALADOR NEXO LLAMA                                 ║"
echo "║                                                              ║"
echo "║   Asistente de IA Local con Llama + Ollama                   ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Directorio de instalación
INSTALL_DIR="$HOME/.local/bin/nexo-llama"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${YELLOW}📋 Verificando requisitos...${NC}"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no encontrado. Instalalo primero.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip3 no encontrado, intentando instalar...${NC}"
    sudo apt-get install -y python3-pip 2>/dev/null || sudo yum install -y python3-pip 2>/dev/null || true
fi

echo ""
echo -e "${YELLOW}📦 Instalando dependencias de Python...${NC}"
pip3 install -r "$SCRIPT_DIR/requirements.txt" --user

echo ""
echo -e "${YELLOW}📁 Creando directorio de instalación...${NC}"
mkdir -p "$INSTALL_DIR"

echo ""
echo -e "${YELLOW}📋 Copiando archivos...${NC}"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/prompts" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/memory" "$INSTALL_DIR/"

# Crear script de inicio
cat > "$INSTALL_DIR/nexo" << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/src/nexo.py" "$@"
EOF
chmod +x "$INSTALL_DIR/nexo"

# Crear script de inicio alternativo
cat > "$INSTALL_DIR/start.sh" << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
python3 src/nexo.py "$@"
EOF
chmod +x "$INSTALL_DIR/start.sh"

echo ""
echo -e "${YELLOW}🔗 Creando alias en bashrc/zshrc...${NC}"

# Detectar shell
SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == */zsh ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

# Agregar alias si no existe
if ! grep -q "alias nexo=" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# 🦙 Nexo Llama alias" >> "$SHELL_RC"
    echo "alias nexo='$INSTALL_DIR/nexo'" >> "$SHELL_RC"
    echo -e "${GREEN}✅ Alias agregado a $SHELL_RC${NC}"
else
    echo -e "${GREEN}✅ Alias ya existe en $SHELL_RC${NC}"
fi

echo ""
echo -e "${YELLOW}🔍 Verificando Ollama...${NC}"

if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama encontrado${NC}"
    
    # Verificar si Ollama está corriendo
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama está corriendo${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama no está corriendo. Inicialo con: ollama serve${NC}"
    fi
    
    # Verificar modelo
    if ollama list 2>/dev/null | grep -q "llama3.2"; then
        echo -e "${GREEN}✅ Modelo llama3.2 encontrado${NC}"
    else
        echo -e "${YELLOW}⚠️  Modelo llama3.2 no encontrado${NC}"
        echo -e "${YELLOW}   Descargalo con: ollama pull llama3.2${NC}"
    fi
else
    echo -e "${RED}❌ Ollama no encontrado${NC}"
    echo -e "${YELLOW}   Instalalo desde: https://ollama.com${NC}"
    echo -e "${YELLOW}   O ejecuta: curl -fsSL https://ollama.com/install.sh | sh${NC}"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ✅ ¡INSTALACIÓN COMPLETADA!                                ║"
echo "║                                                              ║"
echo "║   Para usar Nexo:                                            ║"
echo "║     1. Abrí una nueva terminal                               ║"
echo "║     2. Escribí: nexo                                         ║"
echo "║                                                              ║"
echo "║   O ejecutá directamente:                                    ║"
echo "║     $INSTALL_DIR/nexo                                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
