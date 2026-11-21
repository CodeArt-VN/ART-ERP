---
name: fe-card-multi-row
description: >-
  Places the ART-ERP-FE summary card app-card-multi-row: title, numeric value,
  and comparitionValue with a percent delta. Use when adding or changing a
  summary card, statistic row, or app-card-multi-row in ART-ERP-FE.
---

# FE card multi row

Ionic + Angular NgModule. `standalone: false`. A summary stat, not a chart. `.card-chart-preview` in the template is empty.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/visualizations/card-multi-row/card-multi-row.component.ts`
- Template: `ART-ERP-FE/src/app/components/visualizations/card-multi-row/card-multi-row.component.html`
- Caller: `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.html`
- Selected host style: `ART-ERP-FE/src/app/components/visualizations/report-chart/report-chart.component.scss` (`.statistic-row app-card-multi-row.selected`)
- Declared and exported by `ShareVisualizationsModule` in `share-visualizations.modules.ts`. `ShareComponentsModule` re-exports that module. `ShareModule` re-exports `ShareComponentsModule`.

A page that already imports `ShareModule` can use the selector. Do not declare `CardMultiRowComponent` again.

## Inputs and output

Copy these names. The comparison input is spelled `comparitionValue`.

| Binding | Kind | What the component does |
| --- | --- | --- |
| `title` | `@Input() title: any` | Text in `.card-header`. |
| `value` | `@Input() set value` | Stored on `_value` (default `0`). Rendered with the `numberFriendly` pipe. |
| `comparitionValue` | `@Input() set comparitionValue` | Stored on `_comparitionValue` (default `null`). When truthy, the template appends that figure and the percent. |
| `selected` | `@Input() selected: any` | Declared. The template and the class never read it. |
| `onChange` | `@Output() onChange` | `onClick(e)` emits the click argument. The template never calls `onClick`. |

`percent` is a getter, not an input:

`_comparitionValue ? ((_value - _comparitionValue) / _comparitionValue) * 100 : 0`

`0` is falsy, so a comparison value of `0` hides the delta and the percent is `0`.

When the comparison value is truthy, `ion-text` color is `success` if `percent > 0`, `danger` if `percent < 0`, and `warning` otherwise. The icon is `caret-up`, `caret-down`, or `warning` in that same order. The percent text uses the `number` pipe with digits `1.0-1`, then `%`.

`numberFriendly` (`friendly-format.pipe.ts`) prints `lib.currencyFormatFriendly(value)` when the value is numeric, and the raw value otherwise.

## Caller

Full mode in `report-chart` is the real binding. Selection is the host class `selected`, styled by the parent. The click is the host `(click)`, not `(onChange)`.

```html
<app-card-multi-row
	[title]="m.Title || m.Property"
	[value]="m.Value"
	[comparitionValue]="m.ComparitionValue"
	[ngClass]="{ selected: viewDimension == (m.Title || m.Property) }"
	*ngFor="let m of report.DataConfig.MeasureBy"
	(click)="onViewDimensionChange(m.Title || m.Property)"
></app-card-multi-row>
```

Dashboard summary cards in the same template pass the same three inputs and set `class="selected"` on every card. They do not bind a click.

Put the cards in a parent that owns the grid. `.statistic-row` in `report-chart.component.scss` is `display: grid` with `repeat(auto-fit, minmax(150px, 250px))`. The card component does not layout itself.

## Do not

- Invent an input. There is no color, icon, subtitle, series, or chart binding.
- Rename `comparitionValue` to `comparisonValue`.
- Bind `[selected]` and expect a highlight. Put class `selected` on the host.
- Bind `(onChange)` and expect the current template to emit. It does not call `onClick`.
- Edit `card-multi-row.component.ts` or its template to add an API.
- Set `standalone: true`.
