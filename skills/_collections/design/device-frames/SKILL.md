---
name: device-frames
description: Source and integrate credible phone or tablet frames for UI previews, interactive prototypes, screenshots, and videos. Use when showing content inside a named device, choosing iPhone or Android mockups, or correcting inaccurate bezels and outlines.
---

# Device frames

Make the represented device believable without distorting its content. Prefer an existing, verifiable frame over drawing a named phone from memory. This skill selects and integrates assets; it does not maintain a universal device catalog or turn a browser preview into a device emulator.

## Choose the representation

Resolve the exact model and variant from the request or project: iPhone 16, 16 Plus, 16 Pro, and 16 Pro Max are distinct. For Android, identify the manufacturer and model; there is no single Android housing. Include orientation, and folded/unfolded state when relevant. If no model is required, a clearly generic shell is valid; do not invent model fidelity.

Judge candidates by model and silhouette match, screen geometry, license for the intended use, and fit with the delivery format. Use the [source guide](references/sources.md) to find official bezels, transparent frame catalogs, or live components. Verify current availability and the actual asset rather than trusting a library name, search snippet, or advertised device count.

- For screenshots and video, a transparent frame overlay is usually sufficient. Preserve enough source resolution for the final export.
- For live HTML, use a transparent overlay around an independently interactive viewport, or a component whose supported model and layout match. A PNG can frame live content; CSS is not required to draw the housing.
- For realistic hardware, preserve manufacturer geometry and material treatment. Apply the surrounding project's visual style to the presentation, without reshaping the hardware to match it.

Reuse a suitable frame already in the project. Otherwise prefer a matching official asset where its terms allow the task, then a verified community asset. Custom CSS/SVG is a fallback when no suitable reusable asset is available or the user requests stylization. Ground it in dimensional drawings or clear reference imagery, and distinguish measured geometry from illustrative details. A nearby model is a disclosed substitution, not an exact match. If exact fidelity is essential and the source cannot be verified, report that specific gap.

## Integrate the frame

Keep the outer artwork, screen opening, and content viewport separate. Record the frame canvas dimensions and the screen rectangle or mask in that same coordinate system; transparent artwork margins are not physical bezels. Scale all layers uniformly. Do not stretch the screenshot to fit an unrelated aspect ratio or silently crop controls. Resolve a mismatch through a matching capture/viewport, an explicit crop, or a disclosed fit treatment.

Distinguish hardware millimetres, screenshot pixels, logical points/dp, and browser CSS pixels. A resolution alone does not establish logical layout dimensions or Android density. A named frame does not establish its safe areas. Browser `env(safe-area-inset-*)` describes the host viewport, not a simulated phone inside it; use verified target insets when the preview needs them.

For live previews, size the inner viewport deliberately before scaling the whole presentation. When responsive behavior or viewport units matter, use an appropriately sized iframe or another genuine viewport boundary supported by the host; an ordinary narrow div is not equivalent. Decorative frame layers should be hidden from assistive technology and should not intercept pointer events. Keep controls reachable and focus visible.

Treat status bars, navigation bars, home indicators, keyboards, and cutouts as separate responsibilities. Inspect the captured content and frame to avoid drawing them twice. In landscape, rotate/reposition the housing and cutout while laying out the content for landscape; rotating the entire portrait screenshot is only appropriate when that is the requested presentation. Do not rotate OS navigation chrome blindly with the shell.

Pin reused dependencies to an exact version or commit and retain the relevant license/attribution. Preserve the source URL, asset path, model/variant, screen placement, and material modifications in the project's existing asset or review record. Fetch public assets independently of private screenshots; do not upload user content to a mockup service without task authorization. Bundle the needed files when the target host cannot load external assets or scripts.

## Verify the result

Inspect the rendered frame with real task content at its delivery size, beside an authoritative reference. Check the body-to-screen proportions, bezel thickness, corner curves, cutout, and visible buttons. Check clipping and alignment at the screen opening, including at a narrow presentation width and each requested orientation. For interactive output, exercise the important controls, scrolling, and supported light/dark states; changing the app theme should not silently change the hardware model or color.

Use the actual screenshot or device/simulator measurements when native layout accuracy matters. Frame inspection establishes presentation quality, not native behavior, device performance, or physical-device acceptance. If visual inspection is unavailable, say what remains unverified rather than claiming an accurate result from dimensions alone.

Return the result with its model, frame source, any approximation, and the checks performed. Keep provenance in the project record rather than adding technical clutter to the product interface.
