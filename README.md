# ART-ERP — start BE and FE (AI)

Workspace root. Two apps to run locally:

| App | Folder | What it is |
| --- | --- | --- |
| **BE** | [`ART-DMS`](ART-DMS/) | ASP.NET Web API 2 (.NET Framework 4.7.2). Solution `DMS-Server.sln`. |
| **FE** | [`ART-ERP-FE`](ART-ERP-FE/) | Ionic + Angular 20. Start with `ionic serve`. |

`ART-ERP-BE/` is not the API. Do not look for a .NET project there and do not try to `dotnet run` it.

Agent constraints: [`.cursor/rules/`](.cursor/rules/). Workflows: [`.cursor/skills/`](.cursor/skills/). App notes: [`ART-DMS/README.md`](ART-DMS/README.md), [`ART-ERP-FE/README.md`](ART-ERP-FE/README.md).

---

## Must / must not

**Must**

- Run commands from the Mac host. Repo must stay under `$HOME` (Parallels share `\\Mac\Home\...`).
- Before starting either app, check whether it is already listening. If it is, leave that process alone.
- Start BE only with [`ART-DMS/scripts/run-dms.sh`](ART-DMS/scripts/run-dms.sh). Start FE only with `ionic serve` in `ART-ERP-FE`.
- One BE process (port **54009**) and one FE process (port **8100**). Do not open a second terminal for the same app.

**Must not**

- Do not run MSBuild, `dotnet`, or IIS Express on macOS. Build and the site run inside the Parallels VM **`Win11`**.
- Do not call `run-dms.sh` when `http://192.168.1.99:54009/` already responds. That script kills IIS Express and starts it again.
- Do not health-check BE via Mac `http://localhost:54009/` — the VM is bridged; use `192.168.1.99`.
- Do not start FE with `npm start`, `ng serve`, or `npm run dev`. The command is `ionic serve`.
- Do not edit `ART-ERP-FE/src/environments/environment.ts` just to start the apps.
- Do not ask the user to click Run in Visual Studio or to start the servers themselves when these scripts succeed.

---

## 1. Backend — `ART-DMS`

API from the Mac: `http://192.168.1.99:54009/` (`api/v1/...`). IIS Express listens on port **54009** inside Parallels VM **`Win11`** (bridged). Mac `localhost:54009` does **not** reach it.

### Already up?

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://192.168.1.99:54009/
```

Any HTTP status (including 401/403/404) means IIS Express is up. Skip start.

No response → start:

```bash
cd ART-DMS
./scripts/run-dms.sh
```

The script starts VM `Win11` if needed, builds Debug, then starts IIS Express. It blocks until the port listens, then exits. The site keeps running in the VM.

| Need | Command |
| --- | --- |
| Build only | `cd ART-DMS && ./scripts/build-dms.sh` |
| Start without rebuild | `cd ART-DMS && NO_BUILD=1 ./scripts/run-dms.sh` |
| Release build | `cd ART-DMS && ./scripts/build-dms.sh Release` |

After BE code changes that must be live: `./scripts/build-dms.sh`, then `NO_BUILD=1 ./scripts/run-dms.sh` only if the API was stopped or you need a fresh IIS Express. One run at a time — the script `taskkill`s `iisexpress.exe`.

Stop:

```bash
prlctl exec Win11 cmd /c "taskkill /F /IM iisexpress.exe /T"
```

One-time VM setup (urlacl, `applicationhost.config`, VS 18) is in [`ART-DMS/README.md`](ART-DMS/README.md#build-and-run-parallels-desktop). If `run-dms.sh` fails on a missing `applicationhost.config` or port permission, follow that section. Do not invent another host or port.

---

## 2. Frontend — `ART-ERP-FE`

App: `http://localhost:8100/` (hash router, so routes are `http://localhost:8100/#/...`).

### Already up?

```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://localhost:8100/
```

`200` → already running. Do not start another `ionic serve`.

Otherwise, from `ART-ERP-FE`:

```bash
cd ART-ERP-FE
npm install     # only when node_modules is missing or package.json changed
ionic serve
```

`ionic serve` stays in the foreground. Run it in one background terminal and wait until the log says the dev server is listening. Do not start a second `ionic serve` while port 8100 is taken.

Node.js **20+** (Angular 20). Stop by ending that one `ionic serve` process.

Login talks to `environment.appDomain` (`http://192.168.1.99:54009/` in dev). On the login screen pick **Local server** with that same URL. Do not retarget `appDomain` unless the user asked.

---

## Order

1. BE: confirm `http://192.168.1.99:54009/`, or `./scripts/run-dms.sh`.
2. FE: confirm `:8100`, or `npm install` (if needed) then `ionic serve`.
3. Open `http://localhost:8100/`, choose **Local server** (`http://192.168.1.99:54009/`).

Rebuild BE after API changes (`build-dms.sh`). FE `ionic serve` recompiles on save; do not restart it for a normal edit.

---

## Slash commands (Customize → Commands)

Project prompts in [`.cursor/commands/`](.cursor/commands/). Details stay in [`.cursor/rules/run-local.mdc`](.cursor/rules/run-local.mdc).

| Command | What it does |
| --- | --- |
| `/start-be` | Start API if `192.168.1.99:54009` is down |
| `/start-fe` | `ionic serve` on Mac `:8100` if down |
| `/start-local` | BE then FE; skip whichever is already up |
| `/build-dms` | Debug build only (no IIS restart) |
| `/rebuild-be` | Build; start with `NO_BUILD=1` only if VM API is down |
| `/stop-be` | Kill IIS Express in VM `Win11` |
