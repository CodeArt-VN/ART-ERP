---
name: fe-formula-expand-modal
description: >-
  Documents ART-ERP-FE app-formula-expand-modal: the Monaco formula expand
  sheet opened from input-control / form-control type formula, with token
  dataSource insert and dismiss-on-save. Use when adding or changing a
  formula field, formula expand modal, or type formula Monaco editor in
  ART-ERP-FE. Do not place app-formula-expand-modal on a page template or
  reimplement the expand sheet.
---

# FE formula expand modal

Standalone Ionic modal (`standalone: true`). Full-screen Monaco SQL editor plus a left token tree. Pages never host the selector — `app-input-control` opens it when `type: 'formula'`.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/controls/formula-expand-modal.ts`, `formula-expand-modal.html`, `formula-expand-modal.scss`
- Opened by: `ART-ERP-FE/src/app/components/controls/input-control.component.ts` (`openFormulaModal`)
- Inline host: `input-control.component.html` (`*ngSwitchCase="'formula'"`)
- Label chrome: `app-form-control` forwards the same `[field]` (skill `fe-form-control`)

There is **no** page `type: 'formula'` call site in the repo today. Wire new hosts against the field shape below.

## How pages use it

Prefer **`app-form-control` with `type: 'formula'`**. That wraps `app-input-control`, which:

1. Loads Monaco into a compact inline editor (`chartScriptId`).
2. Shows Save + Expand outline icon buttons.
3. On Expand, `modalController.create({ component: FormulaExpandModalComponent, cssClass: 'modal90', componentProps: { dataSource, value, item } })`.
4. On dismiss with a string, patches `form.get(id)`, marks dirty, emits `(change)`, and syncs the inline Monaco value.

Direct `app-input-control` with the same field works when the page already owns the label.

Do **not** put `<app-formula-expand-modal>` in a page template. Do not call `modalController.create(FormulaExpandModalComponent)` from a page — keep open/dismiss in input-control.

```html
<app-form-control
	[field]="{
		id: 'Formula',
		label: 'Formula',
		type: 'formula',
		form: formGroup,
		dataSource: tokenList
	}"
	(change)="onFormulaChange($event)"
></app-form-control>
```

`dataSource` items: `Code`, `Name`, optional `Group` / `SubGroup` / `Icon` / `Color`. Leaf rows (tree level 3) insert `[Code]` at the caret; `/` triggers Monaco completion for the same tokens.

## `@Input` / dismiss

| Binding | Kind | Role |
| --- | --- | --- |
| `value` | Input | Initial Monaco text (`form.get(id).value`). |
| `dataSource` | Input | Flat token list; modal groups by `Group` / `SubGroup`. |
| `item` | Input | Passed as `this.form` today; unused in the modal body — do not rely on it. |

No `@Output`. `save()` → `modalCtrl.dismiss(editorValue)`. `dismiss()` / header Close → `modalCtrl.dismiss(null)`. Parent applies the value only when dismiss `data` is truthy.

## Modal chrome

This sheet is a one-off formula editor (Monaco + `ion-fab` token tree), not a CRUD popup. Do not copy it as a popup template — new CRUD/filter sheets use skill `fe-popup`.

When editing **this** modal’s header/footer only, align toward `fe-popup`: translucent header + Close (`slot="primary"`, `color="secondary"`, icon `close`), translucent footer with Cancel outline (`color="warning"`) and strong primary Save. Keep the Monaco pane and token fab; do not invent a second button bar.

Current template still uses a simpler Close (`close-outline`, `slot="end"`) and a single warning Save in the footer — change those only when the task is chrome cleanup.

## Do not

- Host `app-formula-expand-modal` on a routed page or invent a second open path beside `type: 'formula'`.
- Reimplement Monaco expand / token insert beside input-control.
- Treat this modal as the canonical popup chrome (skill `fe-popup`).
- Convert the component to NgModule/`standalone: false` unless the task explicitly migrates it with the rest of ShareInputControls.

New UI strings: skill `i18n-keys`.
