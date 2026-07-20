---
name: jules
description: "Jules is SWAL's autonomous coding agent from Google. Use via Jules CLI, GitHub issues with `jules` label, or EPIC orchestration. Includes Anti-Conflict Protocol, Wave delegation, and auto-merge patterns."
metadata:
  openclaw:
    emoji: "🤖"
    autoLoad: true
    requires:
      anyBins: ["jules"]
    triggers:
      - "jules"
      - "jules ai"
      - "agente asíncrono"
      - "agente asincrono"
      - "google agent"
      - "jules-ai"
  hermes:
    tags: [jules, async, autonomous-agent, github-issues, orchestrator, anti-conflict]
    related_skills: [subagentes-cli, github-code-review, github-pr-workflow, github-issues, synapse-trader]
---

# Jules Skill — Autonomous Coding Agent & EPIC Orchestrator

> **⚡ SWAL Agent System — Updated 2026-07-20**
> **Repos:** ONLY `iberi22/*`

---

## ⚡ Quick Reference

```bash
# 🎯 Assign task to Jules (CLI)
jules new --repo iberi22/<REPO> "task description"
jules new --repo iberi22/<REPO> --parallel 3 "task"

# 🎯 Assign via GitHub issue (label = trigger)
gh issue create --repo iberi22/<REPO> --title "..." --body "$(cat body.md)" --label jules

# 📋 List sessions
jules remote list --session
jules remote list --repo

# 📥 Pull completed session
jules remote pull --session <ID>
jules teleport <SESSION_ID>

# 🔍 Check PRs from Jules
gh pr list --repo iberi22/xavier --state all --json number,title,body --jq '.[] | select(.body | test("created automatically by Jules")) | "#\(.number) \(.title)"'
```

---

## 1. Authentication

```bash
# Check if logged in
jules remote list --repo

# Login (one-time, opens browser)
jules login
```

---

## 2. How Jules Works

Jules monitorea issues de GitHub con el label **`jules`**. Flujo típico:

```
1. Creas issue + label jules
2. Jules responde en 1-5 min: "Jules is on it" + enlace a Google Tasks
3. Jules trabaja (segundos a minutos)
4. Jules abre PRs como Draft con body "Fixes #N" + enlace Google Tasks
```

**⚠️ Importante:**
- `@jules-ai` mention = NO trigger
- Issue assignment = NO trigger
- **`jules` label = ONLY trigger**
- Jules usa `iberi22` como author de PRs (mismo que humano)
- Para distinguir PRs de Jules: branch termina en 20 dígitos (Google Task ID) o body contiene "created automatically by Jules"

---

## 3. CLI Session Management

```bash
# List ALL sessions (PRIMARY monitor command)
jules remote list --session

# List connected repos
jules remote list --repo

# Create new session
jules new --repo iberi22/<REPO> "implement feature X"
jules new --repo iberi22/<REPO> --parallel 3 "write unit tests"

# Pull session result (view what Jules did)
jules remote pull --session <ID>

# Pull AND apply patch to local repo
jules remote pull --session <ID> --apply

# Teleport (clone repo + checkout + apply patch)
jules teleport <SESSION_ID>
```

### Session Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `In Progress` | Jules trabajando | Esperar |
| `Awaiting User F` | Jules pidió input | Extraer trabajo parcial, eliminar sesión, relanzar |
| `Completed` | Listo para review | `jules remote pull --apply` |
| `Failed` | Error | Revisar, crear issue nuevo |

---

## 4. Asignar Tareas via GitHub Issues

### Template de Issue (OBLIGATORIO — Jules NO pregunta, solo ejecuta)

Cada issue DEBE incluir esta estructura. Si falta "Web Research Required", Jules produce soluciones subóptimas:

```markdown
> Wave context: [Ola/Número de sprint]

## Web Research Required (Jules MUST search the web FIRST)

**MANDATORY**: Before implementing any code, search for current approaches (2025-2026).
1. **[Current Best Practice]** - search: "specific query 2025 2026"
2. **[Architecture/Design]** - search: "design pattern query"

## Exact Technical Context
- **File**: `path/to/file.rs` (N lines)
- **Function**: `function_name` at line ~XXX

> CRITICAL: gotchas, excluded crates, feature flags

## Problem
[1-3 sentences]

## Acceptance Criteria
- [ ] Specific change with exact code
- [ ] `cargo check --workspace` passes
- [ ] Tests pass

## Files to Modify
| File | Change |
|------|--------|
| `src/path.rs` | What changes |

**NEVER create `.patch` / `.py` / `part1.rs` loose files in repo root.**

## Verification
```bash
git pull origin main --rebase && cargo check --workspace
```

## Dependencies and Merge Order
- **Depends on:** [issue N]
- **Can run in parallel with:** [issue P]
```

### Trigger / Re-trigger

```bash
# Trigger
gh issue edit <N> --repo iberi22/<REPO> --add-label jules

# Re-trigger (si Jules falló o no respondió)
gh issue edit <N> --remove-label jules
sleep 5
gh issue edit <N> --add-label jules
```

---

## 5. Anti-Conflict Protocol

**THE #1 RULE: If two issues touch the same file, they CANNOT run in parallel.**

### File Ownership Map

Antes de crear issues, mapear qué archivos tocará cada issue:

```bash
# Declaración de conflictos (usar antes de taggear)
$fileOwnership = @{
  "src/auth2/mod.rs"                   = @(774, 775, 776)  # CONFLICT — sequential only
  "tests/integration/auth_test.rs"     = @(777)             # SAFE
  "panel-ui/vite.config.ts"            = @(773)             # SAFE
}
```

### Wave Tagging Rules

| Condition | Action | Ejemplo |
|-----------|--------|---------|
| Different files | Tag ALL at once → parallel PRs | Wave 1: #773, #780, #781 |
| Same file, sequential | Tag #1 → wait merge → Tag #2 | Wave 2: #774→#775→#776 |
| Docs/config only | Tag any time (never conflicts) | Wave 4: #782 |
| Tests (new files) | Tag after source PRs merged | Wave 3: #777→#778→#779 |

### Rebase Before PR (mandatory for Jules)

Agregar a la **Verification** section de cada issue:

```bash
git pull origin main --rebase
cargo check --workspace
```

### One-file-per-PR principle

- ✅ 1-2 files: low risk
- ⚠️ 3-5 files: medium — verify ownership map
- ❌ 6+ files: split into smaller issues

---

## 6. EPIC & Sub-issues Organization

### Crear EPIC

```bash
gh issue create --title "Ola N — Feature Completion to 100%" \
  --body "## EPIC: Ola N\n\nSprint description." \
  --label epic
```

### Crear Sub-issues (vinculados al EPIC)

```bash
gh issue create --parent EPIC_NUMBER \
  --title "[Ola N.X] Short description" \
  --body "$(cat body.md)" \
  --label jules
```

### Monitoring EPIC Progress

```bash
# Ver todos los sub-issues abiertos
for num in 773 774 775 776 777 778 779 780 781 782; do
  gh issue view "$num" --json number,state,title --jq '"#\(.number) [\(.state)] \(.title)"'
done
```

---

## 7. Batch Merge Workflow (for Jules PRs)

### Detectar PRs de Jules

```bash
# PRs con body que dice "created automatically by Jules"
gh pr list --repo iberi22/xavier --state all --json number,title,body,headRefName,isDraft \
  --jq '.[] | select(.body | test("created automatically by Jules|Jules for task")) | "#\(.number) [\(.state)] \(.title) draft=\(.isDraft)"'

# PRs con branch que termina en 20 dígitos (Google Task ID)
gh pr list --repo iberi22/xavier --state all --json number,headRefName,title \
  --jq '.[] | select(.headRefName | test("\\d{20}$")) | "#\(.number) \(.title) [\(.headRefName)]"'
```

### Merge Order

```
1. PRs de FUNDACIÓN (crates compartidos, types, schemas)
2. PRs de INFRAESTRUCTURA CORE (PluginHost, DB, FTS5)
3. PRs de PLUGINS/PARSERS (binarios standalone)
4. PRs de HERRAMIENTAS (MCP, tools, CLI)
5. PRs de ESTABILIZACIÓN (tests, fixes, lint)
```

### Mergear PRs de Jules (workflow completo)

```bash
# 1. Verificar estado
gh pr view <N> --repo iberi22/xavier --json state,isDraft,mergeable,additions,deletions

# 2. Marcar como ready (Jules siempre crea Draft)
gh pr ready <N> --repo iberi22/xavier

# 3. Mergear con squash
gh pr merge <N> --repo iberi22/xavier --squash --delete-branch

# 4. Cerrar issue asociado
gh issue close <N_issue> --repo iberi22/xavier --comment "✅ Delivered in main via PR #N"
```

### Resolver Conflictos entre PRs Paralelos

Cuando Jules trabaja en N issues simultáneamente:
- Cada PR se crea desde `main` en su momento
- Al mergear PR #1, los PRs #2..#N quedan con conflictos
- **NO re-triggerear a Jules** para resolver conflictos — resolverlos manualmente es más rápido

```bash
# 1. Clonar la branch del PR
git fetch origin pull/<N>/head:pr-<N>
git checkout pr-<N>

# 2. Hacer merge trial
git merge origin/main --no-commit --no-ff

# 3. Ver conflictos
git diff --name-only --diff-filter=U

# 4. Resolver o abortar
git merge --abort  # si es muy complejo
```

### Detectar PRs Obsoletos (Superseded)

Si dos PRs tocan la misma feature:

```bash
# Identificar cuál es el más completo / reciente
gh pr diff <old> --name-only
gh pr diff <new> --name-only

# Si el nuevo cubre el mismo scope + mejoras:
gh pr comment <old> --body "❌ Superseded por #<new> (merged). Cerrando."
gh pr close <old>
```

---

## 8. Autonomous Orchestrator Pattern (Auto-Merge + Wave Advance)

Para sprints continuos, combinar Jules con un script orquestador que corre cada 20 min:

```
Jules ──abre PRs Draft──► GitHub ──poll cada 20 min──► Orchestrator (no_agent script)
                                                            │
                                            ┌───────────────┼───────────────┐
                                            ▼               ▼               ▼
                                       Convert Ready    Merge Squash   Close Issue
                                            │               │               │
                                            └───────────────┴───────────────┘
                                                          │
                                                    Wave complete?
                                                          │
                                                    ┌─────┴─────┐
                                                    ▼           ▼
                                                  Sí           No
                                                    │           │
                                          Tag next wave     (wait 20 min)
                                          + assign Jules
                                                    │
                                                    ▼
                                              ──► Jules starts next wave
```

### El orquestador:

1. **Detecta** current wave (lock file o GitHub states)
2. **Tags** issues para Jules si no tienen label (agrega `jules`, `ola5`, `wave-N` + assign)
3. **Mergea** Draft PRs: `gh pr ready N` → `gh pr merge N --squash --delete-branch`
4. **Cierra** issues con comentario
5. **Avanza** wave: si todos los issues están cerrados, taggea siguiente wave
6. **Reporta** solo en cambios (watchdog silent pattern)

```bash
# Crear el cronjob
hermes cronjob create \
  --script ~/.hermes/scripts/ola5-epic-orchestrator.py \
  --no-agent \
  --deliver origin \
  --schedule "every 20 min"
```

### Pitfalls del orquestador

- **Labels must exist before adding.** Create `jules`, `ola5`, `wave-N` first.
- **`gh` returns UPPERCASE states.** Always `.upper()` in comparisons.
- **Shell escaping.** Use `gh(args=[...])` for args with spaces/quotes.
- **Comment bodies.** Use temp file + `--body-file` for multi-line markdown.
- **Dynamic PR→issue matching.** PR body dice "Fixes #N" — check body, not just title.

---

## 9. Quality Scorecard & Post-Merge Checklist

### Evaluar PR de Jules

| Dimensión | Peso | Check |
|-----------|------|-------|
| Cobertura funcional | 30% | ¿Implementa todas las estrategias/pasos? |
| Tests | 25% | ¿Incluye tests? ¿Pasan? |
| Compilación | 15% | ¿Compila al mergear? |
| No regresiones | 15% | ¿No borra métodos usados? |
| Estilo/Calidad | 10% | ¿Código limpio? |
| Documentación | 5% | ¿Actualiza docs? |

### Post-Merge Checklist

```bash
# 1. Compila?
cargo check --workspace

# 2. Tests pasan?
cargo test --workspace 2>&1 | tail -10

# 3. Clippy limpio?
cargo clippy --all-targets -- -D warnings 2>&1 | tail -10

# 4. Funcionalidad eliminada? Jules puede borrar métodos usados
grep -rn "fn find_by_lang\|fn clear_by_file\|fn contains_call" code-graph/src/
```

### Errores Comunes de Jules

| Error | Síntoma | Fix |
|-------|---------|-----|
| Import duplicado | `error[E0252]` | Eliminar línea duplicada |
| Método faltante en DB | `error[E0599]` | Implementar en CodeGraphDB |
| Type mismatch | `error[E0308]` | Unificar tipos |
| Eliminación de método usado | Tests fallan | Restaurar método |
| API renamed by parallel PR | `error[E0425]` | Actualizar caller a nueva API |
| Stub sin implementar | `fn by_language() -> Ok(vec![])` | Conectar a DB real |
| Cargo.lock corrupto | `TOML parse error` | `rm Cargo.lock && cargo generate-lockfile` |

---

## 10. Verificación de Merge (Protocolo Obligatorio)

**NUNCA asumir que un PR de Jules está mergeado.** Siempre verificar:

```bash
gh pr view <N> --repo iberi22/xavier --json state,mergeable,isDraft

# state = "MERGED" → mergeado ✅
# state = "OPEN" + isDraft = true → Draft, no mergear
# state = "OPEN" + isDraft = false → ready, check mergeable

# Verificar commits en main
git log --oneline main | head -5
```

**Lección aprendida (Julio 2026):** Confundir "commits en la branch" con "PR mergeado a main" engaña al usuario. Siempre verificar con `gh pr view` antes de reportar.

---

## 11. Troubleshooting

### Session stuck ("Awaiting User F")

1. Revisar: `jules remote pull --session <ID>`
2. Extraer trabajo parcial del output
3. Eliminar sesión desde app.jules.ai
4. Relanzar con mejor contexto

### Jules no responde al issue

```bash
gh issue edit <N> --remove-label jules
sleep 5
gh issue edit <N> --add-label jules
```

### Jules falló con error

- Revisar comentarios del issue
- Ajustar descripción (más específica)
- Forzar re-trigger o crear issue nuevo

### PR con 0 adiciones

Jules puede abrir PRs con 0 additions/0 deletions (empty commit):

```bash
gh pr view <N> --json additions,deletions
# Si ambos son 0 → no-op. Cerrar y re-trigger con issue más específico.
```

---

## 12. Jules + Gestalt Swarm — Combined Workflow

**Jules** = async coding (refactors, features, PRs).  
**Gestalt Swarm** = fast parallel CLI (scans, analysis, bulk ops).

```
User → Swarm (fast analysis) → Jules (implement fixes) → PR → Merge
```

### When to Use Each

| Task | Use |
|------|-----|
| Large refactors, new features | Jules (`jules new --repo iberi22/...`) |
| Bug finding, security audit | Gestalt Swarm (`swarm_bridge.py`) |
| Quick status checks | Gestalt Swarm only |
| Deep coding, PR review | Jules only |

---

## 13. Proyectos SWAL Activos

| Project | Repo | Status |
|---------|------|--------|
| Xavier | iberi22/xavier | ✅ Active (Ola 5 EPIC) |
| OrionHealth | iberi22/OrionHealth | ✅ Active |
| Cortex | iberi22/cortex-1 | ✅ Active |
| Synapse Protocol | iberi22/synapse-protocol | ✅ Active |
| WorldExams | iberi22/worldexams | ✅ Active |

> ⚠️ Jules ONLY works in `iberi22/*` repos.

---

*Last updated: 2026-07-20*
*Jules = Google's autonomous AI coding agent*
*Gestalt Swarm = SWAL's parallel execution bridge*
*Anti-Conflict Protocol v1 + Wave Orchestration v4*
