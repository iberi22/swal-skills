---
name: codex
description: 'Codex CLI integration for SWAL code generation and review'
---

# Codex CLI - SWAL Configuration

## Basic Usage

```bash
# One-shot execution
codex exec "Your coding task"

# With auto-approve
codex exec --full-auto "Your task"

# Yolo mode (no sandbox)
codex --yolo "Your task"
```

## Model

Default: `gpt-5.2-codex` (configured in `~/.codex/config.toml`)

## SWAL Context

- Use for code generation and review
- Always work in a git repo
- For parallel execution, use git worktrees
- Coordinate with Xavier2 for context

## See Also

- `coding-agent` skill for multi-agent orchestration
- `xavier2-context` for central memory
