---
name: qwen
description: 'Qwen Coder CLI integration for SWAL code generation'
---

# Qwen Coder CLI - SWAL Configuration

## Basic Usage

```bash
# Basic execution
qwen "Your coding task"

# With provider/model selection
qwen --provider openai --model gpt-4o-mini -p "Your task"
```

## SWAL Context

- Use for code generation tasks
- Coordinate with Xavier2 for project context
- For parallel work, use git worktrees

## See Also

- `coding-agent` skill for multi-agent orchestration
- `xavier2-context` for central memory
