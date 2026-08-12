# ART-ERP

Umbrella repo: FE (Ionic/Angular/Capacitor), DMS API, MCP, and **ART-ERP-Edge** (restaurant edge host).

## VMS / ERP-Edge (feature/vms)

| Path | Role |
|------|------|
| [ART-ERP-Edge/](ART-ERP-Edge/) | Cross-platform edge: platform API + VMS face attendance/guest |
| [ART-DMS/scripts/vms/](ART-DMS/scripts/vms/) | SQL schema for `tbl_VMS_*` |
| [ART-DMS/API/Controllers/CustomAPI/VMS/](ART-DMS/API/Controllers/CustomAPI/VMS/) | Edge + ERP VMS APIs |
| [ART-ERP-FE/src/app/pages/VMS/](ART-ERP-FE/src/app/pages/VMS/) | FE views |

See `ART-ERP-Edge/docs/` for OpenAPI, UC, NFR, pilot checklist.
