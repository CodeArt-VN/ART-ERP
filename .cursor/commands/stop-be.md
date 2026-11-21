---
name: stop-be
description: Stop ART-DMS IIS Express in the Win11 Parallels VM (does not touch FE)
---

# Stop BE

Stop only the API. Do not stop FE / `ionic serve`.

```bash
prlctl exec Win11 cmd /c "taskkill /F /IM iisexpress.exe /T"
```

Confirm from the Mac that `http://192.168.1.99:54009/` no longer responds, then report stopped. Do not use Mac `localhost:54009` for that check. Do not start the API again unless the user asked.
