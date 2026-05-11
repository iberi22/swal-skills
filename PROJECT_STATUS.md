# PROJECT_STATUS.md — SWAL Skills

> Estado funcional del proyecto al último commit. Actualizar tras cada cambio significativo.

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Skills físicas (directorios) | 24 |
| Skills registradas en manifest | 27 |
| Skills públicas | 12 |
| Skills privadas | 15 |
| Recetas POML | 39 |
| Versiones de skills con semver | 2 |
| Departamentos POML | 8 |
| Protocolo GitCore | 3.6.0 |

---

## Skills — Estado por Directorio

### Frameworks & Lenguajes (Públicas)

| Skill | Versión | Estado | Notas |
|-------|---------|--------|-------|
| `astro` | — | ✅ Estable | Cloudflare Pages, i18n. Sin versión semver. |
| `nextjs` | **1.1.0** | ✅ Estable | App Router, caching, auth. Versión en front matter. |
| `tailwindcss` | — | ✅ Estable | Responsive + dark mode. Sin versión semver. |
| `vite` | — | ✅ Estable | Build + HMR. Sin versión semver. |
| `rust` | **1.0.1** | ✅ Estable | Systems programming. Versión en front matter. |
| `python` | — | ✅ Estable | Best practices. Sin versión semver. |

### DevOps & Herramientas (Públicas)

| Skill | Estado | Notas |
|-------|--------|-------|
| `deploy-anywhere` | ✅ Estable | Multi-hosting: Cloudflare, Vercel, Railway, Fly.io, Netlify. |
| `web-design-guidelines` | ✅ Estable | 100+ reglas de audit a11y/UI. |
| `frontend-agent` | ✅ Estable | React/Vue/Angular. Depende de react + tailwindcss. |
| `frontend-doctor` | ✅ Estable | Debug UI con Web MCP + Chrome DevTools. Depende de playwright. |
| `web-research` | ✅ Estable | Tavily, Brave Search, scraping. |

### Integraciones CLI (Privadas)

| Skill | Estado | Notas |
|-------|--------|-------|
| `github` | ✅ Estable | gh CLI + SWAL methodology. Privada. |
| `gemini` | ✅ Estable | Gemini CLI, summarization. Privada. |
| `codex` | ✅ Estable | Codex CLI, code review. Privada. |
| `qwen` | ✅ Estable | Qwen Coder CLI. Privada. |
| `minimax-tools` | ✅ Estable | MCP web_search + understand_image + Groq Whisper. Privada. |
| `coding-agent` | ✅ Estable | Delega a Codex/Claude/OpenCode/Pi + DeepSeek V4 Pro + MiniMax-M2.7. Privada. |
| `skill-launcher` | ✅ Estable | Inyección de contexto en subagentes. Privada. |
| `jules` | ✅ Estable | Jules autonomous coding (Google AI Pro). Privada. |

### Skills SWAL Internas (Privadas)

| Skill | Estado | Notas |
|-------|--------|-------|
| `xavier2-context` | 🔄 Activa | Context engine CEO brain. GitCore 3.6.0. |
| `worldexams-generator` | 🔄 Activa | ICFES bundles via MiniMax MCP. Depende de minimax-tools + cortex-memory. |
| `worldexams-curator` | 🔄 Activa | QC y formatting de bundles. Depende de cortex-memory. |
| `worldexams-validator` | 🔄 Activa | Validación y regeneración automatizada. Depende de worldexams-generator + cortex-memory. |

### Skills Registradas sin Directorio Físico

Las siguientes 5 skills aparecen en `_registry/manifest.yaml` pero **no tienen directorio** en `skills/`:

| Skill | Razón probable |
|-------|----------------|
| `sales-pro` | Privada, posiblemente en otro repo o pendiente de portar. |
| `cortex-memory` | Privada, posiblemente en transición a otro repo. |
| `gestalt-swarm` | Apunta a `iberi22/gestalt-rust`, skill externa. |
| `healthcheck` | Privada, pendiente de creación o migración. |
| `src-generator` | Privada, pendiente de creación o migración. |

> ⚠️ **Acción requerida:** Resolver desfase entre manifest (27) y directorios físicos (24).

---

## Recetas POML — Desglose

**Total: 39 recetas** repartidas en 8 departamentos.

| Departamento | Cantidad | Recetas |
|--------------|----------|---------|
| Engineering | 9 | ai-engineer, frontend-developer, backend-architect, devops-automator, test-writer-fixer, rapid-prototyper, mobile-app-builder, swarm-operator, cortex-manager |
| Marketing | 7 | content-creator, growth-hacker, app-store-optimizer, twitter-engager, instagram-curator, reddit-community-builder, tiktok-strategist |
| Testing | 5 | api-tester, tool-evaluator, test-results-analyzer, workflow-optimizer, performance-benchmarker |
| Design | 5 | ux-researcher, ui-designer, brand-guardian, visual-storyteller, whimsy-injector |
| Studio Operations | 5 | support-responder, infrastructure-maintainer, finance-tracker, analytics-reporter, legal-compliance-checker |
| Project Management | 3 | project-shipper, experiment-tracker, studio-producer |
| Product | 3 | feedback-synthesizer, trend-researcher, sprint-prioritizer |
| Bonus | 2 | studio-coach, joker |

### Topología

- **Solo**: 39 recetas (100%). Todas usan topología `solo`.
- **Multi / RAG / tools-first**: 0. Pendiente de implementar recetas multi-agente.

### Modelos soportados por receta

Todas las recetas POML declaran triple provider:
- **OpenAI**: `gpt-5`, temp 0.2
- **Gemini**: `gemini-2.5-pro`, temp 0.2
- **Qwen**: `Qwen2.5-Coder`, temp 0.1

---

## _registry — Estado

| Componente | Estado | Notas |
|------------|--------|-------|
| `manifest.yaml` | ✅ Válido | v1.0, última actualización 2026-04-17. 27 skills + 39 recipes. |
| `skill-provider.js` | ✅ Funcional | CLI Node.js con: list, get, install, search, sync, recipes, recipe. Soporta OpenClaw, Codex y agentes genéricos. |
| Cache local | ⚠️ Parcial | `.skill-cache/` se crea bajo demanda. No hay invalidación automática. |
| Tool aliases | ✅ Completos | Mapeo universal + específico por agente (openclaw, codex, claude, qwen, opencode). |

### Validación de manifest

- **Skills duplicadas**: Ninguna detectada.
- **raw_url rotos**: No verificado automáticamente. skills privadas sin `raw_url` son esperadas.
- **Dependencias circulares**: Ninguna detectada.
- **IDs huérfanos**: 5 skills en manifest sin directorio físico (ver tabla arriba).

---

## Scripts & Tooling

| Script | Propósito | Estado |
|--------|-----------|--------|
| `scripts/check_poml_headers.py` | Valida headers POML | ✅ Funcional |
| `scripts/convert_md_to_poml.py` | Conversión MD → POML | ✅ Funcional |
| `scripts/bench-run.py` | Ejecuta benchmarks de recetas | ✅ Funcional |
| `scripts/bench-aggregate.py` | Agrega métricas de bench | ✅ Funcional |
| `scripts/adapters/` | Adaptadores openai, gemini, qwencoder | 🔄 Stub / parcial |

---

## Qué Falta por Hacer

### Crítico (bloqueante para v1.0 del ecosistema)

1. **Sincronizar manifest con filesystem**: Crear o eliminar las 5 skills huérfanas (`sales-pro`, `cortex-memory`, `healthcheck`, `src-generator`, `gestalt-swarm` si es local).
2. **Versionar todas las skills públicas**: Solo `nextjs` (1.1.0) y `rust` (1.0.1) tienen semver. El resto debería declarar `version` en front matter.
3. **Taggear releases en git**: No hay tags. Necesario para semver y referencia estable de raw URLs.
4. **Tests automatizados para POML recipes**: `bench-run.py` existe pero no hay CI que lo ejecute en cada PR.

### Importante (mejora de calidad)

5. **Schema validation CI**: Validar `_registry/manifest.yaml` contra schema formal en cada push.
6. **Healthcheck de URLs**: Verificar periódicamente que `raw_url` públicas respondan 200.
7. **Recetas multi-agente**: 39/39 son `solo`. Necesitamos al menos 3 recetas `multi` o `rag`.
8. **Documentar `skill-provider` en README**: El provider es poderoso pero poco descubierto.
9. **Contenido de `docs/prd/` y `docs/stories/`**: Vacíos salvo `.gitkeep`.
10. **Eliminar `memory/`**: El directorio no existe pero `.gitignore` ya lo prevé; crear estructura o eliminar referencia.

### Nice to have

11. **npm/package.json en raíz**: Scripts de conveniencia (`npm run list`, `npm run validate`).
12. **GitHub Actions**: Lint de YAML, validación de POML, link-check de raw URLs.
13. **Dashboard de bench**: `bench/ai-engineer/` tiene estructura pero falta visualización de resultados.
14. **Auto-generar AGENTS.md desde manifest**: Evitar duplicación de tablas.

---

## Changelog Reciente

- **2026-04-17**: Última actualización de manifest. Marcaron `codex`, `gemini`, `qwen`, `github`, `coding-agent`, `skill-launcher`, `jules`, `gestalt-swarm`, `xavier2-context` como privados.
- **2026-03-31**: Añadido `xavier2-context` engine. GitCore 3.6.0 integrado.
- **2026-03**: Suite WorldExams completa (generator + curator + validator + minimax-tools).
- **2026-03**: MIT headers en 16 skills + 2 nuevas (`deploy-anywhere`, `web-design-guidelines`).

---

*Última actualización: generado automáticamente. Mantener vivo.*
