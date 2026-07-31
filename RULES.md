# RULES.md — SWAL Skills

> *"La disciplina es la diferencia entre un skill que funciona y uno que confunde a un agente a las 3 AM."*

---

## 1. Naming Conventions

### Skills
- **kebab-case obligatorio.** `deploy-anywhere`, `web-research`, `skill-launcher`.
- **No uses camelCase, snake_case ni PascalCase** para nombres de directorio.
- El nombre del directorio debe coincidir con el campo `name` (o `slug`) del frontmatter.
- Evita nombres genéricos. `frontend` es malo; `frontend-agent` o `frontend-doctor` son buenos.

### POML Recipes
- **kebab-case también aquí.** `ai-engineer.poml`, `test-writer-fixer.poml`.
- El nombre del archivo debe coincidir con el `bench_id` interno.
- Organízalo por departamento: `poml/<departamento>/<nombre>.poml`.

### Archivos auxiliares
- `SKILL.md` — siempre en mayúsculas. Es el contrato.
- `setup.md`, `memory-template.md`, `routing.md` — kebab-case, minúsculas.
- `_meta.json` — con guion bajo inicial solo para metadatos del skill.

---

## 2. Frontmatter Requerido (SKILL.md)

Todo `SKILL.md` debe comenzar con un bloque YAML entre `---`. Campos obligatorios:

```yaml
---
name: deploy-anywhere
description: "Deploy applications to any hosting platform..."
license: MIT
metadata:
  author: swal
  version: "1.0.0"
---
```

### Campos obligatorios

| Campo | Tipo | Reglas |
|-------|------|--------|
| `name` | string | kebab-case. Coincide con el nombre del directorio. |
| `description` | string | Una sola línea. Incluye triggers de uso ("Use when..."). |
| `metadata.version` | string | SemVer obligatorio. `"1.0.0"`, no `"1.0"`. |

### Campos recomendados

| Campo | Cuándo usarlo |
|-------|---------------|
| `slug` | Si el `name` visible difiere del directorio (ej: `name: NextJS`, `slug: nextjs`). |
| `license` | Siempre. MIT por defecto en este repo. |
| `metadata.author` | Siempre `"swal"` a menos que sea contribución externa documentada. |
| `metadata.openclaw` | Si necesitas configuración específica para OpenClaw (emoji, autoLoad, forSubagents). |

### Ejemplos válidos

```yaml
---
name: web-research
description: Use for all web research tasks - market research, competitor analysis...
license: MIT
metadata:
  author: swal
  version: "1.0.0"
  {
    "openclaw": { "emoji": "🔍", "requires": {} }
  }
---
```

```yaml
---
name: skill-launcher
description: Automatically inject skill context into subagent spawning...
license: MIT
metadata:
  author: swal
  version: "1.0.0"
  openclaw:
    autoLoad: true
    forSubagents: true
---
```

### Errores comunes a evitar
- ❌ `metadata: {"clawdbot":...}` como string JSON en una línea (a menos que sea intencional para compatibilidad).
- ❌ Omitir `version` o poner `"1.0"` en lugar de `"1.0.0"`.
- ❌ `name` con espacios o mayúsculas: `name: Deploy Anywhere`.

---

## 3. Estructura SKILL.md

Un skill bien formado sigue esta anatomía:

```markdown
---
# Frontmatter obligatorio
---

# Título del Skill (H1)

## When to Use / Cuándo Usar
- Lista de triggers que activan este skill.
- Frases que el usuario diría. Ej: "Deploy my app", "Set up a blog".

## Prerequisites / Prerrequisitos
- Lo que el agente necesita saber o tener antes de ejecutar.

## Quick Start / Inicio Rápido
- Comandos copiar-pegar.
- Configuraciones mínimas viables.

## Core Rules / Reglas Principales
- Las 3-5 reglas de oro. Lo que NUNCA debe hacerse mal.

## Sectiones específicas del dominio
- Tablas de referencia rápida.
- Snippets de código.
- Decision trees ("If X then Y").

## Examples / Ejemplos
- Input del usuario → Output esperado del agente.
```

### Reglas de formato
- Usa **tablas** para comparaciones rápidas (plataformas, opciones, versiones).
- Usa **bloques de código** con lenguaje especificado (`bash`, `javascript`, `yaml`).
- Mantén las líneas de descripción por debajo de 120 caracteres cuando sea posible.
- El `SKILL.md` raíz (`skills/SKILL.md`) es el **skill genérico de GitHub CLI** — no lo confundas con un índice.

---

## 4. Formato POML

Las recetas POML son **especificaciones de agente**, no prompts largos. Estructura obligatoria:

```xml
<poml>
  <let name="topology">solo|multi|rag|tools-first</let>
  <let name="bench_id">nombre-receta</let>
  <let name="tool_mode">auto|required|none</let>
  <let name="providers">
    {
      "openai": { "model": "gpt-5", "temperature": 0.2 },
      "gemini": { "model": "gemini-2.5-pro", "temperature": 0.2 },
      "qwen":   { "model": "Qwen2.5-Coder", "temperature": 0.1 }
    }
  </let>
  <let name="tools">["fs.read", "fs.write", "shell.run"]</let>
  <let name="tool_aliases">
    {
      "fs.read@qwen": "read_file",
      "fs.write@qwen": "write_file",
      "shell.run@qwen": "run_shell_command"
    }
  </let>

  <stylesheet>
    verbosity: concise|detailed
    bullets: true|false
    tone: expert, pragmatic|creative, playful|...
  </stylesheet>

  <role>
    # Rol del agente
    ## Description
    ## Core Responsibilities
    ## Expertise Areas
  </role>

  <task>
    # Instrucciones de ejecución
    # Pasos numerados
    # Referencias a papers o frameworks cuando aplique
  </task>

  <output-format>
    - Bullets obligatorios del formato de salida
  </output-format>

  <example>
    <commentary>Razonamiento interno</commentary>
    User: "..."
    Assistant: "..."
  </example>
</poml>
```

### Reglas POML
- `topology` debe ser uno de: `solo`, `multi`, `rag`, `tools-first`.
- `roles` es obligatorio cuando `topology` no es `solo`.
- `tools` es un array JSON de strings.
- `tool_aliases` debe mapear cada herramienta a los nombres específicos de cada proveedor.
- El `<role>` debe incluir **Description**, **Core Responsibilities** y **Expertise Areas**.
- El `<task>` debe seguir el patrón **Plan → Act → Verify**.
- El `<output-format>` obliga consistencia entre proveedores.

### Validación
El schema en `schema/recipe.schema.yaml` valida el header semántico. Asegúrate de que tu POML sea parseable como XML y que los bloques JSON dentro de `<let>` estén bien formados.

---

## 5. Reglas del Registro

Si creas o modificas un skill:

1. **Actualiza `_registry/manifest.yaml`.** Añade o edita la entrada del skill.
2. **Asegúrate de que estos campos del manifest estén completos:**
   - `id` (coincide con directorio)
   - `name`, `description`
   - `visibility`: `public` o `private`
   - `path`: `skills/<id>/SKILL.md`
   - `raw_url`: URL completa de raw GitHub
   - `tags`: array de 2-6 tags relevantes
   - `agents`: array de agentes soportados
3. **Si es una receta POML, verifica que `skill-provider.js` la liste** con el comando `recipes`.

---

## 6. GitCore Protocol v3.6.0

Todo skill en este repo debe declarar compatibilidad:

```yaml
meta:
  gitcore_protocol: "3.6.0"
```

Esto habilita:
- Cross-repo skill loading via raw URLs.
- Versionado consistente entre proyectos SWAL (Cortex, ManteniApp, GOS, gestalt-rust, worldexams).
- Interoperabilidad universal entre agentes.

---

*Protocolo GitCore v3.6.0 — SWAL (SouthWest AI Labs)*
