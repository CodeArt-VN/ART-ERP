# Yêu cầu CRM Wedding (handoff local)

**Ngày ghi:** 2026-08-07  
**Nguồn:** yêu cầu sponsor từ chat Cloud Agent CRM Wedding G3 → G3.4  
**Phạm vi file này:** chỉ yêu cầu / luật / quyết định đã chốt. **Không** gồm tiến độ triển khai hay source đã làm.

---

## 1. Mục tiêu sản phẩm

| Hạng mục | Yêu cầu |
|----------|---------|
| Domain | CRM **nhà hàng / tiệc cưới / sự kiện** — thiết kế theo đặc trưng ngành, không CRM generic |
| AI | Theo dõi thực hiện; hướng tới AI hỗ trợ / làm việc thay sale (AI inbox = hàng đợi tín hiệu inbound) |
| Vai trò sponsor | Confirm theo gate, xem demo, hỏi |
| Tài liệu bắt buộc | Hướng dẫn sử dụng · Flow xử lý · Danh sách forms · Chức năng trong form · Test cases |

### Quy trình làm việc (bắt buộc xin confirm)

```text
Tổng hợp nghiệp vụ → đề xuất flow → CONFIRM
→ danh sách form / chức năng → CONFIRM
→ prototype FE → demo → chốt
→ BE + FE + unit test → UAT demo → Hướng dẫn sử dụng
```

| Gate | Trạng thái chốt |
|------|-----------------|
| G1 — nghiệp vụ / flow | **CONFIRMED** |
| G2 — danh sách form (mã bỏ prefix `crm-`) | **CONFIRMED** |
| G3 — prototype đạt chuẩn ART-ERP + ≥7/10 | **Chưa Confirm** |

---

## 2. Luật cứng (không được phá)

1. **SalesOrder không phải trung tâm CRM.** Hệ cũ đặt SO trung tâm là sai bản chất; lead chưa chắc đi tới SO.
2. **Bỏ qua toàn bộ sync SAP** trong phạm vi CRM (đã có phân hệ riêng).
3. **Không tách module/entity SalesOrderDraft** — draft chỉ là status; duyệt ở phân hệ Approval.
4. **LeadO2O không chấp nhận** như cấu trúc riêng — phải là một phần của Lead (inbound/O2O absorb vào Lead; AI inbox = signal queue).
5. **Báo giá bắt buộc version + so sánh thay đổi.**
6. **Import data DB cũ chỉ sau UAT.** Được phân tích DB cũ để hiểu và thiết kế; không execute import trước UAT. Import đúng nghiệp vụ mới, có loại bỏ (ví dụ LeadO2O).
7. **Không nhét báo cáo / BI vào từng form CRM** (đã có phân hệ BI).
8. **Bỏ luồng duyệt chỉnh sửa SO trong CRM** (đã có Approval).
9. Đánh giá gap = **cái đang thiết kế/làm thiếu gì**, không phải “DB cũ thiếu gì”.
10. Phản biện **toàn bộ role** (BA, Architect, PM, UX, Sales, Ops, Finance, Marketing…), không chỉ 3 role.
11. Prototype / demo phải chạy **source FE thật** trong module CRM — không dùng HTML artifact thay app.

---

## 3. Business flow mục tiêu

```text
Inbound signal (AI inbox)
        ↓ Apply signal to lead
Lead (absorb channel / campaign / pax / hall / date / UTM)
        ↓ convert
Opportunity (commercial cockpit)
        ↓
Quote versions (v1 / v2… + change reason + compare)
        ↓
Hold / Booking (Soft → Hard theo payment gate) + Hall calendar
        ↓
Contract + Payment milestones (gate có hậu quả nghiệp vụ)
        ↓
BEO (ops handoff packet)
        ↓
Event / Attendance / …
```

### Rules G1 đã chốt

| Hạng mục | Quyết định |
|----------|------------|
| Cọc | Set theo quy trình sale: required hay không; tối thiểu % hoặc số tiền |
| Stage / checklist | Mục **required** bắt buộc; thiếu → chặn đổi stage |
| Commission | Tạm để vậy |
| Ký duyệt | Tạm owner ký trước (status); sau tích hợp Approval đồng ký |
| KPI | Cấu hình linh động |

### Sales process

- Gộp **sales-process + checklist-template + payment-rule** thành **một form**.
- Kéo-thả sắp xếp thứ tự stage / checklist / payment milestone.
- Checklist khi hoàn thành có thể sinh document: báo giá / phiên bản báo giá / booking / SO / task…

### Sale team / quota

- CRUD team, gán nhân viên, quota target + items.
- Sản phẩm được bán / không được bán + SL tối đa.
- Chỉ tiêu team phân bổ xuống nhân viên.
- Metric mở rộng kiểu FMCG: số khách · doanh số · số lượng.
- Không nhúng báo cáo BI trên form này.

### Opportunity (yêu cầu xuyên suốt)

Phải nhìn được: quy trình sale, tiến độ stage, checklist, activities, next step, hợp đồng / cọc / thanh toán theo tiến độ.

---

## 4. Forms — mã & danh sách

**Quy tắc mã:** không dùng prefix `crm-` / `crm/`.  
**Title:** chỉ viết hoa chữ đầu câu; giữ keyword KPI, BEO, SLA, AI, SO, PDF…

| # | Mã form | Tên (sentence case) | Nhóm | Ghi chú |
|---|---------|---------------------|------|---------|
| 1 | `sale-team` | Sale team | Setup | CRUD / policy / allocation |
| 2 | `sale-quota` | Sale quota | Setup | |
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
| 15 | `sale-quotation` | Sale quotation | Quote | Version + compare bắt buộc |
| 16 | `event-hold` | Event hold | Hold | Soft / Hard / Booked + rule |
| 17 | `hall-calendar` | Hall calendar | Hold | |
| 18 | `contract` | Contract | Contract | |
| 19 | `contract-payment` | Contract payment | Contract | Gate có hậu quả |
| 20 | `beo` | BEO | Ops | Packet đủ tin cho ops |
| 21 | `attendance-booking` | Attendance booking | Ops | |
| 22 | `ai-inbox` | AI inbox | AI | Signal → Apply to lead |
| 23 | `campaign` | Campaign | Mkt | Không funnel BI giả |
| 24 | `customer` | Customer | Master | Tái dụng BP |
| 25 | `kpi-board` | KPI board | Report | Đề xuất **cắt** khỏi Wedding menu (trùng BI) |

**Tái dùng, không tạo form CRM mới:** Incoming payment ngân hàng, Sale order (ngoài CRM center), Approval (phase sau), WMS Item (menu lines).

**Phase sau:** floor plan kéo-thả, Approval multi-sign BEO/Contract, Zalo OA sâu.

---

## 5. Luật UI / UX (chuẩn ART-ERP)

Tham chiếu pattern: `ar-invoice` (+ detail), kanban `PM/task` (cuộn ngang).

1. Sentence case cho title / menu (trừ keyword).
2. Mobile: không cuộn ngang trừ bất khả kháng.
3. Kanban được cuộn ngang theo pattern task board.
4. Không insight / KPI strip kiểu BI trên form vận hành.
5. Nút chức năng trên **toolbar**; tái dụng PageBase, data-table, form-control, page-title.
6. List = **data-table** + cards; **toggle view** trên toolbar (Opportunity thêm kanban).
7. Form setup phải CRUD thật (mock được), không poster đọc.
8. Control đúng kiểu dữ liệu — field chọn không dùng textbox.
9. Detail theo kiểu **outlet** (status bar theo dõi giai đoạn).
10. Không marketing hero / action bar “app khác” gắn vào ERP shell.
11. Responsive mobile; ưu tiên chuẩn hóa vài trang mẫu rồi lan toàn bộ forms.

**Tiêu chí chấm:** khi toàn bộ forms **≥ 7/10** theo luật trên thì demo lại xin Confirm G3.

---

## 6. Yêu cầu nghiệp vụ tối thiểu phải thấy trên prototype/demo

1. **Inbound → Lead signal** — channel, campaign, hall, pax, event date, UTM, timeline; Apply signal to lead (không fake Approve/Reject kiểu ticket).
2. **Opportunity = cockpit** sau qualify — stage, checklist blocker, quote, hold, payment gate, BEO readiness, deep-link các bước.
3. **Quote versioning** — v1/v2… + lý do đổi + so sánh thay đổi.
4. **Không ngôn ngữ SO-centric** trên mặt CRM — dùng contract / booking / ops handoff.
5. **Hold + calendar** giải thích Free / Soft / Hard / Booked, conflict, expiry, next action.
6. **Payment gate có hậu quả** — trả mốc nào thì mở gate nào (Confirmed / HardBook / BEOLock…).
7. **BEO đủ tin cho ops** — menu, allergen, run-of-show, staffing, beverage, table plan, lock/print.

---

## 7. Mapping old → new (chỉ khung thiết kế)

Mục đích: các role hiểu DB cũ để thiết kế. **Không execute import trước UAT.**

| Khái niệm cũ | Target mới | Quyết định |
|--------------|------------|------------|
| Lead cơ bản | Lead | Import |
| LeadO2O / O2O inquiry | Lead + AI inbox signal | Transform (absorb) |
| Inquiry | Opportunity | Transform |
| Quotation | Sale quotation (versions) | Transform |
| Booking / soft reserve | Event hold | Transform |
| Contract | Contract | Import |
| Deposit / milestone | Contract payment (+ gate) | Transform |
| BEO sheet | BEO | Transform |
| SalesOrder (wedding path) | Không làm CRM center | Drop (as center) |
| SalesOrderDraft module | Status trên doc hiện có | Drop (as module) |
| SAP sync objects | — | Drop |
| Activity / campaign / hall / customer roles | Activity / Campaign / Event hall / roles | Import hoặc Transform |

Lead absorb từ O2O-ish: Channel, Campaign, Guests, PreferredHall, EventDate, UTM; raw message giữ ở AI inbox / timeline.

---

## 8. Explicit DO NOT

1. Không lấy SalesOrder làm trung tâm CRM  
2. Không sync SAP trong CRM  
3. Không module SaleOrderDraft riêng  
4. Không entity LeadO2O riêng  
5. Không import DB cũ trước UAT  
6. Không nhét BI / báo cáo vào form CRM  
7. Không duyệt chỉnh sửa SO trong CRM (dùng Approval)  
8. Không chỉ phản biện 3 role  
9. Không Title Case lung tung  
10. Không cuộn ngang (trừ kanban)  
11. Không textbox cho field chọn  
12. Không demo bằng HTML artifact thay source  
13. Không Confirm G3 khi còn Fail luật ART-ERP  

---

## 9. Tài liệu tham chiếu trong repo (nếu cần chi tiết hơn)

Các file dưới đây là mở rộng của cùng bộ yêu cầu (không phải tiến độ code):

- `g1-nghiep-vu-flow.md` — G1  
- `03-danh-sach-forms.md` — danh sách forms  
- `04-chuc-nang-trong-form.md` — chức năng từng form  
- `12-phan-bien-g34-theo-feedback-sponsor.md` — luật UI + phản hồi sponsor  
- `16-gap-multi-role-phan-bien-2-vong-g34.md` — phản biện multi-role + 7 outcome  
- `17-ba-architect-mapping-framework-g34.md` — mapping Import / Transform / Drop  

**File này (`18-…`) đủ để mang về local làm việc theo yêu cầu.**
