# 🦙 Instalador de Nexo Llama para Windows

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗"
Write-Host "║                                                              ║"
Write-Host "║   🦙  INSTALADOR NEXO LLAMA                                 ║"
Write-Host "║                                                              ║"
Write-Host "║   Asistente de IA Local con Llama + Ollama                   ║"
Write-Host "║                                                              ║"
Write-Host "╚══════════════════════════════════════════════════════════════╝"
Write-Host ""

# Colores
$Green = "`e[0;32m"
$Yellow = "`e[1;33m"
$Red = "`e[0;31m"
$NC = "`e[0m"

# Directorio de instalación
$InstallDir = "$env:USERPROFILE\.local\bin\nexo-llama"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "${Yellow}📋 Verificando requisitos...${NC}"

# Verificar Python
try {
    $PythonVersion = python --version 2>&1
    Write-Host "${Green}✅ $PythonVersion encontrado${NC}"
} catch {
    Write-Host "${Red}❌ Python no encontrado. Instalalo desde: https://python.org${NC}"
    exit 1
}

# Verificar pip
try {
    pip --version 2>&1 | Out-Null
    Write-Host "${Green}✅ pip encontrado${NC}"
} catch {
    Write-Host "${Yellow}⚠️  pip no encontrado, intentando instalar...${NC}"
    python -m ensurepip --upgrade
}

Write-Host ""
Write-Host "${Yellow}📦 Instalando dependencias de Python...${NC}"
pip install -r "$ScriptDir\requirements.txt" --user

Write-Host ""
Write-Host "${Yellow}📁 Creando directorio de instalación...${NC}"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

Write-Host ""
Write-Host "${Yellow}📋 Copiando archivos...${NC}"
Copy-Item -Recurse -Force "$ScriptDir\src" "$InstallDir\"
Copy-Item -Recurse -Force "$ScriptDir\config" "$InstallDir\"
Copy-Item -Recurse -Force "$ScriptDir\prompts" "$InstallDir\"
Copy-Item -Recurse -Force "$ScriptDir\memory" "$InstallDir\"

# Crear script de inicio
$NexoScript = @"
@echo off
python "%~dp0\src\nexo.py" %*
"@
Set-Content -Path "$InstallDir\nexo.bat" -Value $NexoScript

Write-Host ""
Write-Host "${Yellow}🔗 Agregando al PATH del usuario...${NC}"

# Obtener PATH actual
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Verificar si ya está en el PATH
if ($CurrentPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$InstallDir", "User")
    Write-Host "${Green}✅ Directorio agregado al PATH${NC}"
    Write-Host "${Yellow}⚠️  Reiniciá la terminal para que surta efecto${NC}"
} else {
    Write-Host "${Green}✅ Directorio ya está en el PATH${NC}"
}

Write-Host ""
Write-Host "${Yellow}🔍 Verificando Ollama...${NC}"

try {
    $OllamaVersion = ollama --version 2>&1
    Write-Host "${Green}✅ Ollama encontrado${NC}"
    
    # Verificar si Ollama está corriendo
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 5
        Write-Host "${Green}✅ Ollama está corriendo${NC}"
    } catch {
        Write-Host "${Yellow}⚠️  Ollama no está corriendo. Inicialo con: ollama serve${NC}"
    }
    
    # Verificar modelo
    $models = ollama list 2>&1
    if ($models -match "llama3.2") {
        Write-Host "${Green}✅ Modelo llama3.2 encontrado${NC}"
    } else {
        Write-Host "${Yellow}⚠️  Modelo llama3.2 no encontrado${NC}"
        Write-Host "${Yellow}   Descargalo con: ollama pull llama3.2${NC}"
    }
} catch {
    Write-Host "${Red}❌ Ollama no encontrado${NC}"
    Write-Host "${Yellow}   Instalalo desde: https://ollama.com${NC}"
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗"
Write-Host "║                                                              ║"
Write-Host "║   ✅ ¡INSTALACIÓN COMPLETADA!                                ║"
Write-Host "║                                                              ║"
Write-Host "║   Para usar Nexo:                                            ║"
Write-Host "║     1. Abrí una nueva terminal (PowerShell o CMD)            ║"
Write-Host "║     2. Escribí: nexo                                         ║"
Write-Host "║                                                              ║"
Write-Host "║   O ejecutá directamente:                                    ║"
Write-Host "║     $InstallDir\nexo.bat                                     ║"
Write-Host "║                                                              ║"
Write-Host "╚══════════════════════════════════════════════════════════════╝"
Write-Host ""
