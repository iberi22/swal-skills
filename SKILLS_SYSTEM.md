# SWAL Dynamic Skills System

> Sistema de skills dinámicos para todos los coding agents de SWAL.

## Overview

Este sistema permite que **OpenClaw, Codex, Claude Code, Qwen, OpenCode** y cualquier otro agente acceda a skills compartidos desde un único repositorio (`iberi22/agents-flows-recipes`).

## Arquitectura

```
iberi22/agents-flows-recipes/
├── _registry/
│   ├── manifest.yaml      # Catálogo central de todos los skills
│   └── skill-provider.js  # CLI para cargar skills dinámicamente
├── skills/                # Skills source (junctions a clawd skills)
│   ├── astro/
│   ├── nextjs/
│   ├── tailwindcss/
│   └── ... (14+ skills)
└── poml/                  # POML recipes (ejecutables)
    ├── engineering/
    ├── marketing/
    └── ...
```

## Cómo Funciona

### 1. Skill Provider (Dynamic Loading)

```bash
# Listar skills públicos
node _registry/skill-provider.js list --public

# Listar skills privados
node _registry/skill-provider.js list --private

# Listar todos los POML recipes
node _registry/skill-provider.js recipes

# Buscar skills
node _registry/skill-provider.js search tailwind

# Obtener contenido de un skill
node _registry/skill-provider.js get astro

# Obtener un POML recipe
node _registry/skill-provider.js recipe ai-engineer
```

### 2. Raw GitHub URLs (Para Agentes que Pueden Fetchear URLs)

Los skills están disponibles via raw GitHub:

```
https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/astro/SKILL.md
https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/nextjs/SKILL.md
https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/tailwindcss/SKILL.md
...
```

### 3. Symlinks Locales

Los skills también están disponibles via symlinks/junctions:

```
C:\Users\belal\clawd\skills\          # Skills globales (50+)
E:\scripts-python\skills\clawd\        # Junction → clawd\skills
E:\scripts-python\agents-flows-recipes\skills\  # Skills para este repo
```

## Skills Disponibles

### Coding Frameworks (PÚBLICOS)
| Skill | Descripción | Agentes |
|-------|-------------|---------|
| astro | Astro framework + Cloudflare | Todos |
| nextjs | Next.js 15 App Router | Todos |
| tailwindcss | Tailwind CSS patterns | Todos |
| vite | Vite build tool | Todos |
| react | React patterns | Todos |
| rust | Rust patterns | Codex, Claude, Qwen |
| python | Python best practices | Todos |

### Herramientas (PÚBLICAS)
| Skill | Descripción |
|-------|-------------|
| github | GitHub CLI (gh) |
| web-research | Tavily + Brave search |
| gemini | Gemini CLI |
| codex | Codex CLI |
| qwen | Qwen Coder CLI |

### Agentes SWAL (PRIVADOS)
| Skill | Descripción |
|-------|-------------|
| sales-pro | RFIs, proposals, cotizaciones |
| src-generator | SRC documents (IEEE 830) |
| frontend-agent | Desarrollo frontend completo |
| frontend-doctor | Debug UI con DevTools |

### POML Recipes (EJECUTABLES)
| Recipe | Departamento | Descripción |
|--------|-------------|-------------|
| ai-engineer | engineering | AI Engineer |
| frontend-developer | engineering | Frontend Developer |
| backend-architect | engineering | Backend Architect |
| test-writer-fixer | engineering | Testing automatizado |
| content-creator | marketing | Marketing content |
| growth-hacker | marketing | Growth strategies |
| studio-coach | bonus | Coach de agentes |

## Integración por Agente

### OpenClaw
```bash
# Usar skill-provider
node "E:\scripts-python\agents-flows-recipes\_registry\skill-provider.js" get <skill-id>

# O acceder directamente
Read: C:\Users\belal\clawd\skills\<skill-id>\SKILL.md
```

### Codex
```bash
# Ya configurado en C:\Users\belal\.codex\config.toml
# Skills apuntan a E:\scripts-python\skills\clawd\<skill>\SKILL.md
```

### Claude Code
```bash
# Puede leer skills via raw URLs
curl https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/astro/SKILL.md
```

### Qwen / OpenCode
```bash
# Similar a Claude Code - usar raw URLs
```

## Para Nuevo Desarrollador

1. **Este repo es la fuente de verdad** para skills
2. **Usa el skill-provider** para listar/buscar skills
3. **Los skills se cargan dinámicamente** — no necesitas instalarlos todos
4. **Para contribuir**: añade skills al manifest.yaml y haz PR

## Manifesto (manifest.yaml)

```yaml
skills:
  - id: astro
    name: "Astro Framework"
    visibility: public
    repo: iberi22/agents-flows-recipes
    path: skills/astro/SKILL.md
    raw_url: https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/skills/astro/SKILL.md
    agents: [openclaw, codex, claude, qwen, opencode]
    tags: [astro, svelte, cloudflare]
```

## Comandos Útiles

```bash
# Ver todos los skills públicos
node _registry/skill-provider.js list --public

# Ver todos los POML recipes
node _registry/skill-provider.js recipes

# Buscar por tecnología
node _registry/skill-provider.js search react

# Obtener skill para leer
node _registry/skill-provider.js get nextjs

# Sincronizar todos los skills (requiere acceso a clawd)
node _registry/skill-provider.js sync
```

## Roadmap

- [x] Sistema de manifest con skill provider
- [x] Symlinks para todos los agents
- [x] Raw URLs para acceso público
- [ ] Subir cambios a GitHub (iberi22/agents-flows-recipes)
- [ ] Configurar Windsurf/OpenCode skills
- [ ] MCP server para recipes (ejecutar POML via agent)
- [ ] Sistema de versionado de skills
- [ ] Métricas de uso por skill

## Notas

- **PRIVADO**: Los skills `sales-pro`, `src-generator` son internos de SWAL
- **PÚBLICO**: Los skills de frameworks (astro, nextjs, etc.) son públicos
- **Junctions**: Los symlinks junctions no funcionan sobre VPN — usar raw URLs en ese caso
- **Raw URLs**: Cualquier agente puede acceder skills via `https://raw.githubusercontent.com/iberi22/agents-flows-recipes/main/...`

---

*Última actualización: 2026-03-31*
