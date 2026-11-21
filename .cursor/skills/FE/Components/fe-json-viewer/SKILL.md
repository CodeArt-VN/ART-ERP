---
name: fe-json-viewer
description: >-
  Embeds ART-ERP-FE app-json-viewer to show a JSON object or JSON string as a
  tree, with an optional previous value and a difference filter. Use when
  adding or changing a JSON viewer, log payload, or before/after JSON compare
  in ART-ERP-FE. Do not invent inputs or outputs.
---

# FE JSON viewer

Ionic + Angular NgModule. `app-json-viewer` draws one JSON value as a tree inside `app-data-table`. `standalone: false`. Do not convert it, and do not edit `json-viewer.component.ts` or `json-viewer.component.html`.

`JsonViewerComponent` is declared and exported by `ShareComponentsModule`, which `ShareModule` re-exports. A page module that already imports `ShareModule` can use the selector. Do not declare the component again.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/json-viewer/json-viewer.component.ts`
- Compare: `ART-ERP-FE/src/app/pages/APPROVAL/request-detail/request-detail.page.html`
- Single document: `ART-ERP-FE/src/app/pages/SYS/system-log-detail/system-log-detail.page.html`

## Inputs

There is no `@Output`. `Output` and `EventEmitter` are imported and unused. Bind only these inputs.

| Input | Default | Role |
| --- | --- | --- |
| `item` | — | Object, array, JSON string, or a scalar. Guard with `*ngIf` so `Object.keys` is not called on null. A string is parsed, including unquoted keys and single-quoted values. A scalar becomes one row named `Data`. |
| `oldItem` | — | Previous value, same shape as `item`. Compared per key. Shown in the Old value column when `isCompare` is true. |
| `properties` | — | Map of raw key to the Name-column label. A missing key stays as the raw key. The label goes through `translate`. |
| `isCompare` | `true` | Shows the Old value column. |
| `isShowDifference` | `true` | When truthy, keeps rows whose `Value` differs from `OldValue`, plus ancestors that still have a visible child. A bound `undefined` is stored as-is and turns the filter off. |
| `notShowProperties` | `[]` | Names to drop. Match the Name column: the `properties` label when that key is mapped, otherwise the raw key. A falsy value clears the list. |

`showProperties` on the approval page is not an input.

`item`, `oldItem`, and `properties` are read in `ngOnInit`. They are not setters. Create the viewer only after those values exist. request-detail waits on `isLoadedOldItem` before the compare viewer is created. Later writes to those three do not rebuild the tree. `isShowDifference` and `notShowProperties` rebuild after the first load, and only when the bound value changes. Assign a new array for `notShowProperties` (request-detail copies it with `[...]`).

Array children are named `1`, `2`, … (`index + 1`).

## Compare

From request detail. `properties` is a key-to-label map such as `{ CompanyName: 'Company name', TaxCode: 'Tax code' }`. `notShowProperties` is a string array such as `['DeletedAddressFields', 'DeletedTaxInfoFields']`.

```html
<app-json-viewer
	[item]="item.UDF16"
	[oldItem]="oldItem"
	[properties]="this.propertiesLabelDataCorrection"
	[isCompare]="true"
	[isShowDifference]="jsonViewerConfig.isShowDifference"
	[notShowProperties]="jsonViewerConfig.notShowProperties"
>
</app-json-viewer>
```

A document with no previous value, from system-log detail:

```html
<app-json-viewer *ngIf="item" [item]="item" [isCompare]="false"> </app-json-viewer>
```

History log uses the same pair plus `[isShowDifference]="false"`.

## Do not

- Add an input, an output, or a `(change)` binding.
- Pass `showProperties`, or any field that is not in the table above.
- Restyle the inner `app-data-table`, or add columns on the caller.
- Edit the component to change parsing, the tree, or the difference filter.
