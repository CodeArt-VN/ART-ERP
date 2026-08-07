# 18 — Handoff yêu cầu sponsor (làm việc local)

**Ngày ghi:** 2026-08-07  
**Nguồn:** toàn bộ chat Cloud Agent `bc-9bb84caf-d1eb-4a86-9d59-20872ceaa303` (CRM Wedding G3 → G3.4)  
**Mục đích:** anh kéo về local làm tiếp — đây là **toàn bộ yêu cầu / luật / quyết định đã chốt** trong chat, không phải ước lượng lịch.

> **Cách đọc:** mục có **[USER]** = anh nói/chốt trực tiếp. Mục có **[GATE]** = đã Confirm qua gate. Mục có **[ASST]** = assistant tổng hợp theo luật anh (ưu tiên quote USER khi xung đột).

---

## 0. Intent hiện tại

Anh yêu cầu: *đọc lại toàn bộ chat, ghi lại toàn bộ chi tiết yêu cầu để chuyển về local làm việc*.

Làm local = **không phụ thuộc** cloud agent này (run cũ không gắn multi-repo env; CRM submodule push bị 403 → code demo từng mất khi reset VM).

---

## 1. Mục tiêu sản phẩm

| Hạng mục | Yêu cầu |
|----------|---------|
| Domain | CRM **nhà hàng / tiệc cưới / sự kiện** — thiết kế theo đặc trưng ngành, không CRM generic |
| AI | Theo dõi thực hiện; hướng tới AI hỗ trợ / làm việc thay sale (AI inbox = signal queue) |
| Vai trò anh | **Khách hàng / nhà tài trợ** — confirm theo gate, xem demo, hỏi |
| Vai trò agent | PM điều phối + BA/DEV/TEST; chủ động làm, reminder chỉ là ánh xạ task |
| Prototype | Chạy **source FE thật** trong `ART-ERP-FE/src/app/pages/CRM` — **cấm** demo bằng HTML artifact |
| Docs bắt buộc (5 loại) | Hướng dẫn sử dụng · Flow xử lý · Danh sách forms · Chức năng trong form · Test cases → `.cursor/plans/CRM` |

### Quy trình gate (anh bắt buộc)

```text
Tổng hợp nghiệp vụ → đề xuất flow → CONFIRM
→ danh sách form/chức năng → CONFIRM
→ prototype FE → demo → chốt
→ BE + FE + unit test → UAT demo → Hướng dẫn sử dụng
```

| Gate | Trạng thái |
|------|------------|
| **G1** nghiệp vụ/flow | **CONFIRMED** |
| **G2** danh sách form (mã bỏ `crm-`) | **CONFIRMED** (*“ok confirm G2 làm tiếp đi”*) |
| **G3** prototype UX ≥7/10 + ART pattern | **Chưa Confirm chính thức** — nhiều vòng sửa; điểm G3.3 bị invalidate bởi luật G3.4 |

---

## 2. Luật cứng sponsor (không được phá)

| # | Luật | Nguyên văn / ý anh |
|---|------|-------------------|
| 1 | **SalesOrder không phải trung tâm CRM** | Phần mềm cũ đặt SO trung tâm là **sai bản chất**; lead chưa chắc đi tới SO |
| 2 | **Ignore SAP sync** | Đã có phân hệ riêng |
| 3 | **Ignore module SalesOrderDraft riêng** | Chỉ là **status**, không tách entity/module |
| 4 | **LeadO2O không chấp nhận** | *“cấu trúc này tao không chấp nhận được, nó phải là một phần của lead”* |
| 5 | **Quote versioning + so sánh** | *“ở bước báo giá phải đặt quan tâm vào version báo giá, so sánh thay đổi”* |
| 6 | **Import data cũ sau UAT** | Không làm migration/import **ngay bây giờ**; vẫn phải hiểu DB cũ để thiết kế |
| 7 | **Không nhét BI/báo cáo vào form CRM** | Đã có phân hệ BI |
| 8 | **Bỏ luồng duyệt chỉnh sửa SO trong CRM** | Đã có module Approval |
| 9 | **Đánh giá gap = cái đang làm thiếu** | *“tao không nói db cũ thiếu gì”* — BA/Architect/PM soi prototype vs DB cũ |
| 10 | **Phản biện đủ role**, không chỉ 3 | *“toàn bộ các role không phải 3 role”* (BA, Architect, PM, UX, Sales, Ops, Finance, Marketing…) |

---

## 3. Business flow đã chốt (target)

```text
Inbound signal (AI inbox)
        ↓ Apply signal to lead
Lead (absorb channel / campaign / pax / hall / date / UTM)
        ↓ convert
Opportunity (commercial cockpit)
        ↓
Quote versions (v1/v2… + change reason + compare)
        ↓
Hold / Booking (Soft → Hard theo payment gate) + Hall calendar
        ↓
Contract + Payment milestones (gate có hậu quả nghiệp vụ)
        ↓
BEO (ops handoff packet)
        ↓
Event / Attendance / …
```

**Không** lấy SalesOrder làm master lifecycle CRM.

### Rules G1 đã chốt **[GATE]**

| Hạng mục | Quyết định |
|----------|------------|
| Cọc | Set theo quy trình sale: required hay không, tối thiểu % hoặc số tiền |
| Stage / checklist | Mục **required** bắt buộc; thiếu → chặn đổi stage |
| Commission | Tạm để vậy |
| Ký duyệt | Tạm **owner ký trước** (status); sau tích hợp Approval đồng ký |
| KPI | Cấu hình **linh động** |

### Sales process gộp **[USER]**

- `sales-process` + `checklist-template` + `payment-rule` → **1 form**
- Kéo-thả sắp xếp stage / checklist / payment milestone
- Checklist hoàn thành có thể **sinh document**: báo giá / phiên bản BG / booking / SO / task…

### Sale team / quota **[USER]**

- CRUD team, gán NV, quota target + items
- Sản phẩm được / không được bán + SL tối đa
- Chỉ tiêu team phân bổ xuống NV
- Metric FMCG-style: số khách · doanh số · số lượng
- **Không** nhét báo cáo BI trên form này

---

## 4. Forms — mã & danh sách (G2 confirmed naming)

**Quy tắc:** mã form **không** prefix `crm-` / `crm/`.  
**Title case:** chỉ hoa chữ đầu câu; giữ keyword KPI, BEO, SLA, AI, SO, PDF…

| # | Mã | Tên (sentence case) | Nhóm | Ghi chú |
|---|-----|---------------------|------|---------|
| 1 | `sale-team` | Sale team | Setup | P0 — redesign CRUD/policy/allocation |
| 2 | `sale-quota` | Sale quota | Setup | Có thể gắn/cùng narrative team |
| 3 | `event-hall` | Event hall | Setup | |
| 4 | `event-package` | Event package | Setup | |
| 5 | `price-book` | Price book | Setup | |
| 6 | `segment` | Segment | Setup | |
| 7 | `sales-process` | Sales process | Setup | **Gộp** checklist + payment rule |
| 8 | `checklist-template` | — | Setup | Deprecate → merge vào process |
| 9 | `payment-rule` | — | Setup | Deprecate → merge vào process |
| 10 | `kpi-config` | KPI config | Setup | Cân nhắc cắt / deep-link BI |
| 11 | `lead` | Lead | Pipeline | Absorb inbound |
| 12 | `opportunity` | Opportunity | Pipeline | Cockpit |
| 13 | `activity` | Activity | Pipeline | |
| 14 | `tour-booking` | Tour booking | Pipeline | |
| 15 | `sale-quotation` | Sale quotation | Quote | Version + compare **bắt buộc** |
| 16 | `event-hold` | Event hold | Hold | Soft/Hard/Booked + rule |
| 17 | `hall-calendar` | Hall calendar | Hold | |
| 18 | `contract` | Contract | Contract | |
| 19 | `contract-payment` | Contract payment | Contract | Gate consequence |
| 20 | `beo` | BEO | Ops | Packet đủ tin ops |
| 21 | `attendance-booking` | Attendance booking | Ops | |
| 22 | `ai-inbox` | AI inbox | AI | Signal queue → Apply to lead |
| 23 | `campaign` | Campaign | Mkt | Không funnel BI giả |
| 24 | `customer` | Customer | Master | Tái dụng BP |
| 25 | `kpi-board` | KPI board | Report | **Đề xuất cắt** khỏi Wedding menu (trùng BI) |

Folder code: `ART-ERP-FE/src/app/pages/CRM/` (submodule `ART-ERP-FE-CRM`).

---

## 5. Luật UI / UX ART-ERP (G3.4)

Tham chiếu code: `ACCOUNTANT/ar-invoice` (+ detail), `PM/task` kanban (`scrollx`).

| # | Luật |
|---|------|
| R1 | Sentence case title (trừ keyword) |
| R2 | Mobile: **không** cuộn ngang trừ bất khả kháng |
| R3 | Kanban **được** cuộn ngang (pattern task board) |
| R4 | Không insight/KPI strip kiểu BI trên form vận hành |
| R5 | Nút chức năng trên **`app-toolbar`**; reuse PageBase / `app-data-table` / `app-form-control` / `app-page-title` |
| R6 | List = **data-table** + cards; **toggle view** trên toolbar (Opp thêm kanban) |
| R7 | Setup form phải CRUD thật (mock OK), không poster |
| R8 | Control đúng kiểu dữ liệu — chọn không dùng textbox |
| R9 | Detail theo **outlet** (status bar tracking giai đoạn) |
| R10 | Không marketing hero / action bar “app khác” sống nhờ ERP shell |

**Tiêu chí demo:** khi **trên 7/10 hết** thì demo lại. Điểm G3.3 cũ **invalidate** dưới luật ART-ERP.

Ưu tiên prototype chuẩn trước (sale team, lead, opportunity) rồi lan ra toàn bộ forms.

---

## 6. Phản biện multi-role & backlog 7 outcome (doc 16)

Anh yêu cầu agent **tự họp đủ role, phản biện 2 lần**, rồi sửa prototype demo lại — không chỉ Marketing/Sales/Ops.

Sau 2 vòng, backlog tối thiểu phải thấy trong demo:

1. **Inbound → Lead signal** (channel/campaign/hall/pax/date/UTM + timeline)
2. **Opportunity = cockpit** (stage, checklist blocker, quote, hold, payment, BEO readiness)
3. **Quote versioning** nhẹ nhưng rõ (v1/v2 + what changed)
4. **Bỏ ngôn ngữ SO-centric** trên demo (contract / booking / ops handoff)
5. **Hold + calendar** giải thích Free/Soft/Hard/Booked, conflict, expiry, next action
6. **Payment gate có hậu quả** (mốc trả → mở gate nào)
7. **BEO đủ tin ops** (menu, allergen, run-of-show, staffing, beverage, table plan, lock/print)

Chi tiết: `16-gap-multi-role-phan-bien-2-vong-g34.md`

---

## 7. Option B đã approve (*“Ok làm tiếp b”*)

Anh chọn **Hướng B** (agent chủ động sâu), không phải A (anh tự test rồi chỉ lỗi).

### B1 — Lead + AI inbox một narrative inbound

- AI inbox: ART data-table; triage `New / Reviewed / Applied / Discarded`
- Action chính: **Apply signal to lead** (không fake Approve/Reject kiểu ticket)
- Lead: Channel, Inbound, timeline Apply; absorb field từ signal

### B2 — Sâu Opportunity cockpit + Quote / Hold / Payment / BEO

- Commercial path + blockers
- Deep-link: Tour → Quote → Hold → Contract → Payment → BEO
- Quote: `createNextVersion` + compare
- Hold / Payment / BEO link ngược cockpit; BEO packet + BEOLock gate

### B3 — Khung mapping BA/Architect (doc 17)

- Import / Transform / Drop (vd LeadO2O→Lead, Inquiry→Opp, Booking→Hold)
- Drop SO/SAP/SODraft khỏi CRM center
- **Chưa execute migration** (đúng luật sau UAT)

Chi tiết: `17-ba-architect-mapping-framework-g34.md`

---

## 8. Demo kỹ thuật (local)

| Mục | Giá trị |
|-----|---------|
| Flag | `environment.g3Demo = true` |
| FE branch (remote) | `AI/crm-wedding-g34-serve-a303` (`CodeArt-VN/ART-ERP-FE`) |
| CRM branch (local từng có, **chưa push được**) | `AI/crm-wedding-g34-proto-a303` (`CodeArt-VN/ART-ERP-FE-CRM`) |
| Docs branch | `AI/crm-wedding-g34-docs-a303` (`codeart-vn/art-erp`) — PR docs |
| Serve | `npx ng serve --host 0.0.0.0 --port 4200 --configuration development` |
| Base URL | `http://localhost:4200/` |

### Routes demo trọng tâm

- `/#/ai-inbox`
- `/#/lead/1`
- `/#/opportunity/1001`
- `/#/sale-quotation/1`
- `/#/event-hold/2`
- `/#/contract-payment/1`
- `/#/beo/2`
- `/#/hall-calendar`

### Cảnh báo source

- Commit CRM Option B từng chỉ **local trên cloud VM** → mất khi reset (403 push `cursor[bot]` → `ART-ERP-FE-CRM`).
- FE có thể vẫn trỏ submodule SHA cũ hơn demo Option B đầy đủ.
- Khi làm local: ưu tiên recover từ branch/commit local của anh, hoặc rebuild theo docs 16/17 + backlog 7 outcome; **không** tin cloud VM còn giữ object CRM.

---

## 9. Explicit DO NOT

1. Không demo bằng HTML artifact  
2. Không BI/report nhét form CRM  
3. Không SO-centric CRM  
4. Không SAP sync trong CRM  
5. Không module SaleOrderDraft riêng  
6. Không entity LeadO2O riêng  
7. Không import DB cũ trước UAT  
8. Không chỉ phản biện 3 role  
9. Không Title Case lung tung  
10. Không cuộn ngang (trừ kanban)  
11. Không dùng textbox cho field chọn  
12. Không đánh giá “DB cũ thiếu gì” — đánh giá **đang làm thiếu gì**  
13. Không Confirm G3 khi còn Fail luật ART-ERP  

---

## 10. Checklist làm local (đề xuất thứ tự)

1. Pull docs: `art-erp` branch `AI/crm-wedding-g34-docs-a303` — đọc **12, 14, 15, 16, 17, g1, 03** + file này  
2. Clone/pull FE `AI/crm-wedding-g34-serve-a303` + CRM submodule (quyền write bằng account anh)  
3. Bật `g3Demo`, `ng serve`, walk 7 outcome + routes mục 8  
4. So với backlog 7 + Option B — liệt kê gap còn thiếu trên source anh đang có  
5. Ưu tiên sửa P0: Lead+AI Apply · Opp cockpit · Quote version · Hold/Payment/BEO · gộp Sales process · Sale team CRUD  
6. Mapping: dùng doc 17 để thiết kế; **không** chạy import  
7. Khi ≥7/10 toàn form theo luật R1–R10 → demo lại → xin **Confirm G3**  

---

## 11. Chỉ mục docs liên quan

| File | Vai trò |
|------|---------|
| `g1-nghiep-vu-flow.md` | G1 CONFIRMED |
| `03-danh-sach-forms.md` | G2 list (naming confirmed) |
| `04-chuc-nang-trong-form.md` | Chức năng form |
| `12-phan-bien-g34-theo-feedback-sponsor.md` | Luật cứng UI + phản hồi sponsor |
| `14-mau-3-trang-ar-invoice-outlet.md` | Mẫu 3 trang ART |
| `15-danh-gia-design-control-g34.md` | Design + control |
| `16-gap-multi-role-phan-bien-2-vong-g34.md` | 2 vòng phản biện + backlog 7 |
| `17-ba-architect-mapping-framework-g34.md` | Mapping Import/Transform/Drop |
| **`18-handoff-yeu-cau-sponsor-local.md`** | **File này — handoff local** |

---

## 12. Infra cloud (chỉ để biết — local không cần)

- GitHub App All repos ≠ token write cho mọi submodule trên run cũ  
- Env anh tạo: `57bb5fa9-9156-11f1-ba66-0e7d0216e441` (**ART-ERP +17**) — chat cũ **không** tự gắn  
- Muốn cloud push CRM: New agent + chọn env +17 + repo `ART-ERP-FE-CRM` trong env  
- Local: anh push bằng credential cá nhân/org của anh là đủ  

---

*Ưu tiên quote / luật [USER] khi xung đột với tóm tắt assistant.*
