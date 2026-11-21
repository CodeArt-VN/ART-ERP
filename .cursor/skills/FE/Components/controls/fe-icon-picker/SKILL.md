---
name: fe-icon-picker
description: >-
  Documents ART-ERP-FE app-icon-picker: bind icon and color inputs, handle the
  selected output, and prefer app-form-control field types icon or icon-color
  on detail forms. Use when adding or changing an Ionic icon picker, Icon form
  field, icon-color composite, or Change icon control in ART-ERP-FE. Do not
  reimplement the icon grid or duplicate the built-in items list.
---

# FE icon picker

Ionic + Angular NgModule (`standalone: false`). `app-icon-picker` is a searchable grid of Ionic / custom icon names. Pages almost always reach it through `app-form-control` (`type: 'icon'` or `'icon-color'`). Direct use is rare and only needed when embedding the grid outside that field flow (e.g. a custom modal that already mirrors `app-input-control`).

`IconPickerComponent` is declared and exported by `ShareInputControlsModule` (`share-input-controls.modules.ts`), which `ShareModule` re-exports. A page module that already imports `ShareModule` can use the selector. Do not redeclare it in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/controls/icon-picker/icon-picker.component.ts`, `icon-picker.component.html`
- Wired by input-control: `ART-ERP-FE/src/app/components/controls/input-control.component.html` (`*ngSwitchCase="'icon'"` / `'icon-color'`)
- Field type union: `ART-ERP-FE/src/app/components/controls/controls.interface.ts` (`InputControlField`)

Detail field chrome is skill `fe-form-control`. New UI strings: skill `i18n-keys`.

## Prefer form-control (usual path)

**Icon only** — stores the icon name on `id` (string). Opens a sheet modal; picking an icon calls `control.setValue(icon.Name)`, marks dirty, closes the sheet, and emits change.

```html
<app-form-control
	[field]="{ id: 'Icon', label: 'Icon', type: 'icon', form: formGroup }"
	(change)="saveChange()"
></app-form-control>
```

Optional tint via `field.color` (passed through to `[color]` on the picker). Example: form detail binds badge color:

```html
<app-form-control
	[field]="{
		id: 'Icon',
		type: 'icon',
		form: formGroup,
		color: formGroup.controls.BadgeColor.value
	}"
></app-form-control>
```

**Icon + color** — `id` holds the icon name; `secondaryId` holds the color code. The modal shows `app-color-picker` above `app-icon-picker`. Color selection does **not** close the sheet (unlike type `'color'` alone); icon selection does.

```html
<app-form-control
	[field]="{
		id: 'Icon',
		secondaryId: 'Color',
		label: 'Icon',
		type: 'icon-color',
		form: formGroup
	}"
	(change)="saveChange()"
></app-form-control>
```

Both `Icon` and `Color` (or whatever `id` / `secondaryId` you use) must exist on the same `form`. Default preview icon name when empty is `layers`. Button label falls back to `'Change icon' | translate`.

### Form-control usages in the repo

| Path | `type` |
| --- | --- |
| `ADMIN/form-detail` | `icon` (+ `color` from `BadgeColor`) |
| `OSM/notification-category-detail` | `icon` |
| `BI/dynamic-report-detail`, `BI/dynamic-dashboard-detail` | `icon-color` |
| `SYS/system-type-detail`, `SYS/schema-detail`, `SYS/integration-action-detail`, `SYS/integration-trigger-detail` | `icon-color` |
| `HRM/employee-policy-detail`, `HRM/leave-type-detail` | `icon-color` |
| `CRM/reward-category-detail`, `CRM/level-policy-detail` | `icon-color` |
| `PM/space-detail`, `PM/space-status-modal` | `icon-color` |

No page template currently embeds `<app-icon-picker>` directly; only `input-control.component.html` does.

## Direct use (custom host)

Only when you own the trigger/modal (do not invent a second icon catalog):

```html
<app-icon-picker
	[icon]="formGroup.controls.Icon.value"
	[color]="formGroup.controls.Color?.value || 'dark'"
	(selected)="onIconPicked($event)"
></app-icon-picker>
```

`(selected)` emits the catalog row `{ Name, Tags }`, not a bare string. Persist with `event.Name` (same as `onSelectIcon` in `input-control.component.ts`).

## `@Input` / `@Output`

| Member | Default | Role |
| --- | --- | --- |
| `icon` | — | Current selected name; matching grid button uses `fill="outline"`. |
| `color` | — | Ionic color for the grid buttons (`[color]` on each `ion-button`). |
| `selected` | — | `@Output` `EventEmitter`; fires the `{ Name, Tags }` item on click. |

There are no other public inputs. Search keyword and the `items` catalog live on the component instance; do not pass them from the page.

## Behavior (do not reimplement)

- **Catalog:** hard-coded `items` array of `{ Name, Tags }` (Ionic names plus project icons such as `quotation`, `warehouse`, `flag-vn`).
- **Search:** `ion-searchbar` bound to `keyword`; list filtered with `searchNoAccent` on `Tags`.
- **Select:** `onSelected(i)` sets `this.icon = i.Name` and `this.selected.emit(i)`.
- **Form path:** `presentPopupPicker()` opens `ion-modal` breakpoints `[0.5, 0.75]`; `onSelectIcon` writes `icon.Name` into the form control.

## Do not

- Import or declare `IconPickerComponent` in a page NgModule.
- Put a raw `<app-icon-picker>` on a detail form when `type: 'icon'` or `'icon-color'` already covers the field.
- Copy or extend the `items` list on the page; change the component (and its spec) only when the task is to add catalog icons.
- Emit or bind a string for `(selected)`; handlers must read `.Name`.
- Use `type: 'icon-color'` without a real `secondaryId` control on the same form.
- Edit `icon-picker.component.*` when the task is only to wire a page — change the page template / `formGroup` instead.

New detail field layout: skill `fe-form-control`. Popup chrome: skill `fe-popup`.
