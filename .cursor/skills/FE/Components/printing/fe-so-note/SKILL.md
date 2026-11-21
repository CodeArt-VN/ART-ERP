---
name: fe-so-note
description: >-
  Embeds the ART-ERP-FE sale order delivery and payment slip, selector
  app-so-note (SaleOrderNoteComponent). Use when adding or changing a sale
  order print slip, delivery note, or payment slip that uses app-so-note.
  Pass the sale order id with [ID]. The component is standalone false and is
  exported by SharePrintingModule through ShareModule. The routed page
  sale-order-note is a different screen and does not use this selector.
---

# FE sale order note

Ionic + Angular NgModule. `app-so-note` renders one sale order slip. It is not a routed page and it does not print. Routed screens stay on skill `new-fe-crud-page`.

`pages/SALE/sale-order-note` (`app-sale-order-note`) is a different screen. It prints its own HTML and does not use `app-so-note`.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/printing/sale-order-note/sale-order-note.ts`
- Template: `ART-ERP-FE/src/app/components/printing/sale-order-note/sale-order-note.html`
- Module: `ART-ERP-FE/src/app/components/printing/share-printing.module.ts`
- Only call site: `ART-ERP-FE/src/app/pages/APPROVAL/request-detail/request-detail.page.html`

## Module

`standalone: false`. `SaleOrderNoteComponent` is declared and exported only in `SharePrintingModule`, next to `PurchaseOrderNoteComponent`. `ShareComponentsModule` imports and re-exports `SharePrintingModule`. `ShareModule` exports `ShareComponentsModule`.

A page that already imports `ShareModule` can use `<app-so-note>`. Do not declare `SaleOrderNoteComponent` on the page module. Do not import `SharePrintingModule` again when `ShareModule` is already imported.

## Inputs

No `@Output`. Do not add inputs. The class declares only these two:

| Input | Behavior |
| --- | --- |
| `ID` | Sale order id. `preLoadData` copies it to `this.id`. When `item` is null, `PageBase` loads `SALE_OrderProvider.getAnItem`. |
| `item` | When not null, skip the get and call `loadedData`. No template in the repo binds `[item]`. |

`pageProvider` is `SALE_OrderProvider`. The constructor sets `pageConfig.isDetailPage = true`.

The only real usage is the approval request when `item.Type=='SaleOrder'`. `item.UDF01` is that request's sale order id, not a component input.

```html
<ion-row *ngIf="item.Type=='SaleOrder'">
	<ion-col size="12" class="A4">
		<div style="overflow: auto" *ngIf="item">
			<div class="giao-nhan">
				<section class="sheet padding-10mm rpt p1">
					<app-so-note [ID]="item.UDF01"></app-so-note>
				</section>
			</div>
		</div>
	</ion-col>
</ion-row>
```

Keep that host chrome when embedding the slip on a print sheet. `app-po-note` flags (`PONShowPackingUoM`, `PONShowEACaseOnly`, `PONConvertToLargerUoM`) are not inputs of `app-so-note`.

## Slip

The root table is `*ngIf="item?.Id"`. After load, `loadDeliveryNote` formats date and money text on `item`, sets `BranchName`, `BranchLogoURL`, and `BranchAddress` from `env.branchList` by `IDBranch`, and writes `item.QRC` with `lib.genBankTransferQRCode('mb', '0908061119', OriginalTotalAfterTax, 'SO' + Id)`. Bank and QR options live in `generatePaymentQRCODE`. There is no input for them.

The header reads `item._Customer` (Code, Id, Name, WorkPhone, Address) and `item.OrderLines` (ItemCode or IDItem, ItemName, Quantity, UoMName, UoMPrice, OriginalTotalAfterDiscount). The get behind `[ID]` fills `_Customer` only when the order has both `IDContact` and `CustomerId`. The template does not guard `_Customer` before those fields.

`loadDeliveryNote` sets `HasDiscountFromSalesman = false`, so the salesman discount table does not show. `CompanyPhone` and `CompanyPhone2` render only when they are already on `item`. This component does not load them.

Labels are English translate keys. New strings: skill `i18n-keys`.

## Do not

- Add an `@Input` or `@Output`, or bind `[item]` because a call site does not.
- Point a sale order print task at `pages/SALE/sale-order-note` when the screen should use `app-so-note`.
- Set `standalone: true`, or convert this component to signals or native control flow.
- Give `app-so-note` the purchase-order note flags.
- Edit the component to add a print button. Printing belongs to the host page.
