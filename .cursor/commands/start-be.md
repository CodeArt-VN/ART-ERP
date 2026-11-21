---
name: start-be
description: Start ART-DMS API on VM 192.168.1.99:54009 (skip if already up)
---

# Start BE

BE runs in Parallels VM **Win11** (bridged). From the Mac, do **not** curl `localhost:54009`.

1. Check if the API is already up:

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://192.168.1.99:54009/
```

2. Any HTTP status (including 401/403/404) means IIS Express is up. Report that and stop. Do **not** call `run-dms.sh` (it kills IIS Express).

3. No response → start from the Mac host:

```bash
cd ART-DMS
./scripts/run-dms.sh
```

4. When done, report `http://192.168.1.99:54009/`. Do not run MSBuild/`dotnet`/IIS Express on macOS. Do not ask the user to click Run in Visual Studio.
