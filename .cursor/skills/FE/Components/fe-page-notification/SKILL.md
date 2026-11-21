---
name: fe-page-notification
description: >-
  Documents the ART-ERP-FE short notification list (selector app-page-notification)
  embedded under the page heading by app-page-title, filtered by pageName → query.Form.
  Use when adding or changing app-page-notification, page-title notification chips,
  or page-scoped notification read/delete in ART-ERP-FE. Not the inbox
  app-notifications-modal (skill fe-notifications).
---

# FE page notification

Ionic + Angular NgModule. `app-page-notification` is the short per-page notification list under the heading remark. It is not the inbox. `standalone: false`.

`ShareComponentsModule` declares and exports `PageNotificationComponent`; `ShareModule` re-exports it. Page authors do not place this tag themselves — `app-page-title` already embeds it. Do not declare `PageNotificationComponent` again.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/page-notification/page-notification.component.ts`, `.html`, `.scss`
- Host: `ART-ERP-FE/src/app/components/page-title/page-title.component.html`
- List service: `ART-ERP-FE/src/app/services/custom/notifications.service.ts` (`OSM_NotificationService`)
- Mark-read provider: `OSM_NotificationReceiverProvider` from `services/static/services.service.ts`

Inbox / full list: skill `fe-notifications` (`app-notifications-modal`). Heading chrome: skill `fe-page-title`.

## How it is embedded

Only host markup (inside `app-page-title`):

```html
<app-page-notification [pageName]="pageName"></app-page-notification>
```

`pageName` on the title comes from `pageConfig.pageName` (or the scalar `[pageName]` binding). That value is the form/page code used as the notification filter.

Do not add a second `<app-page-notification>` on a list or detail template. Do not put `app-notifications-modal` under the page title.

## Inputs

No `@Output`.

| Input | Use |
| --- | --- |
| `pageName` | Copied onto `this.query.Form` in `preLoadData` before `super.preLoadData`. Filters the list to notifications for that form/page. |

There is no `autoLoad`, `item`, `id`, or mark-all input. Do not invent them.

## Behavior (source)

Extends `PageBase`. Constructor `pageProvider` is `OSM_NotificationService`. List load uses inherited `PageBase` → `pageProvider.read` with `query.Form = pageName`.

| Action | Method | What it does |
| --- | --- | --- |
| Row click / link | `readNoti(i)` | `notificationReceiverProvider.save({ Id: parseInt(i.IDReceiver), ReadDate: new Date() })`, then `env.publishEvent({ Code: 'EVENT_TYPE.APP.NOTIFICATION' })`. `nav(i.Link)` is commented out — navigation is the `<a [href]="'#/' + i.Link">` only. |
| Trash button | `deleteNoti(i, event)` | `event.stopPropagation()`, confirm via `env.showPrompt`, then `pageProvider.deleteNotification({ Ids: [i.IDReceiver], IsAll: false })`, publish the same event, splice `i` from `items`. |

Template row fields: `Title`, `Body`, `IsRead` (gray vs black), `Link`, `IDReceiver`. No checkboxes, no mark-all, no unread, no popover, no infinite-scroll chrome beyond `PageBase`.

`AppComponent` listens for `EVENT_TYPE.APP.NOTIFICATION` to refresh menu badge counts. This component does not reload itself on that event after delete beyond the local splice; after read it does not update `IsRead` in `items` in source.

## Not app-notifications-modal

| | `app-page-notification` | `app-notifications-modal` |
| --- | --- | --- |
| Skill | `fe-page-notification` | `fe-notifications` |
| Role | Short list under `app-page-title` | Embedded inbox on `#/notifications` |
| Filter | `pageName` → `query.Form` | No `pageName` |
| Actions | Mark one read; delete one | Mark/unmark/delete selection or all; row navigates via `nav` |
| Host | Only inside `page-title.component.html` | `notifications.page.html` |

## Do not

- Edit `page-notification.component.ts` / `.html` / `.scss` unless the task is specifically about this short list.
- Place `app-page-notification` on a page template next to `app-page-title` (it is already inside the title).
- Pass inbox-only inputs or restore commented `nav(i.Link)` unless the task says so.
- Confuse this with `app-notifications-modal` or open it via `modalController.create`.
- Invent outputs, mark-all, or a second filter input beyond `pageName`.
