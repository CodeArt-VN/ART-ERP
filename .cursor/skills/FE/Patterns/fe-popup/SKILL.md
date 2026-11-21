---
name: fe-popup
description: >-
  Builds ART-ERP-FE Ionic popups with the currency-detail chrome: translucent
  collapsing header, fullscreen scrollbar content, a white `.edit-box` around
  form controls, and a translucent collapse footer with outline actions on the
  left and a strong primary action on the right. Use when adding or changing a
  popup, modal, ion-modal, sheet, dialog, or filter sheet in ART-ERP-FE. Do not
  ask how the header, content box, or footer buttons should look.
---

# FE popup

Ionic + Angular NgModule. A popup is a modal, not a routed detail page. Routed screens stay on skill `new-fe-crud-page` (`app-toolbar` in the header).

Copy the chrome. Do not invent a button bar, `expand="block"`, `ion-buttons` in the footer, or extra footer CSS. `ion-buttons` shrinks a button to a 32px toolbar control.

Canonical files:

- Chrome: `ART-ERP-FE/src/app/pages/ACCOUNTANT/currency-detail/currency-detail.page.html`
- Form box (`.edit-box`): `ART-ERP-FE/src/theme/common.scss` + CRM example `ART-ERP-FE/src/app/pages/CRM/opportunity-detail/modals/activity-modal.page.html`
- Edit footer (Discard changes): `ART-ERP-FE/src/app/pages/SYS/system-type-detail/system-type-detail.page.html`
- List filter sheet: `ART-ERP-FE/src/app/components/data-table/data-table.component.html` (`ion-modal.form-1column`)

## Chrome

```html
<ion-header [translucent]="true" collapse="fade">
	<ion-toolbar>
		<ion-title>{{ item?.Name || ('Title' | translate) }}</ion-title>
		<ion-buttons slot="primary">
			<ion-button title="{{ 'Close' | translate }}" color="secondary" (click)="closeModal()">
				<ion-icon slot="icon-only" name="close"></ion-icon>
			</ion-button>
		</ion-buttons>
	</ion-toolbar>
</ion-header>
<ion-content [fullscreen]="true" appScrollbarTheme>
	<!-- dropdown host when the popup uses ng-select / appendTo -->
	<div id="my-popup-modal" style="position: absolute; z-index: 30005"></div>
	<form [formGroup]="formGroup">
		<!-- required: white box around form controls (theme/common.scss .edit-box) -->
		<div class="edit-box">
			<ion-grid fixed>
				<ion-row>
					<ion-col size="12" size-sm="12" size-md="6">
						<app-form-control [field]="{ id: 'Name', label: 'Name', type: 'text', form: formGroup }"></app-form-control>
					</ion-col>
				</ion-row>
			</ion-grid>
		</div>
	</form>
</ion-content>
<ion-footer [translucent]="true" collapse="fade">
	<ion-toolbar>
		<div slot="start">
			<ion-button fill="outline" *ngIf="item?.Id && pageConfig.canDelete" (click)="delete()" color="danger">{{ 'Delete' | translate }}</ion-button>
		</div>
		<div slot="end">
			<ion-button fill="outline" color="warning" (click)="closeModal()">{{ 'Cancel' | translate }}</ion-button>
			<ion-button [strong]="true" (click)="saveChange()" [disabled]="!formGroup.dirty">{{ 'Save' | translate }}</ion-button>
		</div>
	</ion-toolbar>
</ion-footer>
```

Header and footer are both `[translucent]="true" collapse="fade"`. `ion-content` stays `[fullscreen]="true"` so the form scrolls under the bars.

### Form box (`.edit-box`) — required for form popups

Any popup whose body is `app-form-control` fields must wrap the `ion-grid` in `<div class="edit-box">`. Style lives in `theme/common.scss` (do not re-declare in the page SCSS unless the page needs extra rules like `.edit-box .hr-group`).

- Looks like detail-page cards: white background, light border, 6px radius, 12px margin.
- At ≤425px, global `ion-modal` rules flush the box to the sheet edges (no side margin / side border / radius) while keeping the 12px padding inside — same idea as data-table edge-to-edge.
- Do not invent a per-popup box class. Reuse `.edit-box`.
- Skip `.edit-box` only when the body is not a form: inset `ion-list`, reorder list, map, or a custom preview. Those keep their own chrome. The list **filter sheet** still uses `.edit-box` around its filter fields.

`ion-content` has no `ion-padding` when it holds an `ion-grid fixed` (inside `.edit-box`) or an inset `ion-list`: both already pad, and the class pads a second time. Add `ion-padding` only when raw elements sit directly in the content.

| Place | Control |
| --- | --- |
| Header end | Close, `slot="primary"`, `color="secondary"`, icon `close`. Calls `closeModal()`. |
| Footer start | Destructive outline only. Delete is `fill="outline" color="danger"` when `item.Id` and `pageConfig.canDelete`. |
| Footer end, left of primary | Outline `color="warning"`. New record: Cancel. Existing dirty record: Discard changes (`refresh()`, `[disabled]="!formGroup.dirty"`), as in system-type-detail. |
| Footer end, primary | `[strong]="true"`. Save, Add, or Apply. Disable Save while `!formGroup.dirty`. |

Do not drop `[translucent]="true"` from the footer. Do not add `ion-no-border`, `expand="block"`, `fill="clear"`, or a custom flex row for these buttons.

## Page class

Extend `PageBase`. `standalone: false`. `pageConfig.isDetailPage = true`. Build `formGroup` in the constructor. Read the record from `navParams.data` in `preLoadData` when the page is opened as a modal (`item`, `id`), then `loadData()`. `saveChange()` returns `saveChange2()`. `delete()` calls `closeModal()` after a successful detail delete. Dismiss only through `PageBase.closeModal()`.

Open with `modalController.create`. Wide forms use `cssClass: 'modal90'`. Do not add a new modal size class when `modal90` or `modal90vh` already fits.

## Sheet popup for a record or a child record

A popup that edits one record (a child of a detail page, a rule, a task) is not full screen. Open it as the sheet that the sale-order3 customer picker and cart use, with the one class `form-1column` (`theme/common.scss`):

```ts
const modal = await this.modalController.create({
	component: MyModalPage,
	componentProps: { item: { ...row }, pipeline: this.item },
	cssClass: 'form-1column',
	breakpoints: [0, 0.25, 0.5, 0.75, 1],
	initialBreakpoint: 0.75,
	handleBehavior: 'cycle',
	expandToScroll: false,
});
await modal.present();
const { role } = await modal.onWillDismiss();
if (role === 'saved') await this.reload();
```

- One class only. Do not add a per-popup size class. `form-2columns` and `form-full-width` exist for wide forms; use them only when the form needs two columns.
- The popup takes the row through `@Input() item` and calls `modalController.dismiss(null, 'saved')` after a save or delete. The page reloads its list on that role. Skip the `PageBase` route bootstrap: `ngOnInit` patches `formGroup` from `item` and sets `pageConfig.showSpinner = false`.
- Pass the sibling data the popup needs as inputs (for example every stage and every task of the pipeline) so the popup does not read it again.
- A popup that edits a child also has a field for its parent (`IDStage`, `IDParent`), so the record can be moved. A moved record goes to the end of the target: `Sort = nextSort(tasksOfStage(...))`. Reject a save with no parent.
- Do not use theme-breaking values in popup CSS: no `#000`, no `rgba(0, 0, 0, ...)`. Use theme variables (`--ion-color-primary-rgb`, `--main-background-top`).
- Form body still uses `.edit-box` → `ion-grid fixed` → `app-form-control` (see Chrome above).

## Child list inside a popup

When a popup edits a parent and also lists its children (a stage and its tasks), the list goes last in the popup, as an iOS settings group:

- Section head: `div.ios-settings-head` (theme/common.scss) wrapping `ion-text color="medium"` — do **not** put `padding-inline` inline (≤425px clears head padding with the inset list). The head's right side holds icon-only `ion-button size="small" fill="clear"`: add (`add-circle-outline`) first, then sort (`swap-vertical-outline`, `fill="solid"` while on). Only an icon, no text.
- `ion-list [inset]="true"` with one `ion-item` per child: type icon `slot="start"`, name, and an edit icon button `slot="end"` (`create-outline`). Tapping edit opens the child sheet popup.
- Sort switches on in place: `ion-reorder-group [disabled]="!sorting"` and `ion-reorder slot="end"` replace the edit button while on. Each drop renumbers from 1 and saves only the rows whose `Sort` changed; on a failed save, restore the previous order and show the error. Do not open a second popup for sorting.
- Empty state is a single `ion-item lines="none"` with a medium label.

Fields are `app-form-control` inside `.edit-box` → `ion-grid fixed`. Labels are English translate keys. New strings: skill `i18n-keys`. Reuse `Close`, `Cancel`, `Save`, `Add`, `Delete`, `Discard changes`, `Apply`, `Clear all filters`, `Filter`.

## Narrow phone (≤425px)

Do not add per-popup padding overrides for small screens. `theme/common.scss` already zeros side padding on `ion-modal` content / grid / `.edit-box` margins at `max-width: calc(425px)`, matching data-table edge-to-edge. Keep using `.edit-box` and the sheet classes (`form-1column`, `form-2columns`).

## List filter sheet

Do not add a filter popup to a list page. `app-data-table` already opens an `ion-modal` with class **`form-1column`** on phone, and on widths up to 1164px when the table has `responsive` or `small-width`. Desktop keeps the inline filter row. Do not invent a filter-only size class (`mobile-filter-modal` is retired).

When that sheet changes, keep `class="form-1column"`, the same header, `ion-content [fullscreen]="true" appScrollbarTheme` (no `ion-padding` — the box pads), wrap the filter fields in `.edit-box` → `ion-grid fixed`, and keep the footer slots. Clear all filters is `fill="clear" color="warning"` in `slot="start"`. Apply is `[strong]="true"` in `slot="end"`. Sheet snaps are `0`, `0.25`, `0.5`, `0.75`, `1`, starting at `0.5`, with `[expandToScroll]="false"` so the fields scroll at every snap. `handleBehavior="cycle"`. Do not put the footer back in `ion-buttons`, and do not add CSS that pins or resizes `ion-footer` during the snap.

## Do not

- Ship a form popup or the list filter sheet without `.edit-box` around the controls.
- Ask where Close, Cancel, Delete, or Save go, or whether the form needs a white box.
- Restyle footer buttons to match a one-off modal (`payment-modal`, VMS merge).
- Use the flat-detail `app-toolbar` header inside a popup.
- Edit `page-base.ts` to change popup chrome.
- Re-declare `.edit-box` in a page SCSS unless the page needs extra nested rules.
