# TOOLS.md — SWAL Skills

> *"Conoce tu taller antes de levantar el martillo."*

---

## Estructura del Proyecto

```
swal-skills/
├── skills/                   # 25 skills (SKILL.md + recursos)
│   ├── astro/
│   ├── nextjs/
│   ├── tailwindcss/
│   ├── deploy-anywhere/
│   ├── web-research/
│   ├── skill-launcher/
│   └── ... (y 18 más)
├── poml/                    # 39 recetas ejecutables por departamento
│   ├── engineering/
│   ├── marketing/
│   ├── design/
│   ├── product/
│   ├── project-management/
│   ├── studio-operations/
│   ├── testing/
│   └── bonus/
├── _registry/               # Catálogo central + CLI
│   ├── manifest.yaml          # Fuente de verdad de todos los skills
│   └── skill-provider.js      # CLI para listar, buscar y obtener skills
├── schema/                  # Validación
│   └── recipe.schema.yaml     # JSON Schema para headers de recetas POML
├── docs/                    # Documentación de arquitectura
├── bench/                   # Benchmarks y evaluaciones
├── scripts/                 # Utilidades de build y deploy
└── memory/                  # Templates de memoria para agentes
```

---

## Comandos Útiles

### Explorar Skills

```bash
# Listar todos los directorios de skills
ls skills/

# Contar skills reales (excluye _meta.json y SKILL.md raíz)
ls skills/ | grep -v '^_' | grep -v '^SKILL.md$' | wc -l

# Ver la estructura interna de un skill
tree skills/astro

# Buscar un skill por nombre
ls skills/ | grep -i "deploy"
```

### Leer un SKILL.md

```bash
# Leer localmente
cat skills/astro/SKILL.md

# Leer vía raw GitHub (cualquier agente puede hacer esto)
curl -s https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/astro/SKILL.md | head -50

# Leer vía skill provider
node _registry/skill-provider.js get astro
```

### Explorar Recetas POML

```bash
# Listar todos los departamentos con recetas
ls poml/

# Contar recetas totales
find poml/ -name "*.poml" | wc -l

# Listar recetas de engineering
ls poml/engineering/

# Ver una receta específica
cat poml/engineering/ai-engineer.poml

# Buscar recetas por nombre
find poml/ -name "*test*.poml"
```

### Usar el Skill Provider

```bash
# Listar skills públicos
node _registry/skill-provider.js list --public

# Listar skills privados
node _registry/skill-provider.js list --private

# Buscar skills por tag o nombre
node _registry/skill-provider.js search tailwind
node _registry/skill-provider.js search deploy

# Obtener contenido de un skill
node _registry/skill-provider.js get nextjs

# Listar todas las recetas POML
node _registry/skill-provider.js recipes

# Obtener una receta específica
node _registry/skill-provider.js recipe ai-engineer
```

### Validar POML

```bash
# Verificar que una receta tenga el header requerido (topology, roles, tools, bench_id)
# Nota: recipe.schema.yaml valida el header YAML/JSON, no la sintaxis XML POML completa.

# Validar sintaxis básica de XML/grep de estructura
grep -E "^\\s*<(poml|let|role|task|output-format|example|stylesheet)>" poml/engineering/ai-engineer.poml

# Validar que todos los .poml tengan <poml> de apertura y cierre
for f in $(find poml/ -name "*.poml"); do
  if ! grep -q "^</poml>$" "$f"; then
    echo "Falta cierre </poml>: $f"
  fi
done
```

### Validar Manifest

```bash
# Verificar que manifest.yaml sea YAML válido
node -e "const yaml=require('fs').readFileSync('_registry/manifest.yaml','utf8'); console.log(yaml.includes('skills:') && yaml.includes('meta:') ? 'OK' : 'Faltan secciones clave')"

# Contar skills declarados en el manifest
grep -c "^\\s*- id:" _registry/manifest.yaml

# Buscar un skill en el manifest
grep -A 10 "id: astro" _registry/manifest.yaml
```

### Sincronización y Cache

```bash
# El skill-provider usa un directorio de cache local
ls _registry/.skill-cache/ 2>/dev/null || echo "Cache vacía o inexistente"

# Forzar resincronización (si tienes acceso a clawd)
node _registry/skill-provider.js sync
```

---

## Convenciones de Paths

| Contexto | Path válido |
|----------|-------------|
| Local repo | `skills/astro/SKILL.md` |
| Raw GitHub | `https://raw.githubusercontent.com/iberi22/swal-skills/main/skills/astro/SKILL.md` |
| Skill Provider | `node _registry/skill-provider.js get astro` |
| OpenClaw local | `C:\Users\belal\clawd\skills\astro\SKILL.md` |

---

*Protocolo GitCore v3.6.0 — SWAL (SouthWest AI Labs)*
