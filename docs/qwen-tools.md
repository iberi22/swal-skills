# Qwen Code – Herramientas nativas (tool calling)

Este documento resume las herramientas nativas expuestas por Qwen Code y cómo mapearlas en nuestras recetas unificadas.

## Inventario de herramientas

- **File System**
  - `list_directory` (ReadFolder)
    - Lista archivos/subdirectorios de un path.
    - Args: `path` (req), `ignore?[]`, `respect_git_ignore?` (por defecto true).
  - `read_file` (ReadFile)
    - Lee un archivo (texto, imágenes, PDF; soporta `offset`/`limit` en texto).
    - Args: `path` (req), `offset?`, `limit?`.
  - `write_file` (WriteFile)
    - Escribe/crea un archivo. Requiere confirmación.
    - Args: `file_path` (req), `content` (req).
  - `glob` (FindFiles)
    - Busca archivos por patrón.
    - Args: `pattern` (req), `path?`, `case_sensitive?`, `respect_git_ignore?`.
  - `search_file_content` (SearchText)
    - Grep por regex en archivos con filtro de glob.
    - Args: `pattern` (req), `path?`, `include?`, `maxResults?`.
  - `replace` (Edit)
    - Reemplazo preciso en archivo. Requiere confirmación. Usa contexto amplio en `old_string`.
    - Args: `file_path` (req), `old_string` (req), `new_string` (req), `expected_replacements?`.

- **Shell**
  - `run_shell_command`
    - Ejecuta comandos de shell controlados. Requiere confirmación y respeta restricciones.
    - Args clave: `command` (req). Sugerido: restringir/deshabilitar comandos destructivos.

- **Web**
  - `web_fetch`
    - Descarga y procesa 1 URL con un prompt (convierte HTML→Markdown). Requiere confirmación.
    - Args: `url` (req), `prompt` (req).
  - `web_search`
    - Búsqueda web vía Tavily. Requiere `TAVILY_API_KEY` configurada.
    - Args: `query` (req).

- **Lectura múltiple**
  - `read_many_files`
    - Lee varios archivos y devuelve contenido agregado.

- **Memoria**
  - `save_memory`
    - Persiste un hecho en `~/.qwen/QWEN.md` para sesiones futuras.
    - Args: `fact` (req).

Referencias oficiales:

- Qwen Code Tools – índice: [docs/tools/index.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/index.md)
- File System: [docs/tools/file-system.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/file-system.md)
- Shell: [docs/tools/shell.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/shell.md)
- Web Fetch: [docs/tools/web-fetch.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/web-fetch.md)
- Web Search: [docs/tools/web-search.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/web-search.md)
- Multi File: [docs/tools/multi-file.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/multi-file.md)
- Memory: [docs/tools/memory.md](https://github.com/QwenLM/qwen-code/blob/main/docs/tools/memory.md)

## Mapeo sugerido (receta unificada → Qwen)

Usa nombres canónicos en la receta y mapea a nombres nativos de Qwen con `tool_aliases` cuando difieran.

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

## Notas de uso

- Confirmaciones: `write_file`, `replace`, `run_shell_command` y `web_fetch` solicitan confirmación antes de ejecutar cambios/descargas.
- Seguridad shell: define una política de comandos permitidos y evita operaciones destructivas (`rm -rf`, `mkfs`, etc.).
- Web Search: configura `TAVILY_API_KEY` (env/archivo settings/CLI) o la herramienta no se registrará.
- Límites: ajusta `maxResults` en `search_file_content` para evitar desbordes de contexto.
