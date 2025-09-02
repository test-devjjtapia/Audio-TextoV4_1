# Whisper Transcription Tool

A simplified, containerized audio transcription tool using OpenAI's Whisper model with Podman/Docker. This tool provides real-time progress bars and intelligent time estimations for both container building and audio transcription processes.

## Features

- **Containerized Whisper**: Runs Whisper in isolated containers (Podman/Docker)
- **Multiple Output Formats**: Generates TXT, SRT, VTT, and JSON files
- **Intelligent Progress Bars**: Real-time progress with ETA calculations
- **Model Selection**: Support for all Whisper models (tiny to large-v3)
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Automatic Language Detection**: Smart language detection with manual override
- **Realistic Time Estimates**: Model-specific processing time predictions

## Requirements

### System Requirements
- Python 3.8 or higher
- Podman or Docker installed and accessible
- FFmpeg (for audio duration detection)

### Supported Audio/Video Formats
- Audio: MP3, WAV, FLAC, M4A, AAC, OGG, OPUS
- Video: MP4, AVI, MOV, MKV, WEBM (extracts audio automatically)

## Installation

1. **Clone or download** the script file:
   ```bash
   wget https://example.com/whisper_transcriber.py
   # or
   curl -O https://example.com/whisper_transcriber.py
   ```

2. **Install container runtime**:
   
   **For Podman (Recommended)**:
   ```bash
   # Windows (using winget)
   winget install RedHat.Podman
   
   # macOS (using Homebrew)
   brew install podman
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install podman
   ```
   
   **For Docker**:
   ```bash
   # Follow official Docker installation guide
   # https://docs.docker.com/get-docker/
   ```

3. **Verify installation**:
   ```bash
   podman --version
   # or
   docker --version
   ```

## Quick Start

### Basic Usage
```bash
python whisper_transcriber.py your_audio_file.mp3
```

### With Custom Options
```bash
python whisper_transcriber.py audio.wav --language en --model medium --output-dir ./results
```

## Command Line Options

### Required Arguments
- `audio_file`: Path to the audio or video file to transcribe

### Optional Arguments

| Option | Default | Choices | Description |
|--------|---------|---------|-------------|
| `--model` | `base` | `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3` | Whisper model to use |
| `--language` | `es` | Any ISO language code or `auto` | Audio language (use `auto` for detection) |
| `--output-dir` | Same as input file | Any valid path | Output directory for transcription files |
| `--container-tool` | `podman` | `podman`, `docker` | Container runtime to use |
| `--image-tag` | `whisper-transcriber` | Any string | Custom container image tag |

### Model Performance Comparison

| Model | Size | Speed | Accuracy | Memory Usage | Recommended For |
|-------|------|-------|----------|--------------|-----------------|
| `tiny` | ~39MB | Very Fast (0.1x) | Basic | Low | Quick drafts, testing |
| `base` | ~74MB | Fast (0.15x) | Good | Low | General use |
| `small` | ~244MB | Moderate (0.25x) | Better | Medium | Balanced quality/speed |
| `medium` | ~769MB | Slow (0.4x) | High | High | Professional transcription |
| `large` | ~1550MB | Very Slow (0.6x) | Highest | Very High | Maximum accuracy |

*Speed multipliers indicate processing time relative to audio duration*

## Usage Examples

### 1. Basic Transcription
```bash
python whisper_transcriber.py podcast.mp3
```
**Output**: Creates `podcast.txt`, `podcast.srt`, `podcast.vtt`, `podcast.json` in the same directory

### 2. Spanish Audio with Medium Model
```bash
python whisper_transcriber.py spanish_interview.wav --language es --model medium
```

### 3. Auto-detect Language
```bash
python whisper_transcriber.py multilingual_audio.m4a --language auto
```

### 4. Custom Output Directory
```bash
python whisper_transcriber.py lecture.mp4 --output-dir ./transcriptions --model large
```

### 5. Using Docker Instead of Podman
```bash
python whisper_transcriber.py audio.opus --container-tool docker
```

### 6. Long-form Content (High Accuracy)
```bash
python whisper_transcriber.py conference_call.wav --model large-v3 --language en
```

## Progress Bar Features

The tool provides two types of progress indicators:

### 1. Container Building Progress
```
⠋ Construyendo imagen: [████████████░░░░░░░░] 60.0% (01:23) ETA: 00:57
```
- **Duration**: ~2 minutes (first run only)
- **Cached**: Subsequent runs skip this step
- **Progress**: Based on estimated build steps

### 2. Transcription Progress
```
⠙ Transcribiendo audio: [███████████████████░] 95.0% (12:34) ETA: 00:43
```
- **Real-time ETA**: Based on actual processing speed
- **Model-aware**: Different estimates per Whisper model
- **Accurate timing**: Progress based on elapsed vs estimated time

## Output Files

The tool generates multiple output formats:

### 1. Plain Text (.txt)
```
This is the transcribed text from your audio file...
```

### 2. SubRip Subtitle (.srt)
```
1
00:00:00,000 --> 00:00:05,000
This is the transcribed text from your audio file...

2
00:00:05,000 --> 00:00:10,000
Continuing with the next segment...
```

### 3. WebVTT Subtitle (.vtt)
```
WEBVTT

00:00.000 --> 00:05.000
This is the transcribed text from your audio file...

00:05.000 --> 00:10.000
Continuing with the next segment...
```

### 4. JSON (.json)
```json
{
  "text": "Complete transcription...",
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "This is the transcribed text..."
    }
  ]
}
```

## Architecture Overview

### Component Breakdown

#### 1. `ProgressBar` Class
- **Purpose**: Visual progress indication with ETA
- **Features**: 
  - Animated spinner
  - Real-time percentage calculation
  - HH:MM:SS time formatting
  - ETA estimation based on actual performance

#### 2. `WhisperTranscriber` Class
- **Core functionality**: Main transcription orchestrator
- **Methods**:
  - `check_requirements()`: Validates container runtime
  - `build_image()`: Creates Whisper container image
  - `transcribe()`: Executes transcription process
  - `get_audio_duration()`: Extracts audio metadata

#### 3. Container Management
- **Image**: Custom Python 3.11-slim with Whisper
- **Volumes**: Mounts local directory for input/output
- **Isolation**: Containerized execution for consistency

#### 4. Error Handling
- **Encoding**: Windows-specific character encoding fixes
- **Timeouts**: Prevents hanging on large files
- **Graceful failures**: Informative error messages

## Troubleshooting

### Common Issues

#### 1. Container Tool Not Found
```
[ERROR] podman no está instalado
```
**Solution**: Install Podman or Docker, ensure it's in PATH

#### 2. Permission Denied (Linux)
```
[ERROR] Error en Verificando podman: permission denied
```
**Solution**: Add user to docker/podman group:
```bash
sudo usermod -aG docker $USER
# or
sudo usermod -aG podman $USER
# Then logout and login again
```

#### 3. Audio File Not Found
```
[ERROR] Archivo no encontrado: /path/to/file.mp3
```
**Solution**: Verify file path and permissions

#### 4. Encoding Issues (Windows)
**Solution**: The tool automatically handles UTF-8 encoding

#### 5. Out of Memory (Large Models)
**Solution**: Use smaller model or increase system RAM

### Performance Tips

1. **Choose appropriate model**: Balance accuracy vs speed
2. **Use SSD storage**: Faster I/O for large files
3. **Close other applications**: Free up system resources
4. **Monitor disk space**: Output files can be large

## Advanced Configuration

### Custom Container Image
```bash
python whisper_transcriber.py audio.mp3 --image-tag my-custom-whisper
```

### Batch Processing (Shell Script)
```bash
#!/bin/bash
for file in *.wav; do
    python whisper_transcriber.py "$file" --model base --language en
done
```

### Integration with Other Tools
```bash
# Convert video to audio first
ffmpeg -i video.mp4 -vn -acodec copy audio.m4a
python whisper_transcriber.py audio.m4a
```

## License

This tool wraps OpenAI's Whisper model. Please refer to:
- [OpenAI Whisper License](https://github.com/openai/whisper/blob/main/LICENSE)
- This wrapper tool: MIT License

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify your system requirements
3. Create an issue with detailed error logs

---

**Version**: 4.1  
**Last Updated**: August 2025  
**Python Version**: 3.8+  
**Tested Platforms**: Windows 10/11, Ubuntu 20.04+, macOS 12+