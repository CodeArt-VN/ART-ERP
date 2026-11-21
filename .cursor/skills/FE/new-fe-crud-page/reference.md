# FE page reference

Read this when writing a page class or template. Samples live in `src/app/pages/_template/`.

## Constructor

`PageBase` assigns these public fields. Detail also needs `route`, `formBuilder`, and `cdr`.

```ts
constructor(
  public pageProvider: SYS_ActionProvider,
  public env: EnvService,
  public navCtrl: NavController,
  public modalController: ModalController,
  public popoverCtrl: PopoverController,
  public alertCtrl: AlertController,
  public loadingController: LoadingController,
  public location: Location,
) {
  super();
}
```

Detail constructor sets `this.pageConfig.isDetailPage = true` and builds `formGroup`. `Id`, `IsDisabled`, `IsDeleted`, and the audit fields are disabled controls. `IDBranch` defaults to `this.env.selectedBranch`.

## Lifecycle

Call `super`. Almost never override `ngOnInit`.

| Hook | Behavior |
| --- | --- |
| `preLoadData` | Load ng-select sources, set `pageConfig.sort`, then `super.preLoadData()` → `loadData()` |
| `loadData` | List: `pageProvider.read(query)`. Detail: `loadAnItem`. Rarely override |
| `loadedData` | Detail patches `formGroup`. Map display fields, then `super.loadedData(event)` |
| `saveChange` | `return super.saveChange2()` so only dirty fields plus `Id` and `IDBranch` are sent |

List query default: `{ Keyword: '', Take: 200, Skip: 0 }`. Sort: `pageConfig.sort = [{ Dimension: 'Id', Order: 'DESC' }]`.

Leave `isDetailPage` false on the list. Feature pane: `isShowFeature` + `isFeatureAsMain`, class `left`, `[ngClass]="{ withFeature: pageConfig.isShowFeature }"`. Omit when unused.

## List HTML

Keep `ion-header` > `app-toolbar`, then `ion-content.appScrollbarTheme` with `ion-refresher` → `refresh`, `app-page-title`, and `app-data-table`.

Bind `[rows]="items"`, `[trackBy]="'Id'"`, `[(selectedRows)]="selectedItems"`, `[showSpinner]`, `[showFilter]`, `[(query)]="query"`, `(dataInfinite)="loadData($event)"`, `(filter)="onDatatableFilter($event)"`, `(sort)="onSort($event)"`, `(selectedRowsChange)="showCommandBySelectedRows($event)"`.

Columns: checkbox, then `property="Id"` with `[navLink]="pageConfig.pageName"`, then data columns. Width classes: `col-id`, `col-code`, `col-name`, `col-date`, `col-number`, `col-status`, `col-icon`, `flex-break`.

Custom cell uses `ng-template let-i="row" datatable-cell-template`. Filter: `filterControlType` `date` or `ng-select`, `[filterDataSource]`, default `bindValue` `Id`, `bindLabel` `Name`.

Do not copy `system-type.page.html` (`<section class="table">`) for a new list.

## Detail form

- `*ngIf="item && pageConfig.showSpinner==false"` around the form.
- `app-page-title`, then `ion-grid.fixed` and `form [formGroup]="formGroup"`.
- Section rows: `ion-row.hr-group`, title `ion-col size-xl="3"`, fields `size-xl="4"`.
- Every input: `<app-form-control [field]="{ id, label, type, form: formGroup }" (change)="saveChange()">`.
- Footer when `item.Id`: Created/Modified, `type: 'branch-breadcrumbs'`, Remark. Copy flat-detail.
- `<app-page-message [itemsLength]="item? 1: 0" [showSpinner]="pageConfig.showSpinner">`.

`type` values: `text`, `number`, `textarea`, `checkbox`, `date`, `datetime-local`, `ng-select`, `ng-select-branch`, `ng-select-status`, `ng-select-bp`, `ng-select-item`, `ng-select-staff`, `ng-select-async`, `span-datetime`, `branch-breadcrumbs`, `icon-color`, `time-frame`.

ng-select sets `dataSource`, `bindLabel`, `bindValue`, and `appendTo: '#my-detail-page'`. Put `<div id="my-detail-page" style="position: absolute; z-index: 30005"></div>` on the page so the menu is not clipped.

Lookups resolve before `super.preLoadData`. On failure, still call `super.preLoadData`.

Segments (`segmentView` / `ion-segment`) only when the form has multiple tabs.

## Other shapes

| Shape | When | Sample |
| --- | --- | --- |
| Flat list + routed detail | Default CRUD | `_template/flat` + `flat-detail` |
| Tree + routed detail | `IDParent` hierarchy | `_template/tree` |
| List + modal detail | Small entity, no own URL | `pages/SYS/system-type` |
| Custom workspace | Dashboard, POS, report | Still `PageBase` + `ShareModule` |

If the list uses `app-data-table` and `navLink`, the detail is a routed page, not a modal.

## Messages

`env.showMessage(key, 'success' | 'danger' | …)`, `env.actionConfirm(…)`, `env.getStatus('Code')`, `env.getType('Code')`, `env.branchList`, `env.selectedBranch`.

SCSS stays colocated. Reuse `safe-max-width`, `box-shadow`, `hr-group`, `ion-padding`. Do not add a CSS framework.
