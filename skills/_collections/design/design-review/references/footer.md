# Reuse the review drawer

Use the [footer](../assets/design-footer.js), [state model](../assets/design-state.js), [inline annotations](../assets/design-annotations.js), [persistence helpers](../assets/design-persistence.js), and [tool CSS](../assets/design-footer.css) together. Preserve their relative imports when copying or bundling them. Only the app supplies its screens and design variables. The [example adapter](../assets/review-example.js) and [example styles](../assets/review-example.css) belong to the fictional task app.

Create the shared resource copy with the [pinned-release helper](template-updates.md). It records an exact template release and supports optional checks, explicit updates and rollback while preserving the app's renderer and review data.

## Minimal mount

Mount once per review page. Give the review a stable ID, an integer version and a preview element. Mark the page header with `data-review-header` or pass its element as `headerHost` for the comparison and appearance controls. The mount adds the shared `dr-review-header` layout; the host supplies its title, surface and spacing. Load the tool CSS alongside the host app and avoid overriding the header's responsive control layout. For example:

```js
import {mountDesignFooter} from './design-footer.js';

mountDesignFooter(drawer, {
  reviewId: 'signup-button',
  reviewVersion: 1,
  reviewArea: preview,
  design: {
    id: 'signup', title: 'Sign-up button',
    defaults: {label: 'Continue'},
    controls: [{key:'label', label:'Button label', type:'text', required:true}]
  },
  onChange({draft}) {
    preview.querySelector('button').textContent = draft.tweaks.label;
  }
});
```

For a standalone review, reuse the [example page's layout](../assets/review-example.html): one `data-review-layout` container with the header, scrollable preview and drawer as direct children. The shared controls use that structure for mobile header scrolling; live apps without this wrapper keep their own page layout. The preview's top spacing can be set with `--dr-preview-top-gap` (12px by default).

For a comparison, pass `changes` in place of `design`. Each package has a stable ID, title and optional `options` and `scenes`. Options own their defaults, controls and source revision. Scenes are ID/label pairs. Single choices use internal IDs without displaying a selector. Give each real option its own stable ID. Increment its source revision when changing the design. Render from the current change, option, draft and state in the callback. Use `state.sides` (current, proposed, both), `state.previewThemes` (light, dark, both), and `state.scene` to show the requested combination. Both themes in comparison mode pair Current and Proposed within each theme. Label theme groups `{Variation} · {State} ({Theme})`, omitting absent levels. Label the individual previews Current or Proposed with their theme. Mark panes with `data-reference="current"` or `"proposal"` and `data-theme="light"` or `"dark"` for quote navigation.

## Interaction

The drawer opens on Comments. Its two icon tabs are Comments and Design Controls, with the active name in the drawer header. Hide Design Controls when the selected option has no controls. Both tabs navigate via the same dropdown breadcrumbs. Omit singleton levels and use the available drawer width. Place breadcrumbs alongside the toolbar on wide screens and on their own full-width row when narrow. The comment composer has an initially unchecked Apply to entire review checkbox above its action buttons. Unchecked actions apply to the current view/variation. Checked comments belong to the entire review; checked Approve/Reject applies to the active variation in each package. The tick commits the text; Approve/Reject also commits any entered comment with the decision. × discards the uncommitted edit. These actions clear the checkbox, and committed/discarded text clears the composer. Switching tabs retains unfinished text in memory. Only committed comments enter the review export. Show new comments first and their individual save status in the list. Selecting text offers Add comment beside the quote. Its inline editor commits with a tick or discards with ×. Once saved, a small marker and the matching list entry share the quote’s highlight color. Hover previews the note. Click or tap to read, edit or minimize it. The inline card shows that comment's save status too. Selecting its list entry returns to the same scope and opens the note beside its text. Restore quotes using pane, text position and surrounding text. Keep unmatched notes readable in the list. Reset parameters lives inside Design Controls and affects the current variation.

The compact app header contains the page title at the body text size in bold, the Current/Proposed/Both and Light/Dark/Both selectors, and the interface appearance button at the right. When the full row cannot fit, both selectors collapse together to one cycling button each: Current → Proposed → Both → Current, and Light → Dark → Both → Light. The buttons show the current choice and identify the next action accessibly; they do not open dropdowns. Collapse follows the actual header width and title, and both expand together when room returns without changing selections or losing keyboard focus. The sun/moon button independently changes interface appearance. Allow long titles and enlarged text to reflow.

On mobile, the standalone header moves out on downscroll and returns on upscroll, one CSS pixel per pixel scrolled, clamped to its full height. It has no timed transition or snap threshold. The preview scrolls under it without leaving an empty header row or doubling the content's movement. Returning to the top or focusing a header control with the keyboard exposes it; desktop keeps the header visible. Check partial and full hide/reveal, direction reversal, text enlargement and resize along with the selectors.

The drawer fills its host width, including extra-wide screens. Drag its top edge to adjust docked height, or use the expand/collapse button. The focused height separator also supports arrows, Home and End. The drawer’s expand/collapse, dock/detach, history and export icons align right at every width. The entire detached header background drags the drawer and its corners resize it. Mobile stays docked. Overflow holds displaced utility icons. `mode:'live'` defaults to floating on desktop. Standalone live tuning mounts this same drawer into an actual running app.

## Export and follow-up

Export review downloads the current review ID/version, per-option source revisions, parameter values, decisions, approval snapshots, comments and view state. Each comment has a stable ID, originating version, scope IDs, readable label, text, optional quote/theme/side, status and optional reply. Legacy comments of unknown screen state retain a null state ID. Drawer and inline comments save explicitly. Parameter changes autosave through the selected adapter. Preserve in-memory export on storage failure. Review export itself creates no revision.

Pass the earlier exported JSON records as `revisions:[priorExport]` to make them available read-only through History. On a new version, the latest matching earlier export supplies comments for a fresh browser. A browser already using the review archives its outgoing revision before loading the new defaults. Local snapshots and author-supplied revisions retain their provenance. `initialReview` can seed the same version from its export in a fresh browser. Give each new version the intended starting parameters. Treat the prior approval as evidence for its exact earlier design.

To resolve a comment, pass `commentUpdates:{[id]:{expectedText,status:'resolved',reply}}` when mounting. The expected text can also come from the source export. A reply is optional. The update applies only to matching text and is remembered, so later edits can reopen the comment. A chat answer or resolution need not create a design revision. Example history is explicitly fictional and separate from working data.

## Delivery

Local browser storage is the default adapter. For hosted reviews, load the adapter before mounting and pass it as `persistence`. Its core contract is hydrated `data`, `search`, `save(state)`, `flush()`, `onStatus(callback)` and `beforeLeave(capture)`. `save` snapshots immediately and returns the acknowledged `{data}` envelope; comments are marked saved only when their current contents match that acknowledgement. Transport status is not part of the review export.

The [Artifact Box adapter](../assets/artifact-persistence.js) adds device-local `view`/`saveView`, `check`/`onUpdate`, `captureRecovery`, `continueLatest`, and retained `recoveries`/`isAcknowledged`. Reuse it for authorized Artifact Box delivery rather than recreating the bridge. Keep the app's build and delivery recipe in its owning source project. Other hosts can supply the same capabilities when needed; the drawer remains usable with local storage.

Shared state contains committed comments, parameters, decisions and review history. Package/variation/state navigation, preview selectors, appearance and drawer placement stay in the current browser profile. View-only changes must not create shared revisions. Unsubmitted text remains a draft; recovery capture does not submit it as a comment or decision.

The drawer checks for newer shared revisions on open and when the tab returns, with a first-interaction fallback for embedded browsers. A clean session adopts the latest review while retaining its local view. When unfinished work exists, present **Continue latest saved review** and **Review my unsaved changes** in the recovery dialog. The first checks out the latest shared base and preserves the device's draft. The second shows differences and exports the complete local draft, with readable JSON as a download fallback. Retained drafts remain available through History. Pause editing during checkout, preserve a confirmed local copy before replacing unfinished work, and keep the loaded-revision check on every shared save. There is no automatic merge or claim that another device is currently online.

Comment save states appear on their list entries and inline cards; parameter state stays in Design Controls. Ordinary save updates remain inline. Storage or network failures keep the current work exportable rather than implying a shared save succeeded.

History uses a viewport-owned dialog outside the resizable drawer, with a persistent title/close row and a scrollable body. Match that dialog pattern for host recovery, including narrow viewports; routine save updates remain inline. The scope checkbox reads Apply to entire review and aligns left within the action area.

Distinguish local capture from a shared acknowledgement, keep unsaved work exportable on conflict, and preserve the source of the exported review. Use the delivery capability already authorized for the task. The drawer owns review semantics independently of the host.
