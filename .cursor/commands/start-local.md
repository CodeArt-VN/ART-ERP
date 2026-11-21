---
name: start-local
description: Start local BE then FE (skip whichever is already listening)
---

# Start local (BE + FE)

Do the steps in order. Do not restart an app that is already up.

BE runs in Parallels VM **Win11** (bridged). From the Mac, health-check BE at `192.168.1.99:54009`, not `localhost:54009`. FE is on the Mac at `localhost:8100`.

## 1. BE (VM 192.168.1.99:54009)

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://192.168.1.99:54009/
```

- Any HTTP status → leave BE alone.
- No response → `cd ART-DMS && ./scripts/run-dms.sh`.

## 2. FE (Mac port 8100)

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://localhost:8100/
```

- `200` → leave FE alone.
- Otherwise → `cd ART-ERP-FE`, `npm install` only if needed, then `ionic serve` in one background terminal. Wait until it listens.

## 3. Report

- BE: `http://192.168.1.99:54009/`
- FE: `http://localhost:8100/`
- Login: choose **Local server** (`http://192.168.1.99:54009/`).

Do not call `run-dms.sh` when BE already responds. Do not use `npm start` / `ng serve` / `npm run dev` for FE.
