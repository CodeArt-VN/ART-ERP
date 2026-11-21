---
name: fe-color-picker
description: >-
  Documents ART-ERP-FE app-color-picker: Ionic color-token grid, [color] input,
  (selected) output of { Code, Name }. Use when adding or changing a color
  picker, form-control type color or icon-color, or Color / BadgeColor fields
  in ART-ERP-FE. Prefer app-form-control; do not reimplement the palette.
---

# FE color picker

Ionic + Angular NgModule (`standalone: false`). `app-color-picker` is a fixed grid of Ionic color tokens. Pages almost never host it directly — `app-input-control` embeds it for `type: 'color'` and `type: 'icon-color'`, reached from pages via `app-form-control` (skill `fe-form-control`).

`ColorPickerComponent` is declared and exported by `ShareInputControlsModule` (pulled in through `ShareModule`). Do not redeclare it in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/controls/color-picker/color-picker.component.ts`, `color-picker.component.html`
- Host switch cases: `ART-ERP-FE/src/app/components/controls/input-control.component.html` (`color`, `icon-color`)
- Page usage (`icon-color`): `ART-ERP-FE/src/app/pages/SYS/system-type-detail/system-type-detail.page.html`

## Prefer form-control (usual path)

Color-only field — stores the Ionic token string (`Code`) on `field.id`:

```html
<app-form-control
	[field]="{ id: 'Color', label: 'Color', type: 'color', form: formGroup }"
	(change)="saveChange()"
></app-form-control>
```

Icon + color — `id` is the icon control; `secondaryId` is the color control. Example from system-type detail:

```html
<app-form-control
	[field]="{ id: 'Icon', secondaryId: 'Color', label: 'Icon', type: 'icon-color', form: formGroup }"
	(change)="saveChange()"
></app-form-control>
```

`input-control` opens a popover (`color`) or modal (`icon-color`), binds `[color]` from the form value (fallback `'dark'`), and on `(selected)` calls `onSelectColor`, which `setValue`s **`color.Code`** and marks dirty. For `type === 'color'` it also closes the picker; for `icon-color` the modal stays open so the user can pick an icon next.

Do not invent other field keys for the palette. Ensure both `id` and `secondaryId` (when used) exist on the same `FormGroup`.

## Direct `app-color-picker` (rare)

Only when a screen cannot use `app-form-control` / `app-input-control`. Same module export; bind the source API only:

```html
<app-color-picker [color]="currentColor || 'dark'" (selected)="onColorPicked($event)"></app-color-picker>
```

`$event` is the palette row `{ Code: string, Name: string }`. Persist **`Code`** (e.g. `'primary'`, `'danger'`), not `Name`.

## `@Input` / `@Output` (source only)

| Member | Kind | Role |
| --- | --- | --- |
| `color` | `@Input() string` | Current token; highlights context for the host. Not used to filter `items`. |
| `selected` | `@Output()` | Emits the clicked `items` row (`{ Code, Name }`). |

No other public inputs or outputs. Do not bind inventeds such as `colors`, `palette`, `(change)`, or `[(ngModel)]`.

## Palette (`items`)

Hardcoded in the component (order preserved):

`primary`, `secondary`, `tertiary`, `success`, `warning`, `danger`, `red`, `pink`, `purple`, `blue`, `bluegreen`, `dark`, `medium`, `light`.

Template renders round `ion-button`s with `[color]="r.Code"`. A second “Palettes” hex UI (`segmentView == 's2'`) exists in the template but the segment chrome is commented out — only the app-color grid (`s1`) is active. Do not wire callers to `segmentView` / `segmentChanged`.

## Do not

- Redeclare `ColorPickerComponent` in a page NgModule.
- Put raw `app-color-picker` on a detail form when `type: 'color'` or `type: 'icon-color'` via `app-form-control` works.
- Store display `Name` or a hex string from this picker; store Ionic `Code`.
- Edit `color-picker.component.ts` / `.html` only to add a field on a page — change the page `field` / form controls instead.
- Reimplement a parallel color swatch list on the page.

Form field wiring: skill `fe-form-control`. New UI strings: skill `i18n-keys`.
