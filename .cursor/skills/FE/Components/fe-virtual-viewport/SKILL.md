---
name: fe-virtual-viewport
description: >-
  Documents ART-ERP-FE app-virtual-viewport and the virtualItemMeasure directive
  for variable-height virtual scroll outside app-data-table. Use when adding or
  changing a custom long list, dropdown tree, or non-table viewport; do not use
  when the page already scrolls rows through app-data-table virtualization.
---

# FE virtual viewport

Ionic + Angular NgModule (`standalone: false`). Selector `app-virtual-viewport` (`exportAs: 'virtualViewport'`). Pair every projected row with `[virtualItemMeasure]` so real heights lock into the engine.

`ShareModule` → `ShareComponentsModule` exports `ShareVirtualScrollModule`. Pages that import `ShareModule` already have both the component and the directive. Feature modules that do not use `ShareModule` can import `ShareVirtualScrollModule` directly (as `share-input-controls.modules.ts` does).

Canonical files:

- Viewport: `ART-ERP-FE/src/app/components/virtual-scroll/virtual-viewport.component.ts`, `virtual-viewport.component.html`
- Measure: `ART-ERP-FE/src/app/components/virtual-scroll/virtual-item-measure.directive.ts`
- Module: `ART-ERP-FE/src/app/components/virtual-scroll/share-virtual-scroll.module.ts`
- Engine (do not reimplement): `virtual-scroll.engine.ts`

## When to use this vs `app-data-table`

| Need | Use |
| --- | --- |
| Routed list / CRUD grid / detail line table | `app-data-table` — virtual scroll is **on by default** (`[virtualScroll]="true"`). It already wraps `app-virtual-viewport` inside `datatable-body`. Do **not** put another viewport around the table. |
| Custom long list that is not a data-table (dropdown panel, tree, sheet rows) | `app-virtual-viewport` + `virtualItemMeasure` in that template. |

Real in-repo consumers of the selector:

- `datatable-body.component.html` — internal; pages only toggle `app-data-table` inputs (`virtualScroll`, `virtualScrollMode`, buffers, `virtualScrollDefaultItemSize`).
- `input-control.component.html` — branch tree inside `ng-select` `ng-header-tmp` (`mode="container"`, `idKey="Id"`).

`PageBase.ionViewDidEnter` dispatches `app:virtual-viewport-relayout` so viewports that patched while the ion-page was `display:none` recompute. Do not invent a second relayout bus on the page.

## Copy this

Custom list (container scroll — pattern from branch tree / data-table body):

```html
<app-virtual-viewport
	#vp="virtualViewport"
	mode="container"
	class="container-mode"
	[items]="items"
	idKey="Id"
	[defaultItemSize]="36"
	[style.height]="'240px'"
>
	<div
		*ngFor="let item of vp.renderedItems; trackBy: trackById"
		[virtualItemMeasure]="item.Id"
		[measureGeneration]="vp.measureGeneration"
		(heightMeasured)="vp.onItemMeasured(item.Id, $event)"
	>
		<!-- row markup -->
	</div>
</app-virtual-viewport>
```

Page scroll (`mode="page"`, default): viewport stays in document flow; ancestor `ion-content` is the scroll element. Prefer this when the list fills `ion-content` the same way list tables do. Add `class="page-mode"` only if you mirror data-table styling; height style is not required.

Do not bind a getter that returns a fresh `.filter(...)` array every CD unless ids are stable — the viewport skips engine rebuild when the id sequence is unchanged, but still pays for array allocation.

## `@Input` / `@Output` (`app-virtual-viewport`)

| Binding | Default | Role |
| --- | --- | --- |
| `items` | `[]` | Full list. Engine keys rows by `idKey`. |
| `mode` | `'page'` | `'page'` = `ion-content` scroll; `'container'` = viewport `overflow:auto`. |
| `idKey` | `'id'` | Stable id property (`Id`, `requestId`, …). |
| `defaultItemSize` | `51` | Placeholder height before measure; set near real row height. |
| `minBufferPx` / `maxBufferPx` | `300` / `600` | Overscan above/below the visible window. |
| `scrollToId` | — | Scroll so that id is in view (queued until layout is ready). |
| `scrollAlign` | `'center'` | `'center'` or `'start'` for `scrollToId`. |
| `scrollToTick` | — | Bump (number) to retry scroll after a panel finishes positioning. |
| `scrollProgress` | `@Output` | `{ distanceToEndPx }` — data-table uses this for infinite load near the end. |

Template API via `#vp="virtualViewport"`: `renderedItems`, `measureGeneration`, `totalHeight`, `contentTransform`. Call `vp.onItemMeasured(id, height)` from `(heightMeasured)`. Public helpers on the instance: `relayout()`, `requestRemeasure()`, `scheduleRemeasureAfterResize()`, `invalidateHeights()` (hard reset — prefer remeasure).

## `virtualItemMeasure` directive

| Binding | Role |
| --- | --- |
| `[virtualItemMeasure]="id"` | Stable item id (same value passed to `onItemMeasured`). |
| `[measureGeneration]` | Bind `vp.measureGeneration` so width/breakpoint remounts measure once. |
| `(heightMeasured)` | Emit real px height → `vp.onItemMeasured(id, $event)`. |

Required on every virtual row root. Runs outside NgZone; the viewport batches locks per animation frame.

## Do not

- Wrap `app-data-table` in `app-virtual-viewport`, or reimplement virtual rows on a list page that already uses the table.
- Project rows without `[virtualItemMeasure]` / `(heightMeasured)` — heights stay at `defaultItemSize` and scroll jumps.
- Declare `VirtualViewportComponent` / `VirtualItemMeasureDirective` again in a page module.
- Edit `virtual-scroll.engine.ts` or the viewport when the task is only to wire a consumer — change the consumer template and inputs.
- Use CDK `cdk-virtual-scroll-viewport` for new ERP lists; this component owns the variable-height contract.

List shell / table pages: skill `new-fe-crud-page`. Toolbar on those pages: skill `fe-toolbar`.
