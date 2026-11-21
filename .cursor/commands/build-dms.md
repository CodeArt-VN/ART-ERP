---
name: build-dms
description: Build ART-DMS Debug via Parallels only (does not restart IIS Express)
---

# Build DMS

Build only — do not start or kill IIS Express.

From the Mac host:

```bash
cd ART-DMS
./scripts/build-dms.sh
```

Report success or the script error. Do not run MSBuild/`dotnet` on macOS. Do not call `run-dms.sh` unless the user also asked to start the API.
