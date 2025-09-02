# 🎤 Herramienta de Transcripción Whisper V4.1

Esta herramienta permite transcribir archivos de audio y video a texto de forma eficiente y precisa utilizando el modelo Whisper de OpenAI. El proyecto está containerizado con Podman/Docker para facilitar su despliegue y uso, y proporciona una interfaz amigable con barras de progreso en tiempo real.

## 🌟 ¿Por qué usar esta herramienta?

- **Fácil de usar**: Interfaz simple por línea de comandos
- **Sin configuraciones complejas**: Todo está containerizado
- **Múltiples formatos soportados**: Trabaja con casi cualquier formato de audio/video
- **Resultados profesionales**: Transcripciones precisas con marcas de tiempo
- **Experiencia de usuario mejorada**: Barras de progreso y estimaciones de tiempo realistas

## 📂 Estructura del Proyecto

```
.
├── setup_and_run_whisper-V4-1.py    # Script principal
├── README-setup_and_run_whisper-V4-1_ESP.md   # Documentación en español
├── README-setup_and_run_whisper-V4-1_ENG.md   # Documentación en inglés
└── Audios/                          # Directorio de ejemplos
    ├── Conferencia/                 # Ejemplos de conferencias
    ├── Entrevista/                  # Ejemplos de entrevistas
    ├── FresesENG/                  # Ejemplos en inglés
    └── Salesforce/                 # Ejemplos específicos
```

## ✨ Características

- **Whisper Containerizado**: Ejecuta Whisper en contenedores aislados (Podman/Docker)
- **Múltiples Formatos de Salida**: Genera archivos TXT, SRT, VTT y JSON
- **Barras de Progreso Inteligentes**: Progreso en tiempo real con cálculos de ETA
- **Selección de Modelo**: Soporte para todos los modelos Whisper (tiny hasta large-v3)
- **Multiplataforma**: Funciona en Windows, Linux y macOS
- **Detección Automática de Idioma**: Detección inteligente con override manual
- **Estimaciones de Tiempo Realistas**: Predicciones de tiempo específicas por modelo

## Requisitos

### Requisitos del Sistema
- Python 3.8 o superior
- Podman o Docker instalado y accesible
- FFmpeg (para detección de duración de audio)

### Formatos de Audio/Video Soportados
- Audio: MP3, WAV, FLAC, M4A, AAC, OGG, OPUS
- Video: MP4, AVI, MOV, MKV, WEBM (extrae audio automáticamente)

## Instalación

1. **Clonar o descargar** el archivo del script:
   ```bash
   wget https://example.com/whisper_transcriber.py
   # o
   curl -O https://example.com/whisper_transcriber.py
   ```

2. **Instalar runtime de contenedor**:
   
   **Para Podman (Recomendado)**:
   ```bash
   # Windows (usando winget)
   winget install RedHat.Podman
   
   # macOS (usando Homebrew)
   brew install podman
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install podman
   ```
   
   **Para Docker**:
   ```bash
   # Seguir la guía oficial de instalación de Docker
   # https://docs.docker.com/get-docker/
   ```

3. **Verificar instalación**:
   ```bash
   podman --version
   # o
   docker --version
   ```

## Inicio Rápido

### Uso Básico
```bash
python whisper_transcriber.py tu_archivo_audio.mp3
```

### Con Opciones Personalizadas
```bash
python whisper_transcriber.py audio.wav --language es --model medium --output-dir ./resultados
```

## Opciones de Línea de Comandos

### Argumentos Requeridos
- `audio_file`: Ruta al archivo de audio o video para transcribir

### Argumentos Opcionales

| Opción | Por Defecto | Opciones | Descripción |
|--------|-------------|----------|-------------|
| `--model` | `base` | `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3` | Modelo de Whisper a usar |
| `--language` | `es` | Cualquier código ISO de idioma o `auto` | Idioma del audio (usar `auto` para detección) |
| `--output-dir` | Mismo que archivo entrada | Cualquier ruta válida | Directorio de salida para archivos de transcripción |
| `--container-tool` | `podman` | `podman`, `docker` | Runtime de contenedor a usar |
| `--image-tag` | `whisper-transcriber` | Cualquier string | Tag personalizado de imagen de contenedor |

### Comparación de Rendimiento de Modelos

| Modelo | Tamaño | Velocidad | Precisión | Uso de Memoria | Recomendado Para |
|--------|--------|-----------|-----------|----------------|------------------|
| `tiny` | ~39MB | Muy Rápido (0.1x) | Básica | Bajo | Borradores rápidos, pruebas |
| `base` | ~74MB | Rápido (0.15x) | Buena | Bajo | Uso general |
| `small` | ~244MB | Moderado (0.25x) | Mejor | Medio | Equilibrio calidad/velocidad |
| `medium` | ~769MB | Lento (0.4x) | Alta | Alto | Transcripción profesional |
| `large` | ~1550MB | Muy Lento (0.6x) | Máxima | Muy Alto | Máxima precisión |

*Los multiplicadores de velocidad indican tiempo de procesamiento relativo a la duración del audio*

## 🚀 Ejemplos Prácticos

### Transcribir una conferencia
```bash
python setup_and_run_whisper-V4-1.py Audios/Conferencia/DESINTOXICA_TU_MENTE.m4a --model medium
```

### Transcribir una entrevista con detección automática de idioma
```bash
python setup_and_run_whisper-V4-1.py Audios/Entrevista/WhatsApp.opus --language auto --model large-v3
```

### Procesar múltiples archivos
```bash
for archivo in Audios/Salesforce/*.m4a; do
    python setup_and_run_whisper-V4-1.py "$archivo" --output-dir resultados/
done
```

## ❗ Solución de Problemas

### Error: No se puede encontrar el runtime de contenedor
Asegúrate de que Podman o Docker estén instalados y en ejecución:
```bash
# Para Podman
systemctl --user start podman.socket

# Para Docker
sudo systemctl start docker
```

### Error: Memoria insuficiente
Si experimentas errores de memoria con modelos grandes:
1. Intenta con un modelo más pequeño (medium en lugar de large)
2. Aumenta la memoria swap disponible
3. Cierra aplicaciones innecesarias

### Error: Formato de audio no soportado
Convierte tu archivo a un formato soportado usando FFmpeg:
```bash
ffmpeg -i tu_archivo.xxx -c:a libmp3lame output.mp3
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
## Ejemplos de Uso

### 1. Transcripción Básica
```bash
python whisper_transcriber.py podcast.mp3
```
**Salida**: Crea `podcast.txt`, `podcast.srt`, `podcast.vtt`, `podcast.json` en el mismo directorio

### 2. Audio en Español con Modelo Medium
```bash
python whisper_transcriber.py entrevista_espanol.wav --language es --model medium
```

### 3. Auto-detectar Idioma
```bash
python whisper_transcriber.py audio_multiidioma.m4a --language auto
```

### 4. Directorio de Salida Personalizado
```bash
python whisper_transcriber.py conferencia.mp4 --output-dir ./transcripciones --model large
```

### 5. Usar Docker en Lugar de Podman
```bash
python whisper_transcriber.py audio.opus --container-tool docker
```

### 6. Contenido de Larga Duración (Alta Precisión)
```bash
python whisper_transcriber.py llamada_conferencia.wav --model large-v3 --language es
```

## Características de las Barras de Progreso

La herramienta proporciona dos tipos de indicadores de progreso:

### 1. Progreso de Construcción de Contenedor
```
⠋ Construyendo imagen: [████████████░░░░░░░░] 60.0% (01:23) ETA: 00:57
```
- **Duración**: ~2 minutos (solo primera ejecución)
- **Cache**: Ejecuciones posteriores saltan este paso
- **Progreso**: Basado en pasos estimados de construcción

### 2. Progreso de Transcripción
```
⠙ Transcribiendo audio: [███████████████████░] 95.0% (12:34) ETA: 00:43
```
- **ETA en tiempo real**: Basado en velocidad real de procesamiento
- **Consciente del modelo**: Diferentes estimaciones por modelo Whisper
- **Tiempo preciso**: Progreso basado en tiempo transcurrido vs estimado

## Archivos de Salida

La herramienta genera múltiples formatos de salida:

### 1. Texto Plano (.txt)
```
Este es el texto transcrito de tu archivo de audio...
```

### 2. Subtítulo SubRip (.srt)
```
1
00:00:00,000 --> 00:00:05,000
Este es el texto transcrito de tu archivo de audio...

2
00:00:05,000 --> 00:00:10,000
Continuando con el siguiente segmento...
```

### 3. Subtítulo WebVTT (.vtt)
```
WEBVTT

00:00.000 --> 00:05.000
Este es el texto transcrito de tu archivo de audio...

00:05.000 --> 00:10.000
Continuando con el siguiente segmento...
```

### 4. JSON (.json)
```json
{
  "text": "Transcripción completa...",
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "Este es el texto transcrito..."
    }
  ]
}
```

## Vista General de la Arquitectura

### Desglose de Componentes

#### 1. Clase `ProgressBar`
- **Propósito**: Indicación visual de progreso con ETA
- **Características**: 
  - Spinner animado
  - Cálculo de porcentaje en tiempo real
  - Formato de tiempo HH:MM:SS
  - Estimación de ETA basada en rendimiento real

#### 2. Clase `WhisperTranscriber`
- **Funcionalidad principal**: Orquestador principal de transcripción
- **Métodos**:
  - `check_requirements()`: Valida runtime de contenedor
  - `build_image()`: Crea imagen de contenedor Whisper
  - `transcribe()`: Ejecuta proceso de transcripción
  - `get_audio_duration()`: Extrae metadatos de audio

#### 3. Gestión de Contenedores
- **Imagen**: Python 3.11-slim personalizado con Whisper
- **Volúmenes**: Monta directorio local para entrada/salida
- **Aislamiento**: Ejecución containerizada para consistencia

#### 4. Manejo de Errores
- **Codificación**: Correcciones específicas para Windows
- **Timeouts**: Previene colgado en archivos grandes
- **Fallos elegantes**: Mensajes de error informativos

## Solución de Problemas

### Problemas Comunes

#### 1. Herramienta de Contenedor No Encontrada
```
[ERROR] podman no está instalado
```
**Solución**: Instalar Podman o Docker, asegurar que esté en PATH

#### 2. Permiso Denegado (Linux)
```
[ERROR] Error en Verificando podman: permission denied
```
**Solución**: Agregar usuario al grupo docker/podman:
```bash
sudo usermod -aG docker $USER
# o
sudo usermod -aG podman $USER
# Luego cerrar sesión y volver a iniciar
```

#### 3. Archivo de Audio No Encontrado
```
[ERROR] Archivo no encontrado: /ruta/al/archivo.mp3
```
**Solución**: Verificar ruta del archivo y permisos

#### 4. Problemas de Codificación (Windows)
**Solución**: La herramienta maneja automáticamente codificación UTF-8

#### 5. Sin Memoria (Modelos Grandes)
**Solución**: Usar modelo más pequeño o aumentar RAM del sistema

### Consejos de Rendimiento

1. **Elegir modelo apropiado**: Equilibrar precisión vs velocidad
2. **Usar almacenamiento SSD**: I/O más rápido para archivos grandes
3. **Cerrar otras aplicaciones**: Liberar recursos del sistema
4. **Monitorear espacio en disco**: Los archivos de salida pueden ser grandes

## Configuración Avanzada

### Imagen de Contenedor Personalizada
```bash
python whisper_transcriber.py audio.mp3 --image-tag mi-whisper-personalizado
```

### Procesamiento en Lote (Script Shell)
```bash
#!/bin/bash
for file in *.wav; do
    python whisper_transcriber.py "$file" --model base --language es
done
```

### Integración con Otras Herramientas
```bash
# Convertir video a audio primero
ffmpeg -i video.mp4 -vn -acodec copy audio.m4a
python whisper_transcriber.py audio.m4a
```

## Casos de Uso Reales

### 1. Transcripción de Podcasts
```bash
# Para podcasts largos, usar modelo medium para equilibrio
python whisper_transcriber.py podcast_2h.mp3 --model medium --language es
```

### 2. Subtítulos para Videos
```bash
# Extraer audio y crear subtítulos
python whisper_transcriber.py video_curso.mp4 --language es --model base
# Genera archivos .srt y .vtt listos para usar
```

### 3. Transcripción de Entrevistas
```bash
# Alta precisión para entrevistas importantes
python whisper_transcriber.py entrevista.wav --model large --language es --output-dir ./entrevistas_transcritas
```

### 4. Contenido Multiidioma
```bash
# Detección automática para contenido mixto
python whisper_transcriber.py conferencia_internacional.m4a --language auto --model medium
```

### 5. Procesamiento Rápido para Borradores
```bash
# Transcripción rápida para revisión inicial
python whisper_transcriber.py reunion.opus --model tiny --language es
```

## Estimaciones de Tiempo por Caso de Uso

| Duración Audio | Modelo | Tiempo Estimado | Uso Recomendado |
|----------------|--------|-----------------|-----------------|
| 5 minutos | tiny | 30 segundos | Pruebas rápidas |
| 30 minutos | base | 4-5 minutos | Podcasts, reuniones |
| 1 hora | medium | 20-25 minutos | Entrevistas profesionales |
| 2 horas | large | 70-80 minutos | Conferencias académicas |
| 3+ horas | large-v3 | 2+ horas | Documentales, seminarios |

## Licencia

Esta herramienta encapsula el modelo Whisper de OpenAI. Consulte:
- [Licencia de OpenAI Whisper](https://github.com/openai/whisper/blob/main/LICENSE)
- Esta herramienta wrapper: Licencia MIT

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Haz fork del repositorio
2. Crea una rama de característica
3. Envía un pull request

## Soporte

Para problemas y preguntas:
1. Revisar la sección de solución de problemas
2. Verificar los requisitos del sistema
3. Crear un issue con logs de error detallados

## Roadmap Futuro

### Características Planificadas
- [ ] Interfaz web opcional
- [ ] Procesamiento en lote automático
- [ ] Detección de hablantes múltiples
- [ ] Exportación a más formatos (DOCX, PDF)
- [ ] Integración con servicios en la nube
- [ ] GPU acceleration support

### Mejoras en Progreso
- [ ] Progreso más granular durante transcripción
- [ ] Soporte para archivos muy grandes (>4GB)
- [ ] Configuración de calidad personalizable
- [ ] Modo silencioso completo

---

**Versión**: 4.1  
**Última Actualización**: Agosto 2025  
**Versión Python**: 3.8+  
**Plataformas Probadas**: Windows 10/11, Ubuntu 20.04+, macOS 12+

## Ejemplos Adicionales de PowerShell (Windows)

```powershell
# Transcribir múltiples archivos
Get-ChildItem *.mp3 | ForEach-Object { 
    python whisper_transcriber.py $_.FullName --model base --language es 
}

# Transcribir con timestamp en nombre de salida
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
python whisper_transcriber.py audio.wav --output-dir "transcripciones_$timestamp"

# Verificar archivos generados
python whisper_transcriber.py test.mp3 --model tiny
Get-ChildItem *.txt, *.srt, *.vtt, *.json | Select-Object Name, Length, LastWriteTime
```