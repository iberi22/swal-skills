# Mobile Responsive Fix - Tripro.cl Case Study

**Fecha:** 2026-03-17  
**Problema:** Text overflow en móvil (390px viewport)  
**Solución:** CSS reset + container constraints

---

## El Problema

En móviles (iPhone 390px), el texto se cortaba en el lado derecho:
- Badge: "SOFTWAR" cortado
- Párrafo: "indu", "inte", "vent" cortados
- Stats cards: overflow horizontal

---

## Solución Implementada

### 1. CSS Global Reset (global.css)

```css
/* ULTRA AGGRESSIVE MOBILE RESET */
* {
  max-width: 100vw !important;
  box-sizing: border-box !important;
}

html, body {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
}
```

### 2. Section Container Fix

```css
.section-shell {
  margin-inline: auto;
  width: 100%;
  max-width: 100%;  /* Mobile: no max-width */
  padding-inline: 1rem;
}

@media (min-width: 640px) {
  .section-shell {
    padding-inline: 1.5rem;
    max-width: 80rem;  /* Desktop: limit width */
  }
}
```

### 3. Layout HTML Tag

```astro
<html lang="es-CL" class="overflow-x-hidden">
```

### 4. Main Container

```astro
<main class="relative overflow-x-hidden w-full max-w-full">
```

---

## Reglas de Responsive para Astro/Tailwind

### Always Use These Patterns:

| Pattern | Correcto | Incorrecto |
|---------|----------|------------|
| Container width | `w-full max-w-full` | `w-[500px]` |
| Text overflow | `truncate` o `break-word` | Sin control |
| Padding mobile | `px-4` (16px min) | `px-2` |
| Font mobile | `text-xs` o `text-sm` | `text-base` |
| Section max | `max-w-full` (mobile) | `max-w-4xl` |

### Mobile-First Checklist:

- [ ] `html` tiene `overflow-x: hidden`
- [ ] `body` tiene `width: 100%`
- [ ] `.section-shell` tiene `max-width: 100%` en móvil
- [ ] Todos los textos usan `truncate` o `break-word`
- [ ] Padding mínimo 16px en móvil
- [ ] Fuentes menores a 16px en móvil

---

## Files Modificados

- `src/styles/global.css` - CSS reset + section-shell fix
- `src/layouts/Layout.astro` - overflow-x-hidden en html
- `src/pages/index.astro` - containers responsive
- `src/components/home/HeroMotion.tsx` - componentes responsive

---

## Testing

1. Abrir DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Seleccionar iPhone 12 Pro (390px width)
4. Verificar que NO hay overflow horizontal
5. Hacer scroll horizontal - no debe moverse

---

*Documento creado: 2026-03-17*
