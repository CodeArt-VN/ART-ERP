---
name: fe-form-control
description: >-
  Binds ART-ERP-FE detail and popup form fields through app-form-control and
  the InputControlField object (id, label, type, form, dataSource, bindLabel,
  bindValue, appendTo, and related keys). Use when adding or changing inputs on
  a routed detail page, modal form, or ion-grid form in ART-ERP-FE. Do not
  place app-input-control beside app-form-control for the same control.
---

# FE form control

Ionic + Angular NgModule. `standalone: false`. Templates keep `*ngIf` / `*ngFor`.

`app-form-control` renders the translated label and wraps `app-input-control`. The page passes one `[field]` object; the wrapper forwards `(change)` from the inner control. Do not add a sibling `app-input-control` for the same form control unless the screen already uses a deliberate exception (inline table rows, nested `FormGroup` lines).

Canonical markup:

- Routed detail: `ART-ERP-FE/src/app/pages/_template/flat-detail/flat-detail.page.html`
- Popup form grid: `ART-ERP-FE/src/app/pages/ACCOUNTANT/currency-detail/currency-detail.page.html`
- ng-select + auto-save: `ART-ERP-FE/src/app/pages/HRM/timesheet-detail/timesheet-detail.page.html`

Source: `form-control.component.ts`, `form-control.component.html`, `controls.interface.ts` (`InputControlField`).

Popup chrome (header, footer, Save/Cancel) is skill `fe-popup`. New CRUD wiring is skill `new-fe-crud-page`. New visible strings: skill `i18n-keys`.

## Page layout

**Routed detail** — `form [formGroup]="formGroup"` inside `ion-grid fixed`, often with `ion-row class="hr-group"` and section `ion-list-header`. Fields sit in `ion-col` columns. Toolbar stays `app-toolbar` in `ion-header`.

**Popup / modal** — same `form` + `ion-grid fixed` + `ion-col` pattern inside `ion-content`. Footer Save calls `saveChange()`; fields usually omit `(change)` (see Save).

Every `field.id` must match a `formControlName` on the same `form` (typically `formGroup` built in the page constructor).

## Basic binding

Inline object (most pages):

```html
<app-form-control
	[field]="{ id: 'Name', label: 'Name', type: 'text', form: formGroup }"
></app-form-control>
```

Routed detail with auto-save on edit (`saveChange()` → `saveChange2()`):

```html
<app-form-control
	[field]="{ id: 'Remark', label: 'Remark', type: 'textarea', form: formGroup }"
	(change)="saveChange()"
></app-form-control>
```

Lookup (ng-select):

```html
<app-form-control
	(change)="saveChange()"
	[field]="{
		id: 'Type',
		label: 'Classification',
		type: 'ng-select',
		form: formGroup,
		dataSource: timesheetTypeList,
		bindLabel: 'Name',
		bindValue: 'Code',
		appendTo: '#detail-page'
	}"
></app-form-control>
```

Read-only audit row (no `(change)`):

```html
<app-form-control [field]="{ id: 'CreatedDate', type: 'span-datetime', label: 'Created date', form: formGroup }"></app-form-control>
<app-form-control
	[field]="{ id: 'IDBranch', type: 'branch-breadcrumbs', label: 'Branch', form: formGroup, dataSource: env.branchList }"
></app-form-control>
```

`label` values are English ngx-translate keys. The component pipe is `{{ label | translate }}`. If `label` is omitted, `ngOnInit` sets `label` from `id`.

## `InputControlField` keys

Defined in `controls.interface.ts`. Required: `form`, `id`.

| Key | Role |
| --- | --- |
| `form` | `FormGroup` that owns `id` |
| `id` | Control name (`formControlName`) |
| `type` | Widget kind (see table below). Interface also allows `string` for extensions. |
| `label` | Translate key; shown except where checkbox/radio layout differs |
| `secondaryId` | Second control id (used by some composite types in `app-input-control`) |
| `color` | Styling hint for supported types |
| `placeholder` | Placeholder translate/text where the inner control supports it |
| `showInput` | When `false`, hides `app-input-control`; label and projected `[control]` content still render. Default `true`. |
| `dataSource` | Options list or config for selects, breadcrumbs, async lookups |
| `bindValue` | Option value field (e.g. `'Id'`, `'Code'`) |
| `bindLabel` | Option display field (e.g. `'Name'`) |
| `multiple` | Multi-select ng-select |
| `clearable` | Clear button on ng-select |
| `noCheckDirty` | Skips dirty checks in inner control where implemented |
| `mask` | ngx-mask for `type: 'number'`. Default money-style `separator.2`; port `'99999'` for digits without thousand separator (see interface comment) |
| `thousandSeparator` | Thousand separator for number mask |
| `appendTo` | CSS selector for ng-select dropdown parent (avoids clipping in scroll areas) |
| `condition` | Extra filter/visibility config for specialized controls |
| `virtualScroll` | Virtual scroll on ng-select |
| `treeConfig` | Tree ng-select: `isTree`, `isCollapsed`, `searchFn`, `searchFnDefault`, `rootCollapsed` |
| `branchConfig` | Branch picker: `selectedBranch`, `showingType`, `showingKeepDisabled`, `showingDisable`, `showingMode` (`'showAll'` \| `'showSelectedAndChildren'`) |

Pass these on `[field]` unless the page already sets the matching `@Input` on `app-form-control` (`clearable`, `virtualScroll` can mirror `field`).

## `type` values (interface)

| `type` | Typical use |
| --- | --- |
| `text` | Single-line text |
| `number` | Numeric input (optional `mask`, `thousandSeparator`) |
| `email` | Email |
| `date` | Date |
| `datetime-local` | Date and time |
| `checkbox` | Boolean; label renders after the control |
| `radio` | Radio group; label renders after the control |
| `select` | Native `<select>` |
| `ng-select` | Generic searchable select (`dataSource`, `bindLabel`, `bindValue`) |
| `ng-select-branch` | Branch lookup |
| `ng-select-warehouse` | Warehouse lookup |
| `ng-select-status` | Status lookup |
| `ng-select-bp` | Business partner lookup |
| `ng-select-item` | Item lookup |
| `ng-select-staff` | Staff lookup |
| `ng-select-async` | Async search select |
| `ng-select-schema` | Schema-driven select |
| `textarea` | Multi-line text |
| `branch-breadcrumbs` | Branch breadcrumb display (`dataSource`, often `env.branchList`) |
| `span-text` | Read-only text |
| `span-number` | Read-only number |
| `span-date` | Read-only date |
| `span-datetime` | Read-only date-time |
| `icon` | Icon picker/display |
| `color` | Color |
| `icon-color` | Icon + color |
| `time-frame` | Time range preset control |
| `date-compare-to` | Compare-to date helper |

Do not invent types not listed here unless matching an existing page that relies on the interface’s `string` fallback.

## Component API (`app-form-control`)

| Input | Notes |
| --- | --- |
| `[field]` | `InputControlField`; setter also copies `form`, `type`, `id`, `label`, `showInput` to component fields |
| `[inline]` | Adds `inline-control` layout class |
| `[clearable]` | Overrides ng-select clearable; defaults from `field.clearable` |
| `[virtualScroll]` | Overrides virtual scroll; defaults from `field.virtualScroll` |
| `[showInput]` | When `false`, hides inner `app-input-control` |
| `[inputControlTemplate]` | Custom ng-select label/option template |

| Output | When |
| --- | --- |
| `(change)` | User finished editing; bind `saveChange()` on routed details that auto-persist |
| `(controlChange)` | Finer-grained inner `inputChange` events |
| `(nav)` | Navigation from branch-breadcrumbs and similar |

Projected content (optional):

- `[label]` — extra markup beside the label (flat-detail sample: `<small label>…</small>`)
- `[control]` — custom control when `showInput: false` or supplemental UI
- `[message]` — validation hint inside the `(*…)` danger suffix

Validation: label shows `(*…)` when the control is invalid, not pending, and dirty.

## Save behavior

| Screen | Pattern |
| --- | --- |
| Routed detail using `saveChange2()` | `(change)="saveChange()"` on editable fields (flat-detail, timesheet-detail). Audit `span-*` fields usually have no `(change)`. |
| Popup / modal | Footer `[strong]` Save / Add calls `saveChange()`; fields in currency-detail have no per-field `(change)`. Dirty gating: `[disabled]="!formGroup.dirty"` on Save when editing. |

Do not wire `(change)="saveChange()"` on popup fields unless matching an existing page in the same module.

## ng-select `appendTo`

Dropdowns inside `ion-content`, segments, or overflow containers get clipped unless `appendTo` points at a host on the page.

1. Add an empty host `div` with a stable `id` near the form (sibling inside scroll content is fine):

```html
<div id="detail-page" style="position: absolute"></div>
```

Some pages add `z-index: 30005` (zone-detail, item-detail `#ng-select-header`).

2. Set `appendTo: '#detail-page'` (or `'#ng-select-header'`, `'#scenario-detail-page'`, etc.) on the `field` object for each ng-select on that screen. Reuse the same id string the sibling page in that domain uses.

Popups with many selects follow the same idea when existing modals in the repo do (e.g. `#vms-person-merge-modal`).

## Popup forms

Use `app-form-control` inside `ion-grid fixed` / `ion-row` / `ion-col` under `[formGroup]="formGroup"`. Do not restyle or relocate Save/Cancel — skill `fe-popup`.

## Do not

- Place `app-input-control` for the same `id` when `app-form-control` already wraps that field.
- Hand-write `<label class="c-label">` + raw `<input>` for standard CRUD fields when `app-form-control` is used elsewhere on the page (legacy blocks may remain; new fields use `app-form-control`).
- Use Vietnamese or sentence-case labels in `field.label`; use English keys and skill `i18n-keys`.
- Skip `form` on the field object — `app-input-control` requires `field.form`.
- Forget `bindLabel` / `bindValue` / `dataSource` on `ng-select` types when the canonical page for that entity sets them.
