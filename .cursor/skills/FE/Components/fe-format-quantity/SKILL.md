---
name: fe-format-quantity
description: >-
  Renders a quantity split across units of measure with Ionic styling in
  ART-ERP-FE via `<app-format-quantity>`. Use when a list or detail template
  should show multi-UoM breakdown (integer amounts plus UoM labels) and
  highlight negative totals.
---

# ART-ERP-FE `app-format-quantity`

Read-only display component. Source: `ART-ERP-FE/src/app/components/format-quantity/`.

## What it does

- Loops `splitQuantityList` and prints each line: **integer quantity** (`number: '1.0-0'`) and **UoM name** in `<small>`.
- Uses `quantity` (total) for `ion-text` `[title]` and for sign styling: if `quantity < 0`, color is `danger` and a `-` prefix is shown once per line (magnitude comes from each item’s `Quantity`, not negated in the pipe).
- `standalone: false` — declare `FormatQuantityComponent` in the NgModule that owns the template (it is not referenced in `share.module.ts` in the current tree).

## API (`format-quantity.component.ts`)

| Binding | Direction | Type (source) | Role |
|--------|-----------|---------------|------|
| `splitQuantityList` | `@Input()` | untyped | Array iterated in the template; each element needs `Quantity` and `UoMName`. |
| `quantity` | `@Input()` | untyped | Total quantity; drives tooltip (`title`) and negative styling. |

**Outputs:** none (`@Output` not defined).

**Item shape** (from `format-quantity.component.spec.ts`):

```ts
{ Quantity: number; UoMName: string }
```

## Page usage in this repo

Search `ART-ERP-FE` for `<app-format-quantity`: **no page or component templates use it yet.** Only the component, its spec, and this skill reference the selector.

When adding the first screen usage, bind parent fields that already hold the total and split list (same names as `@Input` unless the page maps aliases in the template).

## Copy-this snippet

Minimal template (input names match the component API):

```html
<app-format-quantity
	[quantity]="quantity"
	[splitQuantityList]="splitQuantityList">
</app-format-quantity>
```

Example values from `format-quantity.component.spec.ts` (positive total):

```ts
quantity = 12;
splitQuantityList = [
	{ Quantity: 1, UoMName: 'Thùng' },
	{ Quantity: 2, UoMName: 'Hộp' },
];
```

Negative total (danger + minus prefix):

```ts
quantity = -3;
splitQuantityList = [{ Quantity: 3, UoMName: 'Cái' }];
```

## Module wiring

1. Import `FormatQuantityComponent` from `src/app/components/format-quantity/format-quantity.component`.
2. Add it to the page (or shared) module `declarations`.
3. Import `IonicModule` (or a module that already exports it) so `ion-text` works — same as the component spec.

## Do not

- Do not add `@Output` or two-way binding; the component is display-only.
- Do not expect decimals in the UI; the template uses `'1.0-0'`.
- Do not convert to standalone unless the whole repo convention changes (`fe-ngmodule` rule).

## Verify

Extend or run `format-quantity.component.spec.ts` when changing behavior. After wiring into a page, add a colocated spec or template test if the page module policy requires it.
