#!/usr/bin/env python3
"""
Herramienta simplificada para transcripción de audio usando Whisper con containers
"""
import os
import sys
import json
import argparse
import subprocess
import tempfile
import time
import threading
from pathlib import Path
from typing import Optional

class ProgressBar:
    def __init__(self, total_steps=10, description="Progreso", estimated_duration=None):
        self.total_steps = total_steps
        self.description = description
        self.current_step = 0
        self.running = False
        self.thread = None
        self.estimated_duration = estimated_duration
        self.start_time = None
        
    def start(self):
        """Inicia la barra de progreso animada"""
        self.running = True
        self.current_step = 0
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
        
    def update(self, step):
        """Actualiza el progreso a un paso específico"""
        self.current_step = min(step, self.total_steps)
        
    def stop(self):
        """Detiene la barra de progreso"""
        self.running = False
        if self.thread:
            self.thread.join()
        # Limpiar línea
        print("\r" + " " * 80 + "\r", end="", flush=True)
        
    def _format_time(self, seconds):
        """Formatea tiempo en HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
        
    def _animate(self):
        """Animación de la barra de progreso"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        spinner_idx = 0
        
        while self.running:
            # Calcular porcentaje real basado en tiempo transcurrido vs estimado
            elapsed = time.time() - self.start_time
            
            if self.estimated_duration and self.estimated_duration > 0:
                # Usar tiempo real para calcular progreso más preciso
                time_progress = min(elapsed / self.estimated_duration, 0.95)  # Max 95% hasta completar
                percentage = time_progress * 100
            else:
                # Fallback al método de pasos
                percentage = (self.current_step / self.total_steps) * 100
            
            # Crear barra visual
            filled = int(percentage // 5)  # 20 caracteres total
            bar = "█" * filled + "░" * (20 - filled)
            
            # Tiempo formateado
            elapsed_str = self._format_time(elapsed)
            
            # Estimación de tiempo restante
            if self.estimated_duration and percentage > 5:  # Solo mostrar ETA después del 5%
                remaining = (self.estimated_duration - elapsed) if elapsed < self.estimated_duration else 0
                remaining_str = self._format_time(max(0, remaining))
                eta_info = f" ETA: {remaining_str}"
            else:
                eta_info = ""
            
            # Mostrar progreso
            spinner = spinner_chars[spinner_idx % len(spinner_chars)]
            print(f"\r{spinner} {self.description}: [{bar}] {percentage:5.1f}% ({elapsed_str}){eta_info}", 
                  end="", flush=True)
            
            spinner_idx += 1
            time.sleep(0.2)  # Un poco más lento para mejor legibilidad

class WhisperTranscriber:
    def __init__(self, container_tool='podman', image_tag='whisper-transcriber_v4-1'):
        self.container_tool = container_tool
        self.image_tag = image_tag
        
    def log(self, message: str, level: str = 'INFO'):
        """Logger simple"""
        colors = {
            'INFO': '\033[94m',
            'SUCCESS': '\033[92m', 
            'ERROR': '\033[91m',
            'WARNING': '\033[93m'
        }
        color = colors.get(level, '')
        reset = '\033[0m'
        print(f"{color}[{level}]{reset} {message}")
        
    def run_command(self, cmd: list, description: str = "") -> subprocess.CompletedProcess:
        """Ejecuta comandos con manejo de errores mejorado para Windows"""
        try:
            if description:
                self.log(f"Ejecutando: {description}")
            
            # Configurar encoding para Windows
            encoding = 'utf-8' if os.name == 'nt' else None
            
            return subprocess.run(
                cmd, 
                check=True, 
                capture_output=True, 
                text=True, 
                timeout=3600,
                encoding=encoding,
                errors='ignore'  # Ignorar errores de encoding
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            self.log(f"Error en {description}: {error_msg[:500]}", 'ERROR')
            raise
        except FileNotFoundError:
            self.log(f"Comando no encontrado: {cmd[0]}", 'ERROR')
            raise
            
    def check_requirements(self):
        """Verifica que las herramientas necesarias estén disponibles"""
        try:
            self.run_command([self.container_tool, '--version'], f"Verificando {self.container_tool}")
            self.log(f"{self.container_tool} disponible", 'SUCCESS')
        except:
            self.log(f"{self.container_tool} no está instalado", 'ERROR')
            sys.exit(1)
            
    def image_exists(self) -> bool:
        """Verifica si la imagen ya existe"""
        try:
            result = self.run_command([self.container_tool, 'images', '-q', self.image_tag])
            return bool(result.stdout.strip())
        except:
            return False
            
    def build_image(self):
        """Construye la imagen de contenedor con Whisper"""
        self.log("Construyendo imagen de Whisper...")
        
        # Iniciar barra de progreso
        progress = ProgressBar(10, "Construyendo imagen", estimated_duration=120)  # ~2 minutos estimados
        progress.start()
        
        try:
            containerfile_content = """FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar Whisper
RUN pip install --no-cache-dir openai-whisper

# Configurar directorio de trabajo
WORKDIR /workspace
ENV PYTHONUNBUFFERED=1

# Punto de entrada
ENTRYPOINT ["whisper"]
"""
            
            with tempfile.TemporaryDirectory() as build_dir:
                progress.update(1)  # Preparando archivos
                
                containerfile_path = Path(build_dir) / "Containerfile"
                containerfile_path.write_text(containerfile_content, encoding='utf-8')
                progress.update(2)  # Archivo creado
                
                # Ejecutar build en thread separado para poder actualizar progreso
                build_thread = threading.Thread(
                    target=self._run_build_command,
                    args=(build_dir, containerfile_path, progress)
                )
                build_thread.start()
                build_thread.join()
                
                progress.update(10)  # Completado
                time.sleep(0.5)  # Mostrar 100% brevemente
                
        finally:
            progress.stop()
            
        if self.image_exists():
            self.log("Imagen construida exitosamente", 'SUCCESS')
        else:
            self.log("Error: No se pudo construir la imagen", 'ERROR')
            sys.exit(1)
    
    def _run_build_command(self, build_dir, containerfile_path, progress):
        """Ejecuta el comando build con actualizaciones de progreso simuladas"""
        try:
            # Simular progreso durante el build
            def update_progress():
                steps = [3, 4, 5, 6, 7, 8, 9]  # Pasos simulados durante build
                for step in steps:
                    if progress.running:
                        progress.update(step)
                        time.sleep(2)  # Esperar un poco entre actualizaciones
            
            progress_thread = threading.Thread(target=update_progress, daemon=True)
            progress_thread.start()
            
            # Ejecutar build real
            subprocess.run([
                self.container_tool, 'build', 
                '-t', self.image_tag,
                '-f', str(containerfile_path),
                build_dir
            ], check=True, capture_output=True, text=True, 
              timeout=1800, encoding='utf-8', errors='ignore')
            
        except subprocess.CalledProcessError as e:
            # Continuar si hay errores de encoding pero la imagen se creó
            pass
        
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Obtiene la duración del audio usando ffprobe"""
        try:
            result = self.run_command([
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', str(audio_path)
            ])
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except:
            return None
            
    def transcribe(self, audio_file: str, **options):
        """Ejecuta la transcripción"""
        audio_path = Path(audio_file).resolve()
        if not audio_path.exists():
            self.log(f"Archivo no encontrado: {audio_file}", 'ERROR')
            sys.exit(1)
            
        # Preparar directorio de salida - FIX del error original
        output_dir_arg = options.get('output_dir')
        if output_dir_arg is None:
            output_path = audio_path.parent
        else:
            output_path = Path(output_dir_arg)
        
        output_path = output_path.resolve()
        output_path.mkdir(exist_ok=True)
        
        # Verificar/construir imagen
        if not self.image_exists():
            self.build_image()
        else:
            self.log("Usando imagen existente")
            
        # Obtener información del audio
        if duration := self.get_audio_duration(str(audio_path)):
            self.log(f"Duración del audio: {duration:.1f} segundos")
            
        # Preparar comando de transcripción
        # Usar path estilo Windows para volúmenes
        if os.name == 'nt':
            volume_mount = f"{output_path}:/workspace"
        else:
            volume_mount = f"{output_path}:/workspace:Z"
            
        audio_filename = audio_path.name
        language = options.get('language', 'auto')  # Cambiar default a 'es' en lugar de 'auto'
        
        # FIX: Whisper no acepta 'auto', usar None para detección automática
        cmd = [
            self.container_tool, 'run', '--rm',
            '-v', volume_mount,
            self.image_tag,
            f"/workspace/{audio_filename}",
            '--model', options.get('model', 'small'),
            '--output_dir', '/workspace',
            '--output_format', 'all',
            '--verbose', 'False'
        ]
        
        # Solo agregar language si no es 'auto'
        if language and language != 'auto':
            cmd.extend(['--language', language])
            
        # Ejecutar transcripción
        self.log("Iniciando transcripción...")
        
        # Calcular tiempo estimado más realista para Whisper
        if duration:
            # Whisper típicamente procesa a 0.1x - 0.5x tiempo real dependiendo del modelo
            model_multipliers = {
                'tiny': 0.1,    # Muy rápido
                'base': 0.15,   # Rápido  
                'small': 0.25,  # Moderado
                'medium': 0.4,  # Lento
                'large': 0.6,   # Muy lento
                'large-v2': 0.6,
                'large-v3': 0.6
            }
            multiplier = model_multipliers.get(options.get('model', 'small'), 0.2)
            estimated_duration = duration * multiplier + 30  # +30s overhead
            self.log(f"Tiempo estimado: {self._format_duration(estimated_duration)} "
                    f"(audio: {self._format_duration(duration)}, modelo: {options.get('model', 'small')})")
        else:
            estimated_duration = 300  # 5 minutos por defecto
        
        progress = ProgressBar(100, "Transcribiendo audio", estimated_duration=estimated_duration)
        progress.start()
        
        try:
            # Ejecutar transcripción en thread separado
            transcription_thread = threading.Thread(
                target=self._run_transcription_command,
                args=(cmd, progress)
            )
            transcription_thread.start()
            transcription_thread.join()
            
            progress.update(100)  # Completado
            time.sleep(0.5)  # Mostrar 100% brevemente
            
        finally:
            progress.stop()
            
        self.log("Transcripción completada", 'SUCCESS')
        
        # Mostrar archivos generados
        base_name = audio_path.stem
        output_files = []
        for ext in ['.txt', '.srt', '.vtt', '.json']:
            file_path = output_path / f"{base_name}{ext}"
            if file_path.exists():
                output_files.append(file_path)
        
        if output_files:
            self.log(f"Archivos generados en: {output_path}")
            for file in output_files:
                size_kb = file.stat().st_size / 1024
                self.log(f"  • {file.name} ({size_kb:.1f} KB)")
        else:
            self.log("No se encontraron archivos de salida", 'WARNING')
            self.log("Verificando contenido del directorio...")
            all_files = list(output_path.iterdir())
            for f in all_files:
                if f.is_file():
                    self.log(f"  - {f.name}")
    
    def _format_duration(self, seconds):
        """Formatea duración en formato legible"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    def _run_transcription_command(self, cmd, progress):
        """Ejecuta el comando de transcripción con actualizaciones de progreso"""
        try:
            # No simular progreso, dejar que el tiempo real lo maneje
            # El progreso se basa en tiempo transcurrido vs estimado
            
            # Ejecutar transcripción real
            result = subprocess.run(
                cmd, 
                check=True, 
                capture_output=True, 
                text=True,
                timeout=7200,  # 2 horas máximo
                encoding='utf-8',
                errors='ignore'
            )
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error en transcripción: {e.stderr[:200] if e.stderr else str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Transcripción de audio usando Whisper en contenedor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s audio.mp3
  %(prog)s audio.wav --language es --model medium
  %(prog)s video.mp4 --output-dir ./transcripciones
        """
    )
    
    parser.add_argument('audio_file', help='Archivo de audio/video a transcribir')
    parser.add_argument('--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3'],
                       help='Modelo de Whisper a usar (default: base)')
    parser.add_argument('--language', default='auto', 
                       help='Idioma del audio (default: es, usa "auto" para detección automática)')
    parser.add_argument('--output-dir', help='Directorio de salida (default: mismo directorio del audio)')
    parser.add_argument('--container-tool', default='podman', choices=['podman', 'docker'],
                       help='Herramienta de contenedor (default: podman)')
    parser.add_argument('--image-tag', default='whisper-transcriber_v4-1',
                       help='Tag de la imagen de contenedor')
    
    args = parser.parse_args()
    
    # Crear transcriptor
    transcriber = WhisperTranscriber(
        container_tool=args.container_tool,
        image_tag=args.image_tag
    )
    
    # Verificar requisitos
    transcriber.check_requirements()
    
    # Ejecutar transcripción
    transcriber.transcribe(
        audio_file=args.audio_file,
        model=args.model,
        language=args.language,
        output_dir=args.output_dir
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        sys.exit(1)
