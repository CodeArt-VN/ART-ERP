---
name: fe-quill-editor
description: >-
  Documents ART-ERP-FE rich text via app-quill-editor and input-control
  type editor: form binding, optional insert-token dataSource, change
  emit, and preview/edit page patterns. Use when adding or changing a Quill
  editor, HTML template body, or type editor field in ART-ERP-FE. Do not
  reimplement Quill on the page or edit quill-editor.component.* for wiring.
---

# FE quill editor

Ionic + Angular NgModule (`standalone: false`). Rich text is Quill (snow), loaded at runtime via `DynamicScriptLoaderService` / `thirdPartyLibs.quill`. Value stored on the reactive form is **HTML string** (empty editor → `null`).

Pages already import `ShareModule` → `ShareInputControlsModule`. `QuillEditorComponent` is declared/exported there. Do not redeclare `app-quill-editor` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/controls/quill-editor.component.ts`, `quill-editor.component.html`, `quill-editor.component.scss`
- Wired by: `ART-ERP-FE/src/app/components/controls/input-control.component.html` (`*ngSwitchCase="'editor'"`)
- Module: `ART-ERP-FE/src/app/components/controls/share-input-controls.modules.ts`
- Page pattern (direct `app-input-control`): `ART-ERP-FE/src/app/pages/HRM/contract-template-detail/contract-template-detail.page.html`
- Page pattern (remark / modal): `ART-ERP-FE/src/app/pages/PM/task-modal/task-modal.page.html`
- Insert tokens (`dataSource`): same contract-template page (`dataSource: UDFList`)

## How pages use it

Prefer **`app-input-control` with `type: 'editor'`**. That switch case hosts `app-quill-editor` and passes `form`, `id`, `quillEditorId`, `dataSource`, `placeholder`, and forwards `(change)`.

`app-form-control` also works: it wraps `app-input-control` and forwards the same `[field]` / `(change)`. Existing screens usually call `app-input-control` directly for large template bodies (edit/preview toggle, full-width column).

Do **not** put a raw `<div id="editor">` + `new Quill(...)` on new pages. Legacy raw Quill remains on `SYS/help-detail` (and similar preview-only markup elsewhere); do not copy that when adding a field.

`InputControlField.type` accepts `'editor'` via the open `| string` union in `controls.interface.ts` (not listed as a named literal).

## Copy this

Edit/preview block (most detail pages):

```html
<div *ngIf="!showEditorContent && item?.Remark" [innerHtml]="item?.Remark | safeHtml" class="ql-editor"></div>
<form *ngIf="showEditorContent" [formGroup]="formGroup" id="screenEditor">
	<app-input-control
		[field]="{
			form: formGroup,
			type: 'editor',
			id: 'Remark',
			label: 'Template Content',
			placeholder: 'Enter template content...'
		}"
		(change)="onTemplateChange($event)"
	></app-input-control>
</form>
<div class="c-control ion-text-right">
	<label class="c-label" for=""></label>
	<ion-button (click)="saveChange()">{{ 'Save' | translate }}</ion-button>
</div>
```

With insert-token sidebar (`dataSource` items: `Code`, `Name`, optional `Group` / `SubGroup` / `Icon` / `Color`):

```html
<app-input-control
	[field]="{
		form: formGroup,
		type: 'editor',
		id: 'Template',
		label: 'Template Content',
		placeholder: 'Enter template content...',
		dataSource: UDFList
	}"
	(change)="onTemplateChange($event)"
></app-input-control>
```

Clicking a leaf token inserts `[Code]` at the caret.

Via `app-form-control` (same field shape):

```html
<app-form-control
	[field]="{ id: 'Remark', label: 'Remark', type: 'editor', form: formGroup, placeholder: 'Remark' }"
	(change)="saveChange()"
></app-form-control>
```

`field.id` must match a control on `formGroup`. Preview HTML uses the `safeHtml` pipe and class `ql-editor`.

## `@Input` / `@Output` (`app-quill-editor`)

| Binding | Default | Role |
| --- | --- | --- |
| `form` | — | `FormGroup` holding the HTML value. |
| `id` | — | Control name; `form.get(id)` is read/written. |
| `quillEditorId` | auto UID if missing | DOM id for the Quill mount (`#quillEditor…`). `input-control` generates one when `type == 'editor'`. |
| `placeholder` | `'Typing ...'` | Quill placeholder. |
| `dataSource` | — | Optional token list; non-empty shows the left fab search tree and enables insert. |
| `(change)` | — | Emits current HTML after text-change / show-html toggle. |

No other public inputs. Toolbar (bold, lists, headers, image URL prompt, show-html, etc.) is fixed inside the component.

## Behavior (do not reimplement on the page)

- **Load:** if `Quill` is undefined, loads `thirdPartyLibs.quill.source`, then `initQuill()`.
- **Write:** `text-change` sets `form.get(id)` to `root.innerHTML`, `markAsDirty()`, emits `(change)`. Bare `<p><br></p>` clears to `null`.
- **Sanitize:** initial HTML and show-html round-trip go through `DomSanitizer` (`SecurityContext.HTML`).
- **Image:** toolbar image handler prompts for a URL and `insertEmbed`s it.
- **Show HTML:** toolbar `showhtml` toggles between rich HTML and raw markup text in the editor surface.

## Known page usages (`type: 'editor'`)

| Page | Control id | Notes |
| --- | --- | --- |
| `PM/task-modal` | `Remark` | Modal; edit/preview. |
| `CRM/brand-detail` | `Remark` | Direct `app-input-control`. |
| `HRM/contract-template-detail` | `Template` | `dataSource: UDFList`. |
| `HRM/staff-contract-detail` | `_ContractContent` | Custom template body. |
| `HRM/employee-policy-detail` | `Remark` | |
| `HRM/work-rule-detail` | `ComplianceRules`, `DisciplinaryActions` | Two editors. |
| `HRM/work-rule-violation-detail` | `Remark` | |

## Do not

- Import or declare `QuillEditorComponent` in a page NgModule.
- Call `new Quill(...)` or duplicate `loadQuillEditor` / `initQuill` on a page for a new field.
- Use Monaco/`type: 'formula'` when the field is rich HTML (that path is code, not Quill).
- Edit `quill-editor.component.ts` / `.html` when the task is only to wire a page — change the page template and `formGroup` instead.
- Drop `form` or `id`; without them the editor cannot persist.

Field labels / placeholders: skill `i18n-keys`. Form field object shape: skill `fe-form-control`. Popup chrome: skill `fe-popup`.
