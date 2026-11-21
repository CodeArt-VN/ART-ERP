---
name: fe-input-control
description: >-
  Documents ART-ERP-FE app-input-control: the widget that binds a FormGroup
  control via InputControlField (id, type, form, dataSource, bindLabel,
  bindValue, and related keys) without rendering the translated label chrome.
  Use when adding or changing a direct app-input-control (custom label layout,
  nested FormGroup row, modal inline field, or table editor cell) in ART-ERP-FE.
  Routed detail and popup forms use app-form-control instead — skill
  fe-form-control. Do not place app-input-control beside app-form-control for
  the same control.
---

# FE input control

Ionic + Angular NgModule. `standalone: false`. Templates keep `*ngIf` / `*ngFor`.

`app-input-control` renders the widget only (text, number, ng-select, spans, pickers, etc.). It does **not** render the `c-label` or validation `(*…)` suffix — that chrome belongs to `app-form-control`, which wraps this component and forwards `(change)` / `(inputChange)` / `(nav)`.

**Default for pages:** use `app-form-control` (skill `fe-form-control`). Use `app-input-control` directly only for deliberate exceptions: custom label / spinner beside the field, nested `FormGroup` lines inside another control, or compact inline layouts that already hand-roll `<label class="c-label">`.

Source: `ART-ERP-FE/src/app/components/controls/input-control.component.ts`, `input-control.component.html`, `controls.interface.ts` (`InputControlField`). Declared/exported by `share-input-controls.modules.ts` (`ShareInputControlsModule`); pages get it through `ShareModule` — do not redeclare.

Canonical direct usage: `ART-ERP-FE/src/app/modals/payment-modal/payment-modal.component.html`. Wrapper path: `form-control.component.html` (`*ngIf="field && showInput"` → `[field]="field"`).

## When to use which

| Need | Use |
| --- | --- |
| Routed detail / popup CRUD field with label | `app-form-control` |
| Same widget, custom label markup (spinner, conditional title) | `app-input-control` + own `<label>` |
| Nested control inside another widget’s template | `app-input-control` with that nested `form` |
| Hide widget but keep form-control label / `[control]` slot | `app-form-control` with `showInput: false` |

## Basic binding

Prefer one `[field]` object (same `InputControlField` as form-control). `field.form` and `field.id` are required so `[formControlName]` resolves.

```html
<div class="c-control inline-control">
	<label class="c-label" for="InputAmount">{{ 'Payment amount' | translate }}</label>
	<app-input-control
		[field]="{
			id: 'InputAmount',
			label: 'Payment amount',
			type: 'number',
			form: formGroup,
		}"
	></app-input-control>
</div>
```

Live input (Enter / keystroke) vs blur/commit — payment-modal:

```html
<app-input-control
	[field]="{
		id: 'VoucherCode',
		label: 'Voucher code',
		type: 'text',
		form: formGroup,
	}"
	(inputChange)="voucherCodeChange()"
></app-input-control>

<app-input-control
	[field]="{
		id: 'InputPoint',
		label: 'Loyalty points used',
		type: 'number',
		form: formGroup,
	}"
	(inputChange)="loyaltyPointChange()"
	(change)="loyaltyPointChange()"
></app-input-control>
```

Async lookup:

```html
<app-input-control
	[field]="{
		id: 'IDApproverContact',
		label: 'Approver',
		type: 'ng-select-async',
		form: formGroup,
		dataSource: approverDataSource,
		bindValue: 'Id',
		bindLabel: 'Name',
		clearable: true,
	}"
></app-input-control>
```

Nested `FormGroup` (inside the date-picker popover in `input-control.component.html`):

```html
<app-input-control
	[field]="{
		id: 'Period',
		type: 'select',
		dataSource: _timePeriodList,
		bindValue: 'code',
		bindLabel: 'name',
		form: pickerControl,
	}"
></app-input-control>
```

## `InputControlField` keys

Defined in `controls.interface.ts`. Required: `form`, `id`.

| Key | Role |
| --- | --- |
| `form` | `FormGroup` that owns `id` |
| `id` | Control name (`formControlName`) |
| `type` | Widget kind (table below). Interface also allows `string` for template extensions |
| `label` | Optional; input-control does not show it (form-control does) |
| `secondaryId` | Second control id (`icon-color`, `time-frame`) |
| `color` | Styling hint for icon/color pickers |
| `placeholder` | Placeholder translate/text where supported |
| `showInput` | Used by form-control to hide this widget; ignored when using input-control alone |
| `dataSource` | Options list or async config for selects / breadcrumbs |
| `bindValue` / `bindLabel` | Option value / display fields |
| `multiple` / `clearable` | ng-select multi / clear |
| `noCheckDirty` | Adds `no-check-dirty` class where the template binds it |
| `mask` / `thousandSeparator` | ngx-mask for `type: 'number'` (default `separator.2` / `,`) |
| `appendTo` | ng-select dropdown parent; component default `'#ng-select-holder'` |
| `condition` | Extra filter/visibility config for specialized controls |
| `virtualScroll` | Virtual scroll (branch select defaults `true` when unset) |
| `treeConfig` | Tree ng-select: `isTree`, `isCollapsed`, `searchFn`, `searchFnDefault`, `rootCollapsed` |
| `branchConfig` | Branch picker: `selectedBranch`, `showingType`, `showingKeepDisabled`, `showingDisable`, `showingMode` (`'showAll'` \| `'showSelectedAndChildren'`) |

The `[field]` setter copies these onto matching `@Input`s. Individual `@Input`s may also be set on the host; prefer putting values on `field` unless mirroring form-control’s clearable/virtualScroll pattern.

## `type` values (interface)

| `type` | Typical use |
| --- | --- |
| `text` | Single-line text (also `*ngSwitchDefault` for unknown HTML input types) |
| `number` | Numeric + ngx-mask |
| `email` / `date` / `datetime-local` | Native input types via default branch |
| `checkbox` / `radio` / `select` | Boolean, radio group, native `<select>` |
| `ng-select` | Generic searchable select |
| `ng-select-branch` | Branch tree select |
| `ng-select-warehouse` | Remapped to branch select + warehouse load |
| `ng-select-status` / `ng-select-bp` / `ng-select-item` / `ng-select-staff` / `ng-select-async` / `ng-select-schema` | Domain lookups |
| `textarea` | Multi-line |
| `branch-breadcrumbs` | Read-only branch path |
| `span-text` / `span-number` / `span-date` / `span-datetime` | Read-only display |
| `icon` / `color` / `icon-color` | Icon and/or color pickers (`secondaryId` for color on `icon-color`) |
| `time-frame` / `date-compare-to` | Relative/absolute time config (`secondaryId` for range end) |

Template also switches on string extensions not listed in the union: `toggle`, `formula`, `editor`, `ng-select-level`. Do not invent further types unless an existing page already uses them.

## Component API (`app-input-control`)

| Input | Notes |
| --- | --- |
| `[field]` | `InputControlField` setter; primary binding |
| `[form]` / `[type]` / `[id]` / `[secondaryId]` / `[label]` / `[placeholder]` / `[color]` | Mirrored from field or set directly |
| `[dataSource]` / `[bindValue]` / `[bindLabel]` | Select options (defaults bindValue `'Code'`, bindLabel `'Name'`) |
| `[multiple]` / `[clearable]` / `[noCheckDirty]` | Defaults `false` |
| `[mask]` / `[thousandSeparator]` | Number mask defaults `separator.2` / `,` |
| `[appendTo]` | Default `'#ng-select-holder'` |
| `[virtualScroll]` | Ignores `undefined`/`null` so branch default is not wiped |
| `[inputControlTemplate]` | Custom ng-select / span-text template (`InputControlTempateDirective` content child also works) |
| Tree / branch `@Input`s | `searchFn`, `searchFnDefault`, `isTree`, `isCollapsed`, `rootCollapsed`, `branchConfig`, `selectedBranch`, `showingType`, `showingKeepDisabled`, `showingDisable`, `showingMode` |

| Output | When |
| --- | --- |
| `(change)` | Commit for ng-select family / color / icon / time-frame (via `onInputChange`); also formula modal/save and editor |
| `(inputChange)` | Native input `change`, Enter keydown, and select/picker updates |
| `(select)` | `onSelect` path |
| `(selectKeyDown)` | Barcode-style buffer on ng-select-bp Enter |
| `(nav)` | Schema open link and similar navigation |

## Must

- Pass `form` + `id` on `field` (or equivalent `@Input`s) so `formControlName` matches a control on that group.
- For page CRUD fields with standard labels, use `app-form-control` instead.
- Set `dataSource` / `bindLabel` / `bindValue` on select types the same way sibling screens do.
- For ng-select in scroll/overflow hosts, set `appendTo` to a page host id (see fe-form-control).

## Must not

- Place `app-input-control` next to `app-form-control` for the same `id`.
- Use direct `app-input-control` on a new routed detail/popup field just to skip the label wrapper — use form-control.
- Hand-write raw `<input class="c-input">` for types this component already covers when the screen already uses these controls.
- Redeclare `InputControlComponent` in a page module; import `ShareModule`.
- Invent `type` values beyond the interface union / existing template switch cases.

New UI strings: skill `i18n-keys`. Label + validation chrome: skill `fe-form-control`. Config-value editor: skill `fe-field-control`.
