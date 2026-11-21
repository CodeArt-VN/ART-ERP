---
name: fe-report-chart
description: >-
  Documents ART-ERP-FE app-report-chart: BI report/dashboard chart host that
  loads ReportService data by reportId, shows measure cards, and delegates
  drawing to app-e-chart. Use when adding or changing a report chart widget,
  dynamic-report preview, dynamic-dashboard grid item, or app-report-chart in
  ART-ERP-FE. Do not reimplement the chart or invent chart bindings on the page.
---

# FE report chart

Ionic + Angular NgModule. `standalone: false`. Chart host for a `BIReport`, not the ECharts wrapper and not the report data-config editor.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.ts`
- Template: `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.html`
- Styles: `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.scss`
- Declared and exported by `ShareVisualizationsModule` in `share-visualizations.modules.ts`. `ShareComponentsModule` / `ShareModule` re-export that module.

A page that already imports `ShareModule` can use the selector. Do not declare `ReportChartComponent` again.

## Relate to

| Selector | Role vs `app-report-chart` |
| --- | --- |
| `app-e-chart` | Child renderer. Report-chart passes `chartType`, `chartScript`, `chartOption`, dimensions, series keys, and `rawData` / `comparitionData`. Do not put `app-e-chart` on the page for the same report. |
| `app-card-multi-row` | Child summary cards for `MeasureBy` (full mode and dashboard Summary card type). Skill `fe-card-multi-row`. |
| `app-report-config` | Sibling editor of `DataConfig` on the report detail page — not embedded here. |
| `app-filter` | Lives inside report-config / other editors — skill `fe-filter`. Not used in this template. |

## Callers

Only these two page templates:

```html
<!-- dynamic-report-detail.page.html — preview beside page title -->
<app-report-chart
	rightContent
	viewMode="full"
	*ngIf="item.DataConfig"
	[reportId]="item.Id"
	[data]="runTestData"
	(changeViewDimension)="onViewDimensionChange($event)"
	(chartClick)="onChartClick($event)"
	(dataChange)="onDataChange($event)"
></app-report-chart>
```

```html
<!-- dynamic-dashboard-detail.page.html — one widget per gridster item -->
<app-report-chart
	class="fullfill"
	viewMode="dashboard"
	[reportId]="i.IDReport"
	[gridItem]="i"
	(delete)="removeItem(i)"
	(openReport)="onOpenReport($event)"
	(widgetConfigChange)="onWidgetConfigChange($event)"
></app-report-chart>
```

`viewMode` is also a `@HostBinding('class')`, so the host gets class `full`, `mini`, or `dashboard`.

## Inputs and outputs

Copy these names.

| Binding | Kind | What the component does |
| --- | --- | --- |
| `reportId` | `@Input() set reportId` | Resolves `report` via `ReportService.getReport`, builds the TimeFrame form, seeds compare/measure/interval fields, optional fixed `chartType` / `chartOption`. Schedules `getReportData` and may emit `changeViewDimension`. |
| `data` | `@Input() set data` | Pushes a dataset straight into `updateDataset` (skips waiting on the subscription). Report detail uses this for `runTestData`. |
| `gridItem` | `@Input() set gridItem` | Dashboard gridster item. Syncs `Config.ChartDimension` with `viewDimension`; may call `onViewDimensionChange`. Required for dashboard Type / SummaryCards / delete tools. |
| `viewDimension` | `@Input()` | Active measure/compare dimension string passed through to `app-e-chart` and card selection. |
| `viewMode` | `@Input()` + host class | `'full' \| 'mini' \| 'dashboard'` (default `'dashboard'`). Controls title bar, statistic row, timeframe form, and which chart/cards show. |
| `changeViewDimension` | `@Output()` | Emits after measure card / popover dimension pick. |
| `chartClick` | `@Output()` | Forwards `app-e-chart` `(chartClick)`. |
| `dataChange` | `@Output()` | Forwards `app-e-chart` `(dataChange)`. |
| `delete` | `@Output()` | Dashboard popover Delete. |
| `openReport` | `@Output()` | Dashboard popover / title open — payload is the `BIReport`. |
| `widgetConfigChange` | `@Output()` | Emits `_gridItem` after Type, ChartDimension, or SummaryCards change. |
| `timeRangeChange` | `@Output()` | Emits `report.DataConfig.TimeFrame` after the full-mode time-frame control saves and reloads. |

Data path: `ngOnInit` subscribes to `rpt.regReportTrackingData(this._reportId)`, `rpt.reportConfigTracking`, and `EVENT_TYPE.TENANT.BRANCH_SWITCHED` (reload). `updateDataset` fills `rawData`, `comparitionData`, and per-measure `Value` / `ComparitionValue` sums for the cards.

Dashboard popover can switch `_gridItem.Config.Type` between `'Chart'` and `'Summary card'`. Chart mode shows `app-e-chart`; Summary card mode shows selected `app-card-multi-row` rows from `Config.SummaryCards`.

## Do not

- Invent chart series, option, or script inputs on `app-report-chart`. Those live on the report / `app-e-chart`.
- Mount `app-e-chart` or `app-card-multi-row` next to this host for the same report preview.
- Embed `app-report-config` or `app-filter` inside the chart template.
- Omit `[gridItem]` on dashboard widgets that need Type / dimension / delete behavior.
- Set `standalone: true`, or edit `report-chart.component.*` when the task is only to wire a page.
