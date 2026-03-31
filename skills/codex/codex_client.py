"""
Codex CLI Client for OpenClaw
Provides Python interface to Codex CLI operations.
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List


class CodexCLI:
    """Codex CLI wrapper for headless operation."""
    
    # Model priorities: spark > codex > o3
    MODELS = {
        "spark": "gpt-5.3-codex-spark",     # Fast, Pro only
        "codex": "gpt-5.3-codex",            # Default for Team/Plus
        "o3": "o3",                           # Fallback
    }
    
    def __init__(self, model: str = "codex", sandbox: str = "workspace-write"):
        # Resolve model alias
        if model in self.MODELS:
            self.model = self.MODELS[model]
        else:
            self.model = model
        self.sandbox = sandbox
        
        # Find codex executable
        self._codex_path = self._find_codex()
    
    def _find_codex(self) -> str:
        """Find codex executable in PATH."""
        import shutil
        codex_path = shutil.which("codex")
        if codex_path:
            return codex_path
        # Fallback to npm global
        return "codex"  # Let system resolve
    
    def run(self, prompt: str, 
            approval: str = "on-request",
            allow_unsafe: bool = True) -> str:
        """
        Run Codex with a task in headless mode.
        
        Args:
            prompt: The task/prompt for Codex
            approval: Ignored (kept for compatibility)
            allow_unsafe: Bypass sandbox and approvals
        
        Returns:
            Codex's response as string
        """
        cmd = [self._codex_path, "exec", prompt, "-m", self.model, "-s", self.sandbox]
        
        # Use --dangerously-bypass-approvals-and-sandbox for headless
        if allow_unsafe:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            # If spark fails (not available), fallback to codex
            if "gpt-5.3-codex-spark" in self.model and "not supported" in result.stderr.lower():
                print("⚠️ gpt-5.3-codex-spark not available, falling back to gpt-5.3-codex")
                self.model = self.MODELS["codex"]
                return self.run(prompt, approval, allow_unsafe)
            raise RuntimeError(f"Codex error: {result.stderr}")
        
        return result.stdout
    
    @staticmethod
    def select_model_by_complexity(task: str) -> str:
        """
        Select model based on task complexity.
        
        Simple tasks (list, review, explain) → spark (fast)
        Complex tasks (generate, fix, refactor) → codex (capable)
        """
        simple_keywords = ["list", "show", "get", "find", "search", "explain", "describe", "what is", "check"]
        complex_keywords = ["create", "generate", "fix", "refactor", "build", "implement", "write", "develop"]
        
        task_lower = task.lower()
        
        # Check for simple tasks first
        if any(kw in task_lower for kw in simple_keywords) and not any(kw in task_lower for kw in complex_keywords):
            return "spark"  # Will fallback to codex if not Pro
        
        return "codex"
    
    def generate(self, spec: str) -> str:
        """Generate code from a specification."""
        return self.run(f"Generate code according to this specification:\n\n{spec}")
    
    def review(self, file_path: str) -> str:
        """Review a file for issues."""
        return self.run(f"Review this code file for bugs, security issues, and improvements:\n\nFile: {file_path}")
    
    def fix(self, issue: str, file_path: Optional[str] = None) -> str:
        """Fix a specific issue."""
        task = f"Fix this issue: {issue}"
        if file_path:
            task += f"\n\nFile: {file_path}"
        return self.run(task)
    
    def refactor(self, goal: str, file_path: str) -> str:
        """Refactor code to meet specific goals."""
        return self.run(f"Refactor this code to {goal}:\n\nFile: {file_path}")
    
    def explain(self, file_path: str) -> str:
        """Explain what a file does."""
        return self.run(f"Explain what this code does:\n\nFile: {file_path}")
    
    def apply_diff(self, diff_path: str) -> str:
        """Apply a diff produced by Codex."""
        cmd = [self._codex_path, "apply", diff_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    
    def version(self) -> str:
        """Get Codex version."""
        result = subprocess.run(
            [self._codex_path, "--version"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()


# Convenience function for direct CLI usage
def codex(prompt: str, model: str = "codex") -> str:
    """
    Quick wrapper to run Codex.
    
    Args:
        prompt: The task to perform
        model: Model selection - "spark" (fast), "codex" (capable), or specific model
    
    Example:
        >>> codex("list files in ./src")
        >>> codex("fix this bug", model="codex")
    """
    client = CodexCLI(model=model)
    return client.run(prompt)


def codex_auto(prompt: str) -> str:
    """
    Auto-select model based on task complexity.
    Simple tasks → spark (fast)
    Complex tasks → codex (capable)
    """
    model = CodexCLI.select_model_by_complexity(prompt)
    print(f"🤖 Codex: Using model '{model}' for task")
    client = CodexCLI(model=model)
    return client.run(prompt)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(codex(prompt))
    else:
        print("Usage: python codex_client.py <prompt>")
