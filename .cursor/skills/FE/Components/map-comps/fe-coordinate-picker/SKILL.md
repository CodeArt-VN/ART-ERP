---
name: fe-coordinate-picker
description: >-
  Documents how to place and configure `app-coordinate-picker` on ART-ERP-FE
  address and map screens: pass address Lat/Long, canEdit for marker drag, and
  (change)/(toggleLatLong) outputs. Use when adding or changing a Google Maps
  lat/long picker, geocode-by-address, or current-position control in
  ART-ERP-FE. Do not confuse with app-map-view (multi-marker) or reimplement
  the map inside app-address.
---

# FE coordinate picker

Ionic + Angular NgModule (`standalone: false`). Single-address Lat/Long map with a draggable marker, geocode-by-address, and current GPS. Not a multi-stop map — that is `app-map-view`. Not the address form fields — that is `app-address`.

Declared and exported only by `MapCompsModule` next to `MapViewComponent` and `AddressComponent`. Not re-exported by `ShareModule`. Import `MapCompsModule` on the host NgModule. Do not redeclare `CoordinatePickerComponent`.

Canonical files:

- Component: `ART-ERP-FE/src/app/components/map-comps/coordinate-picker/coordinate-picker.component.ts`, `coordinate-picker.component.html`
- Module: `ART-ERP-FE/src/app/components/map-comps/map-comps.module.ts`
- Sibling address: `ART-ERP-FE/src/app/components/map-comps/address/address.component.ts` (`changeCoordinate`, `showLatLong`)
- Sibling map: `ART-ERP-FE/src/app/components/map-comps/map-view/map-view.component.ts` (`CoordinateList`, `IsDragable`, `savePosition`)

There is **no** live `<app-coordinate-picker>` template call site in the repo today. Wire new hosts against the inputs/outputs below; do not invent extra bindings.

## Copy this

Host that already holds an address object (`Lat`, `Long`, and the address form fields):

```html
<app-coordinate-picker
	[canEdit]="canEdit"
	[address]="item"
	(change)="changeCoordinate($event, formGroup)"
	(toggleLatLong)="showLatLong = !showLatLong"
></app-coordinate-picker>
```

`AddressComponent.changeCoordinate(coordinate, form)` already writes `coordinate.Lat` / `coordinate.Long`, marks them dirty, and calls `submitChange()`. Prefer that helper when the host is (or embeds) `app-address`.

## Relate to map-view / address

| Selector | Role |
| --- | --- |
| `app-coordinate-picker` | One address: show/edit `Lat`/`Long`, geocode from address lines, GPS. |
| `app-address` | Address form (province/district/ward, contact, phones). Owns `showLatLong` and `changeCoordinate` for the picker payload. |
| `app-map-view` | Many points via `[CoordinateList]`; optional drag confirm via `(savePosition)`. Not a Lat/Long form control. |

Do not nest `app-map-view` for a single partner address. Do not paste raw `<google-map>` / `<map-marker>` on the page when this picker covers the job.

## `@Input` / `@Output`

| Binding | Kind | Role |
| --- | --- | --- |
| `canEdit` | Input (setter) | Sets `markerOptions.draggable`. When falsy, Find / Get-current buttons stay hidden (`*ngIf="markerOptions.draggable"`). |
| `address` | Input (setter) | Patches the inner `formGroup`. Coerces `Lat`/`Long` string commas to dots via `parseFloat`. Marks pristine after patch. |
| `change` | Output | Emits full `formGroup.value` after marker drag, geocode, or GPS (`saveChange()`). |
| `toggleLatLong` | Output | Label click; host typically toggles Lat/Long field visibility (`showLatLong` on `app-address`). |

No other inputs. Do not bind `center`, `options`, `markerOptions`, or `formGroup` from the host.

## Behavior (do not reimplement on the page)

- **Map:** `@angular/google-maps` `google-map` + `map-marker`; default center `11.0517262, 106.8842023`, zoom 16; POI/transit off.
- **Drag end:** `changePosition` writes marker lat/lng into `Lat`/`Long` (dirty) and emits `change`.
- **Find coordinates by address:** builds a geocode string from `AddressLine2`, `AddressLine1`, `Ward`, `District`, `Province`, calls Google Geocoding HTTP, then emits `change`.
- **Get current coordinates:** `navigator.geolocation`; writes `Lat`/`Long` and emits `change`.
- **Inner form fields:** `Id`, `Country`, `Province`, `District`, `Ward`, `AddressLine1` (required), `AddressLine2`, `ZipCode`, `Lat`, `Long`, `Contact` (required), `Phone1` (required), `Phone2`, `Remark`. The template only shows the map and coordinate actions; the host/`app-address` owns the visible address fields.

## Do not

- Import or declare `CoordinatePickerComponent` in a page NgModule; import `MapCompsModule`.
- Use `app-map-view` when the screen needs one address Lat/Long editor.
- Duplicate geocode / GPS / marker-drag logic beside the picker.
- Edit `coordinate-picker.component.ts` / `.html` when the task is only to wire a host — change the host template and handlers instead.
- Set `standalone: true`, or convert this component to signals or native control flow.

New UI strings: skill `i18n-keys`. Popup chrome around a map sheet: skill `fe-popup`.
