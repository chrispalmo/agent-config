---
name: design-review
description: Prepare an interactive review when a user needs to compare interface designs, tune proposed changes, or leave feedback in context. Use for requested design comparisons and meaningful review decisions. A small, clear edit can usually proceed directly.
---

# Design review

Entry point for structured reviews. Follow the current authorization for source changes, installation and delivery.

Start with the decision the user needs to make and what they can inspect to make it. A single screen can be the whole review. Include packages, variations, and screen states only where they represent real choices.

For a browser review, **reuse the drawer** through the [mount and handoff reference](references/footer.md). Supply the design, meaningful parameters and preview renderer; do not reconstruct the controls from the example. The [working example](assets/review-example.html) demonstrates the integration with fictional app content. The drawer also supports live experiments.

Pin new consumers to a [template release](references/template-updates.md) with the supplied helper. Existing consumers keep their version until an update is requested; use the same reference for checks, diffs, adoption and rollback. Template updates do not change the design's review version or publish an artifact.

Match the content and state of the screens being compared. Use the product's own components where practical. Identify simulated behavior. Check the important preview states, phone layout, parameter bindings, contextual comments, reload, and exported review. Use a host-appropriate persistence adapter when the task needs shared or remote delivery.

Before delivery, verify the source and rendered appearance of new or changed standard interface icons in relevant states and themes. Follow the active icon-sourcing guidance, retain required attribution, and check preview icons against the product's symbols. Confirm any custom icon is justified by the design or an explicit request, preserving native symbols and approved brand artwork.

On receipt of an export, inspect its review version, exact approved values and open comments. Approve selects a variation and its settings. Comments attached to approval are required tweaks. Reject dismisses only that variation. The optional Apply to entire review checkbox applies a decision to the active variation in each package and resets after the action. A reviewer can leave feedback without a decision.

Use judgment on each comment. Answer a question directly in chat when that settles it. Mark an addressed comment resolved against the text actually reviewed. Issue a new review version when there is a changed design for the human to inspect, and retain the earlier export in History. Carry forward existing implementation authority. Exporting feedback does not authorize publication.
