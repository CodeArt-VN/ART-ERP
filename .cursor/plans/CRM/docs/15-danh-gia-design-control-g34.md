# Đánh giá design + control — CRM Wedding G3.4 (toàn bộ form)

**Ngày:** 2026-07-25  
**Đối tượng:** UX / design review + BA  
**Chuẩn UI:** `ar-invoice` list · `outlet-detail` hr-group · **không** hero marketing / KPI insight trên form nghiệp vụ

---

## 1. Chuẩn đã áp

| Hạng mục | Quy tắc | Trạng thái |
|----------|---------|------------|
| List | `app-toolbar` + `app-page-title` + `app-data-table` (+ cards toggle nếu cần) | Done toàn menu G3 |
| Detail | `app-page-title` + `row-full shadow` + `ion-row.hr-group` liên tục | Done các form demo G3 |
| Action | Nút nghiệp vụ trên toolbar; không sticky CTA trùng | Done |
| Status / stage | Status bar kiểu outlet (Lead, Opp, Hold…) | Done nơi có pipeline |
| BI trên form | Không chart/insight strip | Đã gỡ hero/insight |
| Sentence case | Tên form trong menu/bootstrap | Giữ |
| Mobile | Không h-scroll (trừ kanban Opp / calendar grid) | Giữ |

---

## 2. Quy tắc control (bắt buộc cho design đánh giá)

| Loại dữ liệu | Control đúng | Không dùng |
|--------------|--------------|------------|
| Enum / trạng thái (Status, Stage, Slot, HoldType, Channel…) | `<select class="c-input c-dropdown">` | Textbox |
| Master / FK (Team, Owner, Hall, Package, Process, Campaign, Segment, Opp…) | `<select>` (demo) / `ng-select` (prod) | Textbox gõ tay |
| Số (Score, Amount, Qty, Pax, %) | `type="number"` | text |
| Ngày / giờ | `type="date"` / `datetime-local` | text |
| Ghi chú dài | `textarea` | input 1 dòng |
| Boolean | `checkbox` | text Yes/No |
| Free text thực sự (Name, Subject, Remark, menu note…) | text / textarea | — |

**Nguồn option dùng chung:** `crm-shared/crm-demo.options.ts` (`CRM_DEMO_OPTIONS`).

---

## 3. Checklist theo form (design review)

| Form | List ART | Detail outlet | Control typed | Ghi chú UX |
|------|:--------:|:-------------:|:-------------:|------------|
| Sale team | ✓ | ✓ | ✓ Type/Leader/Branch/Role/Item/Status | Mẫu chuẩn |
| Sale quota | ✓ | ✓ | ✓ Team/Period/Metric/Item/Staff | Config, không báo cáo |
| Event hall | ✓ | ✓ | ✓ Slot | Capacity = number |
| Event package | ✓ | ✓ | ✓ Hall/Item/Unit | Lines table |
| Price book | ✓ | ✓ | ✓ Rule type; package simulator select | % = number |
| Segment | ✓ | ✓ | ✓ Default process / payment / checklist | |
| Sales process | ✓ | ✓ | ✓ Segment/Role/Action/Gate/Payment rule | Checklist+milestone trong 1 form |
| Lead | ✓ | ✓ | ✓ Status/Segment/Source/Owner/Team | Convert inline |
| Opportunity | ✓ | ✓ | ✓ Stage/Hall/Process/Owner/Source/Campaign/Segment | Workspace = hr-group, không segment tab |
| Activity | ✓ | ✓ | ✓ Type/Priority/Regarding | |
| Tour booking | ✓ | ✓ | ✓ Opp/Hall/Result | |
| Sale quotation | ✓ | ✓ | ✓ Opp/Package/Status/Item/Unit | |
| Event hold | ✓ | ✓ | ✓ Opp/Hall/Slot/HoldType/Status | Extend/Release toolbar |
| Hall calendar | ✓ (tool) | — | ✓ Hall/Team filters select | Grid giữ scroll riêng |
| Contract | ✓ | ✓ | ✓ Opp/Quote/Hall/Status/Owner | |
| Contract payment | ✓ | ✓ | ✓ Contract/Milestone/Gate/Status | |
| BEO | ✓ | ✓ | ✓ Opp/Hall/Status/Flag | Sections table |
| Attendance | ✓ | Partial/legacy | Selects sẵn (group/type/status) | Production-ish |
| AI inbox | ✓ | ✓ | ✓ Channel/Status | Approve trên toolbar |
| Campaign | ✓ | Production detail | List OK; detail prod giữ | Channel/Status trên list |
| Customer | Prod BP | Prod BP | Prod controls | Không skin lại sâu |
| Checklist / Payment rule | Redirect | Redirect | — | Gộp vào Sales process |
| KPI config/board | Route-only | Light outlet | Board/Period select | Ẩn menu BI |

---

## 4. Điểm design cần anh duyệt

1. **Một ngôn ngữ visual** — bỏ hết teal hero / chip KPI; form nhìn như Accountant/CRM outlet.
2. **Select thay textbox** — giảm lỗi gõ, khớp master data demo; prod sẽ map `ng-select` + API.
3. **Opportunity workspace** — checklist + commercial path nằm trong hr-group (không tab). Nếu anh muốn tab như ar-invoice Items/Other, có thể thêm lại **sau** Confirm.
4. **Cards view** — chỉ phụ; list data-table là mặc định.
5. **Placeholder merged forms** — checklist-template / payment-rule / kpi-board không còn là form vận hành.

---

## 5. Demo smoke

```
/#/sale-team/1
/#/lead/1
/#/opportunity/1001
/#/event-hold/1
/#/sale-quota/1
/#/sales-process/1
/#/sale-quotation/1
/#/contract/1
/#/beo/1
/#/hall-calendar
```

**Sau Confirm design:** khóa pattern này làm chuẩn G3.4 full; BE map select → lookup API.
