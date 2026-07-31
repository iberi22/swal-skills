#!/usr/bin/env python3
"""
bench-run: Evaluate a recipe over micro-bench cases and write metrics.
Standard library only. Dry-run friendly (no provider calls yet).

Usage (examples):
  # POML recipe (canonical)
  python scripts/bench-run.py --task sample-task --cases all --recipe poml/engineering/ai-engineer.poml --provider openai --model gpt-5

  # Legacy Markdown recipe (with YAML frontmatter)
  python scripts/bench-run.py --task sample-task --cases all --recipe engineering/ai-engineer.md --provider openai --model gpt-5

Outputs:
  bench/<task>/results/<timestamp>.json
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
import re
from glob import glob
from typing import Any, Dict, List, Optional

# Optional YAML parsing if PyYAML is available; otherwise fall back
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_yaml_frontmatter(md_path: Optional[str]) -> Dict[str, Any]:
    """Parse YAML frontmatter between the first two lines containing only '---'.
    Returns {} if not found or if PyYAML is unavailable.
    """
    if md_path is None or not os.path.isfile(md_path):
        return {}
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Normalize Windows CRLF to LF
        content = content.replace("\r\n", "\n")
        lines = content.split("\n")
        if not lines or lines[0].strip() != "---":
            return {}
        # find closing '---'
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break
        if end_idx is None:
            return {}
        header_text = "\n".join(lines[1:end_idx])
        if yaml is None:
            return {}
        data = yaml.safe_load(header_text)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def parse_poml_lets(poml_path: Optional[str]) -> Dict[str, Any]:
    """Parse minimal <let name="…">…</let> blocks from a .poml file.
    Returns a header-like dict with keys: topology, bench_id, tools, roles.
    Providers dict is converted into roles[] with {name, provider, model}.
    Tools are parsed from JSON array in <let name="tools">.</n+    """
    if poml_path is None or not os.path.isfile(poml_path):
        return {}
    try:
        with open(poml_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Normalize newlines
        content = content.replace("\r\n", "\n")
        lets: Dict[str, Any] = {}
        # Use proper escapes in raw string: \s and \S should not be double-escaped
        for m in re.finditer(r"<let\s+name=\"([^\"]+)\">([\s\S]*?)</let>", content, flags=re.MULTILINE):
            key = m.group(1).strip()
            raw = m.group(2).strip()
            # Try JSON parse for arrays/objects; fallback to raw text
            val: Any
            try:
                val = json.loads(raw)
            except Exception:
                val = raw
            lets[key] = val

        header: Dict[str, Any] = {}
        if isinstance(lets.get("topology"), str):
            header["topology"] = lets["topology"]
        if isinstance(lets.get("bench_id"), str):
            header["bench_id"] = lets["bench_id"]
        # tools can be list or comma string
        tools = lets.get("tools")
        if isinstance(tools, list):
            header["tools"] = tools
        elif isinstance(tools, str) and tools:
            header["tools"] = [t.strip() for t in tools.split(",") if t.strip()]
        # providers -> roles
        providers = lets.get("providers")
        roles: List[Dict[str, Any]] = []
        if isinstance(providers, dict):
            for prov, cfg in providers.items():
                model = cfg.get("model") if isinstance(cfg, dict) else None
                roles.append({
                    "name": prov,
                    "provider": prov,
                    "model": model,
                })
        if roles:
            header["roles"] = roles
        return header
    except Exception:
        return {}


def parse_recipe_header(path: Optional[str]) -> Dict[str, Any]:
    """Dispatch to the appropriate lightweight parser based on extension."""
    if not path:
        return {}
    lower = path.lower()
    if lower.endswith(".poml"):
        return parse_poml_lets(path)
    if lower.endswith(".md"):
        return parse_yaml_frontmatter(path)
    # Unknown format
    return {}


def _warn(msg: str) -> None:
    sys.stderr.write(str(msg).rstrip() + "\n")


def _to_text(x: Any) -> str:
    """Best-effort conversion of arbitrary case input to text.
    Serializes dict/list to JSON; falls back to str(x)."""
    if isinstance(x, str):
        return x
    try:
        return json.dumps(x, ensure_ascii=False)
    except Exception:
        return str(x)


def validate_header_min(header: Dict[str, Any]) -> Dict[str, Any]:
    """Minimal, dependency-free checks for required keys and basic types.
    Returns { ok: bool, errors: [..] }.
    """
    errors: List[str] = []
    if not isinstance(header, dict):
        errors.append("header: not a dict or missing YAML frontmatter")
        return {"ok": False, "errors": errors}

    required = ["topology", "roles", "tools", "bench_id"]
    for k in required:
        if k not in header:
            errors.append(f"header.{k}: missing")

    # types
    if "roles" in header and not isinstance(header["roles"], list):
        errors.append("header.roles: must be an array")
    if "tools" in header and not isinstance(header["tools"], list):
        errors.append("header.tools: must be an array")

    # role entries
    roles = header.get("roles", []) if isinstance(header.get("roles", []), list) else []
    for idx, r in enumerate(roles):
        if not isinstance(r, dict):
            errors.append(f"header.roles[{idx}]: must be an object")
            continue
        for rk in ["name", "provider", "model"]:
            if rk not in r:
                errors.append(f"header.roles[{idx}].{rk}: missing")

        provider = r.get("provider")
        if provider not in {"openai", "gemini", "qwen"}:
            errors.append(f"header.roles[{idx}].provider: must be one of ['openai','gemini','qwen']")

    return {"ok": len(errors) == 0, "errors": errors}


def try_validate_with_schema(header: Dict[str, Any]) -> Optional[str]:
    """Best-effort schema validation if jsonschema + yaml are available.
    Returns a note string if validation could not run or found issues; otherwise None.
    """
    try:
        import jsonschema  # type: ignore
    except Exception:
        return "schema: jsonschema not installed, skipping strict validation"

    if yaml is None:
        return "schema: PyYAML not installed, skipping strict validation"

    schema_path = os.path.join("schema", "recipe.schema.yaml")
    if not os.path.isfile(schema_path):
        return f"schema: not found at {schema_path}, skipping"

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_obj = yaml.safe_load(f)
        jsonschema.validate(instance=header, schema=schema_obj)
        return None
    except Exception as e:
        return f"schema: validation error: {e}"


def simulate_model_response(user_input: str) -> str:
    """Dry-run placeholder: echo-like behavior."""
    return user_input


def eval_case(case: Dict[str, Any]) -> Dict[str, Any]:
    start = time.perf_counter()
    input_text = _to_text(case.get("input", ""))
    response = simulate_model_response(input_text)
    latency_ms = (time.perf_counter() - start) * 1000.0

    expected = case.get("expected", {})
    contains = expected.get("contains", [])
    passed_contains = all((token.lower() in response.lower()) for token in contains)

    passed = passed_contains

    return {
        "id": case.get("id"),
        "passed": bool(passed),
        "latency_ms": latency_ms,
        "tool_calls": 0,
        "checks": {
            "contains": {
                "expected": contains,
                "ok": passed_contains,
            }
        },
        "response_preview": response[:200],
    }


def load_cases(task: str, case_selector: str) -> List[Dict[str, Any]]:
    case_dir = os.path.join("bench", task, "cases")
    paths = sorted(glob(os.path.join(case_dir, "*.json")))
    if not paths:
        raise SystemExit(f"No cases found under {case_dir}")

    selected_ids: Optional[List[str]] = None
    if case_selector and case_selector.lower() != "all":
        selected_ids = [c.strip() for c in case_selector.split(",") if c.strip()]

    result = []
    for p in paths:
        case = read_json(p)
        if selected_ids is None or case.get("id") in selected_ids:
            result.append(case)
    if not result:
        raise SystemExit("No cases matched the selector")
    return result


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run micro-bench over a recipe")
    parser.add_argument("--task", required=True, help="Task name under bench/<task>/cases/")
    parser.add_argument("--cases", default="all", help="all or comma-separated case IDs")
    parser.add_argument("--recipe", default=None, help="Path to recipe (.poml canonical, or legacy .md with YAML header)")
    parser.add_argument("--provider", default=None, choices=["openai", "gemini", "qwen"], help="LLM provider")
    parser.add_argument("--model", default=None, help="Model name")
    parser.add_argument("--variants", default=None, help="Comma-separated prompt variant IDs")
    parser.add_argument("--output", default=None, help="Override output JSON path")

    args = parser.parse_args(argv)

    cases = load_cases(args.task, args.cases)

    header = parse_recipe_header(args.recipe)
    bench_id = header.get("bench_id") if isinstance(header, dict) else None
    if not bench_id:
        bench_id = args.task

    # Minimal header validation (warn-only)
    v = validate_header_min(header)
    if not v["ok"]:
        _warn("bench-run: header validation warnings:")
        for e in v["errors"]:
            _warn(f"- {e}")

    # Only attempt YAML schema validation for legacy Markdown recipes
    if args.recipe and args.recipe.lower().endswith(".md"):
        note = try_validate_with_schema(header)
        if note:
            _warn(note)
    else:
        _warn("schema: skipping strict validation for POML input (YAML schema applies to .md only)")

    started_at = datetime.now(timezone.utc).isoformat()

    per_case = [eval_case(c) for c in cases]

    total = len(per_case)
    passed = sum(1 for r in per_case if r["passed"]) 
    accuracy = (passed / total) if total else 0.0
    avg_latency_ms = sum(r["latency_ms"] for r in per_case) / total if total else 0.0
    total_tool_calls = sum(r.get("tool_calls", 0) for r in per_case)

    summary: Dict[str, Any] = {
        "bench_id": bench_id,
        "provider": args.provider,
        "model": args.model,
        "variants": [v.strip() for v in args.variants.split(",")] if args.variants else None,
        "started_at": started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "cases": total,
            "passed": passed,
            "accuracy": round(accuracy, 4),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "tool_calls": total_tool_calls,
        },
        "cases": per_case,
    }

    if args.output:
        out_path = args.output
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = os.path.join("bench", args.task, "results")
        out_path = os.path.join(out_dir, f"results_{ts}.json")

    write_json(out_path, summary)

    # Minimal console summary
    print(json.dumps({
        "output": out_path,
        "accuracy": summary["totals"]["accuracy"],
        "cases": summary["totals"]["cases"],
        "passed": summary["totals"]["passed"],
    }, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
