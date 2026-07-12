# 🦙 Nexo Llama

**Asistente de IA personal que corre en tu PC usando Llama + Ollama**

Nexo Llama es un asistente de IA local, privado y gratuito que puede:
- 💬 Conversar con personalidad
- 🔧 Ejecutar comandos del sistema
- 🧠 Recordar información entre sesiones
- 🌐 Funcionar en Windows y Linux
- 🔒 100% local (sin internet necesario)

## 🚀 Características

| Característica | Descripción |
|----------------|-------------|
| **Local** | Todo corre en tu PC, sin datos en la nube |
| **Multi-plataforma** | Windows, Linux, macOS |
| **Personalizado** | Modifica la personalidad de Nexo |
| **Memoria** | Recuerda conversaciones anteriores |
| **Comandos** | Controla tu PC por voz/texto |
| **Privado** | Tus datos no salen de tu computadora |

## 📋 Requisitos

- **Ollama** instalado ([ollama.com](https://ollama.com))
- **Python 3.8+**
- **4GB RAM mínimo** (8GB recomendado)
- **2GB de espacio en disco** para el modelo

## 🛠️ Instalación Rápida

### Linux / macOS

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/nexo-llama.git
cd nexo-llama

# Ejecutar instalador
chmod +x scripts/install.sh
./scripts/install.sh
```

### Windows

```powershell
# Clonar el repositorio
git clone https://github.com/tu-usuario/nexo-llama.git
cd nexo-llama

# Ejecutar instalador
.\install.ps1
```

## 🎯 Uso

```bash
# Iniciar Nexo (después de instalar)
nexo

# O ejecutar directamente
python3 src/nexo.py
```

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `salir` | Cerrar Nexo |
| `memoria` | Ver qué recuerda |
| `limpiar` | Limpiar contexto |
| `config` | Ver configuración |
| `ayuda` | Mostrar ayuda |

### Comandos del Sistema

| Comando | Descripción |
|---------|-------------|
| `hora` | Hora actual |
| `fecha` | Fecha actual |
| `sistema` | Info del sistema |
| `disk` | Espacio en disco |
| `ram` | Uso de RAM |
| `cpu` | Uso de CPU |
| `procesos` | Procesos principales |
| `red` | Info de red |
| `abrir [app]` | Abrir aplicación |

## 🧠 Cómo Funciona

```
┌─────────────────────────────────────────────┐
│              Nexo Llama                      │
├─────────────────────────────────────────────┤
│  Usuario → Comando/Texto                     │
│     ↓                                        │
│  Procesador de Comandos                      │
│     ↓                                        │
│  Ollama API (localhost:11434)                │
│     ↓                                        │
│  Modelo Llama (local)                        │
│     ↓                                        │
│  Respuesta con personalidad Nexo             │
│     ↓                                        │
│  Memoria Persistente (SQLite)                │
└─────────────────────────────────────────────┘
```

## 📁 Estructura

```
nexo-llama/
├── src/
│   ├── nexo.py           # Archivo principal
│   ├── engine.py         # Motor de comandos
│   ├── memory.py         # Sistema de memoria
│   ├── ollama_client.py  # Cliente de Ollama
│   └── utils.py          # Utilidades
├── config/
│   └── settings.json     # Configuración
├── prompts/
│   ├── system.txt        # Prompt del sistema
│   └── personality.txt   # Personalidad de Nexo
├── memory/               # Base de datos SQLite
├── scripts/
│   └── install.sh        # Instalador Linux/macOS
├── install.ps1           # Instalador Windows
├── requirements.txt      # Dependencias
└── README.md             # Este archivo
```

## ⚙️ Configuración

Edita `config/settings.json`:

```json
{
  "model": "llama3.2",
  "temperature": 0.7,
  "max_tokens": 2048,
  "memory_enabled": true,
  "language": "es"
}
```

## 🎨 Personalización

Modifica `prompts/personality.txt` para cambiar cómo habla Nexo:

```
Sos Nexo, un asistente de IA amigable y bromista.
Hablás en español argentino.
Te gustan los memes y la tecnología.
Siempreayudás al usuario de la mejor forma posible.
```

## 🔧 Modelos Recomendados

| Modelo | Tamaño | RAM Necesaria | Calidad |
|--------|--------|---------------|---------|
| `llama3.2:1b` | 1GB | 2GB | Básica |
| `llama3.2:3b` | 2GB | 4GB | Buena |
| `llama3.1:8b` | 4GB | 8GB | Excelente |
| `llama3.1:70b` | 40GB | 64GB | Máxima |

## 🐛 Solución de Problemas

### Ollama no está corriendo
```bash
# Linux/macOS
ollama serve

# Windows
ollama serve
```

### Modelo no encontrado
```bash
# Descargar modelo
ollama pull llama3.2
```

### Error de Python
```bash
# Verificar versión
python3 --version

# Actualizar pip
pip3 install --upgrade pip
```

## 📝 Licencia

MIT License - Gratis para usar y modificar.

## 🤝 Contribuir

Las contribuciones son bienvenidas! Fork, branch, commit, PR.

---

**Creado por mikuyasha (miku) con ❤️ usando Llama de Meta**
