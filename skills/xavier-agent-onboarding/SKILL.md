# SKILL.md — Xavier Agent Onboarding

> *For agents, by agents. Xavier is an agent-first memory system.*

## Summary

This skill teaches any agent (Claude Code, Codex, Cursor, Windsurf, Jules, etc.) how to:
1. **Connect to Xavier** on first contact
2. **Scan and index** local agent workspaces into Xavier's memory
3. **Detect rule conflicts** that harm Xavier's performance
4. **Notify the user** with editing suggestions — never modify user files directly

## When to load this skill

- On every new connection to Xavier (first-time setup)
- When Xavier's memory seems stale or incomplete
- When user reports Xavier "doesn't know" something it should
- When you detect conflicting rules in agent configs

---

## Section 1 — Agent Onboarding Flow

Execute this flow on first connection to any Xavier instance:

```
STEP 1: SCAN
  Scan known agent workspace directories:
  - ~/.codex/          (sessions, summaries, checkpoints)
  - ~/.claude/         (projects, sessions, configs)
  - ~/.copilot/        (session state, checkpoints)
  - ~/.gemini/         (chat sessions)
  - ~/.windsurf/       (configs, sessions)
  - ~/.cursor/         (configs, sessions)
  - ~/clawd/memory/    (daily notes — highest priority)
  - ~/.xavier-agent-memories/ (previously indexed scripts)
  - Any custom path in XAVIER_SCAN_PATHS env var.

STEP 2: FILTER
  Apply quality scoring to each file (0-15):
  - Base:                +10
  - <200 chars:          -4  (too short, no signal)
  - <500 chars:          -2
  - No headings (#):     -2  (unstructured)
  - <5 non-empty lines:  -2  (too few lines)
  - Decision keywords:   +2  (decided, changed, implemented, solution,
                              conclusion, agreed, resolved, fixed)
  - Code snippets:       +1  (```, function, class, impl, async)
  - Error documentation: +1  (error, bug, failed, problem, warning)
  
  Score threshold: >= 7 is worth indexing.
  Lower scores: skip, they're noise (logs, raw JSONL, binary checkpoints).

STEP 3: DEDUP
  For each candidate:
    hash = SHA256(first 500 characters of content)
    Query Supabase: GET /memories?select=content_hash
    If hash exists → skip (already indexed)
    If hash is new → prepare for upload

STEP 4: CATEGORIZE
  Auto-detect project from content using regex patterns:
  - xavier|pgheart|hormer|mesh         → "xavier"
  - worldexams|exam|quizizz             → "worldexams"
  - gestalt|swarm|hermes                → "gestalt"
  - moonshot|trading.*bot|surrealdb     → "moonshot-trading"
  - cerebro|flutter                     → "cerebro"
  - onlyfans|fansly|nsfw|adult.*content → "content-nsfw"
  - mounjaro|ozempic|dieta|tirzepatida  → "health-diet"
  - tiktok|clip|compilation|video       → "tiktok-content"
  - jules|github|PR.*merge|integration  → "jules-github"
  - supabase|neon|nube|cloud            → "infrastructure"
  - nix.?os|migrat|disco|partition      → "nixos-migration"
  - Default tags if no match: ["general", "unsorted"]

STEP 5: UPLOAD
  Target database:
    Primary: Supabase REST API
    Mirror: Neon PostgreSQL (if available)
  
  Upload payload:
  ```json
  {
    "user_id": "<agent-name>",
    "content": "<full markdown/content>",
    "content_hash": "<sha256-hash>",
    "summary": "<first 200 chars or generated summary>",
    "tags": ["<project-tag>", "<content-type>"],
    "metadata": {
      "source": "<filepath>",
      "scanner": "xavier-agent-onboarding",
      "quality_score": <score>,
      "scan_date": "<ISO-8601>"
    }
  }
  ```
  
  Use Supabase service_role key for POST.
  Handle RLS errors: if 401/42501, log and skip (Xavier will retry on next cycle).

STEP 6: REPORT
  After scan, log a structured report:
  ```
  📋 Xavier Scan Report
  ├─ Files scanned:  10,578
  ├─ Worth indexing: 143
  ├─ Already known:  101 (dedup skipped)
  ├─ Newly indexed:  42
  └─ Skipped (noise): 10,435
  ```

---

## Section 2 — Rule Conflict Detection & Notification Protocol

Xavier's memory quality degrades when user rules contradict or limit it.  
**Do NOT edit user files. Only notify.**

### Detection checklist

When loaded, check these common conflicts:

| Symptom | Likely cause | Suggestion |
|---------|-------------|------------|
| Xavier context truncated | AGENTS.md / MEMORY.md too large | Extract stable knowledge to separate file, keep agent config lean |
| Xavier forgets projects | User rules tell agent to "stay quiet" | Add exception: "Always sync decisions back to Xavier" |
| Indexing loops on same data | Cron job runs too often | Add `deleteAfterRun: true` or extend TTL |
| Duplicate memories | Agent and user both index same files | Dedup by content_hash before upload |
| RLS errors on POST | Supabase policies block inserts | Check service_role key valid, or create Neon mirror |
| `***` in API key | Template string with masked secret | Write full key in script body, not in sandbox template |

### Notification format

When you detect a conflict, format the notification like this:

```
⚠️ Xavier Rule Conflict Detected

File: ~/clawd/agents/lasantacruz/AGENTS.md
Rule: "Red Lines" section — restricts external writes
Impact: Xavier cannot export memories to Supabase
Suggestion: Add exception for XAVIER_DATA_DIR writes

Suggested edit (review only, not auto-applied):
  - Add: "Writing to Xavier's memory store is allowed"
  - Add: "Xavier data dir: ~/xavier-memory/"

Want me to show the exact lines? [reply "yes" to preview]
```

### Escalation chain

```
1. Detect conflict
   → Log quietly (no user distraction)
   
2. If impact is LOW (cosmetic, dedup only):
   → Log only. Report at next heartbeat/check-in.
   
3. If impact is MEDIUM (Xavier works but misses context):
   → Notify user once. Include suggestion + preview diff.
   → Do NOT repeat (dedup the notification by rule-id).
   
4. If impact is HIGH (Xavier cannot connect/index/store):
   → Immediate notify. Include exact fix.
   → Suggest editing AGENTS.md, MEMORY.md, or TOOLS.md.
   → Offer to show the edit (never apply automatically).

### Rate limiting on notifications
- Once a conflict (rule-id) is notified, **do NOT repeat for 8 hours**.
- If user replies or dismisses → reset cooldown.
- If the underlying file changes (different content_hash) → re-evaluate, re-notify.
- Maximum 3 unique conflict notifications per session (prevents spam on first scan).
```

---

## Section 3 — Connection Configuration

Xavier exposes two interfaces. Configure which to use based on environment:

### Option A: Xavier HTTP Server (recommended for local/network)

```env
XAVIER_API_URL=http://localhost:8006
XAVIER_MCP_URL=http://localhost:8100
XAVIER_API_KEY=<if configured>
```

### Option B: Supabase REST API (cloud, always available)

```env
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>
SUPABASE_TABLE=memories
```

### Option C: Neon PostgreSQL (direct, needs pg module or psql)

```env
NEON_URL=postgresql://user:pass@host:5432/db?sslmode=require
NEON_TABLE=memories_supabase_mirror
```

### Option D: Xavier MCP (for IDE agents that support MCP)

```json
{
  "mcpServers": {
    "xavier": {
      "command": "xavier",
      "args": ["mcp", "--port", "8100"],
      "env": {
        "XAVIER_API_URL": "http://localhost:8006"
      }
    }
  }
}
```

### Connection troubleshooting (from production)

| Symptom | Fix |
|---------|-----|
| `ERR_INVALID_CHAR` in header | Full API key string has restricted chars. Write key directly in script body, NOT via template with `***` placeholder |
| Neon pooler timeout on rapid reconnect | Use `connection_timeout=5000` with exponential backoff (double on each retry, cap at 30s) |
| `invalid input syntax for type json` on JSONB insert | The value is already a string. Use `JSON.stringify(val)` — it safely wraps strings AND objects. Never `JSON.parse()`, which fails on strings. |
| Supabase REST POST returns 401 with Bearer challenge | RLS policy blocks inserts even with service_role key. Either disable RLS on table, or use a dedicated insert-only policy. |
| Node 24 ESM/CJS conflict (`require` vs top-level await) | Write scripts as `.cjs` files or add `"type": "commonjs"` to package.json. Bun avoids this entirely. |
| Batch insert partial success (380/533 inserted) | JSONB cast fails on NULL/empty metadata. In `toJson()`: if val is null/empty string, return `'{}'`. Always `JSON.stringify()`, never direct cast. |

---

## Section 4 — What NOT to do (anti-patterns from production)

- ❌ Do NOT index raw JSONL session logs (80% of agent workspace is noise)
- ❌ Do NOT write secrets/API keys to sandbox template strings with `***`
- ❌ Do NOT use `JSON.parse()` for fields that are already strings (use `JSON.stringify()` for JSONB)
- ❌ Do NOT use `https.get()` with masked `***` headers in stand-alone scripts — write full key
- ❌ Do NOT set Neon pooler timeout > 2000ms (hangs on rapid reconnects)
- ❌ Do NOT attempt to index files < 100 bytes (they're always noise)
- ❌ Do NOT overwrite user's AGENTS.md, MEMORY.md, or TOOLS.md — only suggest edits
- ❌ Do NOT run scan+upload on every heartbeat (cache results, re-scan weekly at most)
- ❌ Do NOT output the same command result 3 times due to timeouts (dedup sequential identical outputs)
- ❌ Do NOT run `connection_timeout=2000` for Neon pooler on rapid connections — use 5000ms with backoff
- ❌ NEVER hardcode credentials in scripts pushed to GitHub (even in private repos — scanning bots find them)
- ❌ NEVER use a `.env` file tracked by git — load from `~/.xavier/env` at runtime
- ❌ If a credential is exposed, DELETE the file from git history immediately (`git rm` + push) and rotate the credential

### Security protocol for credentials

1. Always load secrets from `~/.xavier/env` — never inline
2. Template files go in repo as `.env.xavier.example` with placeholders (`***your-key-here***`)
3. Add `scripts/.env*` to `.gitignore` if you create an actual env file in the repo dir
4. If exposed: `git rm` the file, commit, push, then rotate the credential immediately
5. GitHub secret scanning alerts are real — Neon, Supabase, AWS all monitor

---

## Change log

| Date | Change |
|------|--------|
| 2026-06-25 | Created. Based on production scan of 10,578 files across .codex, .claude, .copilot |
