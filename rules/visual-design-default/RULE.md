---
name: visual-design-default
description: Default visual direction for artifacts, interfaces, and other visual work
alwaysApply: true
---

# Default Visual Design

## Visual style

For all visual work—artifacts, documents, slides, charts, screens, websites, and apps—use the `neon-neo-brutalist-minimal` skill by default.

## Titles and labels

Use plain, descriptive titles and labels. Do not invent catchphrases, slogans, taglines, or decorative subtitles unless requested or established by the brand. Express the style through layout, typography, color, and interaction.

## Accessibility and existing design systems

Keep everything readable, accessible, and easy to use. Follow explicit user direction and existing brand or design systems; use this as the default wherever those leave room.

## Icon sourcing

For standard interface icons in product UI and previews, reuse the product's established icon set or the target platform's native symbols where supported. Otherwise use a maintained open-source icon library with suitable licensing. Use library assets directly. Preserve approved brand artwork. Create custom icons only when suitable existing assets cannot meet the design or the user explicitly requests custom artwork. Record a new library's source, version, and license in the project's existing asset or dependency record and retain required attribution. Licensed library SVG may be inlined or vendored.

## Device frames

When presenting UI inside a phone or tablet frame, use the `device-frames` skill to source and verify the frame and content placement.

## Mobile controls

For mobile interfaces, place frequent actions and selectors near the bottom within comfortable thumb reach by default. Prefer a stable action area that keeps active content and essential context visible. Respect platform safe areas and navigation conventions. Adapt placement for the keyboard, enlarged text, assistive technology, and limited screen space; preserve usable control sizes and logical reading and focus order, allowing reflow or scrolling when needed.

## Light and dark themes

For interactive visuals, visualizations, websites, and apps, support both dark and light themes. Design both themes deliberately and keep charts, controls, and interaction states readable. For static artifacts, use a coherent theme suited to the medium.

Use a compact, two-state sun/moon button showing the current theme, with an accessible name for the next action, a usable touch target, and visible focus. Follow system appearance until the user chooses light or dark, then remember that choice where supported and ignore later system changes. Restore the choice on reopening and preserve application state when switching. Use the [static sun/moon reference](references/theme-toggle.svg) as a visual guide; native equivalents are suitable.
