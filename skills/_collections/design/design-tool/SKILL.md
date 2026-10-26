---
name: design-tool
description: Build a temporary chooser to compare and refine complete design proposals in a running application, then retain the selected product implementation and remove experiment-owned code. Use when the user wants to compare design directions before choosing one.
---

# Design Tool

The chooser is temporary developer UI; the candidate widget is product UI. Floating placement of the chooser does not constrain candidate designs, which can be inline, modal, navigation, or another placement suited to the product.

Use a dedicated worktree when substantial temporary code needs isolation; a small comparison can stay in the existing workspace. Record the experiment-owned files, assets, routes, storage keys, and identifiers as they are introduced so cleanup has a precise boundary.

## Build and compare

Make the feature work, then produce several complete numbered directions that differ in meaningful product choices. Each should be a plausible finished design coherent with the application.

The floating chooser should be compact and visually distinct, with a visible drag handle, resize handle, internal vertical scrolling, design dropdown, and previous/next controls. Switch the candidate immediately. Remember position and size for the session when practical.

Include only useful candidate-specific refinement controls. Collapsing hides the refinement area while leaving the handle, switcher, arrows, and expand control usable. Follow the project's components, licensed assets, and visual system. Prefer suitable existing icon and asset libraries over custom artwork or emoji product icons.

Provide a usable preview and invite selection or targeted feedback. Follow active conversation numbering and link conventions. A requested comparison is a useful selection point; do not add unrelated approval gates.

## Retain the selection

Bake the chosen design into ordinary product code. Remove the chooser, rejected candidates, and experiment-owned wiring, temporary assets, tuning APIs, storage keys, and debug hooks. Search for the recorded identifiers in source and relevant production output. Remove stale guidance that refers to the experiment.

Selected and unrelated product UI remain product code even when visible in a development preview. Verify the selected design's important states and viewport sizes after cleanup. Carry forward already-authorized merge, publish, deployment, or worktree-cleanup actions once their prerequisites pass; do not infer authority for those actions merely from design selection.
