---
name: fe-po-note
description: >-
  Embeds the ART-ERP-FE purchase order slip, selector app-po-note
  (PurchaseOrderNoteComponent). Use when adding or changing a purchase order
  print slip that uses app-po-note. Pass the purchase order id with [ID], or
  a loaded order with [item] and optional [configByBranch] / PON* UoM flags.
  The component is standalone false and is exported by SharePrintingModule
  through ShareModule. The routed page purchase-order-note also hosts this
  selector; do not rebuild the slip HTML on that page.
---

# FE purchase order note

Ionic + Angular NgModule. `app-po-note` renders one purchase order slip. It is not a routed page and it does not print. Routed screens stay on skill `new-fe-crud-page`. Sale order slips use skill `fe-so-note`.

`pages/PURCHASE/purchase-order-note` (`app-purchase-order-note`) is a different screen. It loads sheets and print chrome, then embeds `<app-po-note [item]="o">`. Do not duplicate the slip markup on that page.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/printing/purchase-order-note/purchase-order-note.ts`
- Template: `ART-ERP-FE/src/app/components/printing/purchase-order-note/purchase-order-note.html`
- Module: `ART-ERP-FE/src/app/components/printing/share-printing.module.ts`
- Call sites: `ART-ERP-FE/src/app/pages/APPROVAL/request-detail/request-detail.page.html`, `ART-ERP-FE/src/app/pages/PURCHASE/purchase-order-note/purchase-order-note.page.html`

## Module

`standalone: false`. `PurchaseOrderNoteComponent` is declared and exported only in `SharePrintingModule`, next to `SaleOrderNoteComponent`. `ShareComponentsModule` imports and re-exports `SharePrintingModule`. `ShareModule` exports `ShareComponentsModule`.

A page that already imports `ShareModule` can use `<app-po-note>`. Do not declare `PurchaseOrderNoteComponent` on the page module. Do not import `SharePrintingModule` again when `ShareModule` is already imported.

## Inputs

No `@Output`. Do not invent extra inputs. The class declares only these:

| Input | Behavior |
| --- | --- |
| `ID` | Purchase order id. `preLoadData` copies it to `this.id`. When `item` is null, after status load `PageBase` loads `PURCHASE_OrderProvider.getAnItem`. |
| `item` | When not null, skip the get and call `loadedData`. Routed print page binds `[item]="o"`. |
| `PONShowPackingUoM` | Optional. If still null after load, filled from branch config. Packing column markup in the template is commented out. |
| `PONShowEACaseOnly` | Optional. When true, line columns are Box / LCL; when false (default path), Unit / S.L. If null, filled from branch config. |
| `PONConvertToLargerUoM` | Optional. If null, filled from branch config. Not read by the template. |
| `configByBranch` | Optional `{ IDBranch, Configs }`. When `Configs` match `item.IDBranch`, `applyConfigByBranch` uses them and skips `sysConfigService.getConfig`. |

`pageProvider` is `PURCHASE_OrderProvider`. The constructor sets `pageConfig.isDetailPage = true` and `pageConfig.isShowFeature = true`.

Real usages:

```html
<!-- Approval request when item.Type=='PurchaseOrder'. item.UDF01 is the PO id. -->
<ion-row *ngIf="item.Type=='PurchaseOrder'">
	<ion-col size="12" class="A4">
		<div style="overflow: auto" *ngIf="item && purchaseOrderFormGroup">
			<div class="giao-nhan">
				<section class="sheet padding-10mm rpt p1">
					<app-po-note [ID]="item.UDF01" [PONConvertToLargerUoM]="true" [PONShowPackingUoM]="true" [PONShowEACaseOnly]="false"></app-po-note>
				</section>
			</div>
		</div>
	</ion-col>
</ion-row>
```

```html
<!-- Routed purchase-order-note page: host supplies loaded sheet + branch config. -->
<section class="sheet padding-10mm rpt p1">
	<app-po-note [item]="o" [configByBranch]="configByBranch">
	</app-po-note>
</section>
```

Keep that host chrome when embedding the slip on a print sheet. `app-so-note` has no PON* flags.

## Slip

The root table is `*ngIf="item && item.Id > 0"`. After load, `preparePurchaseOrderNote` formats date and money text on `item` and lines, sorts `OrderLines`, and writes `item.QRC` via `QRCode.toDataURL('PO:' + Id, …)`. `loadConfigByIDBranch` then fills null PON* inputs and `_Branch.LogoURL` from `SmallLogo` when config applies.

The header reads `item._Branch` (LogoURL), `item._Storer.CompanyName`, `item._Vendor`, `item._Warehouse` (Name, Address, TemplateHeader, Phone, Phone2), status ribbon for draft / canceled / request statuses, and `item.OrderLines` with `_Item`, `_SplitUoMs`, prices, and amounts. The get behind `[ID]` must return those nested objects; this component does not load vendor or warehouse separately.

Labels are English translate keys. New strings: skill `i18n-keys`.

## Do not

- Add an `@Output`, or invent inputs beyond the six above.
- Point a purchase order print task at rebuilding slip HTML on `pages/PURCHASE/purchase-order-note` when the screen should use `app-po-note`.
- Set `standalone: true`, or convert this component to signals or native control flow.
- Give `app-so-note` the PON* flags, or give `app-po-note` sale-order QR / bank helpers.
- Edit the component to add a print button. Printing belongs to the host page.
