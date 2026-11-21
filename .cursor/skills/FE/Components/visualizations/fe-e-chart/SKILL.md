---
name: fe-e-chart
description: >-
  Documents ART-ERP-FE app-e-chart (Apache ECharts host): chartType modes,
  chartOption / data / comparitionData, chartScript, and chartClick. Usually
  wrapped by app-report-chart; use directly only for page-owned manual options.
  Use when adding or changing an e-chart, report chart series, or pie/bar host
  in ART-ERP-FE. Do not reinvent echarts.init on the page.
---

# FE e-chart

Ionic + Angular NgModule. `standalone: false`. `app-e-chart` is a thin ECharts host: one full-height `div`, lazy-loads `echarts`, `setOption` on changes, resize via `ResizeObserver`. It is not the BI report shell — that is `app-report-chart`.

Declared and exported by `ShareVisualizationsModule` (`share-visualizations.modules.ts`). `ShareComponentsModule` / `ShareModule` re-export that module. A page that already imports `ShareModule` can use the selector. Do not declare `EChartComponent` again.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/visualizations/types/e-chart/e-chart.component.ts` (inline template only; no separate `.html`)
- Option helpers (ReportService): `ART-ERP-FE/src/app/components/visualizations/types/e-chart-option.ts`
- Wrapper (preferred for BI): `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.html`
- Direct callers: `ART-ERP-FE/src/app/pages/SHIP/delivery-review/`, `ART-ERP-FE/src/app/pages/BI/SALE/sale-summary-mobile/`

## When to use which

| Need | Use |
| --- | --- |
| Dynamic report / dashboard tile (schema, measures, timeframe, cards, click drill) | `app-report-chart` — it already hosts `app-e-chart` |
| Page builds a full ECharts option itself (pie, fixed series) | `app-e-chart` directly with `chartType="manual"` and `[chartOption]` |

Do not nest `app-e-chart` inside a page that already has `app-report-chart` for the same series. Do not call `echarts.init` on the page.

## Host size

Template height is `100%`. Parent must give a real height (report-chart uses `class="app-chart"`). Without a sized ancestor the chart collapses.

## Inputs and outputs

Copy these names. Comparison data is spelled `comparitionData`.

| Binding | Kind | Default | Role |
| --- | --- | --- | --- |
| `chartType` | `@Input` | `'auto'` | Option path: `auto` \| `bar` \| `line` \| `fixed` \| `manual` (see below). |
| `viewMode` | `@Input` | — | `'full' \| 'mini' \| 'dashboard'`. Passed into ReportService option builders for `auto` / `fixed`. |
| `chartOption` | `@Input` | `{}` | ECharts option object. Merged on change via `Object.assign`. Used as-is for `manual`; merged/updated for `bar`/`line`/`fixed`. |
| `dimensions` | `@Input` | `[]` | Passed to `getChartOption` when `chartType === 'auto'`. |
| `viewDimension` | `@Input` | — | Declared. Not read in `updateChart`. |
| `compareBy` | `@Input` | `[]` | Declared. Not read in `updateChart`. |
| `measureBy` | `@Input` | `[]` | Declared. Not read in `updateChart`. |
| `dataIntervalProperty` | `@Input` | — | Time/bucket property for `auto`. |
| `dataIntervalType` | `@Input` | — | Interval type for `auto`. |
| `chartScript` | `@Input` | — | Optional JS string run after the base option is built (`eval` with syntax + blacklist checks). Mutates `option` in place via the script. |
| `data` | `@Input` | `[]` | Series rows for `auto` (`getChartOption` only when `data.length`). |
| `comparitionData` | `@Input` | `[]` | Comparison rows for `auto`. |
| `chartClick` | `@Output` | — | ECharts `click` payload. |
| `dataChange` | `@Output` | — | Declared (`outData`). Nothing in the component calls `outData`; report-chart still binds it. |

### `chartType` paths

| Value | What `updateChart` does |
| --- | --- |
| `auto` | If `data.length`, `rpt.echartDefaultOption.getChartOption(...)`. |
| `bar` / `line` | `updateSeriesByDimension(chartOption, chartType, chartOption.dataset['dimensions'])`, then use `chartOption`. |
| `fixed` | `mergeDefaultChartOption(chartOption, viewMode)`. |
| `manual` | Use `chartOption` as-is (direct page callers). |

Then, if `chartScript` is set, `calcChartOption` runs. Finally `chart.setOption(finalChartOption, true)`.

## Prefer wrapper: report-chart

Full binding from `report-chart.component.html`:

```html
<app-e-chart
	class="app-chart"
	*ngIf="(viewMode != 'dashboard' || (viewMode == 'dashboard' && _gridItem?.Config?.Type == 'Chart')) && rptLoaded && (rawData.length || report.DataConfig.Schema.Id == null)"
	[viewMode]="viewMode"
	[chartType]="chartType"
	[chartScript]="chartScript"
	[chartOption]="chartOption"
	[dimensions]="dimensions"
	[viewDimension]="viewDimension"
	[compareBy]="compareBy"
	[measureBy]="measureBy"
	[dataIntervalProperty]="dataIntervalProperty"
	[dataIntervalType]="dataIntervalType"
	[data]="rawData"
	[comparitionData]="comparitionData"
	(chartClick)="onChartClick($event)"
	(dataChange)="onDataChange($event)"
></app-e-chart>
```

Pages like dynamic-report-detail and dynamic-dashboard-detail bind `app-report-chart`, not `app-e-chart`.

## Direct use: manual option

Page owns the ECharts option. Toggle recreate with `*ngIf` when the option must fully remount (delivery-review clears `chartView` then restores it).

```html
<div class="c-box">
	<app-e-chart *ngIf="!chartLoading" [chartOption]="chartOption" chartType="manual"></app-e-chart>
</div>
```

```ts
chartOption = {
	tooltip: { trigger: 'item' },
	series: [{ type: 'pie', radius: ['40%', '70%'], label: { show: false }, color: [], data: [] }],
};
// mutate series[0].data / color, then flip *ngIf or rely on ngOnChanges + Object.assign
```

Callers: `delivery-review.page.html`, `sale-summary-mobile.page.html`.

## Behavior (do not reimplement)

- **Lib load:** `thirdPartyLibs.echart.source` via `DynamicScriptLoaderService`; then `echarts.init` on `#elId` (`lib.generateCode()`).
- **Resize:** `ResizeObserver` → `chart.resize()`.
- **Destroy:** `chart.dispose()` in `ngOnDestroy`.
- **Script safety:** `chartScript` must parse as JS; blacklist blocks `document.cookie`, storage, `fetch`, `eval`, etc. Errors go through `env.showMessage`.

## Do not

- Invent inputs (no `height`, `theme`, or series arrays outside `chartOption` / `data`).
- Rename `comparitionData` to `comparisonData`.
- Expect `viewDimension` / `compareBy` / `measureBy` to drive the chart from this component alone — report-chart owns those; e-chart does not read them in `updateChart`.
- Rely on `(dataChange)` from the current component body — it never emits.
- Edit `e-chart.component.ts` to add an API when the task is only wiring a page.
- Set `standalone: true` or call `echarts.init` on the page.
- Put a second `app-e-chart` under `app-report-chart` for the same report.

Option builders live in `e-chart-option.ts` / `ReportService.echartDefaultOption`. Summary cards beside the chart: skill `fe-card-multi-row`.
