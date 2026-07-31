#!/usr/bin/env python3
"""
Gemini CLI Client

Wrapper para Gemini CLI en tareas de desarrollo local.
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
class GeminiResult:
    """Resultado de ejecución de Gemini."""
    success: bool
    output: str
    error: Optional[str] = None
    model: Optional[str] = None
    tokens_used: Optional[int] = None


class GeminiCLI:
    """Cliente para Gemini CLI."""
    
    DEFAULT_MODEL = "gemini-2.0-flash"
    
    def __init__(self, model: str = None, cwd: str = None):
        """
        Inicializar cliente Gemini.
        
        Args:
            model: Modelo a usar
            cwd: Working directory
        """
        self.model = model or self.DEFAULT_MODEL
        self.cwd = cwd or os.getcwd()
        self._check_installation()
    
    def _check_installation(self):
        """Verificar que Gemini CLI está instalado."""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("⚠️ Gemini CLI no encontrado. Instalar con:")
                print("   npm install -g @google/gemini-cli")
        except FileNotFoundError:
            print("⚠️ Gemini CLI no encontrado. Instalar con:")
            print("   npm install -g @google/gemini-cli")
    
    def _run(self, args: List[str], input_text: str = None) -> subprocess.CompletedProcess:
        """Ejecutar comando Gemini."""
        cmd = ["gemini", "--model", self.model] + args
        
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
        max_tokens: int = 4000,
        system_prompt: str = None,
        format: str = "text"  # text, json, markdown
    ) -> GeminiResult:
        """
        Ejecutar prompt en Gemini.
        
        Args:
            prompt: Prompt a ejecutar
            model: Modelo (override)
            temperature: Temperatura (0-1)
            max_tokens: Máximo de tokens
            system_prompt: System prompt
            format: Formato de output
        
        Returns:
            GeminiResult con el resultado
        """
        # Construir argumentos
        args = [
            "--temperature", str(temperature),
            "--max-tokens", str(max_tokens),
            "--format", format
        ]
        
        if model:
            args.insert(1, "--model")
            args.insert(2, model)
        
        if system_prompt:
            args.extend(["--system", system_prompt])
        
        result = self._run(args, prompt)
        
        return GeminiResult(
            success=result.returncode == 0,
            output=result.stdout,
            error=result.stderr if result.returncode != 0 else None,
            model=self.model
        )
    
    def analyze_file(self, filepath: str, task: str = "Explain") -> GeminiResult:
        """Analizar archivo."""
        if not os.path.exists(filepath):
            return GeminiResult(
                success=False,
                output="",
                error=f"File not found: {filepath}"
            )
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompt = f"""{task} this code:

```{self._get_extension(filepath)}
{content}
```

Provide a detailed analysis."""
        
        return self.run(prompt)
    
    def analyze_directory(self, directory: str, task: str = "Analyze") -> GeminiResult:
        """Analizar directorio completo."""
        dir_path = Path(directory)
        if not dir_path.exists():
            return GeminiResult(
                success=False,
                output="",
                error=f"Directory not found: {directory}"
            )
        
        files_content = []
        for f in dir_path.rglob("*"):
            if f.is_file() and self._is_code_file(f):
                try:
                    files_content.append(f"--- {f.relative_to(dir_path)} ---\n{f.read_text()}")
                except Exception:
                    pass
        
        content = "\n\n".join(files_content)
        prompt = f"""{task} this codebase:

{content}

Summary of structure and key files:"""
        
        return self.run(prompt)
    
    def generate_code(self, description: str, language: str = "python") -> GeminiResult:
        """Generar código."""
        prompt = f"""Generate {language} code for:

{description}

Only output the code, no explanations. Use proper formatting."""
        
        return self.run(
            prompt,
            temperature=0.5,
            format="code"
        )
    
    def write_tests(self, filepath: str, framework: str = "pytest") -> GeminiResult:
        """Generar tests para archivo."""
        if not os.path.exists(filepath):
            return GeminiResult(
                success=False,
                output="",
                error=f"File not found: {filepath}"
            )
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompt = f"""Write {framework} tests for this code:

```{self._get_extension(filepath)}
{content}
```

Include edge cases and mock necessary dependencies."""
        
        return self.run(
            prompt,
            temperature=0.3,
            format="code"
        )
    
    def refactor(
        self,
        filepath: str,
        goal: str = "Improve code quality"
    ) -> GeminiResult:
        """Refactorizar código."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompt = f"""Refactor this code to: {goal}

Original:

```{self._get_extension(filepath)}
{content}
```

Provide the refactored code with explanation of changes."""
        
        return self.run(
            prompt,
            temperature=0.4,
            format="markdown"
        )
    
    def chat_session(self, session_name: str) -> "GeminiChatSession":
        """Crear sesión de chat."""
        return GeminiChatSession(self, session_name)
    
    def interactive(self):
        """Modo interactivo."""
        subprocess.run(["gemini", "interactive", "--model", self.model])
    
    def check_code(self, filepath: str) -> GeminiResult:
        """Revisar código (linting conceptual)."""
        return self.analyze_file(
            filepath,
            task="Review this code for: bugs, security issues, performance problems, best practices"
        )
    
    # === HELPERS ===
    
    def _get_extension(self, filepath: str) -> str:
        """Obtener extensión de archivo."""
        return os.path.splitext(filepath)[1][1:]
    
    def _is_code_file(self, f: Path) -> bool:
        """Verificar si es archivo de código."""
        code_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h',
            '.rs', '.go', '.rb', '.php', '.swift', '.kt',
            '.md', '.json', '.yaml', '.yml', '.toml'
        }
        return f.suffix.lower() in code_extensions
    
    def version(self) -> str:
        """Obtener versión de Gemini CLI."""
        result = subprocess.run(
            ["gemini", "--version"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def status(self) -> Dict:
        """Obtener estado."""
        return {
            "model": self.model,
            "cwd": self.cwd,
            "version": self.version(),
            "installed": self._is_installed()
        }
    
    def _is_installed(self) -> bool:
        """Verificar si está instalado."""
        result = subprocess.run(
            ["which", "gemini"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0


class GeminiChatSession:
    """Sesión de chat con Gemini."""
    
    def __init__(self, client: GeminiCLI, session_name: str):
        self.client = client
        self.session_name = session_name
        self.history = []
    
    def send(self, message: str) -> GeminiResult:
        """Enviar mensaje."""
        result = self.client.run(
            message,
            system_prompt="You are in a chat session. Remember context from previous messages."
        )
        
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": result.output})
        
        return result
    
    def clear(self):
        """Limpiar historial."""
        self.history = []
    
    def save(self, filepath: str):
        """Guardar historial."""
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def load(self, filepath: str):
        """Cargar historial."""
        with open(filepath, 'r') as f:
            self.history = json.load(f)


# === CLI FUNCTIONS ===

def gemini_run(prompt: str, **kwargs):
    """Ejecutar prompt desde CLI."""
    cli = GeminiCLI()
    result = cli.run(prompt, **kwargs)
    print(result.output)


def gemini_analyze_file(filepath: str, task: str = "Explain"):
    """Analizar archivo."""
    cli = GeminiCLI()
    result = cli.analyze_file(filepath, task)
    print(result.output)


def gemini_check(filepath: str):
    """Revisar código."""
    cli = GeminiCLI()
    result = cli.check_code(filepath)
    print(result.output)


# === MAIN ===

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gemini CLI Client")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # run
    run_parser = subparsers.add_parser("run", help="Run prompt")
    run_parser.add_argument("prompt", help="Prompt to execute")
    
    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze file/dir")
    analyze_parser.add_argument("path", help="File or directory")
    
    # chat
    subparsers.add_parser("chat", help="Start chat session")
    
    # status
    subparsers.add_parser("status", help="Show status")
    
    args = parser.parse_args()
    
    cli = GeminiCLI()
    
    if args.command == "run":
        result = cli.run(args.prompt)
        print(result.output)
    
    elif args.command == "analyze":
        if os.path.isdir(args.path):
            result = cli.analyze_directory(args.path)
        else:
            result = cli.analyze_file(args.path)
        print(result.output)
    
    elif args.command == "chat":
        session = cli.chat_session("cli-chat")
        print("Chat session started. Type 'exit' to quit.")
        while True:
            try:
                msg = input("You: ")
                if msg.lower() == "exit":
                    break
                result = session.send(msg)
                print(f"Gemini: {result.output}")
            except KeyboardInterrupt:
                break
    
    elif args.command == "status":
        status = cli.status()
        print(json.dumps(status, indent=2))
