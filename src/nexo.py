#!/usr/bin/env python3
"""
🦙 Nexo Llama - Asistente de IA Local
Asistente personal que corre en tu PC usando Llama + Ollama
Creado por mikuyasha (miku)
"""

import os
import sys
import json
import datetime
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_DIR = BASE_DIR / "prompts"
MEMORY_DIR = BASE_DIR / "memory"
SRC_DIR = BASE_DIR / "src"

# Agregar src al path
sys.path.insert(0, str(SRC_DIR))

from engine import CommandEngine
from memory import MemoryManager
from ollama_client import OllamaClient
from utils import print_colored, clear_screen

class NexoLlama:
    """Clase principal de Nexo Llama."""
    
    def __init__(self):
        self.config = self.load_config()
        self.memory = MemoryManager(MEMORY_DIR / "nexo.db")
        self.ollama = OllamaClient(self.config)
        self.engine = CommandEngine(self)
        self.running = False
        
    def load_config(self):
        """Cargar configuración."""
        config_file = CONFIG_DIR / "settings.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "model": "llama3.2",
            "temperature": 0.7,
            "max_tokens": 2048,
            "memory_enabled": True,
            "language": "es",
            "system_prompt": "Sos Nexo, un asistente de IA amigable."
        }
    
    def load_personality(self):
        """Cargar personalidad de Nexo."""
        personality_file = PROMPTS_DIR / "personality.txt"
        if personality_file.exists():
            with open(personality_file, "r", encoding="utf-8") as f:
                return f.read()
        return "Sos Nexo, un asistente de IA amigable y bromista."
    
    def load_system_prompt(self):
        """Cargar prompt del sistema."""
        system_file = PROMPTS_DIR / "system.txt"
        if system_file.exists():
            with open(system_file, "r", encoding="utf-8") as f:
                return f.read()
        return self.load_personality()
    
    def start(self):
        """Iniciar Nexo."""
        clear_screen()
        self.print_banner()
        
        # Verificar Ollama
        if not self.ollama.check_connection():
            print_colored("❌ Error: No se pudo conectar a Ollama", "red")
            print_colored("   Asegurate de que Ollama esté corriendo: ollama serve", "yellow")
            return
        
        # Verificar modelo
        if not self.ollama.check_model(self.config["model"]):
            print_colored(f"⚠️  Modelo {self.config['model']} no encontrado", "yellow")
            print_colored(f"   Descargando... (esto puede tardar)", "cyan")
            self.ollama.pull_model(self.config["model"])
        
        print_colored("✅ Nexo Llama listo!", "green")
        print_colored("   Escribí 'ayuda' para ver comandos o 'salir' para cerrar\n", "cyan")
        
        # Cargar memoria
        self.memory.load()
        
        self.running = True
        self.run_loop()
    
    def run_loop(self):
        """Loop principal de conversación."""
        while self.running:
            try:
                user_input = input("\033[94m\033[1mvox@nexo~$\033[0m ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiales
                if user_input.lower() in ["salir", "exit", "quit"]:
                    self.stop()
                    break
                
                if user_input.lower() == "limpiar":
                    clear_screen()
                    self.print_banner()
                    continue
                
                if user_input.lower() == "memoria":
                    self.memory.print_stats()
                    continue
                
                if user_input.lower() == "config":
                    self.print_config()
                    continue
                
                if user_input.lower() == "ayuda":
                    self.print_help()
                    continue
                
                # Procesar con el motor
                response = self.process_input(user_input)
                
                # Guardar en memoria
                if self.config["memory_enabled"]:
                    self.memory.add("user", user_input)
                    self.memory.add("assistant", response)
                
                # Mostrar respuesta
                print_colored(f"\n🦙 Nexo: {response}\n", "green")
                
            except KeyboardInterrupt:
                print("\n")
                self.stop()
                break
            except EOFError:
                self.stop()
                break
    
    def process_input(self, text):
        """Procesar entrada del usuario."""
        # Verificar si es un comando
        if self.engine.is_command(text):
            return self.engine.execute(text)
        
        # Procesar con Llama
        system_prompt = self.load_system_prompt()
        context = self.memory.get_context()
        
        response = self.ollama.generate(
            prompt=text,
            system=system_prompt,
            context=context
        )
        
        return response
    
    def stop(self):
        """Detener Nexo."""
        print_colored("\n👋 ¡Hasta luego! Guardando memoria...", "yellow")
        self.memory.save()
        self.running = False
        print_colored("✅ Memoria guardada. ¡Nos vemos!", "green")
    
    def print_banner(self):
        """Mostrar banner de inicio."""
        banner = """
\033[94m╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🦙  \033[1mNEXO LLAMA\033[0m\033[94m                                         ║
║                                                              ║
║   Asistente de IA Local con Llama + Ollama                   ║
║   Creado por mikuyasha (miku)                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝\033[0m
"""
        print(banner)
    
    def print_help(self):
        """Mostrar ayuda."""
        help_text = """
\033[94m📋 Comandos Disponibles:\033[0m

  \033[1mayuda\033[0m      - Mostrar esta ayuda
  \033[1msalir\033[0m      - Cerrar Nexo
  \033[1mlimpiar\033[0m    - Limpiar pantalla
  \033[1mmemoria\033[0m    - Ver estadísticas de memoria
  \033[1mconfig\033[0m     - Ver configuración actual
  \033[1mborrar\033[0m     - Borrar toda la memoria

  También podés hacerle preguntas a Nexo directamente!
"""
        print(help_text)
    
    def print_config(self):
        """Mostrar configuración."""
        print("\n\033[94m⚙️  Configuración Actual:\033[0m")
        for key, value in self.config.items():
            if key != "system_prompt":
                print(f"  {key}: {value}")

def main():
    """Función principal."""
    nexo = NexoLlama()
    nexo.start()

if __name__ == "__main__":
    main()
