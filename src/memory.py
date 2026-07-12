#!/usr/bin/env python3
"""
🧠 Sistema de Memoria de Nexo Llama
Guarda y recuerda conversaciones anteriores
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class MemoryManager:
    """Gestor de memoria persistente."""
    
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.conn = None
        self.context = []
        
    def load(self):
        """Cargar memoria desde disco."""
        # Crear directorio si no existe
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Conectar a SQLite
        self.conn = sqlite3.connect(str(self.db_path))
        self.create_tables()
        
        # Cargar contexto reciente
        self.load_recent_context()
    
    def create_tables(self):
        """Crear tablas de la base de datos."""
        cursor = self.conn.cursor()
        
        # Tabla de mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de hechos aprendidos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                learned_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de configuración
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    def add(self, role, content):
        """Agregar un mensaje a la memoria."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
        
        # Mantener en contexto
        self.context.append({"role": role, "content": content})
        
        # Mantener solo los últimos 20 mensajes en contexto
        if len(self.context) > 20:
            self.context = self.context[-20:]
    
    def learn(self, key, value):
        """Aprender un hecho nuevo."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()
    
    def recall(self, key):
        """Recordar un hecho."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM facts WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_context(self, limit=20):
        """Obtener contexto reciente para el modelo."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        messages = cursor.fetchall()
        
        # Invertir para tener el orden cronológico
        messages.reverse()
        
        return [{"role": role, "content": content} for role, content in messages]
    
    def load_recent_context(self):
        """Cargar contexto reciente en memoria."""
        self.context = self.get_context(20)
    
    def get_stats(self):
        """Obtener estadísticas de memoria."""
        cursor = self.conn.cursor()
        
        # Contar mensajes
        cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = cursor.fetchone()[0]
        
        # Contar hechos
        cursor.execute("SELECT COUNT(*) FROM facts")
        facts_count = cursor.fetchone()[0]
        
        # Primer mensaje
        cursor.execute("SELECT MIN(timestamp) FROM messages")
        first_msg = cursor.fetchone()[0]
        
        # Último mensaje
        cursor.execute("SELECT MAX(timestamp) FROM messages")
        last_msg = cursor.fetchone()[0]
        
        return {
            "messages": msg_count,
            "facts": facts_count,
            "first_message": first_msg,
            "last_message": last_msg
        }
    
    def print_stats(self):
        """Mostrar estadísticas de memoria."""
        stats = self.get_stats()
        
        print("\n\033[94m🧠 Memoria de Nexo:\033[0m")
        print(f"  💬 Mensajes guardados: {stats['messages']}")
        print(f"  📚 Hechos aprendidos: {stats['facts']}")
        
        if stats['first_message']:
            print(f"  📅 Primera conversación: {stats['first_message'][:16]}")
        if stats['last_message']:
            print(f"  📅 Última conversación: {stats['last_message'][:16]}")
        
        # Mostrar algunos hechos
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM facts LIMIT 5")
        facts = cursor.fetchall()
        
        if facts:
            print("\n\033[94m📚 Lo que recuerdo:\033[0m")
            for key, value in facts:
                print(f"  • {key}: {value[:50]}...")
        print()
    
    def clear(self):
        """Borrar toda la memoria."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages")
        cursor.execute("DELETE FROM facts")
        self.conn.commit()
        self.context = []
        print("🗑️  Memoria borrada")
    
    def save(self):
        """Guardar memoria (SQLite lo hace automáticamente)."""
        if self.conn:
            self.conn.commit()
    
    def close(self):
        """Cerrar conexión a la base de datos."""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor."""
        self.close()
