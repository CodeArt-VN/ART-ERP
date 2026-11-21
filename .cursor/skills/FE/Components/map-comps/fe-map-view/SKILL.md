---
name: fe-map-view
description: >-
  Documents how to place and configure `app-map-view` in ART-ERP-FE: pass a
  CoordinateList of markers (Address.Lat/Long), optional IsDragable, and handle
  savePosition. Use when adding or changing a multi-marker Google Map, map
  overview, or drag-to-save pin UI. Relates to app-address / app-coordinate-picker
  (same MapCompsModule). Do not reimplement google-map markers for that job.
---

# FE map view

Ionic + Angular NgModule (`standalone: false`). `app-map-view` is a multi-marker Google Map: fit-bounds overview, info window card, optional drag-to-confirm position save. It is not the single-address editor — that is `app-address` (embeds `app-coordinate-picker`).

Import `MapCompsModule` in the feature/page module. `MapViewComponent` is **not** on `ShareModule`. Do not redeclare `app-map-view` in a page module.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/map-comps/map-view/map-view.component.ts`, `map-view.component.html`
- Module: `ART-ERP-FE/src/app/components/map-comps/map-comps.module.ts` (also declares/exports `AddressComponent`, `CoordinatePickerComponent`)
- Sibling single-pin editor: `ART-ERP-FE/src/app/components/map-comps/coordinate-picker/`
- Sibling address form (uses `app-coordinate-picker`): `ART-ERP-FE/src/app/components/map-comps/address/`
- Consumer of `app-address` (not map-view): `ART-ERP-FE/src/app/modals/data-correction-request-modal/`

No in-repo template currently binds `app-map-view`; wire it only when the screen needs a multi-pin map.

## Copy this

Host needs a sized box (`height` on the map is `100%`):

```html
<div style="height: 360px">
	<app-map-view
		[CoordinateList]="markerRows"
		[IsDragable]="pageConfig.canEdit"
		(savePosition)="onSaveMapPosition($event)"
	></app-map-view>
</div>
```

```ts
onSaveMapPosition(ev: { marker: any; content: any }) {
	const lat = ev.marker.getPosition().lat();
	const lng = ev.marker.getPosition().lng();
	// Persist lat/lng from content / Address; map-view only emits after confirm alert
}
```

## CoordinateList row shape

`CoordinateList` setter copies into `addressList` / `items`. Each row that should show a pin needs nested coords and optional display fields:

| Field | Role |
| --- | --- |
| `Address.Lat` / `Address.Long` | Marker position (numbers or numeric strings). |
| `Color` | Marker fill (default `#FF5733`). |
| `Title` / `Subtitle` / `Content` / `Image` | Info window (`ion-card` on click). |
| `option` | Built by the component (`position`, `draggable`, SVG `icon`); do not invent a parallel marker API on the page. |

Rows without usable Lat/Long get no marker.

## `@Input` / `@Output`

| Binding | Default | Role |
| --- | --- | --- |
| `CoordinateList` | — | Array of marker rows (setter → `addressList`). |
| `IsDragable` | `false` | Enables marker drag; on `mapDragend` shows confirm alert then emits. |
| `savePosition` | — | `@Output` payload `{ marker, content }` after user confirms move. |

No projected content slots. No other public `@Input`s for zoom/styles — map `options` live inside the component.

## Behavior (do not reimplement on the page)

- **Maps script:** loads Google Maps via `HttpClient.jsonp` once; sets `env.isMapLoaded`. Template gates on `env.isMapLoaded \|\| (mapLoaded \| async)`.
- **Fit bounds:** after load, builds markers and `map.fitBounds(bounds, 100)`.
- **Info window:** click marker → `openInfo`; card shows `item.Image`, `Title`, `Subtitle`, `Content`.
- **Drag save:** only when `IsDragable`; confirm dialog then `savePosition.emit`.
- **Loading UI:** `app-page-message` while the map script is not ready (`showSpinner` when `!env.isMapLoaded`). Skill `fe-page-message`.

## Relate: `app-address` / `app-coordinate-picker`

Same `MapCompsModule`. Choose by job:

| Need | Use |
| --- | --- |
| Multi-stop / many pins / overview map | `app-map-view` + `CoordinateList` |
| Edit one address (subdivision + contact + Lat/Long) | `app-address` |
| Single draggable pin + geocode / current position (inside address) | `app-coordinate-picker` (already inside `app-address` when `env.isMapLoaded`) |

Do not nest `app-map-view` inside `app-address`. Do not replace `app-coordinate-picker` with a hand-rolled `google-map` on the page when editing one address.

## Do not

- Import or declare `MapViewComponent` in a page NgModule; import `MapCompsModule`.
- Put `app-map-view` on `ShareModule` or rewrite `map-comps.module.ts` for a one-off page.
- Pass flat `Lat`/`Long` on the row root; the view reads `i.Address?.Lat` / `i.Address?.Long`.
- Rebuild multi-marker `google-map` / `map-marker` loops when `app-map-view` fits.
- Edit `map-view.component.ts` / `.html` when the task is only to wire a page — change the host template and `CoordinateList` / `savePosition` handler instead.

New UI strings: skill `i18n-keys`. Loading chrome: skill `fe-page-message`.
