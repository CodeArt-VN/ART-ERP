---
name: fe-notifications
description: >-
  Documents the ART-ERP-FE inbox selector app-notifications-modal
  (NotificationsComponent): the embedded tag on the notifications page, its
  only input, list actions, and how it differs from app-page-notification.
  Use when adding or changing notifications, the notification inbox,
  app-notifications-modal, mark as read, or the #/notifications screen in
  ART-ERP-FE.
---

# FE notifications

Ionic + Angular NgModule. `app-notifications-modal` is an embedded inbox. The selector name is not an open path. Nothing calls `modalController.create` for `NotificationsComponent`.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/notifications/notifications.component.ts` and `.html`
- Only host: `ART-ERP-FE/src/app/pages/OSM/notifications/notifications.page.html` and `.ts`
- List service: `ART-ERP-FE/src/app/services/custom/notifications.service.ts`
- Inline page list (different component): `ART-ERP-FE/src/app/components/page-notification/`

## Open

Route `#/notifications` (`path: 'notifications'` in `pages/OSM/routing.module.ts`). Host class `NotificationsPage`, selector `app-notifications`. The page module imports `ShareModule`. `NotificationsComponent` is declared and exported by `ShareComponentsModule`. `standalone: false`.

```html
<app-notifications-modal #notificationComponent [autoLoad]="false"></app-notifications-modal>
```

Host holds `@ViewChild('notificationComponent') notificationComponent!: NotificationsComponent` and calls `notificationComponent.refresh()` from `ionViewWillEnter`. Host `preLoadData` and `loadedData` are empty. The page header stays `app-toolbar`. Do not add a second copy of the tag.

## Inputs

The only `@Input()` is `autoLoad = true`. There is no `@Output()`. Do not pass `item`, `id`, `pageName`, or `componentProps`.

The `ngOnInit` that skipped `loadData()` when `autoLoad` was false is commented out. `PageBase.ngOnInit` still calls `preLoadData()`. The host binding `[autoLoad]="false"` does not stop that load. Keep the binding; do not invent a second flag.

## List and actions

Extends `PageBase`. Constructor `pageProvider` is `OSM_NotificationService`. The component `loadData` that called `readNotification` is commented out, so infinite scroll uses inherited `PageBase.loadData` → `pageProvider.read` (`{ count, data }`). `refresh()` is `clearData()` then `loadData()`.

Row click is `readNoti(i)`: `OSM_NotificationReceiverProvider.save({ Id: parseInt(i.IDReceiver), ReadDate: new Date() })`, then `env.publishEvent({ Code: 'EVENT_TYPE.APP.NOTIFICATION' })`, then `nav(i.Link)`.

Checkboxes use `i.isChecked` and `selectNotification(i, e)` into `selectedNotification` (not `PageBase.selectedItems`). Empty selection means all rows.

| Action | Method | Body |
| --- | --- | --- |
| Mark as read / Mark all as read | `pageProvider.markAsRead` | `{ Ids: IDReceiver[], IsAll: selectedNotification.length == 0 }` |
| Mark as unread / Mark all as unread | `pageProvider.markAsUnRead` | same |
| Delete / Delete all | `pageProvider.deleteNotification` | same |

Each action confirms with `env.showPrompt`, then publishes `EVENT_TYPE.APP.NOTIFICATION`. `AppComponent` handles that code in `loadNotifications()` (`getNotificationCount` for menu badges). The inbox does not reload itself on that event.

Popover `#morePopover` (`presentCopyPopover`): the three actions above, plus `nav('notification-setting')`. Labels switch on `selectedNotification.length`. Template row fields are `Title`, `Body`, `IsRead`, `isChecked`, `IDReceiver`, `Link`. The avatar URL is hardcoded. Infinite scroll `[disabled]="isEndOfData"` reads the component field, which live code never sets. Inherited end-of-list is `pageConfig.isEndOfData`. `nav(URL, direction = 'forward', data = null)` references `event` with no parameter.

## Not app-page-notification

`app-page-notification` is the short list inside `app-page-title` (`page-title.component.html`). Its only input is `pageName`, copied onto `query.Form` in `preLoadData`. It marks one row read, deletes one row, and does not navigate. No popover, no mark-all, no route. Do not put `app-notifications-modal` on a page title, and do not give this inbox `pageName`.

## Chrome

This inbox is an embedded tag on a routed page (`app-toolbar` stays on `NotificationsPage`); if a change turns `app-notifications-modal` into a modal the page authors open, follow skill `fe-popup`.

## Do not

- Open this component with `modalController.create` or add inputs it does not declare.
- Restore the commented `loadData` / `readNotification` path unless the task says so.
- Restyle the ellipsis `ion-header` as popup chrome. It has no Close button and no `ion-footer`.
- Edit `page-base.ts` to change this list.
