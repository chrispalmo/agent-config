---
name: neon-neo-brutalist-minimal
description: Apply the default neon neo-brutalist minimal style to visual work, especially websites and app interfaces, or when selected by name or reference. Use bold typography, crisp edges, concentrated neon accents, and deliberate light and dark themes; explicit user direction and established brands take precedence.
---

# Neon neo-brutalist minimal

Use this style by default for visual work wherever explicit user direction or an established brand leaves room. For static artifacts, adapt the typography, hierarchy, outlines, and accent palette to the medium; interface controls and motion apply only where relevant.

Treat `$neon-neo-brutalist-minimal`, `/neon-neo-brutalist-minimal`, and clear references to this style as the same visual direction. This skill guides appearance within the requested task; it does not change the user's chosen product, functionality, or authorization. Explicit project direction and an established brand take precedence.

## Visual principles

Build a simple, high-contrast canvas with bold readable typography, generous spacing, solid outlines, and concentrated neon accents. Minimal means few competing treatments while important elements retain vivid emphasis. Let the actual content dominate.

- Use one coherent type family with a small hierarchy. Prefer an existing suitable product font; Atkinson Hyperlegible is an example, not a requirement. Keep body copy comfortable to read.
- Start with lime and ink for the primary visual identity. Pink and yellow can distinguish meaningful actions or states. Keep supporting surfaces quiet so accent areas carry weight; important elements should not dissolve into gray or washed-out pastels.
- Reuse a small set of edges, spacing, and corner treatments. Modest rounded corners belong in this style; square corners are optional. Flat cards and clear dividers can organize dense content without turning every block into a decorated box.
- Keep labels plain and concise. Express character through composition, typography, color, and purposeful interaction rather than invented slogans or decorative subtitles.

## Interaction hierarchy

Reserve hard, unblurred depth and tactile press movement for prominent filled actions. For a raised button, its pressed face can move into its bottom edge; the motion should communicate physical depth and respect reduced-motion preferences.

Secondary actions, replay, menus, checkboxes, and selection controls stay flat and still. A selected choice may use an accent fill without elevation. A menu icon needs no resting outline. Do not add 3D press movement to shadowless controls, or button construction to informational text and status labels.

Use consistent hover, focus, selected, disabled, and loading states. Keep keyboard focus visible and preserve control geometry when states change. Color may reinforce meaning but should not be its only signal.

## Light and dark

Give both themes equal visual intent, energy, and readable contrast. In light mode, use white or near-white surfaces and ink text. An indigo dark canvas with light text is a useful starting point; retain dark, readable labels on bright action fills. Adapt borders and depth to their surrounding surfaces instead of mechanically inverting every color.

These are starting tokens, not fixed brand requirements:

| Role | Light | Dark |
| --- | --- | --- |
| Canvas | `#ffffff` | `#10121e` |
| Surface | `#ffffff` | `#1b1e32` |
| Text | `#171717` | `#f9f8ff` |
| Supporting text | `#51564a` | `#b9bed6` |
| Subtle divider | `#dce5d2` | `#3d4565` |
| Primary / selection | `#c1ff3d` | `#c1ff3d` |
| Text on primary | `#171717` | `#121909` |
| Optional pink / yellow fills | `#ff5aa7` / `#ffd84a` | `#ff5aa7` / `#ffd84a` |

Keep vivid fills distinct from text colors: bright pink on white may need deeper ink or a different treatment. The exact dark-button edge, font, and corner geometry remain adaptable.

At the surface that owns appearance, follow system mode by default, respond to system changes while open, and provide an accessible remembered override with a way back to System. Embedded components inherit the host's theme rather than adding a competing switch. Theme changes preserve view, input, selection, and application state.

## Avoid

- **Color everywhere:** do not fill every card, label, and control with neon. Concentrate color on actions, selection, and meaningful information.
- **Bland minimalism:** do not mute the important elements into gray or washed-out pastels. Keep hierarchy bold and accents vivid.
- **Everything looking clickable:** do not give informational labels button shapes or raised edges. Secondary and selection controls remain shadowless and still.
- **Excessive variation:** avoid multiple font families, arbitrary corner shapes, inconsistent borders, and bespoke styling for every component.
- **Decorative clutter and copy:** omit invented slogans, ornamental subtitles, unnecessary numbering, tiny uppercase labels, and redundant explanation. Retain numbers, labels, and context when the task needs them.
- **Effects substituting for design:** avoid glow, glass, gradient washes, blurry shadows, and continuous animation. This is a stylistic interpretation of the references, not a ban overriding explicit project direction.
- **Literal copying:** do not force every project to use the same lime, font, mascot, or layout. Brutalism does not require square corners.
- **An unfinished second theme:** do not mechanically invert colors, leave controls illegible, or reset application state when the theme changes.

## Reference and completion

Inspect the [paired component sheet](references/components.svg) when a concrete example would help. It illustrates the palette, flat selection, quiet controls, informational color, and selective action depth; it is not a template or a final choice of dark-button construction. Preserve suitable product components and choose layouts around the actual content.

For an implemented interface, inspect relevant states in both themes and representative narrow and wide layouts. Check label contrast, focus visibility, role-appropriate motion, and state preservation through theme changes. Scale verification to the changed surface; this style skill adds no separate approval gate or requirement to build a comparison tool.
