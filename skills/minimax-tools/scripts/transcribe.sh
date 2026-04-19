#!/bin/bash
# ============================================================
# Transcribe Audio — Groq Whisper API
# Usa: ./transcribe.sh audio.ogg [model]
# ============================================================

set -euo pipefail

AUDIO_FILE="${1:-}"
MODEL="${2:-whisper-large-v3}"
LANGUAGE="${3:-es}"

if [[ -z "$AUDIO_FILE" ]]; then
    echo "Uso: $0 <audio_file> [model] [language]"
    echo "Ejemplo: $0 audio.ogg whisper-large-v3 es"
    exit 1
fi

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "Error: archivo no encontrado: $AUDIO_FILE"
    exit 1
fi

if [[ -z "${GROQ_API_KEY:-}" ]]; then
    echo "Error: GROQ_API_KEY no está configurada"
    echo "Exporta tu key: export GROQ_API_KEY=gsak_..."
    exit 1
fi

TEMP_FILE=$(mktemp /tmp/transcribe.XXXXXX.ogg)
cp "$AUDIO_FILE" "$TEMP_FILE"

echo "Transcribiendo: $AUDIO_FILE"
echo "Modelo: $MODEL"
echo "Idioma: $LANGUAGE"
echo ""

RESPONSE=$(curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -F "file=@$TEMP_FILE" \
    -F "model=$MODEL" \
    -F "language=$LANGUAGE" \
    -F "response_format=text")

rm -f "$TEMP_FILE"

if [[ "$RESPONSE" == *"error"* ]]; then
    echo "Error en la transcripción:"
    echo "$RESPONSE"
    exit 1
fi

echo "$RESPONSE"