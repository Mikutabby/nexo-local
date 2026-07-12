#!/usr/bin/env python3
"""
🧠 Motor de Comandos de Nexo Llama
Procesa comandos del sistema y respuestas del usuario
"""

import os
import sys
import platform
import subprocess
from datetime import datetime

class CommandEngine:
    """Motor de comandos de Nexo."""
    
    def __init__(self, nexo):
        self.nexo = nexo
        self.commands = {
            "hora": self.cmd_time,
            "fecha": self.cmd_date,
            "sistema": self.cmd_system,
            "info": self.cmd_info,
            "disk": self.cmd_disk,
            "ram": self.cmd_ram,
            "cpu": self.cmd_cpu,
            "procesos": self.cmd_processes,
            "red": self.cmd_network,
            "abrir": self.cmd_open,
            "clima": self.cmd_weather,
        }
    
    def is_command(self, text):
        """Verificar si el texto es un comando."""
        parts = text.lower().split()
        return parts[0] in self.commands
    
    def execute(self, text):
        """Ejecutar un comando."""
        parts = text.lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            return self.commands[cmd](args)
        return f"Comando no encontrado: {cmd}"
    
    def cmd_time(self, args):
        """Mostrar hora actual."""
        now = datetime.now()
        return f"🕐 Son las {now.strftime('%H:%M:%S')}"
    
    def cmd_date(self, args):
        """Mostrar fecha actual."""
        now = datetime.now()
        days = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return f"📅 Hoy es {days[now.weekday()]} {now.strftime('%d/%m/%Y')}"
    
    def cmd_system(self, args):
        """Mostrar información del sistema."""
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        processor = platform.processor() or "No disponible"
        
        return (
            f"💻 Sistema: {system} {release}\n"
            f"   Arquitectura: {machine}\n"
            f"   Procesador: {processor}"
        )
    
    def cmd_info(self, args):
        """Mostrar información detallada."""
        import platform
        import os
        
        info = {
            "Sistema": f"{platform.system()} {platform.release()}",
            "Máquina": platform.machine(),
            "Procesador": platform.processor() or "No disponible",
            "Python": platform.python_version(),
            "Hostname": platform.node(),
        }
        
        result = "💻 Información del Sistema:\n"
        for key, value in info.items():
            result += f"  {key}: {value}\n"
        
        return result
    
    def cmd_disk(self, args):
        """Mostrar espacio en disco."""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            
            total_gb = total / (1024**3)
            used_gb = used / (1024**3)
            free_gb = free / (1024**3)
            percent = (used / total) * 100
            
            return (
                f"💾 Disco:\n"
                f"  Total: {total_gb:.1f} GB\n"
                f"  Usado: {used_gb:.1f} GB ({percent:.1f}%)\n"
                f"  Libre: {free_gb:.1f} GB"
            )
        except Exception as e:
            return f"Error al obtener info del disco: {e}"
    
    def cmd_ram(self, args):
        """Mostrar uso de RAM."""
        try:
            import psutil
            mem = psutil.virtual_memory()
            
            total_gb = mem.total / (1024**3)
            used_gb = mem.used / (1024**3)
            available_gb = mem.available / (1024**3)
            
            return (
                f"🧠 RAM:\n"
                f"  Total: {total_gb:.1f} GB\n"
                f"  Usada: {used_gb:.1f} GB ({mem.percent}%)\n"
                f"  Disponible: {available_gb:.1f} GB"
            )
        except ImportError:
            # Fallback para Linux
            try:
                with open("/proc/meminfo", "r") as f:
                    lines = f.readlines()
                
                mem_info = {}
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0].rstrip(":")
                        value = int(parts[1]) / 1024  # KB to MB
                        mem_info[key] = value
                
                total = mem_info.get("MemTotal", 0)
                free = mem_info.get("MemFree", 0)
                available = mem_info.get("MemAvailable", 0)
                used = total - available
                
                return (
                    f"🧠 RAM:\n"
                    f"  Total: {total/1024:.1f} GB\n"
                    f"  Usada: {used/1024:.1f} GB ({(used/total)*100:.1f}%)\n"
                    f"  Disponible: {available/1024:.1f} GB"
                )
            except:
                return "No se pudo obtener info de RAM"
    
    def cmd_cpu(self, args):
        """Mostrar uso de CPU."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            freq = f"{cpu_freq.current:.0f} MHz" if cpu_freq else "No disponible"
            
            return (
                f"⚡ CPU:\n"
                f"  Uso: {cpu_percent}%\n"
                f"  Núcleos: {cpu_count}\n"
                f"  Frecuencia: {freq}"
            )
        except ImportError:
            return "Instala psutil: pip install psutil"
    
    def cmd_processes(self, args):
        """Mostrar procesos principales."""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if info['cpu_percent'] > 0.1:  # Solo procesos activos
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Ordenar por uso de CPU
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            result = "📊 Procesos Principales:\n"
            for i, proc in enumerate(processes[:5]):
                result += f"  {proc['name']}: CPU {proc['cpu_percent']:.1f}%\n"
            
            return result
        except ImportError:
            return "Instala psutil: pip install psutil"
    
    def cmd_network(self, args):
        """Mostrar info de red."""
        try:
            import socket
            hostname = socket.gethostname()
            
            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = "No disponible"
            
            return (
                f"🌐 Red:\n"
                f"  Hostname: {hostname}\n"
                f"  IP: {ip}"
            )
        except Exception as e:
            return f"Error: {e}"
    
    def cmd_open(self, args):
        """Abrir aplicación."""
        if not args:
            return "Uso: abrir [app]"
        
        app = args[0]
        
        # Mapeo de aplicaciones
        apps = {
            "navegador": self._get_browser(),
            "firefox": "firefox",
            "chrome": "google-chrome",
            "chromium": "chromium",
            "terminal": self._get_terminal(),
            "editor": "code",
            "notepad": "notepad",
        }
        
        app_cmd = apps.get(app.lower(), app)
        
        try:
            subprocess.Popen([app_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"✅ Abriendo {app}..."
        except FileNotFoundError:
            return f"❌ No se encontró: {app}"
        except Exception as e:
            return f"❌ Error al abrir {app}: {e}"
    
    def _get_browser(self):
        """Obtener navegador predeterminado."""
        system = platform.system()
        if system == "Linux":
            return "firefox"
        elif system == "Windows":
            return "start chrome"
        else:
            return "open -a Safari"
    
    def _get_terminal(self):
        """Obtener terminal predeterminada."""
        system = platform.system()
        if system == "Linux":
            # Intentar encontrar terminal
            terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "xterm"]
            for term in terminals:
                if os.system(f"which {term} > /dev/null 2>&1") == 0:
                    return term
            return "xterm"
        elif system == "Windows":
            return "cmd"
        else:
            return "open -a Terminal"
    
    def cmd_weather(self, args):
        """Mostrar clima (requiere internet)."""
        return "🌤️  Función de clima no implementada aún. Próximamente!"
