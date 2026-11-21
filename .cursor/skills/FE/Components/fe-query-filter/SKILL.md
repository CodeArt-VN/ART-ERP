---
name: fe-query-filter
description: >-
  Documents ART-ERP-FE app-query-filter: BI report sidebar for group-by
  frequency, time presets, and company-branch toggles via ReportService
  rptGlobal. Use when adding or changing a report query filter panel,
  app-query-filter markup, or wiring changeFrequencyComp /
  changeDateFilterComp / toogleBranchDatasetComp. Do not use for app-filter
  schema builders or app-data-table column filters.
---

# FE query filter

Ionic + Angular NgModule (`standalone: false`). Report feature panel for **Group by** (frequency), **Time** (presets + optional date range), and **Branch** (company buttons). Not a list/detail CRUD filter.

`ShareComponentsModule` declares and exports `QueryFilterComponent`; `ShareModule` re-exports it. Pages that import `ShareModule` can use the selector. Do not redeclare `QueryFilterComponent` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/query-filter/query-filter.component.ts`, `query-filter.component.html`
- Module: `ART-ERP-FE/src/app/components/share-components.module.ts`

**Grep note:** no routed page template currently embeds `<app-query-filter>`. Closest live UI is the inlined Group by / Time block in BI report feature fabs (same `rpt.rptGlobal` pattern), e.g. `ART-ERP-FE/src/app/pages/BI/SALE/sales-reports/sales-reports.page.html` and `ART-ERP-FE/src/app/pages/BI/PURCHASE/purchase-reports/purchase-reports.page.html`. Prefer the component below instead of copying that inline markup.

## Copy this

Host binding (only public API; no `@Input`):

```html
<app-query-filter
	(changeFrequencyComp)="changeFrequency($event)"
	(changeDateFilterComp)="changeDateFilter($event)"
	(toogleBranchDatasetComp)="toogleBranchDataset($event)"
></app-query-filter>
```

Place it in the report feature panel (same role as the inlined filter inside `ion-fab.feature` on sales-reports). Keep page handlers named to match the payloads below; the component only emits — it does not call `ReportService.dateQuery` or toggle `IsHidden` itself.

The template reads and two-way-binds `rpt.rptGlobal` through the injected `ReportService` (`rpt`):

- Frequency buttons: `rpt.rptGlobal.frequency` vs `rpt.rptGlobal.query.frequency`
- Time presets / Options: `rpt.rptGlobal.query.type`, `fromDate`, `toDate`
- Branch buttons: local `reportBranchList` (companies from `env.branchList`)

Parent must update `rpt.rptGlobal.query` (and branch visibility) on each output so the solid/outline fills stay correct.

## vs `app-filter` and datatable filters

| Control | Role |
| --- | --- |
| `app-query-filter` | BI report query chrome: frequency, date presets, company branch toggles on `rpt.rptGlobal`. |
| `app-filter` | Schema / `FilterConfig` rule builder (`[schema]`, `[item]`, `(submit)`). Used on detail config screens (e.g. PR program, cycle-count). Not for report time/branch. |
| `app-data-table` filters | Column `canFilter` / `filterControlType` / `filterValue`; `(filter)` and `(filterInputChange)`. List query, not `rptGlobal`. |

Do not swap these selectors. Do not put `app-query-filter` on a flat CRUD list to replace the datatable filter row.

## `@Output` (page template)

There are **no** `@Input` bindings on `app-query-filter`.

| Output | Payload from source | When |
| --- | --- | --- |
| `changeFrequencyComp` | Frequency row from `rpt.rptGlobal.frequency` (`f` with `Id`, `Name`) | User clicks a Group by button. |
| `changeDateFilterComp` | String type: `'d'`, `'dw'`, `'dm'`, `'m'`, `'m3'`, `'m6'`, `'my'`, `'q'`, `'q2'`, `'q3'`, `'qy'`, `'y'`, `'y2'`, `'y3'`, `'set'`, or `'setdone'` | User clicks a Time preset, Options, or changes a custom date input. |
| `toogleBranchDatasetComp` | Branch object from `reportBranchList` (typo `toogle` preserved in source) | User clicks a company Branch button. |

## Behavior (owned by the component)

- Extends `PageBase`; injects `BRA_BranchProvider`, `ReportService` as `rpt`, `EnvService`.
- Builds `reportBranchList` = `env.branchList` where `Type == 'Company'`, assigns colors, `ShowBtn` / `IsHidden` / `IsHiddenDetailColumn`.
- On `EVENT_TYPE.TENANT.BRANCH_SWITCHED`, `changeBranchBtn()` shows all company buttons when `env.selectedBranch == 16`, otherwise only the selected company.
- Custom range: when `query.type == 'set'`, two `<input type="date">` bind `[(ngModel)]` to `rpt.rptGlobal.query.fromDate` / `toDate` and emit `'setdone'` on `(change)`.

## Do not

- Invent `@Input`s (`page`, `filter`, `schema`, `item`, etc.).
- Rename `toogleBranchDatasetComp` to “toggle…”.
- Use this for SYS schema filters (`app-filter`) or list column filters (`app-data-table`).
- Declare `QueryFilterComponent` again in a page NgModule.
- Edit `query-filter.component.ts` / `.html` when the task is only to wire a report page — bind the three outputs and update `rpt.rptGlobal` in the page (or call `rpt.dateQuery`).

New UI strings: skill `i18n-keys`.
