# AGENTS.md — SWAL Skills

> AI coding agent guidance for working with this repository.

## Overview

This repository contains **skills** for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format — plain `SKILL.md` files with metadata headers.

## Repository Structure

```
agents-flows-recipes/
├── skills/               # 18 public skill directories
│   ├── astro/
│   ├── nextjs/
│   ├── tailwindcss/
│   ├── vite/
│   ├── rust/
│   ├── python/
│   ├── deploy-anywhere/   # ← New: universal deployment
│   ├── web-design-guidelines/  # ← New: UI audit
│   └── ...
├── poml/                 # Multi-provider agent recipes
├── _registry/            # Skill manifest and provider
└── docs/                 # Architecture docs
```

## Skills

| Skill | Description |
|-------|-------------|
| `astro` | Astro + Cloudflare Pages deployment |
| `nextjs` | Next.js 15 App Router patterns |
| `tailwindcss` | Tailwind CSS responsive design |
| `vite` | Vite build optimization |
| `rust` | Idiomatic Rust patterns |
| `python` | Python best practices |
| `deploy-anywhere` | Deploy to any hosting platform |
| `web-design-guidelines` | UI/UX audit (100+ rules) |
| `frontend-agent` | React/Vue/Angular development |
| `frontend-doctor` | Debug UI issues |
| `github` | GitHub CLI operations |
| `gemini` | Gemini CLI integration |
| `codex` | Codex CLI integration |
| `qwen` | Qwen Coder integration |
| `skill-launcher` | Subagent spawning |
| `skill-provider` | Dynamic skill loading |
| `web-research` | Deep research tools |
| `jules` | Jules autonomous coding agent |

## Usage

### Read a Skill

```bash
# Direct from repo
curl https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/astro/SKILL.md

# Via skill provider
node _registry/skill-provider.js get astro
```

### Install All Skills

```bash
# Clone and reference locally
git clone https://github.com/iberi22/agents-flows-recipes.git
```

## License

MIT — See [LICENSE.md](./LICENSE.md)
