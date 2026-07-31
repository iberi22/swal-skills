#!/usr/bin/env python3
"""
Validate required <let> headers exist in POML recipes.
Usage (lint-staged): python scripts/check_poml_headers.py -- <files>

Required let names:
- topology (solo|multi)
- bench_id
- tools
- providers
Optional but recommended:
- variant or variants
- tool_aliases
- constraints
- prompt_variants
"""
import argparse
import re
import sys
from pathlib import Path

LET_RE = re.compile(r"<let\s+name=\"([^\"]+)\"[^>]*>([\s\S]*?)</let>", re.MULTILINE)

REQUIRED = {"topology", "bench_id", "tools", "providers"}
OPTIONAL = {"variant", "variants", "tool_aliases", "constraints", "prompt_variants"}


def parse_lets(text: str) -> dict:
    lets = {}
    for m in LET_RE.finditer(text):
        name = m.group(1).strip()
        body = m.group(2).strip()
        # last occurrence wins
        lets[name] = body
    return lets


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    lets = parse_lets(text)
    missing = [k for k in sorted(REQUIRED) if k not in lets]
    return missing


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)
    if not args.files:
        return 0

    had_error = False
    for f in args.files:
        p = Path(f)
        # Only validate .poml files
        if p.suffix.lower() != ".poml" or not p.exists():
            continue
        missing = validate_file(p)
        if missing:
            had_error = True
            sys.stderr.write(
                f"[check_poml_headers] Missing <let> keys in {p}: {', '.join(missing)}\n"
            )
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
