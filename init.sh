#!/bin/bash
# init.sh — Bootstrap del proyecto
set -e

echo "🔧 Inicializando proyecto..."

# Detectar gestor de paquetes
if [ -f "package.json" ]; then
    echo "📦 Instalando dependencias Node..."
    npm install
elif [ -f "Cargo.toml" ]; then
    echo "🦀 Construyendo proyecto Rust..."
    cargo build
elif [ -f "requirements.txt" ]; then
    echo "🐍 Instalando dependencias Python..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    echo "🐍 Instalando dependencias Python..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
fi

# Copiar .env si no existe
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Creado .env desde .env.example — edítalo con tus claves"
fi

echo "✅ Proyecto listo"
