"""
QwenCoder adapter skeleton (no external deps).
Maps provider-agnostic fields (tool_mode, tool_aliases) to Qwen tool/config.

Note: Placeholder only; actual SDK integration to be added later.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class QwenCoderAdapter:
    """Skeleton adapter for future native tool/function calling with Qwen/QwenCoder.

    tool_mode (auto|required|none) mapping (placeholder):
      - auto -> {"mode": "auto"}
      - required -> {"mode": "required"}
      - none -> {"mode": "none"}
    tool_aliases: logical tool name -> provider-specific function name.
    """

    def __init__(self, model: str, tool_aliases: Optional[Dict[str, str]] = None) -> None:
        self.model = model
        self.tool_aliases = tool_aliases or {}

    def map_tool_mode(self, tool_mode: Optional[str]) -> Dict[str, Any]:
        if tool_mode == "required":
            return {"mode": "required"}
        if tool_mode == "none":
            return {"mode": "none"}
        return {"mode": "auto"}

    def build_tools(self, tools: List[str]) -> List[Dict[str, Any]]:
        """Placeholder: return simple logical tool descriptors with mapped names."""
        result: List[Dict[str, Any]] = []
        for t in tools:
            name = self.tool_aliases.get(t, t)
            result.append({"name": name, "schema": {"type": "object", "properties": {}}, "required": []})
        return result

    def run(self, prompt: str) -> str:
        """Placeholder for model invocation. Echo to preserve dry-run semantics."""
        return prompt
