---
name: design-tool
description: Builds a temporary local floating panel for quickly switching between complete UI design proposals, refining promising candidates, and removing all experiment code before merge. Use when the user wants to compare design directions in a running application before choosing one.
---

# Design Tool

Build a small, development-only design chooser for direct visual comparison of multiple design variations.

## Keep the two designs separate

There are two different things being designed:

- **Design tool panel:** temporary developer UI
- **Candidate widget:** the actual product UI under review

The panel’s floating placement is not a candidate-widget design requirement.
Candidate widgets may be inline, in navigation, a modal, a drawer, a full page,
or floating, according to the proposal being tested.

## Worktree

For any experiment likely to add substantial temporary code, create a dedicated worktree in the current workspace from the target product branch.

- Keep the panel, every candidate, and temporary assets in that worktree.
- After a final design is approved, remove the panel and rejected candidates before merging.
- Verify the cleaned worktree contains only the chosen product implementation.
- For a small, one-file visual comparison, a separate worktree is optional.

## Build

1. Make the underlying feature work before adding the design tool.
2. Create several complete, numbered design proposals. Each must be a plausible finished direction, not a palette or spacing permutation, and must be coherent with the overall product design. Vary the candidate widget's product decisions where relevant.
3. Add a floating panel that:

- is floating, with a visible `≡` drag handle for repositioning.
- is **resizable** via a visible bottom-right corner size handle. remember width/height across the session when practical.
- **scrolls vertically** inside the panel when content exceeds the current height — never clip controls or force the panel to grow unboundedly.
- has a dropdown for switching between `Design 1`, `Design 2`, etc.
- has back/forward arrows for switching between designs
- applies the chosen design immediately
- is compact and visually isolated from the product UI

Include a compact parameter refinement area from the start. For each candidate, expose only the meaningful sliders, selects, checkboxes, or toggles that help tune
that candidate's real design choices. Avoid a giant generic control panel. The user should be able to pick a promising direction and tune it without asking for the first batch of obvious controls.

**Collapse behavior:** Collapse hides only the parameter refinement area below the design switcher. The collapsed panel must still show:

- the drag handle
- the design dropdown
- the back/forward arrows
- the expand control

## Design Requirements

- Use the project’s existing components and licensed assets where available
- When new assets are required, use high-quality open source / public asset libraries.
- Do not draw icons, make custom SVG artwork, or use emoji as product icons except as a last resort.

## Interaction

Present the preview URL and follow up by asking about:

- any particular design/s or design elements that are preferred (maybe use these to generate a fresh batch of candidates?)
- which upfront refinement controls helped or should be adjusted for any favourite designs

## After selection

1. Bake the selected design into normal product code.
2. Remove all experiment code before merge or publish:
   - the design-tool panel and includes
   - rejected candidates and temporary assets
   - dev-only scripts, styles, routes, build wiring, and generated artifacts
   - runtime tuning APIs, globals, storage keys, and debug hooks
   - stale project docs that imply the tool still exists
3. Search source and production output for design-tool identifiers and temporary
   artifact names. Treat anything visible in `npm run dev` as temporary unless
   the user explicitly promotes it to a product feature.
4. Verify the selected design still works in the relevant states and viewport
   sizes.
5. Do not merge, publish, or deploy unless this closeout gate passes and the user
   asks for the next action.
