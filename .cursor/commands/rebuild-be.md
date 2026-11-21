---
name: rebuild-be
description: Build ART-DMS then start IIS Express only if VM 192.168.1.99:54009 is down
---

# Rebuild BE

1. Build (always):

```bash
cd ART-DMS
./scripts/build-dms.sh
```

2. Check the API from the Mac (bridged VM — not localhost):

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://192.168.1.99:54009/
```

3. Any HTTP status → API still up. Report build done; do **not** call `run-dms.sh` (it kills IIS Express). Do not `taskkill` unless the user asked to restart.

4. No response after build → start without rebuilding again:

```bash
cd ART-DMS
NO_BUILD=1 ./scripts/run-dms.sh
```

5. Report `http://192.168.1.99:54009/`.
