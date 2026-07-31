# Reglas para recetas con Qwen Code

Guía práctica para escribir recetas orientadas a Qwen/QwenCoder con la plantilla unificada.

## Parámetros clave de receta

- **provider**: `qwen`
- **model**: modelo Qwen Code apropiado (ej. `Qwen2.5-Coder` o variantes disponibles en tu entorno)
- **tool_mode**: `auto | required | none`
  - `auto`: Qwen decide cuándo invocar herramientas.
  - `required`: fuerza uso de herramientas si están declaradas.
  - `none`: desactiva herramientas (sólo chat/generación).
- **tool_aliases**: mapea nombres canónicos → nombres nativos Qwen.
- **temperature** (recomendado): 0.0–0.2 para codegen/tool-calling estricto.
- **tools**: lista de herramientas canónicas permitidas por la receta.

## Mapeo de herramientas (canónico → Qwen)

Usa estos alias en `tool_aliases` cuando el nombre canónico difiera del nativo:

- `fs.list` → `list_directory`
- `fs.read` → `read_file`
- `fs.write` → `write_file`
- `fs.find` → `glob`
- `fs.search` → `search_file_content`
- `fs.replace` → `replace`
- `shell.run` → `run_shell_command`
- `web.fetch` → `web_fetch`
- `web.search` → `web_search`
- `fs.read_many` → `read_many_files`
- `memory.save` → `save_memory`

Fuentes oficiales en `docs/qwen-tools.md`.

## Snippet de encabezado YAML (ejemplo)

```yaml
---
# Receta base para Qwen Code
provider: qwen
model: Qwen2.5-Coder
bench_id: sample-task
# Permite a Qwen decidir cuándo llamar herramientas
tool_mode: auto
# Mapeo canónico → Qwen nativo
tool_aliases:
  fs.list: list_directory@qwen
  fs.read: read_file@qwen
  fs.write: write_file@qwen
  fs.find: glob@qwen
  fs.search: search_file_content@qwen
  fs.replace: replace@qwen
  shell.run: run_shell_command@qwen
  web.fetch: web_fetch@qwen
  web.search: web_search@qwen
  fs.read_many: read_many_files@qwen
  memory.save: save_memory@qwen
# Habilita sólo las herramientas necesarias
tools:
  - fs.list
  - fs.read
  - fs.search
  - fs.replace
  - web.fetch
# Control de creatividad/adhesión a esquema
temperature: 0.2
prompt_variants: [base]
constraints:
  - confirm_before_write: true
  - disable_shell: true  # habilitar sólo si hace falta
---
```

## Reglas operativas

- **Confirmaciones**: `write_file`, `replace`, `run_shell_command` y `web_fetch` requieren confirmación previa.
- **Shell**: mantener deshabilitado por defecto; definir lista de comandos permitidos si se activa.
- **Web Search**: configura `TAVILY_API_KEY` o la herramienta no se registrará.
- **Contexto y límites**: usar `maxResults` en `search_file_content` y limitar lecturas largas (`offset`/`limit` en `read_file`).
- **Temperaturas**: seguir `docs/temperature.md` (0.0–0.2 para ejecución precisa, 0.6–0.8 para ideación).

## Ejecución con bench-run

Ejemplo:

```bash
python scripts/bench-run.py --provider qwen --recipes recipes/ --bench bench/sample-task
```

Ajusta `--model`, `--temperature` y filtros de casos según sea necesario.
