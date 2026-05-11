# BOOTSTRAP.md — First Boot for New Agents

> You just landed in `swal-skills`. Read this in order. Do not skip.

## 1. What This Repo Is

`swal-skills` is the **official skills library** for SWAL (SouthWest AI Labs) coding agents.

- **Skills** = packaged `SKILL.md` files that teach any agent how to use a framework, tool, or workflow.
- **Recipes** = executable POML files that configure multi-provider agents (OpenAI, Gemini, Qwen).
- **Registry** = `_registry/manifest.yaml` + `skill-provider.js` for dynamic discovery and loading.

## 2. Read These First (5 min)

1. `USER.md` — Who maintains this, their stack, and workflow preferences.
2. `README.md` — Public overview, quick start, and architecture diagram.
3. `AGENTS.md` — How agents should interact with this repo.
4. `SKILLS_SYSTEM.md` — Deep dive on dynamic loading, symlinks, raw URLs, and multi-agent integration.

## 3. Understand the Structure

```
swal-skills/
├── skills/                    # SKILL.md files (frameworks, tools, agents)
│   ├── astro/
│   ├── nextjs/
│   ├── python/
│   └── ...
├── poml/                     # Canonical POML recipes by department
│   ├── engineering/
│   ├── marketing/
│   └── ...
├── _registry/
│   ├── manifest.yaml         # Central catalog (skills + recipes + tool aliases)
│   └── skill-provider.js     # Node CLI: list, get, install, search, sync
├── schema/
│   └── recipe.schema.yaml    # JSON Schema for validating POML headers
├── scripts/                  # Python utilities (no external deps unless optional)
│   ├── check_poml_headers.py # Lint-staged validator
│   ├── convert_md_to_poml.py # Migrate Markdown recipes → POML
│   ├── bench-run.py          # Benchmark harness
│   └── bench-aggregate.py    # Results aggregator
├── docs/                     # Sharded architecture docs (BMAD style)
│   ├── architecture/
│   ├── prd/
│   └── stories/
├── engineering/              # Markdown agent recipes (legacy source for POML)
├── marketing/
├── design/
├── product/
├── project-management/
├── studio-operations/
└── testing/
```

## 4. Quick Commands to Try

```bash
# List all public skills
node _registry/skill-provider.js list --public

# List all POML recipes
node _registry/skill-provider.js recipes

# Search for a skill
node _registry/skill-provider.js search react

# Validate POML headers (run before committing)
python scripts/check_poml_headers.py -- poml/**/*.poml

# Convert Markdown recipes to POML (when needed)
python scripts/convert_md_to_poml.py \
  --departments design marketing product \
  --src-root . --dst-root poml
```

## 5. How to Contribute a New Skill

### 5.1 Create the skill directory

```bash
mkdir skills/<skill-id>
```

### 5.2 Write `SKILL.md`

Follow the [Agent Skills](https://agentskills.io/) format:

```markdown
---
name: <skill-id>
description: One-line description. Use when: (1) ..., (2) ..., (3) ...
license: MIT
metadata:
  author: swal
  version: "1.0.0"
---

# Skill Title

## Prerequisites
## Quick Start
## Commands Reference
## Troubleshooting
```

Rules:
- Start with frontmatter (YAML between `---`).
- Include `name`, `description`, `license`, `metadata.author`, `metadata.version`.
- `description` must state **when to use** the skill (trigger conditions).
- Keep it concise. Agents read this in-context; they do not scroll forever.
- Use fenced code blocks with language tags.
- Add scripts in `skills/<skill-id>/scripts/` if needed (Python stdlib preferred).

### 5.3 Update the manifest

Edit `_registry/manifest.yaml` and append your skill:

```yaml
skills:
  - id: <skill-id>
    name: "Human-readable name"
    description: "Same as SKILL.md description"
    category: framework|tool|agent|language|devops|review|security
    visibility: public|private
    repo: iberi22/swal-skills
    path: skills/<skill-id>/SKILL.md
    raw_url: https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/<skill-id>/SKILL.md
    tags: [tag1, tag2]
    dependencies: []
    agents: [openclaw, codex, claude, qwen, opencode]
```

### 5.4 Validate locally

```bash
# Syntax-check any Python scripts you added
python -m py_compile skills/<skill-id>/scripts/*.py

# Validate POML if you added a recipe
python scripts/check_poml_headers.py -- poml/<dept>/<skill-id>.poml

# Test the skill provider can see it
node _registry/skill-provider.js list | grep <skill-id>
```

### 5.5 Commit and PR

```bash
git checkout -b feat/<skill-id>
git add skills/<skill-id> _registry/manifest.yaml
git commit -m "feat: add <skill-id> skill"
git push origin feat/<skill-id>
```

Open a PR against `main`. Keep it to **one feature per PR**.

## 6. How to Contribute a New POML Recipe

1. Write the agent definition in `poml/<department>/<recipe-id>.poml`.
2. Required `<let>` headers: `topology`, `bench_id`, `tools`, `providers`.
3. Optional but recommended: `variant`, `tool_aliases`, `constraints`, `prompt_variants`.
4. Add the recipe entry to `_registry/manifest.yaml` under `recipes:`.
5. Run `python scripts/check_poml_headers.py -- poml/<department>/<recipe-id>.poml`.

See `schema/recipe.schema.yaml` for the full validation spec.

## 7. Rules of Thumb

- **Raw URLs over local paths.** If an agent cannot access the filesystem, it fetches via `raw.githubusercontent.com`.
- **Windows-safe paths.** The maintainer runs Windows 11 + WSL2. Never assume Unix-only paths.
- **No hardcoded secrets.** Use `.env.example` as the template; never commit real keys.
- **Stdlib first.** Python scripts should run with zero pip installs when possible. Optional `pyyaml` is acceptable.
- **GitCore v3.6.0.** If your skill references other SWAL repos, declare `gitcore_protocol: "3.6.0"`.
- **One thing at a time.** Small, focused commits. No mega-PRs.

## 8. Got Stuck?

1. Search existing skills for patterns: `grep -r "SKILL.md" skills/ | head -20`
2. Check the manifest for category/tags inspiration: `_registry/manifest.yaml`
3. Read `CONTRIBUTING.md` for the contribution process in Spanish.
4. Validate POML headers: `python scripts/check_poml_headers.py -- <file>`

---

*Welcome to SWAL. Build skills that work everywhere.*
