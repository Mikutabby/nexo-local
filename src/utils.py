#!/usr/bin/env python3
"""
🛠️ Utilidades de Nexo Llama
Funciones auxiliares generales
"""

import os
import sys
import platform
from pathlib import Path

# Colores ANSI
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}

def print_colored(text: str, color: str = "white", bold: bool = False):
    """Imprimir texto con color."""
    color_code = COLORS.get(color, COLORS["white"])
    bold_code = COLORS["bold"] if bold else ""
    reset = COLORS["reset"]
    print(f"{bold_code}{color_code}{text}{reset}")

def clear_screen():
    """Limpiar pantalla."""
    os.system("cls" if platform.system() == "Windows" else "clear")

def get_home_dir() -> Path:
    """Obtener directorio home del usuario."""
    return Path.home()

def get_platform() -> str:
    """Obtener plataforma actual."""
    return platform.system().lower()

def is_windows() -> bool:
    """Verificar si es Windows."""
    return platform.system() == "Windows"

def is_linux() -> bool:
    """Verificar si es Linux."""
    return platform.system() == "Linux"

def is_macos() -> bool:
    """Verificar si es macOS."""
    return platform.system() == "Darwin"

def ensure_dir(path: Path):
    """Asegurar que un directorio exista."""
    path.mkdir(parents=True, exist_ok=True)

def read_file(path: Path) -> str:
    """Leer archivo de texto."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        print_colored(f"Error al leer {path}: {e}", "red")
        return ""

def write_file(path: Path, content: str):
    """Escribir archivo de texto."""
    try:
        ensure_dir(path.parent)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print_colored(f"Error al escribir {path}: {e}", "red")

def get_terminal_width() -> int:
    """Obtener ancho de la terminal."""
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def print_separator(char: str = "-", length: int = 50):
    """Imprimir separador."""
    print(char * length)

def format_size(size_bytes: int) -> str:
    """Formatear tamaño en bytes a formato legible."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def check_python_version(min_version: tuple = (3, 8)) -> bool:
    """Verificar versión mínima de Python."""
    current = sys.version_info[:2]
    return current >= min_version

def get_system_info() -> dict:
    """Obtener información del sistema."""
    return {
        "platform": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or "No disponible",
        "python": platform.python_version(),
        "hostname": platform.node(),
    }
