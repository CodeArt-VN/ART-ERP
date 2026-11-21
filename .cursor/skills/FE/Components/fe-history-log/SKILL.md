---
name: fe-history-log
description: >-
  Documents ART-ERP-FE history Time Machine UI: app-history-log-popover and
  app-history-log-json-modal (HistoryLogPopoverComponent /
  HistoryLogJsonModalComponent). Use when adding or changing history log
  picker, history JSON detail modal, toolbar history navigation, or
  historyItems / selectHistoryIndex wiring in ART-ERP-FE. Pages must not mount
  these selectors; app-toolbar opens them. Do not reimplement the picker.
---

# FE history log

Ionic + Angular NgModule (`standalone: false`). Both components live in one file with inline templates (no separate `.html`). Declared in `ShareComponentsModule`; not exported. Opened only via `PopoverController` / `ModalController` — not as page markup.

Canonical files:

- Components: `ART-ERP-FE/src/app/components/toolbar/history-log-popover.component.ts`
- Opener: `ART-ERP-FE/src/app/components/toolbar/toolbar.component.ts` (`openHistoryLogPicker`)
- History chrome: `ART-ERP-FE/src/app/components/toolbar/toolbar.component.html` (history view buttons)
- Page state: `PageBase` — `historyItems`, `historyIndex`, `selectHistoryIndex`, `enterHistoryView` / `exitHistoryView`

## Do not mount on pages

Pages should not put `<app-history-log-popover>` or `<app-history-log-json-modal>` in templates unless a rare non-toolbar host truly needs them. Detail history uses `app-toolbar` with `[page]="this"`; the toolbar position button calls `openHistoryLogPicker`. Related skill: `fe-toolbar`.

**Only usage today:** `ToolbarComponent.openHistoryLogPicker` creates the popover. The JSON modal is opened only from the popover’s code button (`viewJson`). No page template references either selector.

## Open path (toolbar)

When `page.pageConfig.isHistoryView` and `page.historyItems.length`:

```ts
const popover = await this.popoverController.create({
	component: HistoryLogPopoverComponent,
	componentProps: {
		items: this.page.historyItems,
		selectedIndex: this.page.historyIndex,
		onSelect: (index: number) => this.page.selectHistoryIndex(index),
	},
	event: ev,
	cssClass: 'history-log-popover',
	dismissOnSelect: false,
});
await popover.present();
```

`items` / `selectedIndex` are **newest-first** (same order as `page.historyItems`). The popover reverses for display (oldest / #1 at top) and maps clicks back via `displayIndexToNewestFirst`.

If `onSelect` is a function, pick keeps the popover open and calls it (toolbar pattern). Otherwise dismisses with `{ index }`.

## `app-history-log-popover` (`HistoryLogPopoverComponent`)

| Input | Default | Role |
| --- | --- | --- |
| `items` | `[]` | Newest-first history entries (`EnrichedLog`-like). |
| `selectedIndex` | `0` | Newest-first index of the active entry. |
| `onSelect` | — | `(index: number) => void`. Prefer this over dismiss payload when the parent must apply a snapshot without closing. |

No `@Output`. Row shows `LoggedBy`, `_label` / `Method`, formatted time (`_time` or `Date`). Action icon/color from `_action` / `Segment5`, `_badge`, `Method` (aligned with toolbar event icons). End button opens the JSON modal; click does not change selection.

## `app-history-log-json-modal` (`HistoryLogJsonModalComponent`)

Opened from the popover only:

```ts
component: HistoryLogJsonModalComponent,
componentProps: {
	item,           // parsed from entry._data ?? entry.Data ?? entry
	loggedBy: entry?.LoggedBy || '—',
	loggedAt: /* formatted time */,
},
cssClass: 'modal90vh',
```

| Input | Default | Role |
| --- | --- | --- |
| `item` | — | Object shown in `app-json-viewer` (tree) or raw `<pre>` when toggled. |
| `loggedBy` | `''` | Read-only meta via `app-form-control` (`LoggedBy`). |
| `loggedAt` | `''` | Read-only meta (`Date`). |

No `@Output`. Header toggles tree vs raw JSON (`showRaw`). Viewer uses `[isCompare]="false"` and `[isShowDifference]="false"` — skill `fe-json-viewer`.

## Page wiring (not these selectors)

Enable history through `PageBase` + toolbar (`ShowHistory` / `page.pageConfig.ShowHistory`), not by embedding the popover. Navigation: `historyFirst` / `historyPrev` / `historyNext` / `historyLast` / `selectHistoryIndex` / `exitHistoryView`.

## Do not

- Add `<app-history-log-popover>` or `<app-history-log-json-modal>` to list/detail page HTML for standard Time Machine.
- Declare the components again in a page NgModule; they stay on `ShareComponentsModule`.
- Invent `@Output` events; selection is `onSelect` or popover dismiss `{ index }`.
- Reimplement action icon mapping or the JSON modal on the page.
- Edit `history-log-popover.component.ts` when the task is only to show history on a screen — use `app-toolbar` and `PageBase` history APIs instead.
