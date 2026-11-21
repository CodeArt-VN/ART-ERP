---
name: create-dynamic-report
description: >-
  Creates or edits ART-ERP Dynamic BI reports (DataConfig, ChartScript,
  ChartConfig) via ART MCP. Use when the user asks to create/save/edit a
  Dynamic Report, ChartScript, status pie/bar, mini dashboard chart, report
  colors/translate, or report_set_chart / report_create / report_upsert.
---

# Create / edit Dynamic Report

Read this skill **before** writing ChartScript or calling `report_create` / `report_upsert` / `report_set_chart`.

MCP first: `report_ui_guide` (save) · `report_chart_guide` (chart) · ECharts option docs. Do not dig the FE codebase for chart APIs.

Related FE skills (host widgets only): `fe-report-chart`, `fe-e-chart`, `fe-report-config`, `i18n-keys`.

## Intent (do not skip)

| User wants | Do |
| --- | --- |
| Numbers / stats / “xem report” tạm | `bi_query` only — **do not** `report_create` |
| Explicit create / save / edit Dynamic Report | Header + DataConfig (+ chart) via MCP |

Ambiguous timeframe → ask once. Relative phrases (`today`, `hôm qua`, `last N days`) → Relative timePreset — **never** invent Absolute YYYY-MM-DD.

## Workflow

```
Task:
- [ ] Intent: bi_query vs persist
- [ ] schema_list / schema_get (+ branch_resolve if named)
- [ ] report_ui_guide (when saving)
- [ ] Confirm DataConfig with user if ambiguous
- [ ] report_create / report_upsert
- [ ] report_chart_guide → ChartScript (prefer) or ChartConfig
- [ ] Status color + translate if CompareBy is Status*
- [ ] Mini-safe ChartScript if used on dashboard
- [ ] i18n keys for every SYS_Status.Name used
- [ ] Paste viewUrl to user
```

After create/save: always send clickable `viewUrl` from the tool response (or `report_view_link`). Formula `{FE_ORIGIN}/V{latestVersion}/#/dynamic-report/{Id}` — do not hardcode version.

## DataConfig map

| Phrase | Path |
| --- | --- |
| group by / theo chi nhánh | `CompareBy[]` — **no** `GroupBy` field |
| sum / count / measure | `MeasureBy[]` + `Method` |
| data from | `Schema` (`DBTable\|DBView\|…` from `schema_get`, never `"Dataset"`) |
| time column | `TimeFrame.Dimension` |
| time range | `TimeFrame.From` / `To` |
| chart bucket | `Interval` |
| filter | `Transform.Filter` |
| prior period | `CompareTo` |

Prefer header schemas for order totals (`SALE_Order`), not `*Detail`, unless the metric needs detail rows.

Header when saving: `Name` required; `Icon` + `Color` **only** from MCP icon-color list (Ionic tokens, not hex).

## Chart fields

| Field | Use |
| --- | --- |
| `ChartScript` | Default for tweaks: type, stack, pie, mini, colors, translate, tooltip |
| `ChartConfig` | Full custom `option = { … }` only when Script is not enough (`series` → fixed mode) |

Eval context (ChartScript): `option`, `this.chart`, `this.env`, `this.viewMode`, `li` (= `lib`), `ec` (= echarts).

Helpers: `li.currencyFormatFriendly`, `li.findStatusInList`, `li.resolveIonColorCss`, `li.chartTextColor`, `li.applyStatusColorsToPieOptionFromList`.

Async ChartScript **must** end with `this.chart.setOption(option, true)` after promises (same pattern as `getType` scripts).

Forbidden in ChartScript: `eval`, `fetch`, `localStorage`, `document.cookie`, `require`, `import()`.

**Do not** add chart helpers on `env.service` — use `env.getStatus` / `env.translateResource` + `li.*` only.

## Status charts (mandatory rules)

When `CompareBy` is `Status` / `ShipmentStatus` (or pie by status):

1. **Color** — from `SYS_Status.Color` / `BadgeColor` via `li.resolveIonColorCss`. **Never** hardcode hex per status.
2. **Translate** — `env.translateResource(row.Name || row.Code)`.  
   - `SYS_Status.Name` **must** be the English i18n key (same as UI `{{ _Status.Name \| translate }}`).  
   - **Do not** translate with Code-first to “fix” Vietnamese Names — fix/ensure `Name` is English instead.
3. **Lookup** — `env.getStatus('SalesOrder' | 'ShipmentStatus' | …)` then `li.findStatusInList(list, seriesOrSliceName)`.
4. **i18n** — every `Name` key in both `en-US.json` and `vi-VN.json`. VI value must match the **previous display label** users knew (exact old Vietnamese string). If SO and SHIP shared a Code but had different old Names, give them **distinct** English `Name` keys so both VI strings can exist. Do not overwrite shared UI keys (`Debt`, `Picking`, `Packing`) when they mean something else elsewhere — use a status-specific English Name.
5. Theme — prefer CSS / `li.chartTextColor()`; mute axis/grid via existing e-chart defaults, not bright hardcoded greys.

Canonical scripts: report **28** (shipment pie + mini + center total), **3** (SO stacked bar + status + tooltip Total), **5** (gauge mini). Copy patterns from [chartscript-patterns.md](chartscript-patterns.md).

## Mini (`viewMode === 'mini'`)

If the report can appear as a dashboard mini card, ChartScript **must** handle mini (auto option is overwritten by Script):

- Hide legend / toolbox / (usually) labels.
- Pie: thin ring **only in mini** (e.g. `radius: ['72%','88%']`); full mode keeps a normal donut.
- Gauge: compact center / thinner axis in mini only.
- Bar: tighter `grid`, often hide tooltip clutter.
- Center total text: smaller `fontSize` in mini; use `li.chartTextColor()` for fill.

## Confirm before risky edits

- Changing many `SYS_Status.Name` rows or prod DB → confirm tenant/DB and mapping with the user.
- Prefer editing the DB the user named (e.g. `IN-ERP-Dev`); do not push prod unless asked.
- After status Name changes: FE caches `SYS_Status` — user may need logout/login or clear storage.

## Do not

- Create a report when the user only asked for ad-hoc numbers.
- Hardcode status colors or invent Ionic color tokens.
- Prefer `Code` over `Name` for `translateResource` when `Name` is the product convention.
- Put Vietnamese into `SYS_Status.Name` or into i18n keys.
- Edit `env.service.ts` for chart status/translate helpers.
- Open a second FE/BE process that is already listening (see run-local rule).

## Done checklist

- [ ] DataConfig matches schema fields / clarify Status values
- [ ] ChartScript async + `setOption` if using `getStatus` / `translateResource`
- [ ] Mini branch if dashboard use is likely
- [ ] Status color from SYS_Status; labels via `Name` i18n
- [ ] i18n both locales; VI = old labels
- [ ] `viewUrl` sent to user
