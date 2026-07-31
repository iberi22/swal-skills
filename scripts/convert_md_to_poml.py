#!/usr/bin/env python3
"""
convert_md_to_poml: Migrate Markdown agent recipes to canonical POML.
- Standard library only; optional PyYAML if available for frontmatter.
- Reads department folders with *.md and writes poml/<dept>/*.poml.
- Does not overwrite existing POML unless --force is set.

Usage:
  python scripts/convert_md_to_poml.py \
    --departments design marketing product project-management studio-operations testing bonus \
    --src-root . --dst-root poml

Windows-safe paths; preserves UTF-8.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

CANONICAL_PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openai": {"model": "gpt-5", "temperature": 0.2},
    "gemini": {"model": "gemini-2.5-pro", "temperature": 0.2},
    "qwen":   {"model": "Qwen2.5-Coder", "temperature": 0.1},
}

CANONICAL_TOOLS = ["fs.read", "fs.write", "fs.replace", "shell.run", "fs.search"]
QWEN_ALIASES = {
    "fs.read@qwen": "read_file",
    "fs.write@qwen": "write_file",
    "fs.replace@qwen": "replace",
    "shell.run@qwen": "run_shell_command",
    "fs.search@qwen": "search_file_content",
}

FRONTMATTER_DELIM = re.compile(r"^---\s*$")


def parse_md(path: Path) -> Tuple[Dict[str, Any], str]:
    """Return (frontmatter_dict, body_text). If no frontmatter, {} and all text.
    """
    text = path.read_text(encoding="utf-8")
    # normalize newlines
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    header: Dict[str, Any] = {}
    body = text
    if lines and FRONTMATTER_DELIM.match(lines[0]):
        # find closing '---'
        end_idx = None
        for i in range(1, len(lines)):
            if FRONTMATTER_DELIM.match(lines[i]):
                end_idx = i
                break
        if end_idx is not None:
            header_text = "\n".join(lines[1:end_idx])
            body = "\n".join(lines[end_idx + 1 :])
            if yaml is not None:
                try:
                    parsed = yaml.safe_load(header_text)
                    header = parsed if isinstance(parsed, dict) else {}
                except Exception:
                    header = {}
            else:
                header = {}
    return header, body.strip()


def stem_to_title(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").strip().title()


def build_poml(front: Dict[str, Any], body: str, bench_id: str) -> str:
    providers = front.get("providers") if isinstance(front.get("providers"), dict) else CANONICAL_PROVIDERS
    tools = front.get("tools")
    if isinstance(tools, str):
        tool_list = [t.strip() for t in tools.split(",") if t.strip()]
    elif isinstance(tools, list):
        tool_list = [str(t).strip() for t in tools if str(t).strip()]
    else:
        tool_list = CANONICAL_TOOLS

    tool_aliases = front.get("tool_aliases") if isinstance(front.get("tool_aliases"), dict) else QWEN_ALIASES

    # Escape any accidental closing tags within body minimally
    safe_body = body.replace("</role>", "</ role>").replace("</task>", "</ task>")

    poml = [
        "<poml>",
        "  <let name=\"topology\">solo</let>",
        f"  <let name=\"bench_id\">{bench_id}</let>",
        "  <let name=\"tool_mode\">auto</let>",
        "  <let name=\"variant\">base</let>",
        "  <let name=\"providers\">",
        "    " + json.dumps(providers, ensure_ascii=False, separators=(",", ": ")),
        "  </let>",
        "  <let name=\"tools\">" + json.dumps(tool_list, ensure_ascii=False) + "</let>",
        "  <let name=\"tool_aliases\">" + json.dumps(tool_aliases, ensure_ascii=False) + "</let>",
        "",
        "  <role>",
        safe_body,
        "  </role>",
        "",
        "  <output-format>",
        "    - Summary", 
        "    - Plan",
        "    - Diffs or code blocks (when applicable)",
        "    - Validation notes", 
        "  </output-format>",
        "</poml>",
        "",
    ]
    return "\n".join(poml)


def convert_file(md_path: Path, dst_root: Path, dept: str, force: bool = False) -> Tuple[Path, bool]:
    front, body = parse_md(md_path)
    bench_id = (front.get("bench_id") if isinstance(front.get("bench_id"), str) else md_path.stem)
    out_dir = dst_root / dept
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{md_path.stem}.poml"
    if out_path.exists() and not force:
        return out_path, False
    poml_text = build_poml(front, body, bench_id)
    out_path.write_text(poml_text, encoding="utf-8")
    return out_path, True


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Convert Markdown agent recipes to POML")
    p.add_argument("--src-root", default=".", help="Repository root where dept folders live")
    p.add_argument("--dst-root", default="poml", help="Destination root for POML output")
    p.add_argument("--departments", nargs="+", required=True, help="Dept folders to process (e.g., design marketing)")
    p.add_argument("--force", action="store_true", help="Overwrite existing .poml files")
    args = p.parse_args(argv)

    src_root = Path(args.src_root).resolve()
    dst_root = Path(args.dst_root)
    created = 0
    skipped = 0
    processed = 0

    for dept in args.departments:
        dept_dir = src_root / dept
        if not dept_dir.exists():
            print(f"warn: dept not found: {dept_dir}", file=sys.stderr)
            continue
        for md_path in dept_dir.glob("*.md"):
            processed += 1
            out_path, wrote = convert_file(md_path, dst_root, dept, force=args.force)
            if wrote:
                created += 1
                print(f"wrote: {out_path}")
            else:
                skipped += 1
                print(f"skip (exists): {out_path}")

    print(json.dumps({
        "processed": processed,
        "created": created,
        "skipped": skipped,
        "dst_root": str(dst_root),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
