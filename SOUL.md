# SOUL.md — SWAL Skills

> *"No escribimos documentación. Escribimos superpoderes para máquinas que piensan."*

---

## Nombre

**SWAL Skills** — SouthWest AI Labs Skills Library

## Propósito

Este repositorio es el **arsenal compartido** de skills para agentes de IA. No es un framework. No es una librería. Es un catálogo vivo de instrucciones empacadas que cualquier agente —OpenClaw, Codex, Claude Code, Qwen, OpenCode— puede leer y ejecutar.

Cada skill es un `SKILL.md` con alma. Cada receta POML es un agente ejecutable con identidad. Todo aquí está diseñado para ser **consumido por máquinas, mantenido por humanos**.

## Personalidad

- **Pragmático, no dogmático.** Si funciona y es legible para un agente, es válido.
- **Bilingüe por naturaleza.** El código habla inglés. Los comentarios y la documentación clave hablan español cuando es necesario. No hay vergüenza en mezclar.
- **Minimalista pero completo.** Un skill no necesita 500 líneas para ser útil. Pero sí necesita ser **autocontenido**: si un agente lo lee, debe poder actuar sin buscar en Google.
- **Multi-agente por diseño.** Nada aquí está atado a un solo proveedor. Todo skill debe funcionar con al menos 3 agentes distintos.

## Valores

| Valor | Qué significa en práctica |
|-------|---------------------------|
| **Universalidad** | Un skill no es tuyo, es de todos los agentes. No uses APIs propietarias sin alternativas. |
| **Claridad** | Un agente debe entender el skill en su primera lectura. Si necesita reinterpretar, fallaste. |
| **Utilidad inmediata** | Si un skill no tiene un "When to Use" claro, no es un skill, es un ensayo. |
| **Consistencia** | Seguimos GitCore Protocol v3.6.0 en todos los repos SWAL. No rompemos el contrato. |
| **Evolución rápida** | Los skills envejecen. Actualízalos sin miedo. Prefiere iterar sobre perfeccionar eternamente. |

## Cómo Debe Comportarse un Agente en Este Repo

Si eres un agente leyendo esto, estos son tus mandamientos:

### 1. Lee antes de escribir
Antes de tocar cualquier skill o receta, lee al menos 2 skills existentes para capturar el tono y la estructura. No inventes formatos.

### 2. Respeta el frontmatter
El YAML entre `---` no es decorativo. Es el contrato que otros agentes usan para parsear el skill. Si lo rompes, rompes la cadena de consumo.

### 3. Piensa en raw URLs
Cada skill que escribas será consumido desde `https://raw.githubusercontent.com/iberi22/swal-skills/main/...`. Asegúrate de que los paths internos sean resolubles desde ese contexto.

### 4. Documenta el "por qué", no solo el "cómo"
Los comandos y snippets son fáciles. Lo difícil es saber **cuándo** aplicarlos. Incluye siempre una sección de triggers o "When to Use".

### 5. No dupliques sin justificar
Antes de crear `react-advanced`, pregunta: ¿puedo extender `react`? Si no, documenta por qué el skill merece existir por separado.

### 6. Los POML son agentes, no prompts
Una receta POML no es un "prompt largo". Es una **especificación de agente** con rol, topología, herramientas y formato de salida. Trátala con ese respeto.

### 7. Mantén el registro sincronizado
Si creas un skill, actualiza `_registry/manifest.yaml`. Si creas una receta, asegúrate de que `skill-provider.js` la pueda listar. El registro es la fuente de verdad.

---

*Protocolo GitCore v3.6.0 — SWAL (SouthWest AI Labs)*
