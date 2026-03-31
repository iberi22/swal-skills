#!/usr/bin/env python3
"""
Qwen CLI Client

Wrapper para Qwen CLI en tareas de desarrollo local.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

# Add skills to path
SKILLS_DIR = os.path.dirname(__file__)
CLAWD_DIR = os.path.dirname(SKILLS_DIR)
if CLAWD_DIR not in sys.path:
    sys.path.insert(0, CLAWD_DIR)


@dataclass
class QwenResult:
    """Resultado de Qwen."""
    success: bool
    output: str
    error: Optional[str] = None
    model: Optional[str] = None
    tokens_used: Optional[int] = None


class QwenCLI:
    """Cliente para Qwen CLI."""
    
    DEFAULT_MODEL = "qwen-turbo"
    AVAILABLE_MODELS = ["qwen-turbo", "qwen-plus", "qwen-max"]
    
    def __init__(self, model: str = None, cwd: str = None):
        self.model = model or self.DEFAULT_MODEL
        self.cwd = cwd or os.getcwd()
        self._check_installation()
    
    def _check_installation(self):
        """Verificar instalación."""
        try:
            subprocess.run(
                ["qwen", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
        except FileNotFoundError:
            print("⚠️ Qwen CLI no encontrado.")
            print("   pip install qwen-cli")
    
    def _run(self, args: List[str], input_text: str = None) -> subprocess.CompletedProcess:
        """Ejecutar comando."""
        cmd = ["qwen", "--model", self.model] + args
        
        return subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            cwd=self.cwd
        )
    
    def run(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> QwenResult:
        """Ejecutar prompt."""
        args = [
            "--temperature", str(temperature),
            "--max-tokens", str(max_tokens)
        ]
        
        if model:
            args = ["--model", model] + args
        
        result = self._run(args, prompt)
        
        return QwenResult(
            success=result.returncode == 0,
            output=result.stdout,
            error=result.stderr if result.returncode != 0 else None,
            model=model or self.model
        )
    
    def analyze_file(self, filepath: str) -> QwenResult:
        """Analizar archivo."""
        if not os.path.exists(filepath):
            return QwenResult(success=False, output="", error=f"Not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompt = f"Analyze this code:\n\n```{self._get_ext(filepath)}\n{content}\n```"
        return self.run(prompt)
    
    def generate_code(self, description: str, language: str = "python") -> QwenResult:
        """Generar código."""
        prompt = f"""Generate {language} code for:

{description}

Only output the code, no explanations."""
        return self.run(prompt, temperature=0.5)
    
    def translate(self, text: str, target_lang: str = "Spanish") -> QwenResult:
        """Traducir texto."""
        prompt = f"Translate to {target_lang}:\n\n{text}"
        return self.run(prompt)
    
    def chat_session(self, session_name: str):
        """Crear sesión de chat."""
        return QwenChatSession(self, session_name)
    
    def _get_ext(self, filepath: str) -> str:
        return os.path.splitext(filepath)[1][1:]
    
    def version(self) -> str:
        result = subprocess.run(["qwen", "--version"], capture_output=True, text=True)
        return result.stdout.strip()
    
    def status(self) -> Dict:
        return {
            "model": self.model,
            "cwd": self.cwd,
            "version": self.version()
        }


class QwenChatSession:
    """Sesión de chat con Qwen."""
    
    def __init__(self, client: QwenCLI, session_name: str):
        self.client = client
        self.session_name = session_name
        self.history = []
    
    def send(self, message: str) -> QwenResult:
        result = self.client.run(message)
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": result.output})
        return result
    
    def clear(self):
        self.history = []


# === CLI ===

def qwen_run(prompt: str, **kwargs):
    cli = QwenCLI()
    result = cli.run(prompt, **kwargs)
    print(result.output)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Qwen CLI")
    parser.add_argument("prompt", help="Prompt")
    parser.add_argument("--model", help="Model")
    args = parser.parse_args()
    qwen_run(args.prompt, model=args.model)
