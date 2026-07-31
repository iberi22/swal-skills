# Temperature Recommendations

This guide proposes default temperature settings by task type and provider. Treat them as starting points and override per `roles[].temperature` in recipe YAML.

## Task-type defaults

- Planning / structured reasoning: 0.0–0.2 (favor determinism)
- Strict code generation / tool calling: 0.0–0.2
- Creative ideation / diverse outputs: 0.6–0.8

## Provider-specific suggestions

- OpenAI GPT-5
  - Planning: 0.1–0.2
  - Code/tool-calling: 0.0–0.1
  - Creative: 0.7–0.8

- Gemini 2.5 Pro/Flash
  - Planning: 0.2
  - Code/tool-calling: 0.0–0.1
  - Creative: 0.8

- Qwen / QwenCoder
  - Planning: 0.1–0.2
  - Code/tool-calling: 0.0–0.1
  - Creative: 0.6–0.8

## Usage in YAML

```yaml
roles:
  - name: planner
    provider: openai
    model: gpt-5
    temperature: 0.1
  - name: executor
    provider: gemini
    model: gemini-2.5-pro
    temperature: 0.0
```

Tune per-benchmark empirically and document deviations in the recipe notes.
