---
name: fe-address
description: >-
  Documents how to place and configure `app-address` on ART-ERP-FE detail
  pages and modals: bind address value, canEdit, optional type list and map
  loading flags, and handle onChange / onDelete. Use when adding or changing
  a partner, outlet, staff, or modal address block in ART-ERP-FE. Do not
  reimplement the address form or coordinate picker on the page.
---

# FE address

Ionic + Angular NgModule (`standalone: false`). Detail pages and modals use `app-address` inside an `Addresses` `FormArray` section. Do not confuse with `app-bp-address` / `app-bp-tax-address` (CRM nested components that own their own form rows).

Import `MapCompsModule` in the page or feature NgModule. `AddressComponent` is declared and exported there — not in `ShareModule`. Do not redeclare `app-address` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/map-comps/address/address.component.ts`, `address.component.html`
- Module: `ART-ERP-FE/src/app/components/map-comps/map-comps.module.ts`
- Partner detail: `ART-ERP-FE/src/app/pages/CRM/business-partner-detail/business-partner-detail.page.html`
- Outlet detail: `ART-ERP-FE/src/app/pages/CRM/outlet-detail/outlet-detail.page.html`
- Staff profile: `ART-ERP-FE/src/app/pages/HRM/staff-detail/components/staff-personnel-profile/staff-personnel-profile.component.html`
- Modal: `ART-ERP-FE/src/app/modals/data-correction-request-modal/data-correction-request-modal.html`

## Copy this

Partner / outlet style (no address `Type` select):

```html
<app-address
	*ngFor="let address of formGroup.get('Addresses')['controls']"
	[address]="address.value"
	[canEdit]="pageConfig.canEdit"
	[mapLoading]="env.isMapLoaded"
	(onChange)="changeAddress($event)"
	(onDelete)="removeAddress($event)"
></app-address>
```

Staff style (optional type list; map flag alias `loadingMap`):

```html
<app-address
	*ngFor="let c of formGroup.get('Addresses')['controls']"
	[address]="c.value"
	[canEdit]="pageConfig.canEdit"
	[types]="hrAddressTypeList"
	[loadingMap]="env.isMapLoaded"
	(onChange)="changeAddress($event)"
	(onDelete)="removeAddress($event)"
></app-address>
```

Page module:

```ts
import { MapCompsModule } from 'src/app/components/map-comps/map-comps.module';
// imports: [..., MapCompsModule, ...]
```

The host keeps a `FormArray` named `Addresses`. Each row value must include at least `Id` plus the address fields the component patches (`AddressLine1` required inside `app-address`). Host handlers typically match by `e.Id`, patch dirty controls, then `saveChange()`; delete sets `DeletedAddressFields` when `e.Id > 0` then `removeAt`. See `business-partner-detail.page.ts` / `staff-personnel-profile.component.ts`.

## `@Input` / `@Output` (page template)

Source-only APIs on `AddressComponent`. No content projection.

| Binding | Default | Role |
| --- | --- | --- |
| `address` | — | Setter: assigns `item` and `formGroup.patchValue` when the inner form exists. Pass the FormArray row `.value`. |
| `canEdit` | — | Copied to `pageConfig.canEdit` on load; when falsy the form is disabled and Delete is hidden. |
| `types` | `[]` | Address type options (`{ Name, Code }`). Type `ng-select` renders only when `typeList.length > 0`. |
| `mapLoading` | — | Sets `env.isMapLoaded` so `app-coordinate-picker` can show. |
| `loadingMap` | — | Same as `mapLoading` (`@Input('loadingMap')`). Prefer one; pages use either. |
| `config` | — | Setter: replaces `pageConfig`. Not used on current partner/outlet/staff templates. |
| `(onChange)` | — | Emits `formGroup.value` after a valid field / map change. |
| `(onDelete)` | — | After confirm prompt, emits `formGroup.getRawValue()` for the host to remove the row. |

## Inner form fields (do not rebuild on the page)

`Id`, `Type`, `AddressLine1` (required), `AddressLine2`, `Country`, `Province`, `District`, `Ward`, `ZipCode`, `Lat`, `Long`, `Contact`, `Phone1`, `Phone2`, `Remark`.

Province / district / ward use `env.addressSubdivisionList` (`ProvincialLevel` / `MunicipalLevel` / `SubMunicipalLevel`). Map pin edits go through nested `app-coordinate-picker`.

## Do not

- Import or declare `AddressComponent` in a page NgModule; import `MapCompsModule` only.
- Duplicate province / district / ward / lat-long / delete UI beside `app-address`.
- Use `app-bp-address` when the screen already loops `app-address` over `Addresses`.
- Edit `address.component.ts` / `.html` when the task is only to wire a page — change the page template, `FormArray`, and change/delete handlers instead.

New UI strings: skill `i18n-keys`. Detail field chrome: skill `fe-form-control`. Popup shell: skill `fe-popup`.
