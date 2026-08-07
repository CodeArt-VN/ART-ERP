# G3 — Vị trí form FE (Angular)

**Folder chuẩn:** `ART-ERP-FE/src/app/pages/CRM/`  
(= submodule `ART-ERP-FE-CRM`)

**Branch local submodule:** `AI/crm-wedding-g3-proto-a303`  
**Commit:** xem `git -C ART-ERP-FE/src/app/pages/CRM log -1`

**Routes:** `routing.module.ts` — mã form không prefix `crm-`.

**Push:** cloud agent bị **403** tới `CodeArt-VN/ART-ERP-FE-CRM`.  
Anh/CI cần push branch submodule hoặc apply patch:

`/opt/cursor/artifacts/crm-g3-forms-AI-crm-wedding-g3-proto-a303.patch`

```bash
cd ART-ERP-FE/src/app/pages/CRM
git checkout -b AI/crm-wedding-g3-proto-a303
git am /path/to/crm-g3-forms-AI-crm-wedding-g3-proto-a303.patch
# hoặc: git cherry-pick 1cf3275 nếu có local commit
git push -u origin AI/crm-wedding-g3-proto-a303
```

Sau khi FE-CRM trên remote có commit, cập nhật submodule pointer trên ART-ERP / ART-ERP-FE.
