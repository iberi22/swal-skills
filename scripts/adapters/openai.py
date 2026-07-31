"""
OpenAI adapter skeleton (no external deps).
Maps provider-agnostic fields (tool_mode, tool_aliases) to OpenAI config.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class OpenAIAdapter:
    """Skeleton adapter for future native tool/function calling.

    Notes:
    - tool_mode (auto|required|none) -> OpenAI tool_choice mapping:
      - auto -> {"type": "auto"}
      - required -> {"type": "required"}
      - none -> {"type": "none"}
    - tool_aliases: map logical tool names to OpenAI tool names.
    """

    def __init__(self, model: str, tool_aliases: Optional[Dict[str, str]] = None) -> None:
        self.model = model
        self.tool_aliases = tool_aliases or {}

    def map_tool_mode(self, tool_mode: Optional[str]) -> Dict[str, Any]:
        if tool_mode == "required":
            return {"type": "required"}
        if tool_mode == "none":
            return {"type": "none"}
        return {"type": "auto"}

    def build_tools(self, tools: List[str]) -> List[Dict[str, Any]]:
        """Placeholder: in real impl, return OpenAI tool JSON schema entries.
        Here we just return logical names.
        """
        result: List[Dict[str, Any]] = []
        for t in tools:
            name = self.tool_aliases.get(t, t)
            result.append({"name": name, "schema": {"type": "object", "properties": {}}, "required": []})
        return result

    def run(self, prompt: str) -> str:
        """Placeholder for model invocation.
        Returns prompt echo to preserve dry-run semantics upstream.
        """
        return prompt
