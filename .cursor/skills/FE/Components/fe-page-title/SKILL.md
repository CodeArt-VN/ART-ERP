---
name: fe-page-title
description: >-
  Places the ART-ERP-FE page heading (selector app-page-title) in ion-content on
  routed list and detail screens, binding pageConfig from PageBase for icon,
  color, title, remark, and page name. Use when adding or changing a page title,
  page heading, or app-page-title markup in ART-ERP-FE.
---

# FE page title

Ionic + Angular NgModule. `app-page-title` is the large heading inside `ion-content`. The top bar stays `app-toolbar` in `ion-header`. `standalone: false`.

`ShareModule` already exports it (`ShareComponentsModule` declares and exports `PageTitleComponent`). Import `ShareModule` on the page module. Do not declare `PageTitleComponent` again.

Canonical markup:

- List: `ART-ERP-FE/src/app/pages/_template/flat/flat.page.html`
- Detail: `ART-ERP-FE/src/app/pages/_template/flat-detail/flat-detail.page.html`
- Component: `ART-ERP-FE/src/app/components/page-title/page-title.component.ts`, `page-title.component.html`

## Copy-paste HTML

Default binding (flat list and flat detail):

```html
<app-page-title class="ion-padding safe-max-width" [pageConfig]="pageConfig"></app-page-title>
```

Keep `class="ion-padding safe-max-width"`.

| Screen | Where |
| --- | --- |
| List | In `ion-content`, after `ion-refresher` / feature `ion-fab`, before `app-data-table` (often inside `safe-max-width`). |
| Detail | In `ion-content`, inside `main-view` when the record is shown (flat detail: `*ngIf="item && pageConfig.showSpinner==false"`), before the form grid. |

Popups do not use this (skill `fe-popup`). New CRUD screens still follow skill `new-fe-crud-page`; this skill only covers the heading.

## pageConfig fields the component reads

`PageBase` initializes `pageConfig` with `pageTitle: ''`, `pageRemark: ''`, `pageIcon: 'star'`, `pageColor: 'primary'`, `pageName: ''`.

In `PageBase.ngOnInit`, when the current route matches a user form (`env.user.Forms`, Type 0/1/2), it sets:

| `pageConfig` field | Source |
| --- | --- |
| `pageName` | `currentForm.Code` |
| `pageTitle` | `currentForm.Name` |
| `pageIcon` | `currentForm.Icon` |
| `pageColor` | `currentForm.BadgeColor` |
| `pageRemark` | `currentForm.Remark` |

Pages may override those fields later (example: `flat.page.ts` sets `pageConfig.pageIcon = 'flash-outline'` in `preLoadData`).

## Inputs

No `@Output`.

| Input | Use |
| --- | --- |
| `pageConfig` | Pass the page `pageConfig` object. The setter copies `pageIcon` → `icon`, `pageColor` → `color`, `pageTitle` → `title`, `pageRemark` → `remark`, `pageName` → `pageName`. A falsy value is ignored. |
| `icon`, `color`, `title`, `remark`, `pageName` | Bind individually when `pageConfig` is not bound, or when one field (usually `remark`) is not on `pageConfig`. |

Scalar example when `remark` is computed (`ART-ERP-FE/src/app/pages/VMS/edge-node/vms-edge-node.page.html`):

```html
<app-page-title class="ion-padding safe-max-width" [icon]="pageConfig.pageIcon" [color]="pageConfig.pageColor" [title]="pageConfig.pageTitle" [remark]="fleetLine" [pageName]="pageConfig.pageName"></app-page-title>
```

Do not bind `[pageConfig]` and the five scalars on the same tag. The setter writes all five fields when `pageConfig` is set.

The `pageConfig` setter runs when Angular sets that input, not when individual `pageConfig` properties change later. After mutating `pageConfig.pageIcon` (or similar) in `preLoadData`, prefer scalar bindings or set those fields before the first render.

## What the template renders

- `ion-icon`: `[name]="icon || 'layers'"`, `[color]="color || 'primary'"`.
- `h1`: `(title ? title : 'Untitled') | translate`.
- `p`: `remark | translate`.
- `app-page-notification`: `[pageName]="pageName"`.
- Projected slot: `<ng-content select="[rightContent]">` (no current page template uses it).

Pass English translate keys for `title` and `remark`. Do not add `| translate` on the host bindings. New strings: skill `i18n-keys`.

Global layout: `ART-ERP-FE/src/theme/common.scss` styles `app-page-title` as `display: block; position: sticky; left: 0;`.

## Do not

- Edit `page-title.component.ts` or `page-title.component.html`.
- Redeclare the component or set `standalone: true`.
- Replace `app-toolbar` in `ion-header` with `app-page-title`.
- Invent inputs or outputs (there is no click or action output).
- Put Vietnamese literals in `pageTitle` / `pageRemark`.
- Double-translate `remark`: the inner template already pipes it; `fleetLine` on edge-node already uses `translate.instant`.
