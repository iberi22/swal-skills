# HEARTBEAT.md — Checklist de Health para Agentes

> Lista periódica de verificaciones. Ejecutar cada vez que un agente inicie una sesión de trabajo en swal-skills, o como parte de un cron de mantenimiento.

---

## 📋 Checklist Principal

### 1. Estado de Skills (cada sesión)

- [ ] **Contar directorios físicos**: `find skills/ -maxdepth 1 -type d | wc -l` → debe ser **24**.
- [ ] **Contar SKILL.md**: `find skills/ -name 'SKILL.md' | wc -l` → debe ser **25** (incluye `skills/SKILL.md` raíz).
- [ ] **Validar que cada directorio de skill tenga SKILL.md**: Ningún directorio vacío.
- [ ] **Verificar skills versionadas**: `nextjs` debe declarar `version: 1.1.0`; `rust` debe declarar `version: 1.0.1`.
- [ ] **Detectar skills sin versión**: `grep -L "version:" skills/*/SKILL.md` → idealmente vacío.
- [ ] **Revisar skills privadas**: Asegurar que **no** tengan `raw_url` en `manifest.yaml`.
- [ ] **Revisar skills públicas**: Asegurar que **sí** tengan `raw_url` válido.

### 2. Estado del _registry (diario)

- [ ] **Sintaxis de manifest.yaml**: `python -c "import yaml; yaml.safe_load(open('_registry/manifest.yaml'))"` → sin excepción.
- [ ] **IDs únicos**: No debe haber skills con `id` duplicado en `manifest.yaml`.
- [ ] **Sincronía manifest ↔ filesystem**: Cada `id` en manifest debe tener directorio físico (salvo skills declaradas como externas como `gestalt-swarm`).
- [ ] **Dependencias resolubles**: Para cada skill con `dependencies`, verificar que los IDs existan en el mismo manifest.
- [ ] **Tool aliases completos**: Confirmar que `universal` cubre `fs.read`, `fs.write`, `fs.replace`, `fs.search`, `fs.glob`, `shell.run`, `web.fetch`.
- [ ] **skill-provider.js funcional**: `node _registry/skill-provider.js list` → debe listar 27 skills sin crash.
- [ ] **skill-provider.js recipes**: `node _registry/skill-provider.js recipes` → debe listar 39 recetas sin crash.

### 3. Health de POML Recipes (semanal)

- [ ] **Contar recetas**: `find poml/ -name '*.poml' | wc -l` → debe ser **39**.
- [ ] **Validar headers POML**: `python scripts/check_poml_headers.py` → sin errores.
- [ ] **Schema compliance**: Cada receta debe tener `topology`, `roles`, `tools`, `bench_id` (según `schema/recipe.schema.yaml`).
- [ ] **Modelos vivos**: Verificar que los modelos declarados (`gpt-5`, `gemini-2.5-pro`, `Qwen2.5-Coder`) siguen siendo válidos en sus respectivos providers.
- [ ] **Raw URLs de recetas**: Verificar que `raw_url` en manifest para recipes apuntan a rutas que existen en `main`.
- [ ] **Sin recetas huérfanas**: Toda receta en `poml/` debe estar listada en `manifest.yaml` bajo `recipes:`.
- [ ] **Topología diversa**: Alertar si 100% de recetas son `solo`. Meta: al menos 3 recetas `multi` o `rag`.

### 4. Calidad de Contenido (mensual)

- [ ] **Skills sin front matter roto**: `grep -l "^---$" skills/*/SKILL.md` → todas las skills deberían tener YAML front matter válido.
- [ ] **Recetas sin contenido vacío**: `find poml/ -name '*.poml' -size -500c` → detectar stubs vacíos.
- [ ] **Dead links en docs**: Revisar que `docs/architecture/*.md` no referencien archivos inexistentes.
- [ ] **Eliminar archivos residuales**: Revisar `test-markdownlint.md`, `studio-producer-original.md`, y otros archivos con sufijos `-original`, `-test`, `-backup`.
- [ ] **Revisar `.env.example`**: Asegurar que refleje las variables reales usadas por skills (hoy es genérico y poco útil).

### 5. Benchmarks & Rendimiento (por sprint)

- [ ] **Estructura de bench intacta**: `bench/ai-engineer/` debe tener `cases/`, `metrics/`, `results/`.
- [ ] **Ejecutar bench de muestra**: `python scripts/bench-run.py --recipe ai-engineer --sample` → sin crash.
- [ ] **Agregar métricas**: `python scripts/bench-aggregate.py` → debe generar reporte legible.
- [ ] **Comparar con baseline**: Alertar si alguna receta baja más de 10% en score vs última ejecución.

### 6. Seguridad & Privacidad (cada sesión)

- [ ] **Sin secrets en skills públicas**: `grep -ri "api_key\|token\|password" skills/*/` → solo en skills privadas.
- [ ] **Sin `.env` trackeado**: `git ls-files | grep -E '\.env$'` → vacío.
- [ ] **Skills privadas no accesibles vía raw_url**: Confirmar que intentar `curl` de una `raw_url` privada devuelve 404 (o null).
- [ ] **Permisos de archivos**: `find skills/ -type f -perm /o+w` → vacío en producción.

---

## 📋 Checklist Rápida (30 segundos)

Para agentes que solo van a hacer una tarea puntual:

```bash
cd ~/projects/swal-skills

# 1. Skills OK?
[[ $(find skills/ -maxdepth 1 -type d | wc -l) -eq 24 ]] && echo "✅ Skills dirs" || echo "❌ Skills dirs"

# 2. Recipes OK?
[[ $(find poml/ -name '*.poml' | wc -l) -eq 39 ]] && echo "✅ Recipes" || echo "❌ Recipes"

# 3. Registry OK?
node _registry/skill-provider.js list > /dev/null 2>&1 && echo "✅ Registry" || echo "❌ Registry"

# 4. Manifest parsea?
python3 -c "import yaml; yaml.safe_load(open('_registry/manifest.yaml')); print('✅ Manifest')" 2>/dev/null || echo "❌ Manifest"
```

---

## 🚨 Acciones Correctivas por Alerta

| Alerta | Acción |
|--------|--------|
| Manifest no parsea | Detener todo. Corregir YAML antes de cualquier otro cambio. |
| Skill pública sin `raw_url` | Añadir `raw_url` apuntando a `raw.githubusercontent.com/iberi22/swal-skills/main/skills/<id>/SKILL.md`. |
| Skill privada con `raw_url` | Eliminar `raw_url` o cambiar visibilidad a `public` si es intencional. |
| Directorio skill sin SKILL.md | Crear SKILL.md mínimo o eliminar directorio y limpiar manifest. |
| Receta POML sin `bench_id` | Añadir `bench_id` o marcar como `draft` en manifest. |
| Dependencia no resuelta | Crear skill faltante o eliminar dependencia del manifest. |
| Modelo obsoleto en receta | Actualizar a modelo vigente del provider; documentar en changelog. |
| Bench rompe | Revisar `scripts/adapters/` — probablemente el adaptador del provider está desactualizado. |

---

## ⏰ Frecuencia Recomendada

| Verificación | Frecuencia | Responsable |
|--------------|------------|-------------|
| Checklist rápida | Cada sesión de agente | Agente activo |
| Registry + manifest | Diaria | Mantenedor / CI |
| Health POML recipes | Semanal | Mantenedor |
| Calidad de contenido | Mensual | Mantenedor |
| Benchmarks completos | Por sprint | Equipo de evaluación |
| Seguridad + secrets | Cada push | CI / git hooks |

---

*Última actualización: 2026-05-11. Ejecutar y marcar checkboxes antes de cada modificación significativa.*
