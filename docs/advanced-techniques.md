# Advanced Techniques: Multi-Agent + Tooling

This document summarizes how to incorporate advanced prompting and tooling techniques into POML recipes.

- Source inspiration:
  - Multi-Agent Design: optimizing prompts and topologies (arXiv:2502.02533v1)
  - ToolTrain: tool-integrated RL for repo deep search (arXiv:2508.03012v1)
  - System prompt gist: https://gist.github.com/burkeholland/88af0249c4b6aff3820bf37898c8bacf

## Techniques → POML Mapping

- **Topology**
  - `<let name="topology">solo</let>` for single-agent
  - `<let name="topology">multi</let>` for coordinator + specialists
- **Variants**
  - Use `<let name="variants">{ ... }</let>` to define `base`, `creative`, `fast`
  - Select via `<let name="variant">base</let>` or CLI flag
- **Providers & Overrides**
  - `<let name="providers">{ openai: { model, temperature }, ... }</let>`
  - Keep temperature low (0.2) for code; higher (0.6–0.8) for ideation
- **Canonical Tools**
  - `fs.read`, `fs.write`, `fs.replace`, `fs.search`, `shell.run`, `web.fetch`
  - Map provider-specific names in `<let name="tool_aliases">` (e.g., Qwen)
- **Constraints & Structure**
  - `<let name="constraints">[ ... ]</let>` to enforce safety and brevity
  - Include `prompt_variants` for guided stylistic shifts

## Multi-Agent Patterns

- **Coordinator + N Specialists**
  - Coordinator: planning + routing decisions
  - Specialists: domain expertise (e.g., code, docs, tests)
  - Exchange through structured messages and summarize outputs

- **Debate / Critique**
  - Two specialists critique each other; coordinator synthesizes

- **Tool-First Exploration**
  - Encourage prior file scans (`fs.search`) and quick probes (`shell.run`) before long generations

## ToolTrain-Inspired Repo Deep Search

- Use a staged approach:
  1. Enumerate targets with `fs.search`
  2. Triage findings; rank by relevance
  3. Read minimal context windows with `fs.read`
  4. Iterate small patches (`fs.replace`) with tests

## System Prompt Guidance

- Start from the base gist above; embed constraints and success criteria.
- Keep outputs concise; prefer bullet points and short code diffs.
- Always reference file paths and symbols using backticks.

## Bench Integration

- Choose a `bench_id` and create `bench/<task>/cases/*.json`
- Validate with `scripts/bench-run.py` (dry-run)
- Pin metrics in `recipes.lock.json` per provider/model/variant
