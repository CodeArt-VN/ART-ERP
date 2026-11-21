---
name: fe-toolbar
description: >-
  Documents how to place and configure `app-toolbar` on ART-ERP-FE list and
  detail pages: pass the PageBase instance, optional title and visibility
  inputs, and projected slots for extra actions. Use when adding or changing a
  routed CRUD header, toolbar buttons, history navigation, or custom end-slot
  actions in ART-ERP-FE. Do not reimplement or restyle the toolbar component.
---

# FE toolbar

Ionic + Angular NgModule (`standalone: false`). Routed list and detail pages use `app-toolbar` inside `ion-header`. Popups and modals do not — skill `fe-popup`.

Pages already import `ShareModule`; `ToolbarComponent` is declared there. Do not redeclare `app-toolbar` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/toolbar/toolbar.component.ts`, `toolbar.component.html`
- List: `ART-ERP-FE/src/app/pages/_template/flat/flat.page.html`
- Detail: `ART-ERP-FE/src/app/pages/_template/flat-detail/flat-detail.page.html`

## Copy this

List or detail — same binding:

```html
<ion-header [translucent]="true">
	<app-toolbar [page]="this"></app-toolbar>
</ion-header>
```

The page class extends `PageBase`. `[page]="this"` is required so the toolbar can read `pageConfig`, `query`, `selectedItems`, `item`, and call page methods (`add`, `refresh`, `export`, `import`, `delete`, approval actions, history helpers, etc.).

Optional extra actions (projected into the end area when no rows are selected):

```html
<app-toolbar [page]="this">
	<ion-button title="{{ 'My action' | translate }}" (click)="myAction()">
		<ion-icon slot="icon-only" name="star-outline"></ion-icon>
	</ion-button>
</app-toolbar>
```

Do not duplicate built-in Add, Search, Export, Delete, or other standard icons unless the form truly needs a separate command.

## Permissions and visibility

Built-in buttons render only when **both** apply where the template checks them:

- `page.pageConfig.Show*` — toolbar affordance from SYS_Form setup (defaults on `PageBase.pageConfig`; child form rows under the page form set flags via `pageConfig[p.Code] = true` in `PageBase` ionViewDidEnter / `getPagePermission`).
- `page.pageConfig.can*` — permission flags on the same object (e.g. `canAdd`, `canExport`, `canDelete`).

Do not hardcode `*ngIf="true"` on standard commands in the page template to bypass form permissions. To hide a built-in control for one screen, prefer `[ShowAdd]="false"` (and siblings) on `app-toolbar`, or adjust SYS_Form children — not ad hoc permission logic on `ion-button` copies of toolbar actions.

`pageProvider.showCommandRules` may further toggle `pageConfig` keys when list rows are selected (`showCommandBySelectedRows`).

## `@Input` (page template)

There are **no** `@Output` bindings on `app-toolbar`.

| Input | Default | Role |
| --- | --- | --- |
| `page` | — | PageBase instance (`[page]="this"`). |
| `NoBorder` | `false` | Adds `toolbar-no-border` on the inner `ion-toolbar`. |
| `BackHref` | — | Detail back button `defaultHref` when not using `page.pageConfig.pageName` alone. |
| `pageTitle` | — | Overrides `page.pageConfig.pageTitle` for back label, list title, and `document.title`. |
| `showTitle` | `true` | `false` hides the list form-name button; put replacement UI in `[startTitle]`. |
| `CenterTitle` | — | Detail center `ion-title` text (with optional `[centerTitle]` content). |
| `ShowAdd` | `true` | Hides Add in the mobile overflow popover when `false` (desktop still uses `page.pageConfig.ShowAdd`). |
| `ShowSearch` | `true` | Same pattern for Search in popover vs `page.pageConfig.ShowSearch`. |
| `ShowRefresh` | `true` | Refresh. |
| `ShowExport` | `true` | Export. |
| `ShowImport` | `true` | Import. |
| `ShowCopy` | `true` | Copy (selection). |
| `ShowChangeBranch` | `true` | Change branch. |
| `ShowSubmit` | `true` | Submit for approval. |
| `ShowApprove` | `true` | Approve. |
| `ShowDisapprove` | `true` | Disapprove. |
| `ShowMerge` | `true` | Merge. |
| `ShowSplit` | `true` | Split. |
| `ShowCancel` | `true` | Cancel. |
| `ShowArchive` | `true` | Archive / reopen and archive filter. |
| `ShowDelete` | `true` | Delete. |
| `ShowHelp` | `true` | Help. |
| `ShowHistory` | `true` | History entry on detail (also needs `page.pageConfig.ShowHistory`). |
| `ShowFeature` | `false` | Feature panel toggle in popover; main bar uses `page.pageConfig.ShowFeature`. |
| `AcceptFile` | `'.xlsx'` | Import file input `accept`. |

## Projected content (attributes on child nodes)

| Selector | When it appears |
| --- | --- |
| (default) | Extra `ion-button` / controls at end when no selection. |
| `startTitle` | Start slot beside title (list, no selection). |
| `segment` | Between start and end (e.g. segment in header). |
| `centerTitle` | Inside detail center title next to `CenterTitle`. |
| `tollbarSelected` | End actions when `page.selectedItems.length` (typo preserved in source). |
| `rightScreenPop` | Items inside the mobile “Show more” popover list. |
| `endSlot` | After the popover trigger on end. |

## Behavior (do not reimplement on the page)

- **Search:** toggles `page.pageConfig.isShowSearch`, or opens the data-table mobile filter sheet on compact / Ctrl|Cmd+click (`DataTableMobileFilterService`).
- **Import:** hidden file input; calls `page.import(event)`.
- **Export:** calls `page.export()` or opens `AdvanceFilterModalComponent` when `page.pageConfig.IsRequiredDateRangeToExport`.
- **History:** detail Time Machine uses `page.enterHistoryView()` and `page.historyItems` / `historyIndex`; the toolbar opens `HistoryLogPopoverComponent` via `PopoverController`. Do **not** add `app-history-log-popover` (or equivalent) on the page.
- **History view:** when `page.pageConfig.isHistoryView`, the toolbar shows oldest/newer/picker/exit and calls `page.historyFirst`, `historyPrev`, `historyNext`, `historyLast`, `selectHistoryIndex`, `exitHistoryView`.
- **Mobile:** `ion-hide-md-up` overflow popover mirrors many actions; `@Input` `Show*` gates popover entries.

## Do not

- Import or declare `ToolbarComponent` in a page NgModule.
- Put `app-toolbar` in a modal popup header.
- Add separate history picker markup; the toolbar owns it.
- Recreate standard CRUD / approval buttons outside `app-toolbar` unless they are genuinely custom (use projection).
- Edit `toolbar.component.ts` / `.html` when the task is only to wire a page — change the page template and `pageConfig` / form children instead.

New UI strings: skill `i18n-keys`. New list/detail shell: skill `new-fe-crud-page`.
