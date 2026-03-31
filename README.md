# SWAL Skills

> Official skills library for SWAL (SouthWest AI Labs) coding agents.

Universal skill system for any AI coding agent. Works with **OpenClaw, Codex, Claude Code, Qwen, OpenCode**, and any agent that reads `SKILL.md` files.

## What's Inside

### 🎯 Skills (Framework & Tool Guides)

| Skill | Description | For |
|-------|-------------|-----|
| `astro` | Astro framework + Cloudflare deployment | All agents |
| `nextjs` | Next.js 15 App Router, caching, auth | All agents |
| `tailwindcss` | Tailwind CSS responsive patterns | All agents |
| `vite` | Vite build tool optimization | All agents |
| `react` | React patterns and best practices | All agents |
| `rust` | Rust patterns and systems programming | All agents |
| `python` | Python best practices | All agents |
| `github` | GitHub CLI (gh) operations | All agents |
| `web-research` | Deep research with Tavily + Brave | All agents |
| `gemini` | Gemini CLI integration | All agents |
| `codex` | Codex CLI integration | All agents |
| `qwen` | Qwen Coder CLI integration | All agents |

### 🤖 POML Recipes (Executable Agents)

Multi-provider agent recipes that work with OpenAI, Gemini, and Qwen:

| Recipe | Department | Description |
|--------|------------|-------------|
| `ai-engineer` | engineering | AI Engineer |
| `frontend-developer` | engineering | Frontend Developer |
| `backend-architect` | engineering | Backend Architect |
| `test-writer-fixer` | engineering | Test automation |
| `devops-automator` | engineering | DevOps automation |
| `mobile-app-builder` | engineering | Mobile development |
| `content-creator` | marketing | Marketing content |
| `growth-hacker` | marketing | Growth strategies |
| `studio-coach` | bonus | Agent coach |

### 🛠️ Skill Provider

Dynamic skill loading via CLI:

```bash
# List all skills
node _registry/skill-provider.js list --public

# Get a skill
node _registry/skill-provider.js get astro

# Search skills
node _registry/skill-provider.js search tailwind
```

## Quick Start

### For OpenClaw Agents

Skills are automatically available in `C:\Users\belal\clawd\skills\`.

### For Other Agents

Fetch skills directly from raw GitHub:

```bash
# Read skill
curl https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/astro/SKILL.md

# Or clone the repo
git clone https://github.com/iberi22/swal-skills.git
```

## Architecture

```
swal-skills/
├── skills/                    # SKILL.md files
│   ├── astro/
│   ├── nextjs/
│   ├── tailwindcss/
│   └── ...
├── poml/                     # Multi-provider recipes
│   ├── engineering/
│   └── marketing/
├── _registry/
│   ├── manifest.yaml         # Skill catalog
│   └── skill-provider.js     # CLI tool
└── docs/                     # Architecture docs
```

## Skill Manifest

All skills are documented in `_registry/manifest.yaml`:

```yaml
skills:
  - id: astro
    visibility: public
    repo: iberi22/swal-skills
    path: skills/astro/SKILL.md
    raw_url: https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/astro/SKILL.md
    agents: [openclaw, codex, claude, qwen, opencode]
```

## Contributing

1. Add your skill as `skills/<name>/SKILL.md`
2. Update `_registry/manifest.yaml`
3. Submit a PR

## License

MIT - SWAL (SouthWest AI Labs)

---

**Works with any AI coding agent.** Just read the `SKILL.md` file for context.
