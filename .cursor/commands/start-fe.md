---
name: start-fe
description: Start ART-ERP-FE with ionic serve on port 8100 (skip if already up)
---

# Start FE

FE runs on the Mac (port **8100**).

1. Check if the app is already up:

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://localhost:8100/
```

2. `200` → already running. Report that and stop. Do not start a second `ionic serve`.

3. Otherwise, from `ART-ERP-FE`:

```bash
cd ART-ERP-FE
npm install     # only when node_modules is missing or package.json changed
ionic serve
```

4. Run `ionic serve` in one background terminal. Wait until it is listening. Report `http://localhost:8100/`.

Do not use `npm start`, `ng serve`, or `npm run dev`. Do not edit `src/environments/environment.ts` just to start.
