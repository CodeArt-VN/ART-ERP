---
name: fe-data-table
description: >-
  Documents ART-ERP-FE list tables via `app-data-table` and `datatable-column`:
  page bindings, filter/sort/infinite scroll, selection, and cell templates. Use
  when adding or changing a datatable, list table, filter columns, row selection,
  or column markup in ART-ERP-FE. Do not reimplement the table or invent column
  APIs.
---

# FE data table

Ionic + Angular NgModule (`standalone: false`). Routed list pages put `app-data-table` in `ion-content` under `app-page-title`. Pages already import `ShareModule` → `ShareDataTableModule`; do not redeclare the table in a page module.

Canonical files:

- Component / module: `ART-ERP-FE/src/app/components/data-table/data-table.component.ts`, `.html`, `share-data-table.module.ts`, `directives/`
- List markup to copy: `ART-ERP-FE/src/app/pages/_template/flat/flat.page.html`
- Production list shell (NgModule / PageBase): `pages/WMS/zone/` — still legacy `section.table`; **do not** copy that table HTML for new `app-data-table` lists

Mobile filter sheet chrome lives in `data-table.component.html` (`ion-modal.form-1column` + `.edit-box`). When that sheet changes, skill `fe-popup` — do not duplicate popup chrome here.

Column width CSS tokens live in `ART-ERP-FE/src/theme/data-table.scss` (`.col-*`). Host layout helpers: `box-shadow`, `responsive`, `padding-number-right`, `small-width`.

## Copy this

From `_template/flat` (strip sample columns you do not need):

```html
<div class="safe-max-width">
	<app-data-table
		class="box-shadow responsive padding-number-right"
		[rows]="items"
		[trackBy]="'Id'"
		[(selectedRows)]="selectedItems"
		[showSpinner]="pageConfig.showSpinner"
		[showFilter]="pageConfig.isShowSearch"
		[(query)]="query"
		(dataInfinite)="loadData($event)"
		(filter)="onDatatableFilter($event)"
		(sort)="onSort($event)"
		(selectedRowsChange)="showCommandBySelectedRows($event)"
	>
		<datatable-column [checkbox]="true" name=""></datatable-column>
		<datatable-column class="col-id" name="#" property="Id" [navLink]="pageConfig.pageName"></datatable-column>
		<datatable-column class="col-date" format="yyyy-MM-dd" name="Required date" property="RequiredDate" filterControlType="date"></datatable-column>
		<datatable-column class="col-name flex-break" name="Title" property="Name"></datatable-column>
		<datatable-column class="col-number bold" format="1.0-0" name="Total" property="TotalAfterTax"></datatable-column>
		<datatable-column class="col-name" name="Name" property="Name">
			<ng-template let-i="row" datatable-cell-template>
				<div [routerLink]="['/'+pageConfig.pageName+'/'+i.Id]">
					<a class="bold"><ion-text color="dark">{{i.Name}}</ion-text></a>
				</div>
			</ng-template>
		</datatable-column>
	</app-data-table>
</div>
```

`PageBase` owns `items`, `selectedItems`, `query`, `pageConfig`, `loadData`, `onDatatableFilter`, `onSort`, `showCommandBySelectedRows`. Do not reimplement infinite scroll or filter submit on the page.

## `@Input` / `@Output` (page template)

| Binding | Role |
| --- | --- |
| `[rows]` | Row array (`items`). |
| `[trackBy]` | Property name for row identity (usually `'Id'`). |
| `[(selectedRows)]` | Selected rows ↔ `selectedItems`. |
| `(selectedRowsChange)` | Fires after selection change (wire `showCommandBySelectedRows`). |
| `[showSpinner]` | Loading state (`pageConfig.showSpinner`). Built-in empty/spinner UI. |
| `[showFilter]` | Shows desktop inline filter row (`pageConfig.isShowSearch`). |
| `[(query)]` | List query object; filter form merges into it on submit. |
| `(filter)` | Filter submitted → `onDatatableFilter($event)`. |
| `(sort)` | Sort changed → `onSort($event)` (unless `isQueryLocalOnly`). |
| `(dataInfinite)` | Next page → `loadData($event)`. Disabled when local-only, virtual scroll off, or end of data (from `query.Take` + row growth). |

Other inputs exist on the component (`mobileFilter`, `isTreeList`, `isQueryLocalOnly`, `virtualScroll*`, `editable`, `minHeight`, `columns`) — use only when a nested/modal/editable table already needs them. Do not invent new outputs.

Nested tables that must keep the inline filter row: `[mobileFilter]="false"`.

## `datatable-column`

Selector `datatable-column` (`DataTableColumnDirective`). Declared inside `app-data-table`.

| Attr | Role |
| --- | --- |
| `checkbox` | Selection column; empty `name`. |
| `name` | Header label (translate key). |
| `property` | Row field (`Id`, `Name`, nested path). |
| `navLink` | Default cell becomes `routerLink` `/{navLink}/{row.Id}`. |
| `class` | Width/layout token(s), e.g. `col-id`, `col-name`, `col-code`, `col-status`, `col-remark`, `col-date`, `col-number`, `col-money`, `col-icon`, `col-icon large`, `flex-break`. |
| `format` | Display pipe hint: `1.0-0` → number; `yyyy-…` / `HH` → date; else string. |
| `filterControlType` | Filter control: `text` (default), `number`, `date`, `datetime-local`, `ng-select`, `ng-select-status`, `ng-select-bp`, `ng-select-item`, `time-frame`, plus other union values on the directive. |
| `filterDataSource` | Options for `ng-select*`. |
| `filterBindValue` / `filterBindLabel` | Option bind keys (defaults `Id` / `Name` when resolving chips). |
| `canSort` / `canFilter` | Defaults `true`. Set `false` to disable. |
| `minWidth` / `width` / `maxWidth` | CSS length or px number; unset keeps `.col-*` defaults. |
| `sticky` | Sticky column. |
| `dataType` | Rare override; cell usually infers from `format`. |
| `editable` / `editor` / `editorField` | Only with table `[editable]="'always'"`. |

Disable a column filter without `[canFilter]="false"`: empty `<ng-template datatable-filter-template></ng-template>`.

## Cell / header / filter templates

Projected `ng-template` attrs on a column:

| Attr | Context |
| --- | --- |
| `datatable-cell-template` | `let-i="row"` (also `idx`, selection in cell context). |
| `datatable-header-template` | Custom header cell. |
| `datatable-filter-template` | Custom filter cell / empty to hide filter. |

Optional empty state: `<datatable-empty-message>` with `datatable-empty-message-template` inside the table (overrides built-in `app-page-message`).

## Must

- Use `app-data-table` + `datatable-column` for new list UIs (skill `new-fe-crud-page`).
- Keep the flat host bindings for CRUD lists (`rows` / `trackBy` / `selectedRows` / `showSpinner` / `showFilter` / `query` / `dataInfinite` / `filter` / `sort` / `selectedRowsChange`).
- Prefer `.col-*` classes over one-off widths.
- Column `name` strings: English translate keys — skill `i18n-keys`.
- Put `class="clickable"` (`theme/common.scss`, `cursor: pointer`) on every element that is not an `ion-button` and reacts to `(click)` or `routerLink`: name text, icon, chevron, header toggle, the `div` around a name cell. `ion-button` already shows a pointer. Check both the list and the detail page.

## Must not

- Import or declare `DataTableComponent` / `ShareDataTableModule` in a page NgModule.
- Copy `pages/WMS/zone/` `section.table` markup for new lists.
- Copy `pages/VMS/` table markup as the default pattern.
- Add a page-level filter popup; the table owns the mobile sheet — skill `fe-popup`.
- Pass an infinite-scroll disable `@Input` (there is none; end-of-data is derived).
- Edit `data-table.component.*` when the task is only to wire a page.
- Invent `@Input` / `@Output` / column attrs not present in source.
- Add `flex-break` to the Name column. It forces the column onto its own row, so Name no longer sits beside the ID. Use it only on a column that must wrap under the others.
- Add `padding-number-right` to a list without a numeric last column. The responsive theme gives each row `padding-right: 110px` with that class.
- Hand-style a pill, badge or chip with spans. Use `ion-chip` or `ion-badge`.
- Add a page-specific rule to `src/theme/data-table.scss`. That file applies to every table.

## Cell content

- Name cell: bold name on the first line. Each secondary line (remark, status, badges) is its own `<p>`. The theme gives `.cell p` `margin: 8px 0`. Do not add a margin to `<p>` on the page.
- Put several chips or badges on one line inside one `<p>`. Separate them with `class="ion-margin-start"` on the second item.
- Checkbox and ID cells are centred vertically (`.cell` uses `align-items: center`). In responsive mode they align to the top so they line up with the Name text. Do not add top alignment to other columns.

## Chips and badges in cells

- Outline pill (status, timing): `<ion-chip outline [color]="...">` with an optional `<ion-icon>` and `<ion-label>`. Inside a table the theme sets height 24px, radius 3px, font 12px, and icon `margin-inline-end: 4px`.
- Solid status: `<ion-badge [color]="...">`. The theme sets `font-weight: normal`.
- Colours: `primary` for the default state, `success` for a positive state, `danger` for lost or failed, `warning` for won or pending. Do not invent other colours.
- Do not override height, font weight or padding on these components from a page.
- A status is one `ion-badge [color]="..."`. The colour is the only difference between statuses. Do not add a class per status (`badge-open`) and do not hide one status while another shows: if the badge is hidden at a width, hide every status.

## Parent and child rows (tree)

Show parent and child records (stage and its tasks) in one `app-data-table` with `[isTreeList]="true"`, not in a custom accordion or card list. Build one flat array: parent rows have `IDParent: null`, child rows point at their parent through `IDParent`. Parent and child Ids can overlap, so prefix them (`'S' + id`, `'T' + id`) and keep the source row on `Stage` / `Task`. Run the array through `buildFlatTree` (PageBase) and pass the previous rows so open and closed parents survive a reload. Reference: `pages/CRM/pipeline-detail/pipeline-config.util.ts` (`buildStageRows`).

Name cell, in this order: indent `span.spacing` per level, chevron `ion-icon.min-btn.clickable` when the row has children, then the type chip, name `span.clickable` (parents also `bold`), then the secondary chips. Header: `+/-` icon with `min-btn clickable` toggles every parent.

## Child table on a detail tab

- Header of the actions column holds icon-only `ion-button size="small" fill="clear"`: add (`add-circle-outline`), then reorder (`swap-vertical-outline`, only when there is more than one row). No text button above the table, and no `ion-padding` `div` around it.
- Every row ends with the same icon-only buttons in `div.row-actions`: add child (parent rows only) and edit (`create-outline`). The name `span.clickable` opens the same popup as edit. Edit and add open a sheet popup (skill `fe-popup`), never a routed or full-screen page.
- Sort is drag and drop in a popup (skill `fe-popup`, Child list inside a popup), not a number column.
- Do not show `Code`, dates, numeric fields or other technical values as their own columns. Show only what picks the row out, inline with the name: type icon, state chip, one short value chip. The popup holds the rest.

## Narrow screens (card mode)

`responsive` turns rows into cards at ≤1164px (`max-width: calc(1164px + 0px)` in `data-table.scss`). On a page table keep one line per row:

- Keep the header visible when it holds the add and reorder buttons (the theme hides it in card mode).
- A chip that has an icon and a text becomes a bare icon: no background, no padding, no radius, no `ion-icon` margin, 16px box. Place it before the name (`order: 1`, name `order: 2`). When it is the only content, do not leave a right padding; the icon box is the whole chip.
- Required marker: only the red `*`, no background, after the name (`order: 3`).
- Under 425px hide the secondary chips and let the name take the row. Do not hide the name; truncate it with an ellipsis only when the chips leave no room.
- Card rows keep the height they have on desktop. Desktop row height comes from the 28px edit button; in card mode that button is `position: absolute`, so give the name cell `min-height: 28px` with `box-sizing: content-box`, and give the icon-only chip and its icon `height` and `line-height` of 28px. Stage rows (padding 8px) are then 45px and task rows (padding 2px) 33px at every width.
- Put this CSS in the page SCSS under `:host ::ng-deep app-data-table.<page-class>`. Reference: `pages/CRM/pipeline-detail/pipeline-detail.page.scss`.

## Table inside a card or tab

A detail tab with its own table already sits in a card (`row-full shadow`). The `responsive` mixin then adds a second inset. At ≤1164px it sets on `app-data-table`: `padding-inline: 16px`, `display: flex; flex-direction: column; gap: 16px` (the gap between header and body), and on `datatable-body`: `gap: 16px`, `padding-bottom: 16px`. Set `padding-inline: 0`, `gap: 0`, and on `datatable-body` `gap: 0` and `padding-bottom: 0` in the page SCSS so the header, rows and card edge touch. Do not change `data-table.scss`.

## Global theme

- `src/theme/data-table.scss` affects every `app-data-table`. Column width tokens (`.col-*`) can be changed there. Any other change is global.
- Before reporting a change to that file, open at least two other list pages in the browser at desktop width and at 908px. Check row height, cell alignment and chip size.

## Verify before reporting

- Measure in the browser with `getBoundingClientRect` at desktop width (≥1200px) and at 908px. Record row padding, cell top positions and chip height.
- Take a screenshot at each width. A list is not done until both are checked.
- Card-mode CSS only applies at ≤1164px. Keep device emulation on (`Emulation.setDeviceMetricsOverride`, for example 1100 and 480) while you measure, and clear it when done. Measuring at the desktop width proves nothing about card rules.
- At 1100px and 480px compare row heights with desktop for every row kind, and check that header bottom equals body top, that the table edge equals the header and row edge, and that the last row touches the table bottom. Do not report until the numbers match.
- Open the table with the longest text and check the name is not cut to a letter while the right side is empty.
