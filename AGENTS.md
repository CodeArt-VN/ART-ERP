# ART-ERP

## Cursor Cloud specific instructions

### What this repo is
- Monorepo of **git submodules**. The runnable development product is `ART-ERP-FE` — an Angular 20 + Ionic 8 + Capacitor web/mobile ERP (login screen brands as "CODEART"). Its scripts live in `ART-ERP-FE/package.json`.
- `ART-ERP-BE` is effectively empty (README/LICENSE only) — nothing to run.
- `ART-DMS` is a legacy .NET Framework backend (`DMS-Server.sln`, Visual Studio 2017). It is Windows/MSBuild-only and cannot be built or run in this Linux cloud VM.
- The FE talks to remote backends (e.g. `https://api.inholdings.vn/`, `https://demo1.appcenter.vn/`), not a locally-run server. There is no local backend in this environment.

### Submodules (important)
- Feature modules under `ART-ERP-FE/src/app/pages/*` are themselves git submodules. If they are not initialized, the FE build fails with unresolved imports. The startup update script runs `git submodule update --init --recursive` for this reason.

### Installing dependencies (non-obvious)
- Use `npm install --force` inside `ART-ERP-FE`. Do NOT use a plain `npm install` (fails with an Angular `ERESOLVE` peer conflict between Angular 20.1.x and 20.3.x), and do NOT use `--legacy-peer-deps` (it succeeds but skips the `@fullcalendar/resource` peer dependency, which then breaks `ng build`). `--force` resolves the Angular conflict and still installs the fullcalendar peer.
- `postinstall` patches `@exxili/capacitor-nfc` and `@capacitor/status-bar` inside `node_modules`; it is safe and skips gracefully if files are missing.

### Run / build / lint / test (from `ART-ERP-FE/`)
- Dev server: `npx ng serve --host 0.0.0.0 --port 4200` (or `npm start`). Default build configuration is `production`; pass `--configuration development` for a dev build (`npm run build -- --configuration development`).
- Lint: `npm run lint` runs, but the codebase currently reports ~8000 pre-existing style errors (mostly `@angular-eslint/prefer-inject`). These are not environment problems.
- Unit tests (`npm test` / `ng test`): Karma needs headless Chrome with `--no-sandbox` in this container (define a `ChromeHeadlessNoSandbox` custom launcher and set `CHROME_BIN=$(which google-chrome)`). The toolchain works, but most committed `*.spec.ts` files are NOT migrated to Angular 20 — ~116 import the removed `async` from `@angular/core/testing` and 5 use the removed `TestBed.get(...)`, which blocks the suite from compiling. Fixing those is a code migration task, not an environment fix.

### Logging in / demoing the app
- The login page has a "Change server" control to pick the backend tenant. Reaching authenticated ERP modules requires valid credentials for the chosen server; those are not present in this environment. Server switching and the login request flow work end-to-end against the remote APIs.
