---
topology: solo
roles:
  - name: planner
    provider: openai
    model: gpt-5
    temperature: 0.2
tools:
  - web_search
  - code_run
bench_id: sample-task
prompt_variants:
  - id: v1
    desc: baseline
constraints:
  - "no external calls without approval"
tool_mode: auto
tool_aliases:
  search: responses.tools.web_search    # OpenAI alias
  search@gemini: googleSearch           # Gemini alias
---

# Sample Recipe (Engineering)

This is a minimal example recipe used to validate the YAML header schema and the micro-bench flow.

- Provider: OpenAI (GPT-5)
- Topology: solo
- Tools: `web_search`, `code_run`

Use `scripts/bench-run.py` to evaluate this recipe against `bench/sample-task/cases/`.
