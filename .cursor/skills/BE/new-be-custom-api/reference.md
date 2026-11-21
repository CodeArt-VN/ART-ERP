# ART-DMS customization reference

## Generated surface

`tbl_{Module}_{Resource}` → `BS_{Module}_{Resource}`, `DTO_{Module}_{Resource}`, `{Module}_{Resource}Controller`, route `api/v1/{Module}/{Resource}`.

| Generator | Output (do not hand-edit) |
| --- | --- |
| `ClassLibrary/Model.tt` | `tbl_{Name}.cs` — entity, `DTO_{Name}`, `BS_{Name}` |
| `ClassLibrary/Model.Context.tt` | `Model.Context.cs` — `AppEntities` |
| `GenCode/API.tt` | `API/Controllers/APIControllers.cs` |
| `GenCode` FE templates | `api-list.ts`, `services.service.ts`, `model-list-interface.ts` |

If `BS_{Name}` has a `*Custom` method, reflection uses it instead of the default.

| HTTP | Route | Default | Hook |
| --- | --- | --- | --- |
| GET | `""` | `get` | `getCustom` |
| GET | `Search` | `getSearch` | `getSearchCustom` |
| GET | `{id:int}` | `getAnItem` | `getAnItemCustom` |
| PUT | `{id:int}` | `put` | `putCustom` |
| POST | `""` | `post` | `postCustom` |
| PUT | `Disable/{id}` / `Enable/{id}` | `disable` | — |
| POST | `ChangeBranch` | `changeBranch` | — |
| GET | `Export` | `export` | `exportCustom` |
| POST | `Import` | `import` | `importCustom` |
| DELETE | `{ids}` | `delete` | — |

Already on `BS_{Name}`: `_queryBuilder`, `_sortBuilder`, `_pagingBuilder`, `toDTO`, `patchDynamicToDB`, `getAnItemByCode`, `check_Exists`, `getValidateData`.

Query strings: `Keyword`, `Id` / `Id_ne`, `{Field}` / `{Field}_ne`, date ranges, `Skip` / `Take`, `SortBy`. `ForceCreate` on PUT inserts when missing. `IDBranch` comes from `IDBranch` or `SelectedBranch`.

## Hook signatures

```csharp
getCustom(AppEntities db, int IDBranch, UserModel User, Dictionary<string, string> QueryStrings)
getSearchCustom(AppEntities db, int IDBranch, UserModel User, Dictionary<string, string> QueryStrings)
getAnItemCustom(AppEntities db, int IDBranch, UserModel User, int id)
putCustom(AppEntities db, int IDBranch, UserModel User, int id, dynamic item, Dictionary<string, string> QueryStrings)
postCustom(AppEntities db, int IDBranch, UserModel User, dynamic item)
exportCustom(ExcelPackage package, AppEntities db, int IDBranch, UserModel User, Dictionary<string, string> QueryStrings)
importCustom(ExcelPackage package, AppEntities db, int IDBranch, UserModel User, Dictionary<string, string> QueryStrings)
```

## CustomAPI files

| Pattern | File | Class |
| --- | --- | --- |
| New workflow prefix | `{MODULE}/{Module}_{Resource}Controller.cs` | `{Module}_{Resource}Controller` |
| Extra action on the generated controller | `{MODULE}/{Module}_{Entity}Controller.cs` | `partial` of the GenCode controller |
| Many actions, one prefix | several files, one `partial` class | only one file declares `[RoutePrefix]` and `: CustomApiController` |

Prefer one class per prefix (`WMS_OutboundController` at `api/v1/WMS/Outbound`).

Route rules:

1. Do not steal GenCode CRUD. `tbl_VMS_Person` stays at `api/v1/VMS/Person`. Extra actions use a sub-path or another prefix.
2. One verb attribute per action. Stack extra `[Route]` aliases on that single `[HttpPost]`.
3. Do not collide with generated `GET {id}`. Prefer `{Resource}/{id}/{Verb}`.
4. Read branch from `QueryStrings` (`IDBranch` / `SelectedBranch`).

`[Authorize]` is on `CustomApiController`. `CurrentUser` is `UserModel`. `db` is `AppEntities`. Prefer LINQ on `db.tbl_*`. Raw `SqlCommand` only when EF cannot express the query.

## CustomBusiness names

Folder = module prefix. File name = class name. Namespace `BaseBusiness`.

| What | Path | Class |
| --- | --- | --- |
| Hooks for one table | `{MODULE}/BS_{Module}_{Entity}.cs` | `BS_{Module}_{Entity}` |
| Extra concern, same table | `{MODULE}/BS_{Module}_{Entity}_{Concern}.cs` | same `partial` class |
| EF view | `_vw/BS_vw_{Name}.cs` | `BS_vw_{Name}` |
| Helper that is not the entity | `{MODULE}/{DistinctName}.cs` | not `BS_{Entity}` |

`{Concern}` is PascalCase (`POS`, `Merge`, `BatchImport`). Do not add files that drop `BS_`, use kebab-case, trail with `_`, or sit at the CustomBusiness root. Leave existing root files `Common.cs`, `errorLog.cs`, and `OrderedQueryable.cs` as they are.

## New table

1. SQL under `scripts/{module}/` with the standard audit and soft-delete columns.
2. Update `Model.edmx`.
3. Save `Model.tt` so `tbl_{Name}.cs` is regenerated.
4. Build GenCode so `APIControllers.cs` and the FE provider update.
5. Add `getCustom`, CustomDTO, or CustomAPI only if generated CRUD is not enough.
6. Seed `SYS_Form` when `CustomAuthorize` must allow the screen. `Code` matches the path after `/api/v1/`.
