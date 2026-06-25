# Agent Discovery File — xavier-agent-onboarding

> *For any agent reading this: load this skill to connect to Xavier.*

## Quick Reference

| Field | Value |
|-------|-------|
| Skill name | `xavier-agent-onboarding` |
| Purpose | Connect agent → Xavier memory scan → rule conflict detection |
| Priority | HIGH (load on first contact with Xavier) |
| Author | Xavier Agent Memory System |
| Created | 2026-06-25 |

## Where to find this skill

| Agent / User | Path |
|-------------|------|
| **OpenClaw global** | `~/.openclaw/skills/xavier-agent-onboarding/SKILL.md` |
| **Xavier2 agent** | `~/clawd/agents/xavier2/skills/xavier-agent-onboarding/SKILL.md` |
| **LaSantacruz agent** | `~/clawd/agents/lasantacruz/skills/xavier-agent-onboarding/SKILL.md` |
| **GitHub (swal-skills)** | `https://github.com/iberi22/swal-skills/tree/main/skills/xavier-agent-onboarding` |
| **GitHub (backup)** | `https://github.com/iberi22/swal-openclaw-backup/tree/main/skills/xavier-agent-onboarding` |

## What this skill contains

| Section | Description |
|---------|-------------|
| 1. Agent Onboarding Flow | 6-step protocol: scan → filter → dedup → categorize → upload → report |
| 2. Rule Conflict Detection | How to detect harmful rules in AGENTS.md / MEMORY.md / TOOLS.md |
| 3. Notification Protocol | When and how to notify the user (never auto-edit) |
| 4. Connection Configuration | HTTP, Supabase, Neon, MCP — 4 connection methods |
| 5. Anti-patterns | 8 documented mistakes from production |

## How agents discover this

1. Read `SKILL.md` in full
2. Execute the 6-step onboarding flow
3. After indexing, run rule conflict detection against known agent config files
4. Notify user only if conflicts are MEDIUM or HIGH impact

## Change log

| Date | Change |
|------|--------|
| 2026-06-25 | Created from production scan of 10,578 agent workspace files |
