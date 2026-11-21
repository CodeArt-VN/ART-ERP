---
name: fe-group-control
description: >-
  Documents ART-ERP-FE `app-group-control`: a titled config-option group that
  renders `app-field-control` rows and emits field changes. Use when adding or
  changing SYS_Config / dynamic-config option groups, or when a template is about
  to bind `app-group-control`. Do not confuse with the flat/tree left feature
  pane (`page.groupControl` + `ion-fab` list) — that is not this selector.
---

# FE group control

Ionic + Angular NgModule (`standalone: false`). Declared and exported only from `ShareInputControlsModule` (`ART-ERP-FE/src/app/components/controls/share-input-controls.modules.ts`), which pages reach via `ShareModule`. Do not redeclare `GroupControlComponent` in a page module. Do not edit `share.module.ts`.

## Which folder is live

| Path | Wired? | Notes |
| --- | --- | --- |
| `ART-ERP-FE/src/app/components/group-control/` | **Yes** — import path in `ShareInputControlsModule` | Has `@Input() code`, always shows **View config**, navigates to `/config-grid/{code}`. **No** `<ng-content>`. |
| `ART-ERP-FE/src/app/components/form-group-control/` | **No** — same `selector: 'app-group-control'`, not in any NgModule | Has `<ng-content>` under the title; **no** `code` / View config. Orphan duplicate — do not import or declare it. |

Prefer editing and documenting the **wired** `group-control/` sources. If you find `form-group-control/` in a search hit, treat it as dead code with a colliding selector.

## Not the left group filter

Flat / tree list feature panes (`_template/flat`, `_template/tree`) use a **page property** named `groupControl` (`groupList`, `selectedGroup`, `onGroupChange`) inside an `ion-fab` list. That markup is **not** `<app-group-control>`. Do not replace that pane with this component.

Canonical host for the selector: `ART-ERP-FE/src/app/pages/ADMIN/config/components/dynamic-config/dynamic-config.component.html`.

## Copy this

```html
<app-group-control
	[title]="o.Name"
	[code]="o.Code"
	[fields]="o.children"
	[hideBorder]="idx == optionList.length - 1"
	(onChange)="saveChange($event)"
	*ngFor="let o of optionList; let idx = index"
>
</app-group-control>
```

- `fields` items are config field rows consumed by `app-field-control` (skill `fe-field-control`).
- `(onChange)` re-emits the payload from each nested `app-field-control` (`field.data`). Handle save on the parent (e.g. `saveChange` on dynamic-config).
- Projected children are **ignored** by the wired template (no `ng-content`). Put remarks or extra UI beside the control, not inside it. Do not switch to `form-group-control/` to get projection.

## `@Input` / `@Output` (wired `group-control/`)

| Member | Default | Role |
| --- | --- | --- |
| `@Input() title` | — | Group header label (`ion-label`). |
| `@Input() code` | — | When set, View config navigates to `/config-grid/{code}` with `state` = field `Code` list; when empty, `/config-grid`. |
| `@Input() hideBorder` | — | Truthy removes the `border` class / border style on the `ion-row`. |
| `@Input() fields` | `[]` | Array of field objects; each rendered as `<app-field-control [field]="field">`. |
| `@Output() onChange` | — | Emits whatever nested `app-field-control` emits (`trackChange`). |

There are no other public inputs. `viewConfig()` and `nav()` are internal (View config button).

## Must

- Use the selector only for config / option-group UIs that already have field rows for `app-field-control`.
- Rely on `ShareModule` / `ShareInputControlsModule` — never declare either `GroupControlComponent` file in a feature module.
- Pass `[fields]` and handle `(onChange)` on the parent; do not reimplement field editors beside the group.

## Must not

- Import `form-group-control/group-control.component` or declare that orphan class.
- Use `app-group-control` for the list left feature pane / group sidebar — keep the flat/tree `groupControl` + `ion-item` pattern.
- Expect projected content inside the tag (wired template has no `ng-content`).
- Add `app-form-control` inside this group for config values — nested editors are `app-field-control` only.
- Edit the component sources when the task is only to wire a config screen — change the host template and field data instead.

New UI strings: skill `i18n-keys`. Nested field editors: skill `fe-field-control`. Page forms (CRUD detail): skill `fe-form-control`.
