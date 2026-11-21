---
name: new-be-custom-api
description: Customizes ART-DMS with GenCode hooks, partial BS classes, CustomDTO, or a CustomAPI controller. Use when adding a table, changing list/get/save, adding an endpoint, CustomBusiness, DTO field, or API controller in ART-DMS.
---

# Customize ART-DMS

ASP.NET Web API 2, EF6 database-first (`ClassLibrary/Model.edmx`). Read [reference.md](reference.md) for hook signatures, route rules, and file names.

Copy `ClassLibrary/CustomBusiness/WMS/BS_WMS_Zone.cs` and `API/Controllers/CustomAPI/WMS/WMS.cs` (`WMS_OutboundController`). Do not copy `CustomBusiness/VMS/` or `CustomAPI/VMS/` as a skeleton.

Stored procedure or raw SQL result: follow rule `stored-procedure-api`.

## Choose one path

| Need | Do this |
| --- | --- |
| CRUD for a table already in EDMX | No new BE file. Use `api/v1/{Module}/{Resource}`. |
| Change list, get, or save | `*Custom` hook on the existing `partial class BS_{Name}` |
| Field that is not a column | `partial class DTO_{Name}` in `ClassLibrary/CustomDTO/`. Fill it from the hook. |
| HTTP that is not that table's CRUD | CustomAPI with a prefix that does not repeat GenCode CRUD |
| New table | SQL → EDMX → `Model.tt` → build GenCode → hook only if CRUD is not enough |

If the generated class is missing, update EDMX and run GenCode. Do not paste a controller into `APIControllers.cs`.

## Hook

New file, same class, folder `ClassLibrary/CustomBusiness/{MODULE}/BS_{Name}.cs`, namespace `BaseBusiness`:

```csharp
public static partial class BS_WMS_Zone
{
    public static dynamic getCustom(AppEntities db, int IDBranch, UserModel User, Dictionary<string, string> QueryStrings)
    {
        var query = _queryBuilder(db, IDBranch, User, QueryStrings);
        query = _sortBuilder(query, QueryStrings);
        query = _pagingBuilder(query, QueryStrings);
        return toDTO(query);
    }
}
```

The controller finds the hook by name (`GetMethod("getCustom")`). Match the signatures in [reference.md](reference.md). Call generated `get` / `put` / `post` when the hook only wraps them.

## CustomAPI

Use only when a `*Custom` hook cannot express the operation.

```csharp
namespace API.Controllers.V1
{
    [RoutePrefix("api/v1/WMS/Outbound")]
    public partial class WMS_OutboundController : CustomApiController
    {
        [HttpGet, Route("PickingList")]
        public IHttpActionResult GetPickingList()
        {
            return Ok(/* BS_* */);
        }
    }
}
```

Always: namespace `API.Controllers.V1`, inherit `CustomApiController`, explicit `[HttpGet]` / `[HttpPost]` / `[HttpPut]` / `[HttpDelete]`, thin controller. Add `<Compile Include="Controllers\CustomAPI\..." />` to `API/API.csproj`.

`CustomAuthorize` maps the path after `/api/v1/` to `SYS_Form`. A new route needs a form row or it returns 401. `[AllowAnonymous]` only on an action that is intentionally public.

## Build and test

From `ART-DMS`: `./scripts/build-dms.sh`. Logic that does not need IIS goes in a static helper with a focused test (`ClassLibrary.Tests` or `scripts/`). Do not ask the user to build in Visual Studio when the script succeeds.

## Checklist

- [ ] GenCode + hook was not enough before adding CustomAPI
- [ ] `RoutePrefix` does not duplicate `{Name}Controller` CRUD
- [ ] File under `CustomAPI/{MODULE}/` and registered in `API.csproj`
- [ ] Business logic in `CustomBusiness`; controller stays thin
- [ ] Did not edit `tbl_*.cs`, `Model.Context.cs`, or `APIControllers.cs`
- [ ] CustomBusiness file is `{MODULE}/BS_{Name}.cs` or `{MODULE}/BS_{Name}_{Concern}.cs`
- [ ] Extra DTO fields are `partial` in `CustomDTO/`
- [ ] Secrets masked on GET
- [ ] SQL scripts include `Id`, `IDBranch`, `Code`, `Name`, `Remark`, `Sort`, `IsDisabled`, `IsDeleted`, `CreatedBy`, `CreatedDate`, `ModifiedBy`, `ModifiedDate`
- [ ] `./scripts/build-dms.sh` succeeded
