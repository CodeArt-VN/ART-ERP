---
name: new-fe-crud-page
description: Creates an ART-ERP-FE list and detail page by copying the flat NgModule template, wiring routes, PageBase, and the generated provider. Use when adding or changing an ERP screen, CRUD page, list, detail, route, datatable, or SYS_Form in ART-ERP-FE.
---

# New FE CRUD page

Ionic + Angular 20 **NgModule**. Hash router. Read [reference.md](reference.md) before writing the constructor, list HTML, or detail form.

Canonical samples (copy these):

- List: `ART-ERP-FE/src/app/pages/_template/flat/`
- Detail: `ART-ERP-FE/src/app/pages/_template/flat-detail/`
- Production: `pages/WMS/zone/` + `zone-detail/`
- Tree: `pages/_template/tree/`

Do not copy `pages/VMS/` or `services/vms/`.

## Steps

Goal: list `#/{code}` and detail `#/{code}/:id` (`:id` = `0` means create).

1. Copy `_template/flat` → `src/app/pages/{DOMAIN}/{name}/`.
2. Copy `_template/flat-detail` → `src/app/pages/{DOMAIN}/{name}-detail/`.
3. Rename files, classes, and selectors (`app-{name}`, `app-{name}-detail`). Class suffix `Page`. `standalone: false`.
4. Point `pageProvider` at the generated `{Module}_{Resource}Provider` in `services/static/services.service.ts`. Type rows with `models/model-list-interface.ts`. Custom `providerService` only when the live URL is not `{Module}/{Resource}`.
5. Add routes in `pages/{DOMAIN}/routing.module.ts` with `canActivate: [authGuard]` (match the sibling routes in that file):

```ts
{ path: 'my-entity', loadChildren: () => import('./my-entity/my-entity.module').then((m) => m.MyEntityPageModule), canActivate: [authGuard] },
{ path: 'my-entity/:id', loadChildren: () => import('./my-entity-detail/my-entity-detail.module').then((m) => m.MyEntityDetailPageModule), canActivate: [authGuard] },
```

6. Confirm `{DOMAIN}Routes` is spread into `allRoutes` in `app-routing.module.ts`.
7. Strip the sample feature pane (`groupControl` / `ion-fab`) unless the list needs a left group filter.
8. `SYS_Form.Code` equals the route path (`my-entity`). Child forms set `canEdit`, `canAdd`, `ShowDelete`. Do not hardcode toolbar permissions.

`PageBase.add()` navigates to `pageConfig.pageName + '/0'`.

## Modules

List imports: `IonicModule`, `CommonModule`, `FormsModule`, `ShareModule`, `RouterModule.forChild`. Detail also imports `ReactiveFormsModule`.

## Detail audit row

Every routed detail has an audit row at the bottom of the main form. Copy `flat-detail` (the `Other information` row). Show it only when the record exists (`*ngIf="item.Id"`):

```html
<ion-grid fixed *ngIf="item.Id">
	<form [formGroup]="formGroup">
		<ion-row class="hr-group">
			<ion-col size="12" size-sm="12" size-md="12" size-xl="3">
				<ion-list-header class="ion-no-padding"><ion-label color="primary">{{ 'Other information' | translate }}</ion-label></ion-list-header>
			</ion-col>
			<ion-col size="12" size-sm size-xl="4">
				<app-form-control [field]="{ id: 'CreatedBy', type: 'text', label: 'Created by', form: formGroup }"></app-form-control>
				<app-form-control [field]="{ id: 'CreatedDate', type: 'span-datetime', label: 'Created date', form: formGroup }"></app-form-control>
			</ion-col>
			<ion-col size="12" size-sm size-xl="4">
				<app-form-control [field]="{ id: 'ModifiedBy', type: 'text', label: 'Last modified by', form: formGroup }"></app-form-control>
				<app-form-control [field]="{ id: 'ModifiedDate', type: 'span-datetime', label: 'Last modified date', form: formGroup }"></app-form-control>
				<app-form-control [field]="{ id: 'IDBranch', type: 'branch-breadcrumbs', label: 'Branch', form: formGroup, dataSource: env.branchList }"></app-form-control>
			</ion-col>
		</ion-row>
	</form>
</ion-grid>
```

Audit fields have no `(change)`. Their labels are existing English keys (`Created by`, `Created date`, `Last modified by`, `Last modified date`, `Branch`). Do not repeat a field that is already in the general section (for example `Remark`).

## Detail with child tabs

When a detail owns child records (stages, tasks, rules), keep the routed detail and add tabs. Copy `pages/CRM/pipeline-detail/` for the shape.

- Title: `app-page-title` takes the record name and remark (`[title]="formGroup?.value?.Name || pageConfig.pageTitle"`, `[remark]`). Do not repeat them as a large block above the tabs.
- Tabs: `ion-segment` in `ion-toolbar color="primary"`. The first (leftmost) tab is `General information` (`s3` in `pipeline-detail`). Counts are `ion-badge color="warning" style="vertical-align: top"` inside the `ion-label`. Do not recolour the segment.
- `General information` holds the main form, then `Other information` (the audit row from the section above). Do not add a separate block of fields above the tabs.
- Child tabs show only when `item.Id`. For a new record show an `ion-note` (`Save the pipeline first, then add ...`) and open on General information.
- Each child tab is one `app-data-table` (skill `fe-data-table`: Parent and child rows, Child table on a detail tab, Table inside a card or tab). Add and edit open a sheet popup with `form-1column` (skill `fe-popup`). The page reloads the children when the popup closes.
## Colours and translated text

- No hard-coded colour in page or popup CSS (`#000`, `#fff`, `rgba(0, 0, 0, .2)`). The app has a dynamic theme: use `ion-color-*` props, CSS variables (`--ion-color-primary-rgb`, `--main-background-top`) or the `color` attribute.
- Before translating a status or type, search `vi-VN.json` for how the CRM already translates that word (`Lost`, `Won`). Reuse that meaning; skill `i18n-keys`.

## Form name and remark

- `SYS_Form.Name` is the English key that the title shows (`Pipeline`, not a Vietnamese phrase).
- `SYS_Form.Remark` is also an English key. The page title pipes it through `translate`. A Vietnamese sentence here shows untranslated in English mode. Add the sentence to both locale files.
- Change both fields with `form_upsert` and keep the same text in the seed SQL under `ART-DMS/scripts/`.

## GenCode providers

`tbl_{Module}_{Resource}` → provider `{Module}_{Resource}Provider`, interface `{Module}_{Resource}`, URL `{Module}/{Resource}`. Example: `tbl_WMS_Zone` → `WMS_Zone` / `WMS/Zone`.

Use `read`, `getAnItem`, `save`, `delete`, `disable`, `import`, `export` on `pageProvider`. Do not add a second provider file that re-exports the same class.

| Need | Where |
| --- | --- |
| CRUD for a table already in EDMX | Generated provider. If the class is missing, ask to rebuild GenCode. Do not paste a new `APIList` entity. |
| Extra action on the same resource | `APIList.{Name}.approve = { method, url }` in `global-variable.ts` |
| Cache / local search fields | `search-config.ts` via `SearchConfig.getSearchFields('WMS_Zone')` |

Do not edit `api-list.ts`, `services.service.ts`, or `model-list-interface.ts`.

## i18n and tests

New visible strings: skill `i18n-keys`.

After logic/util changes, colocate `*.spec.ts` (Jasmine + Karma). Prefer a pure helper over a full Ionic page spec. Run:

```bash
cd ART-ERP-FE && npx ng test --include=src/app/path/to/file.spec.ts --browsers=ChromeHeadless --watch=false
```

## Checklist

- [ ] Did not copy `pages/VMS/` or `services/vms/`
- [ ] `standalone: false`, `ShareModule`, property name `pageProvider`
- [ ] Provider is the generated `{Name}Provider`
- [ ] Route in the domain routing module; path = `SYS_Form.Code`
- [ ] List: `app-toolbar` + `app-data-table`
- [ ] Detail: `isDetailPage`, `formGroup`, `app-form-control`, `saveChange2`, audit row (`*ngIf="item.Id"`, see Detail audit row)
- [ ] List Name column does not use `flex-break`; no `padding-number-right` unless the last column is numeric
- [ ] List status pills use `ion-chip` / `ion-badge`, with no custom height or font weight (see fe-data-table, Chips and badges)
- [ ] Form `Name` and `Remark` are English keys in both locale files (see Form name and remark)
- [ ] List checked in the browser at desktop width and at 908px (see fe-data-table, Verify before reporting)
- [ ] Every clickable element that is not an `ion-button` has `class="clickable"` (list and detail)
- [ ] Child records: tabs, tree or table, and sheet popups follow Detail with child tabs
- [ ] No hard-coded colour in the page or popup SCSS
- [ ] Lookups in `preLoadData` before `super.preLoadData`
- [ ] Translate keys reused or added in both locale files
- [ ] Spec added and the test command run
- [ ] Did not edit `page-base.ts` or GenCode outputs
