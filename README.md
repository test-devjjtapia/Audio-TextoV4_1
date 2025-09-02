# 🎤 Whisper Audio Transcription Tool V4.1

## 📝 Descripción
Herramienta automatizada para la transcripción de audio utilizando el modelo Whisper de OpenAI. Esta versión 4.1 está optimizada para trabajar con múltiples formatos de audio y proporciona transcripciones precisas con soporte multilingüe.

## 🎯 Propósito
Este proyecto fue creado para simplificar el proceso de transcripción de audio, haciéndolo accesible a través de una interfaz de línea de comandos sencilla y containerizada. Es especialmente útil para:
- Transcripción de conferencias
- Conversión de audio a texto para análisis
- Generación de subtítulos
- Procesamiento de contenido multimedia

## 📂 Estructura del Repositorio
```
.
├── setup_and_run_whisper-V4-1.py   # Script principal de ejecución
├── Audios/                         # Carpeta de ejemplos
│   ├── Conferencia/               # Ejemplos de conferencias
│   ├── FresesENG/                # Ejemplos en inglés
│   └── Salesforce/               # Ejemplos específicos de Salesforce
├── README-setup_and_run_whisper-V4-1_ESP.md  # Documentación detallada en español
└── README-setup_and_run_whisper-V4-1_ENG.md  # Documentación detallada en inglés
```

## 🚀 Características Principales
- Soporte para múltiples formatos de audio (MP3, WAV, M4A, OPUS, etc.)
- Containerización con Docker/Podman para fácil despliegue
- Barras de progreso en tiempo real
- Múltiples formatos de salida (TXT, SRT, VTT, JSON)
- Detección automática de idioma
- Interfaz de línea de comandos intuitiva

## 📚 Documentación
- Para instrucciones detalladas en español, consulta [README-setup_and_run_whisper-V4-1_ESP.md](README-setup_and_run_whisper-V4-1_ESP.md)
- For detailed instructions in English, check [README-setup_and_run_whisper-V4-1_ENG.md](README-setup_and_run_whisper-V4-1_ENG.md)

## 🛠️ Inicio Rápido
```bash
# Ejemplo básico de uso
python setup_and_run_whisper-V4-1.py Audios/tu_archivo.mp3

# Con opciones personalizadas
python setup_and_run_whisper-V4-1.py tu_archivo.mp3 --language es --model medium
```

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Contribuir
Las contribuciones son bienvenidas. Por favor, revisa la documentación detallada para las guías de contribución.
