---
name: fe-branch-breadcrumbs
description: >-
  Documents how to show branch hierarchy paths with `app-branch-breadcrumbs` or
  `app-form-control` field type `branch-breadcrumbs` in ART-ERP-FE. Use when
  adding or changing audit branch display on detail pages, datatable cells, or
  read-only branch path UI.
---

# Branch breadcrumbs (ART-ERP-FE)

Read-only Ionic breadcrumbs for an org-tree node. The component walks `Items` by `IDParent`, drops the tree root (“Tổng công ty”), and shows the path from F1 downward. It is **not** a branch picker — editable branch fields use `type: 'ng-select-branch'` or `ng-select-warehouse`.

Source: `ART-ERP-FE/src/app/components/branch-breadcrumbs/branch-breadcrumbs.component.ts` (+ `.html`).

## Default: detail audit row via `app-form-control`

CRUD detail pages use **`app-form-control`**, not the tag directly. Copy the **Other information** row from the flat template:

- Canonical: `ART-ERP-FE/src/app/pages/_template/flat-detail/flat-detail.page.html` (segment **Other information**, `*ngIf="item.Id"`).
- Same pattern: `ART-ERP-FE/src/app/pages/VMS/nvr-detail/vms-nvr-detail.page.html`.

```html
<ion-row class="hr-group" *ngIf="item.Id">
	<ion-col size="12" size-sm="12" size-md="12" size-xl="3">
		<ion-list-header class="ion-no-padding">
			<ion-label color="primary">{{ 'Other information' | translate }}</ion-label>
		</ion-list-header>
	</ion-col>
	<ion-col size="12" size-sm size-xl="4">
		<app-form-control [field]="{ id: 'CreatedBy', type: 'text', label: 'Created by', form: formGroup }"></app-form-control>
		<app-form-control [field]="{ id: 'CreatedDate', type: 'span-datetime', label: 'Created date', form: formGroup }"></app-form-control>
		<app-form-control [field]="{ id: 'ModifiedBy', type: 'text', label: 'Last modified by', form: formGroup }"></app-form-control>
		<app-form-control [field]="{ id: 'ModifiedDate', type: 'span-datetime', label: 'Last modified date', form: formGroup }"></app-form-control>
	</ion-col>
	<ion-col size="12" size-sm size-xl="4">
		<app-form-control
			[field]="{ id: 'IDBranch', type: 'branch-breadcrumbs', label: 'Branch', form: formGroup, dataSource: env.branchList }"
		></app-form-control>
		<app-form-control [field]="{ id: 'Remark', type: 'textarea', form: formGroup }" (change)="saveChange()"></app-form-control>
	</ion-col>
</ion-row>
```

### Field object (`InputControlField`)

| Property | Value |
|----------|--------|
| `id` | Form control holding the node id (usually `IDBranch`; some WMS screens use `IDWarehouse` with the same type) |
| `type` | `'branch-breadcrumbs'` (listed in `controls.interface.ts`) |
| `label` | `'Branch'` (or `'Warehouse'` when the control name is warehouse) |
| `form` | Page `formGroup` |
| `dataSource` | Tree array — almost always `env.branchList` |

No `(change)` on this control; it is display-only.

### What `app-input-control` does

`ART-ERP-FE/src/app/components/controls/input-control.component.html` switches on `'branch-breadcrumbs'` and renders:

```html
<app-branch-breadcrumbs
	[maxItems]="3"
	[Id]="form.controls[id].value"
	[Items]="dataSource"
	class="c-input disable breadcrumbs"
></app-branch-breadcrumbs>
```

So the form-control path always passes **`maxItems="3"`** and binds `Id` from the named control. Do not expect to tune `autoFit` through the field object unless you extend `input-control`.

## Direct tag: `<app-branch-breadcrumbs>`

Use the selector when there is **no** form row — typically **`datatable-cell-template`** or custom list markup.

Examples:

- `ART-ERP-FE/src/app/pages/VMS/nvr/vms-nvr.page.html` — under name link, `*ngIf="i.IDBranch"`.
- `ART-ERP-FE/src/app/pages/VMS/edge-node/vms-edge-node.page.html` — multiple ids via `*ngFor`.
- `ART-ERP-FE/src/app/pages/ADMIN/user-group-detail/user-group-detail.page.html` — nested table, custom `Items` (`titlePositions`).

```html
<app-branch-breadcrumbs
	class="medium"
	*ngIf="i.IDBranch"
	[Id]="i.IDBranch"
	[Items]="env.branchList"
></app-branch-breadcrumbs>
```

### `@Input()` on the component

| Input | Role |
|-------|------|
| `Id` | Selected node id (`number`; invalid / missing → empty path) |
| `Items` | Flat tree rows: `Id`, `IDParent`, `Name` (any similar hierarchy works, e.g. job titles on staff list) |
| `maxItems` | Fixed visible crumb count; when set, **disables** width-based `autoFit` |
| `itemsBeforeCollapse` / `itemsAfterCollapse` | Ionic collapse split (defaults `1` / `1`) |
| `autoFit` | Default `true`: shrink middle crumbs to fit cell width (datatable styling in `data-table.scss`) |

Optional `class="medium"` matches list subtitle sizing (VMS lists).

### Module import

`BranchBreadcrumbsComponent` is declared and exported from `ShareInputControlsModule` (`share-input-controls.modules.ts`). Pages that import **`ShareModule`** already have the tag; no extra declarations.

## Behavior to expect

- Root id only → empty breadcrumbs (root hidden by design).
- `Id` set but missing from `Items` → translated **Branch ID not found** (see template).
- Collapsed “…” opens a popover listing full path (`popover.cssClass = 'branch-breadcrumbs'`).
- `data-table.component.ts` queries `app-branch-breadcrumbs ion-breadcrumb` for layout — keep the tag inside datatable cells when using breadcrumbs there.

## Tests

After logic changes to the component, update and run:

`ART-ERP-FE/src/app/components/branch-breadcrumbs/branch-breadcrumbs.component.spec.ts`

(Covers root omission, path building, collapse helper `crumbCollapseLayout`.)

## Checklist

1. Detail audit branch → `app-form-control` + `type: 'branch-breadcrumbs'`; copy flat-detail **Other information** column.
2. List / inline path → `<app-branch-breadcrumbs [Id] [Items]>` inside cell template; guard with `*ngIf` when id can be null.
3. Editable branch on the form → `ng-select-branch` / `ng-select-warehouse`, not breadcrumbs.
4. `dataSource` / `[Items]` must be the same tree list used elsewhere (`env.branchList` unless the row is another hierarchy).
