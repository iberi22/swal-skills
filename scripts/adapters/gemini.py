"""
Gemini adapter skeleton (no external deps).
Maps provider-agnostic fields (tool_mode, tool_aliases) to Gemini config.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class GeminiAdapter:
    """Skeleton adapter for future native function calling.

    Notes:
    - tool_mode (auto|required|none) -> Gemini function_calling_config.mode:
      - auto -> AUTO
      - required -> ANY (always call a function; restrict via allowed_function_names)
      - none -> NONE
    - tool_aliases: map logical tool names to Gemini function names.
    """

    def __init__(self, model: str, tool_aliases: Optional[Dict[str, str]] = None) -> None:
        self.model = model
        self.tool_aliases = tool_aliases or {}

    def map_tool_mode(self, tool_mode: Optional[str]) -> Dict[str, Any]:
        mode = "AUTO"
        if tool_mode == "required":
            mode = "ANY"
        elif tool_mode == "none":
            mode = "NONE"
        return {"function_calling_config": {"mode": mode}}

    def allowed_function_names(self, tools: List[str]) -> List[str]:
        return [self.tool_aliases.get(t, t) for t in tools]

    def run(self, prompt: str) -> str:
        """Placeholder for model invocation.
        Returns prompt echo to preserve dry-run semantics upstream.
        """
        return prompt
