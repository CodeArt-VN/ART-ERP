---
name: fe-reorder
description: >-
  Places the ART-ERP-FE app-reorder list so rows can be dragged into a new
  sort order. Use when adding or changing app-reorder, a drag handle,
  ion-reorder, or the field that stores sort order in ART-ERP-FE.
---

# FE reorder

Ionic reorder list. `standalone: false`. Selector `app-reorder`. `ShareComponentsModule` declares and exports it. A page module that imports `ShareModule` already has the tag. Do not declare `ReorderComponent` again. Do not edit the component.

Canonical binding: `ART-ERP-FE/src/app/pages/WMS/location/location.page.html`. Handler: `doReorder` in `location.page.ts`.

## Binding

```html
<app-reorder *ngIf="items.length>0" [items]="items" sortProperty="RouteSequence" (reoder)="doReorder($event)"> </app-reorder>
```

`labelField` is omitted, so the row text is `Name`. `sortProperty="RouteSequence"` is the string attribute from that page.

## API

Only these bindings exist.

| Binding | Role |
| --- | --- |
| `items` | Input setter. Copies the array with `[...values]`. Item objects stay the same references. |
| `labelField` | Input. Property printed in `ion-label`. Default `Name`. |
| `sortProperty` | Input. Property set to the new index after a drop. Default `Sort`. |
| `reoder` | Output. The emitter name is `reoder`. Emits the reordered array. |

On drop the component calls `complete`, writes `item[sortProperty] = index` from `0`, then emits that array. `ion-reorder-group` is always enabled. There is no disable input.

## Parent

```ts
doReorder(reOrderedItems) {
	this._items = reOrderedItems;
}
```

Keep the emit until the user saves. The component does not call the API. The array copy is shallow, so `sortProperty` on each item changes when the row is dropped.

Pass an array. The location page uses `*ngIf="items.length>0"` so the setter is not fed a missing list.

## Do not

- Bind `(reorder)`, `[disabled]`, `trackBy`, or any input the class does not declare.
- Rename `reoder`. Templates must use that output name.
- Edit `ART-ERP-FE/src/app/components/reorder/reorder.component.ts` or `.html`.
- Set `standalone: true`, or rewrite the list with `@for`.
