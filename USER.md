# USER.md — Maintainer Profile

> Human-in-the-loop profile for SWAL Skills. Read this before assuming context.

## Who

- **Name:** Belal / `iberi22`
- **Org:** SWAL (SouthWest AI Labs)
- **Role:** Founder, principal maintainer
- **Primary repos:** `iberi22/swal-skills`, `iberi22/agents-flows-recipes`, `iberi22/gestalt-rust`

## Stack & Environment

| Layer | Choice |
|-------|--------|
| OS (dev) | Windows 11 + WSL2 (Ubuntu) |
| Python | 3.11+ (target 3.11–3.13). Prefer `uv`; fall back to `pip` |
| Node | 20+ (LTS). `npm` for tooling only — no runtime server |
| AI providers | OpenAI, Google Gemini, Alibaba Qwen, DeepSeek V4 Pro, MiniMax-M2.7 |
| Agent platforms | OpenClaw (primary), Codex CLI, Claude Code, Qwen Coder, OpenCode |
| Infra | Cloudflare Pages (static), Vercel, Railway, Fly.io |

## Workflow Preferences

1. **One thing at a time.** Small, focused commits. No mega-PRs.
2. **Skills-first.** Every piece of knowledge becomes a `SKILL.md` or a POML recipe.
3. **Multi-agent by default.** All skills must work across OpenClaw, Codex, Claude, Qwen, and OpenCode.
4. **Raw URLs > symlinks.** Skills are fetched via raw GitHub URLs so they work anywhere (including over VPN).
5. **GitCore Protocol v3.6.0.** All SWAL repos declare `gitcore_protocol: "3.6.0"` for cross-repo skill loading.
6. **BMAD-style sharded docs.** Architecture, PRD, and stories live in `docs/` as focused `.md` shards, not monolithic files.
7. **POML for agents, Markdown for humans.** Recipes are canonical POML; human docs are Markdown.
8. **Windows-safe paths.** All scripts must handle Windows paths (`C:\Users\belal\...`) and WSL (`/mnt/c/...`).

## Communication Style

- Bilingual codebase: **English** for public-facing docs (`README.md`, `AGENTS.md`), **Spanish** for internal process docs (`CONTRIBUTING.md`, `SKILLS_SYSTEM.md`).
- Concise over verbose. Bullet points over paragraphs.
- Prefer `✅ / ❌ / ⚠️` visual markers in checklists and docs.

## Security & Ops

- No hardcoded secrets. `.env.example` only.
- Private skills (`sales-pro`, `cortex-memory`, `xavier2-context`) never expose `raw_url`.
- Git hooks via `husky` + `lint-staged` validate POML headers before commit.

## How to Reach / Validate

- GitHub: `iberi22`
- Primary skill registry: `https://raw.githubusercontent.com/iberi22/swal-skills/main/`
- Local OpenClaw skills dir: `C:\Users\belal\clawd\skills\`
- Local Codex skills dir: `C:\Users\belal\.codex\skills\`
