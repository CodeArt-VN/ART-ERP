---
name: build-web
description: Build ART-ERP-FE web production via npm run build-web (bump version, ionic build --prod)
---

# Build Web

Production web build for FE on the Mac. Runs from `ART-ERP-FE`.

1. From the Mac host:

```bash
cd ART-ERP-FE
npm run build-web
```

That script runs `node ./replace.build.js build web` (bump version, update `environment.prod` / `baseHref`, `ionic build --prod`, update web resources).

2. Report success or the script error. Do not start `ionic serve` unless the user also asked to run FE locally.
