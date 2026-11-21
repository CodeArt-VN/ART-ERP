---
name: fe-field-control
description: >-
  Documents the ART-ERP-FE app-field-control config-value editor: ngModel on
  field.data.ValueObject, one @Input field, and one @Output onChange. Use when
  adding or changing app-field-control, or when a template is about to bind
  app-field-control on a form, popup, or detail page. Page forms use
  app-form-control.
---

# FE field control

NgModule component. `standalone: false`. The template is inline in `ART-ERP-FE/src/app/components/controls/field-control.component.ts`. There is no html file.

`ShareModule` exports `ShareComponentsModule`, which exports `ShareInputControlsModule`. A page that already imports `ShareModule` can use the selector. Do not declare `FieldControlComponent` again. Do not edit `share.module.ts`.

Keep `*ngIf` and `*ngFor`.

## Page forms

A list, detail, popup, or filter field is `app-form-control` (skills `new-fe-crud-page`, `fe-popup`). `app-field-control` is the editor for one config row (`field.data.ValueObject`), and the only template that hosts it is `app-group-control`.

That split is what the two sources do:

- This control renders only when `field.data` is set, and every editor is `[(ngModel)]="field.data.ValueObject"`. The class has no `FormGroup` input. `app-form-control` copies `field.form` onto `@Input() form` and renders `app-input-control` for that group. Its label is `{{ label | translate }}`. This label is `{{ field.label }}` with no translate pipe.
- An editor exists only for the eight `field.type` strings below. Any other string leaves the label and no input. `toggle` is its own `*ngIf`, outside the `ngSwitch`. `app-input-control` uses other strings (`text`, `ng-select-staff`, `ng-select-branch`, and the rest of `InputControlField` in `controls.interface.ts`).
- Page templates contain no `<app-field-control`. Detail templates bind `<app-form-control [field]="{ id, label, type, form: formGroup }">`.

## API

Do not add inputs. The class declares two members:

| Member | Role |
| --- | --- |
| `@Input() field` | `any`. Everything below is a property of this object. `label`, `type`, and `id` are not `@Input`s. |
| `@Output() onChange` | Emits `field.data`. `trackChange` waits 1ms, then emits. `reset(field)` sets `field.data.ValueObject` to `null` and emits the same way. |

`ngOnInit` is empty. The click handlers pass `field.data`, so the payload is the config row, not the DOM event.

## Caller

`ART-ERP-FE/src/app/components/group-control/group-control.component.html` is the only host. No page template contains `app-group-control` either. Copy that binding when the value is already this config row:

```html
<app-field-control (onChange)="trackChange($event)" [field]="field" *ngFor="let field of fields"></app-field-control>
```

`GroupControlComponent` re-emits `$event` from its own `onChange`. It does not write `field`. Its inputs are `title`, `code`, `hideBorder`, and `fields`. Nothing in the repo assigns `field.data`, `DataSource`, or `_InheritedConfig`.

## field object

The host `div` is `*ngIf="field.data"`.

| Property | Read for |
| --- | --- |
| `data.ValueObject` | ngModel on every editor. `[reset]` when it is not `null` and `data._InheritedConfig` is absent. |
| `data._InheritedConfig` | `[Inherit]`. Together with `field.showInherited`, `app-branch-breadcrumbs` (`[Id]` = `_InheritedConfig.IDBranch`, `[Items]` = `_InheritedConfig._Branches`). The template toggles `field.showInherited`. |
| `label`, `remark`, `labelForId` | Label text, the remark `<p>`, and `for` / `id` / ng-select `labelForId`. |
| `disabled` | Non-toggle `ion-item` `[disabled]`. ng-select and inputs use `[readonly]`. The toggle uses `[disabled]`. |
| `type` | Table below. |
| `bindLabel` | Used when set. Otherwise the template passes `Name`. `bindValue` is passed through as stored. |

| `type` | Editor | Also read |
| --- | --- | --- |
| `select-staff` | ng-select, multi chips, avatar `field.imgPath + item.Code + '.jpg'` (error image `assets/avartar-empty.jpg`) | `multiple`, `DataSource` (`async`), `SearchInput`, `SearchLoading`. Option: `FullName`, `Id`, `Code`, `Phone`. |
| `select-contact` | ng-select | Same four. Option: `Name`, `WorkPhone`, `Code`, `Address` (`AddressLine1`, `Ward`, `District`, `Province`, `AddressLine2`, `Contact`, `Phone1`, `Phone2`). |
| `select-branch` | ng-select, `appendTo="#ng-select-holder"` (`app.component.html`), placeholder `Chọn đơn vị...` | `items`. Search is the component method `searchShowAllChildren`: `lib.searchTreeReturnId(field.items, term)`, then `item.Id`. Option: `levels`, `Type == 'Company'`, `Name`. |
| `select` | ng-select | `items`. Option: `levels`, `Color`, and `bindLabel` or `Name`. |
| `string` | `<input type="text">` | |
| `number` | `<input type="number">` | |
| `textarea` | `<textarea rows="3">` | |
| `toggle` | `ion-toggle` in the same `ion-item` as the label | `(click)` calls `trackChange`. The template does not bind `(ionChange)`. |

`DataSource` is capital D. The form-control field uses `dataSource`. `[multiple]` is bound only for `select-staff` and `select-contact`.

The template hardcodes `[reset]`, `[Inherit]`, `Inherit from`, `Chọn đơn vị...`, and `điện thoại:`.

## Do not

- Declare an `@Input` that is not on the class (`form`, `id`, `label`, `type`, `items`).
- Bind a `FormGroup` here, or pass `text`, `ng-select`, or `ng-select-staff`. Those types belong on `app-form-control`.
- Edit `field-control.component.ts` so a page field will fit.
- Switch the template to `@if` / `@for` or `standalone: true`.
