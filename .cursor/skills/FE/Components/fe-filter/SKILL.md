---
name: fe-filter
description: >-
  Documents ART-ERP-FE app-filter: the recursive FilterConfig / Schema query
  builder (Dimension, Operator, Value, AND/OR Logicals). Use when adding or
  changing app-filter, FilterConfig trees, Transform.Filter, approval/PR/forecast
  rule filters, or report query-builder UI. Do not confuse with app-query-filter
  or app-data-table column filters.
---

# FE filter

Ionic + Angular NgModule (`standalone: false`). `app-filter` edits a nested `FilterConfig` tree against a `Schema` (fields become Dimension options). It is **not** the list-page column filter row and **not** `app-query-filter`.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/filter/filter.component.ts`, `filter.component.html`
- Types: `FilterConfig`, `Schema`, `SchemaDetail` in `ART-ERP-FE/src/app/interfaces/options-interface.ts`
- Declared/exported by `ShareVisualizationsModule` (`share-visualizations.modules.ts`). `ShareComponentsModule` / `ShareModule` re-export that module.
- Callers: `approval-rule-detail.page.html`, `forecast-detail.page.html`, `cycle-count-detail.page.html`, `pr-program-detail.page.html`, `pr-voucher-policy-detail.page.html`, `notification-segment-detail.page.html`, `advance-filter-modal.component.html`, `report-config.component.html`

Pages that already import `ShareModule` can use the selector. Do not redeclare `FilterComponent`. Do not edit `filter.component.*` when the task is only to wire a page — change the page template and the `Schema` / `FilterConfig` bindings.

## Not these siblings

| UI | Role |
| --- | --- |
| `app-filter` | Nested logical query builder → emits `FilterConfig` (`Dimension` / `Operator` / `Value` / `Logicals`). |
| `app-query-filter` | Report chrome: frequency, preset time range, company-branch toggles via `ReportService`. Separate component under `components/query-filter/`. No `FilterConfig`. Do not substitute for `app-filter`. |
| `app-data-table` filters | List column filters: `[showFilter]="pageConfig.isShowSearch"`, header cells `datatable-filter-cell`, mobile sheet `DataTableMobileFilterService`. Bound to page `query` / column fields — not `app-filter`. |

## Copy this

Inline on a detail page (live edits re-emit as `submit` via the `#appFilter` template ref — same pattern as forecast / approval / report-config):

```html
<app-filter
	#appFilter
	[schema]="schema"
	[item]="formGroup.get('_Filter').value"
	[smallWidth]="true"
	(change)="appFilter.onFormSubmit($event)"
	(submit)="saveConfig($event)"
></app-filter>
```

Modal with an explicit Apply button (cycle-count):

```html
<app-filter #appFilter [schema]="schema" [item]="config" [smallWidth]="true" (submit)="filterConfig($event)"></app-filter>
<!-- footer -->
<ion-button (click)="appFilter.onFormSubmit()">{{ 'Filter' | translate }}</ion-button>
```

`schema` must be a `Schema` with `Fields` (`Code`, `Name`, `DataType`, …). The UI is hidden until `_schema` is set (`*ngIf="_schema"` in the component template). Load the schema (e.g. `SYS_SchemaProvider`) before showing the control.

`item` is a `FilterConfig`. Omit or pass `null`/`undefined` → root `{ Dimension: 'logical', Operator: 'AND', Logicals: [] }`. A non-logical leaf is wrapped as a single child under a root `AND`.

Emitted payload (both `change` and `submit`) is always a root logical node: `{ Dimension: 'logical', Operator, Logicals }` (or a wrapped leaf). `UniqueId` is form-only and stripped before emit.

## `@Input` / `@Output` (source)

| Binding | Kind | Role |
| --- | --- | --- |
| `schema` | `@Input() set schema(s: Schema)` | Clones fields; prepends `{ Code: 'logical', Name: 'Logical' }` if missing. |
| `item` | `@Input() set item(i: FilterConfig)` | Seeds the form tree; rebuilds via `buildForm()`. |
| `smallWidth` | `@Input() smallWidth = false` | Adds host class `small-width`. |
| `change` | `@Output()` | Emits current tree after Dimension/Operator/Value edits (and after add/remove when `onInputChange` runs). Invalid form → emits `message` instead. |
| `submit` | `@Output()` | Same payload as `change`, from `onFormSubmit()` (form submit or page calling `appFilter.onFormSubmit()`). |
| `message` | `@Output()` | Validation toast payload, e.g. `{ message: 'Please recheck information highlighted in red above', logLevel: 'warning' }`. |

No content projection. Value editors are `app-input-control` inside the component; Dimension/Operator use `ng-select` appended to `#ng-select-filterComponent`.

Operators in source: logical `AND` / `OR`; transform set includes `=`, `like`, `<>`, `IN`, `NOT IN`, numeric compares, boolean `1`/`0` (grouped labels in the select). Value control type comes from `SchemaDetail.DataType` via `getSchemaDetailType`.

## Do not

- Use `app-filter` for ordinary list Search / column filters — use `app-data-table` `[showFilter]` and toolbar Search.
- Use `app-query-filter` when the page needs a `FilterConfig` / Schema query builder.
- Declare `FilterComponent` in a page NgModule; import `ShareModule` (or already-exported visualizations) instead.
- Invent inputs beyond `schema`, `item`, `smallWidth`.
- Skip `[schema]` — without it the builder does not render.

New UI strings: skill `i18n-keys`. Popup chrome around a filter modal: skill `fe-popup`.
