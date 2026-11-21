---
name: fe-page-message
description: >-
  Adds ART-ERP-FE loading spinners and empty states via selector app-page-message
  on list, detail, and nested table pages. Use when wiring pageConfig.showSpinner,
  hiding main content until data is ready, or showing the standard no-data illustration
  instead of a blank ion-content.
---

# FE page message

Ionic + Angular NgModule. `app-page-message` covers the page (or a section) while data loads or when there is nothing to show. It is not the list filter sheet and not `app-data-table`’s built-in empty row (see `datatable-empty-message` inside `app-data-table` on `_template/flat`).

Source:

- Component: `ART-ERP-FE/src/app/components/page-message/page-message.component.ts`, `page-message.component.html`
- Detail: `ART-ERP-FE/src/app/pages/_template/flat-detail/flat-detail.page.html`
- Header-table list: `ART-ERP-FE/src/app/pages/WMS/zone/zone.page.html`
- Detail line grid: `ART-ERP-FE/src/app/pages/WMS/shipping-detail/shipping-detail.page.html`

Page modules already import `ShareModule`. Do not edit `page-message.component.*` or `share.module.ts` to change page behavior.

## Behavior

The host renders when `showSpinner` is truthy **or** `itemsLength` is falsy (`*ngIf="showSpinner || !itemsLength"`).

| State | What shows |
| --- | --- |
| `showSpinner` truthy | `ion-spinner` (`dots`) |
| `showSpinner == false` and falsy `itemsLength` | Illustration (optional), `message`, `subMessage`, projected `<ng-content>` |
| Truthy `itemsLength` and not loading | Component hidden; show your real UI beside/under it |

`message` and `subMessage` run through the `translate` pipe. Defaults in `ngOnInit`: `'No data available'`, `'Please check again'`. New strings: skill `i18n-keys`.

`imgSrc` setter: values starting with `http` are used as-is; otherwise prefixed with `assets/`. Default image: `assets/undraw_no_data_qbuo.svg`.

## Copy-this markup

Always bind `[showSpinner]="pageConfig.showSpinner"` on CRUD pages unless you intentionally invert it (e.g. map load — see below).

**Header-table list** (WMS zone pattern — table body gated separately):

```html
<ion-content [fullscreen]="true" appScrollbarTheme class="header-table">
	<app-page-message [itemsLength]="items.length" [showSpinner]="pageConfig.showSpinner"></app-page-message>
	<div *ngIf="items.length && pageConfig.showSpinner==false">
		<!-- rows -->
	</div>
</ion-content>
```

**Flat detail** (`_template/flat-detail` — main form gated on `item`):

```html
<ion-content [fullscreen]="true" appScrollbarTheme class="ion-padding">
	<div class="main-view" *ngIf="item && pageConfig.showSpinner==false">
		<!-- form / tabs -->
	</div>
	<app-page-message [itemsLength]="item? 1: 0" [showSpinner]="pageConfig.showSpinner"></app-page-message>
</ion-content>
```

**Optional empty copy** (defaults are fine for generic lists):

```html
<app-page-message
	[itemsLength]="items.length"
	[showSpinner]="pageConfig.showSpinner"
	message="No data available"
	subMessage="Please check again"
	[showImg]="true"
	minHeight="50vh"
	imgSrc="undraw_no_data_qbuo.svg"
></app-page-message>
```

Project extra actions into the empty state:

```html
<app-page-message [itemsLength]="items.length" [showSpinner]="pageConfig.showSpinner">
	<ion-button size="small" (click)="refresh()">{{ 'Refresh' | translate }}</ion-button>
</app-page-message>
```

## List vs detail: `itemsLength`

| Screen | Typical `itemsLength` | Gate real UI with |
| --- | --- | --- |
| List (header-table) | `items.length`, `items?.length`, or `items?.length>0` | `*ngIf="items.length && pageConfig.showSpinner==false"` |
| Detail (single record) | `item? 1: 0` or `item ? 1 : 0` | `*ngIf="item && pageConfig.showSpinner==false"` on `.main-view` |
| Detail segment / fab shell | `[itemsLength]="1"` while only spinner matters | `*ngIf="pageConfig.showSpinner==false"` on sibling content (`item-detail`) |
| Nested detail lines | `formGroup.get('ShippingDetails')['controls']` (same for `OutboundOrderDetails`, `AdjustmentDetails`, etc.) | Row `*ngFor` on the same control array; empty lines rely on spinner + array binding in existing WMS pages |
| Non-CRUD overlay | `[itemsLength]="1"` with `[showSpinner]="!env.isMapLoaded"` | Hide map until loaded (`map-view.component.html`) |

**`_template/flat` list** does not use `app-page-message`. It passes `[showSpinner]="pageConfig.showSpinner"` to `app-data-table` only. Add `app-page-message` when copying **zone-style** header-table lists, not when copying flat datatable lists.

Boolean `itemsLength` (`items?.length>0`) is equivalent to a count for empty vs loaded; prefer `items.length` when the list is always an array.

## @Input API

| Input | Default | Role |
| --- | --- | --- |
| `itemsLength` | — | Falsy → empty state (when not spinning). Truthy → hide message. |
| `showSpinner` | — | Truthy → loading spinner. |
| `message` | set in `ngOnInit` if unset | Title under illustration; translate key. |
| `subMessage` | set in `ngOnInit` if unset | Secondary line; translate key. |
| `minHeight` | `'50vh'` | Container `min-height` while visible. |
| `showImg` | `true` | Toggle illustration block. |
| `imgSrc` | via setter | Override empty-state image (see setter rules above). |

## Do not

- Show list rows or detail forms without also gating on `pageConfig.showSpinner==false` (double condition with `itemsLength` / `item`).
- Replace `app-page-message` on flat datatable lists unless removing `app-data-table` empty/loading behavior too.
- Ask whether to use `pageConfig.showSpinner` — that is the standard PageBase flag.
- Invent a second empty-state layout; reuse this component and optional `ng-content`.
