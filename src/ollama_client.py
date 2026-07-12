#!/usr/bin/env python3
"""
🦙 Cliente Ollama para Nexo Llama
Conecta con Ollama API para generar respuestas
"""

import json
import requests
from typing import Optional, List, Dict

class OllamaClient:
    """Cliente para la API de Ollama."""
    
    def __init__(self, config: dict):
        self.base_url = config.get("ollama_url", "http://localhost:11434")
        self.model = config.get("model", "llama3.2")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2048)
        self.timeout = config.get("timeout", 120)
    
    def check_connection(self) -> bool:
        """Verificar conexión con Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def check_model(self, model: str) -> bool:
        """Verificar si un modelo está disponible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m["name"] for m in data.get("models", [])]
                # Verificar si el modelo está disponible (con o sin tag)
                return model in models or f"{model}:latest" in models
            return False
        except requests.exceptions.RequestException:
            return False
    
    def list_models(self) -> List[str]:
        """Listar modelos disponibles."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def pull_model(self, model: str) -> bool:
        """Descargar un modelo."""
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                timeout=None  # Puede tardar mucho
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def generate(self, prompt: str, system: Optional[str] = None, 
                 context: Optional[List[Dict]] = None) -> str:
        """Generar una respuesta usando Ollama."""
        try:
            # Construir el prompt con contexto
            full_prompt = self._build_prompt(prompt, context)
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No se generó respuesta")
            else:
                return f"Error de Ollama: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "⏰ Timeout: Ollama tardó demasiado en responder"
        except requests.exceptions.ConnectionError:
            return "❌ Error: No se pudo conectar a Ollama. ¿Está corriendo? (ollama serve)"
        except Exception as e:
            return f"❌ Error inesperado: {str(e)}"
    
    def generate_stream(self, prompt: str, system: Optional[str] = None,
                       callback=None) -> str:
        """Generar respuesta con streaming."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    full_response += chunk
                    if callback:
                        callback(chunk)
            
            return full_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _build_prompt(self, prompt: str, context: Optional[List[Dict]] = None) -> str:
        """Construir prompt con contexto de conversación."""
        if not context:
            return prompt
        
        # Formatear contexto
        context_str = ""
        for msg in context[-10:]:  # Últimos 10 mensajes
            role = "Usuario" if msg["role"] == "user" else "Nexo"
            context_str += f"{role}: {msg['content']}\n"
        
        return f"Contexto de conversación:\n{context_str}\nUsuario: {prompt}\nNexo:"
