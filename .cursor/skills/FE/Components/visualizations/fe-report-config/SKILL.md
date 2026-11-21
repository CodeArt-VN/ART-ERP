---
name: fe-report-config
description: >-
  Documents ART-ERP-FE app-report-config: BI report DataConfig editor (schema,
  time frame, interval, compare/measure, Transform filter via app-filter) plus
  Run/Save/Export and optional Ace chart script panels. Use when adding or
  changing report config on dynamic-report detail, wiring reportId /
  canChangeReportConfig / runReport / save, or relating to app-report-chart.
  Do not reimplement the data-source form or confuse with app-query-filter.
---

# FE report config

Ionic + Angular NgModule (`standalone: false`). Feature-panel editor for a BI report’s `DataConfig` (and optional chart scripts). Sibling of `app-report-chart` on the same detail page: config emits a `BIReport`; the page saves/runs and feeds results into the chart.

Declared and exported by `ShareVisualizationsModule` (`share-visualizations.modules.ts`). `ShareComponentsModule` / `ShareModule` re-export it. Pages that import `ShareModule` can use the selector. Do not redeclare `ReportConfigComponent` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/visualizations/report-config/report-config.component.ts`, `report-config.component.html`
- Module: `ART-ERP-FE/src/app/components/visualizations/share-visualizations.modules.ts`
- Caller: `ART-ERP-FE/src/app/pages/BI/dynamic-report-detail/dynamic-report-detail.page.html` (only live `<app-report-config>` usage)
- Types: `BIReport`, `ReportDataConfig` in `ART-ERP-FE/src/app/interfaces/options-interface.ts`
- Service load: `ReportService.getReport(reportId)` (`services/custom/report.service.ts`)

## Copy this

Feature fab on dynamic-report detail (same pattern as the live page):

```html
<app-report-config
	*ngIf="item.Id"
	[canEdit]="pageConfig.canEdit"
	[canExport]="pageConfig.canExport"
	[canChangeReportConfig]="pageConfig.canChangeReportConfig"
	[canEditScript]="pageConfig.canEditScript"
	[reportId]="item.Id"
	(runReport)="onRunReport($event)"
	(exportData)="onExportData()"
	(save)="onSave($event)"
></app-report-config>
```

Place it in the report feature panel (`ion-fab` / accordion), not as the chart itself. Keep `app-report-chart` on the content area with the same `reportId` (and page-supplied `data` after Run).

`[reportId]` is a setter: loads a clone via `rpt.getReport(id)`, builds the reactive `form` from `_report.DataConfig`, and seeds schema search / fields. Without a matching report in `ReportService`, the template’s `*ngIf="_report"` stays empty.

## vs chart and filters

| Control | Role |
| --- | --- |
| `app-report-config` | Edit `DataConfig` + Run/Save/Export; optional Ace `ChartConfigScript` / `ChartScript`. |
| `app-report-chart` | Render chart/cards from report id and/or injected `data`. Does not own the config form. |
| `app-filter` | Embedded inside report-config for `Transform.Filter` (skill `fe-filter`). |
| `app-query-filter` | Frequency / time presets / company branch on `rpt.rptGlobal` (skill `fe-query-filter`). Not this selector. |

Do not swap `app-report-config` for `app-query-filter`. Do not paste a second `app-filter` on the page for the same Transform tree — the component already wires it.

## `@Input` (page template)

| Input | Default | Role |
| --- | --- | --- |
| `reportId` | — | Setter: load report into `_report` and `buildForm(DataConfig)`. |
| `canEdit` | `false` | Shows Save; page still gates persistence. |
| `canExport` | `false` | Shows Export button (`exportData`). |
| `canChangeReportConfig` | `false` | Enables schema, time field, interval, CompareBy, MeasureBy, and Transform/`app-filter`. Time range / Compare to still show when Dimension is set. |
| `canEditScript` | `false` | Shows Ace accordion panels for chart config script and ChartScript. |

## `@Output` (page template)

| Output | Payload | When |
| --- | --- | --- |
| `runReport` | `BIReport` (`_report` after `updateDataConfig`) | Run, or Apply on Interval/CompareBy/MeasureBy popover. |
| `save` | `BIReport` | Save. |
| `exportData` | (void) | Export — page owns CSV / download. |

Canonical page handlers (`dynamic-report-detail.page.ts`): `onRunReport` → `saveReportConfig` + `runTestReport` → set `runTestData` / table; `onSave` → write `DataConfig` / `ChartConfig` / `ChartScript` into `formGroup` and `saveChange`; `onExportData` → CSV from `items`.

## Behavior (do not reimplement on the page)

- Form groups: `Schema`, `TimeFrame` (From/To), `CompareTo`, `Interval`, `CompareBy` / `MeasureBy` (`FormArray`), `Transform.Filter`.
- Schema change loads `SYS_SchemaProvider.getAnItem` → `selectedSchema` / `_schemaDetailsList` for field pickers and `app-filter`.
- Popovers edit Interval / CompareBy / MeasureBy chips; Apply updates `_report.DataConfig` and emits `runReport`.
- Ace editors (when `canEditScript`) sync into `_report` on Run/Save via `rpt.updateChartConfigFromScript` and `ChartScript`.
- Sticky actions: always Run; Export if `canExport`; Save if `canEdit`.

## Do not

- Redeclare `ReportConfigComponent` in a page NgModule.
- Invent inputs like `config`, `form`, or `page` — only the bindings above.
- Duplicate schema / CompareBy / MeasureBy / Transform UI outside `app-report-config`.
- Use this for list CRUD filters or `app-query-filter` time/branch chrome.
- Edit `report-config.component.ts` / `.html` when the task is only to wire a page — bind inputs/outputs and handle Run/Save/Export on the page.

New UI strings: skill `i18n-keys`. Nested query builder: skill `fe-filter`. Chart host: `app-report-chart` under the same `visualizations/` folder.
