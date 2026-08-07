# Phản biện TỪNG FORM × 4 role — G3.4 (trước khi sửa prototype)

**Ngày:** 2026-07-24  
**Roles:** Sale · Marketing · Operator · UX Designer (UI)  
**Luật sponsor:** sentence case · mobile no h-scroll (trừ kanban) · kanban kiểu task · không BI trên form · action trên toolbar · data-table + cards + toggle · reuse `ar-invoice` / ART components.

Thang mỗi role: **UI 1–10 · Dụng 1–10**. Verdict form: Fail / Weak / OK-MVP.

---

## A. SETUP

### A1. `sale-team` → tên hiển thị: **Sale team**
| Role | UI | Dụng | Phản biện chi tiết |
|------|----|------|-------------------|
| Sale | 2 | 2 | Không tạo/sửa/xóa team trên UI chuẩn PageBase. Không gán NV. Không khai báo sản phẩm được bán/cấm + MaxQty. Roster mock đọc-only. Insight “Open opps / Quota pace” = báo cáo giả — thừa vì đã có BI. |
| Mkt | 2 | 2 | Không map team ↔ sản phẩm/segment để routing. |
| Ops | 1 | 1 | Không tra được AE phụ trách khi cần liên hệ tiệc. |
| UX | 2 | — | Cards-only, Title Case, CTA ngoài toolbar, không toggle list, mobile grid dễ lệch. Không giống `ar-invoice` list. |
**Verdict: Fail.** Redesign: data-table + cards; toolbar Add/Delete; detail segment Thành viên · Sản phẩm & hạn mức · (link Quota).

### A2. `sale-quota` → **Sale quota**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 2 | 2 | Progress bar = BI. Thiếu target theo item, thiếu phân bổ xuống NV, thiếu metric FMCG (số khách / doanh số / SL). Leader không khai báo chỉ tiêu được. |
| Mkt | 1 | 1 | — |
| Ops | 1 | 1 | — |
| UX | 2 | — | Hero + bar chart feel; sai job form cấu hình. |
**Verdict: Fail.** Form cấu hình: header kỳ/team/metricType + lines item + allocation staff. Cấm chart.

### A3. `event-hall` → **Event hall**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 5 | Capacity hữu ích nhưng thiếu CRUD table + lọc; upcoming text mỏng. |
| Mkt | 3 | 2 | Không asset venue. |
| Ops | 5 | 5 | Cần min/max/slot/min spend trên detail chuẩn form-control. |
| UX | 3 | — | Cards-only; thiếu toolbar toggle; Title Case. |
**Verdict: Weak.** Table + cards; detail `app-form-control`; calendar link trên toolbar.

### A4. `event-package` → **Event package**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 5 | Lines edit được (mock) nhưng list không table; CTA hero. |
| Mkt | 3 | 3 | — |
| Ops | 4 | 4 | Lines → bếp chưa flag. |
| UX | 3 | — | Lệch ar-invoice detail (thiếu segment Items). |
**Verdict: Weak.**

### A5. `price-book` → **Price book**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Simulator thực dụng; list cards. |
| Mkt | 2 | 2 | — |
| Ops | 2 | 2 | — |
| UX | 3 | — | Nút Preview trong content; thiếu table. |
**Verdict: Weak.**

### A6. `segment` → **Segment**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Default process chip OK; thiếu table. |
| Mkt | 5 | 5 | Xương journey — UI vẫn nông. |
| Ops | 3 | 3 | SLA không runtime rõ. |
| UX | 3 | — | Cards-only. |
**Verdict: Weak.**

### A7–A9. `sales-process` + `checklist-template` + `payment-rule` → **gộp 1 form Sales process**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | 3 form rời: AE không thấy “Done checklist → sinh BG/SO/task” và gate cọc cùng lúc. DnD yếu / Up-Down. |
| Mkt | 3 | 3 | Default process trỏ lung tung 3 chỗ. |
| Ops | 4 | 4 | BEOLock chìm form payment riêng. |
| UX | 2 | — | Ba IA trùng; Title Case; không toolbar; board tự chế ≠ task. |
**Verdict: Fail (gộp P0).** 1 canvas: stage DnD · checklist DnD + OnComplete create doc · payment milestones DnD.

### A10. `kpi-config` / `kpi-board`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 2 | 1 | Không phải việc AE trên CRM Wedding hàng ngày. |
| Mkt | 3 | 2 | Funnel báo cáo → BI. |
| Ops | 2 | 1 | — |
| UX | 2 | — | Widget dashboard = BI clone. |
**Verdict: Fail — cắt khỏi menu Wedding** (deep-link BI nếu cần). Giữ code route redirect/ẩn.

---

## B. PIPELINE

### B1. `lead` → **Lead**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Cards convert tốt; table legacy phụ. Convert chưa toolbar. |
| Mkt | 4 | 4 | Attribution yếu. |
| Ops | 1 | 1 | — |
| UX | 4 | — | Dual UI; Title; mobile cards OK hơn table rộng. |
**Verdict: Weak.** Default **list table**; cards toggle; Convert trên toolbar khi select.

### B2. `opportunity` → **Opportunity**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 7 | Kanban + 360 đúng hướng làm việc; thiếu data-table mode chuẩn; Move stage/CTA nằm content. |
| Mkt | 4 | 4 | Chip campaign OK; không báo cáo. |
| Ops | 5 | 5 | BEO/payment strip hữu ích — không phải BI chart. |
| UX | 3 | — | Kanban tự chế không `scrollx` task; hero actions; Title; mobile path tràn. |
**Verdict: Weak.** Toolbar: list | cards | kanban; kanban region `scrollx`; CTA Move/New quote trên toolbar detail.

### B3. `activity` → **Activity**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Today filter OK; thiếu table. |
| Mkt | 3 | 3 | — |
| Ops | 3 | 3 | — |
| UX | 3 | — | Cards-only; Complete trong card không toolbar selected. |
**Verdict: Weak.**

### B4. `tour-booking` → **Tour / tasting**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Result→checklist có; list cards. |
| Mkt | 4 | 4 | Show rate không đưa BI form — OK nếu chỉ operational. |
| Ops | 3 | 3 | Conflict hall yếu. |
| UX | 3 | — | Thiếu table + toolbar. |
**Verdict: Weak.**

### B5. `sale-quotation` → **Sale quotation**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 7 | 7 | Edit lines tốt (mock). List thiếu table toggle. |
| Mkt | 2 | 2 | — |
| Ops | 3 | 3 | Lines chưa đẩy BEO. |
| UX | 4 | — | Detail gần workspace nhưng lệch `ar-invoice` (segment Items + toolbar Send). |
**Verdict: Weak→sát OK nghiệp vụ; UI chưa chuẩn ERP.**

### B6. `event-hold` → **Event hold**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Extend/Release OK; cards-only. |
| Mkt | 1 | 1 | — |
| Ops | 5 | 5 | Conflict text. |
| UX | 3 | — | Toolbar thiếu. |
**Verdict: Weak.**

### B7. `hall-calendar` → **Hall calendar**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 6 | Thực dụng; Free→hold. |
| Mkt | 2 | 2 | — |
| Ops | 6 | 6 | — |
| UX | 5 | — | Calendar được phép scroll riêng; mobile cần stack filters trên toolbar. |
**Verdict: Weak / sát OK-MVP ops.**

---

## C. CONTRACT / OPS / AI / MKT

### C1. `contract` → **Contract**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 6 | Sign path + pay bar OK. |
| Mkt | 2 | 2 | — |
| Ops | 4 | 4 | Thiếu link attendance. |
| UX | 4 | — | List cards; detail lệch ar-invoice. |
**Verdict: Weak.**

### C2. `contract-payment` → **Contract payment**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 6 | Record payment OK; insight Due = hơi BI — giữ 1–2 số vận hành tối thiểu, không widget. |
| Mkt | 1 | 1 | — |
| Ops | 5 | 5 | Gate alert. |
| UX | 3 | — | Cards-only; Record trên toolbar selected. |
**Verdict: Weak.**

### C3. `beo` → **BEO** (keyword OK)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | — |
| Mkt | 1 | 1 | — |
| Ops | 7 | 7 | Sections + lock đúng việc bếp. |
| UX | 4 | — | List cards; Lock/Print lên toolbar. |
**Verdict: Weak / Ops gần OK.**

### C4. `attendance-booking` → **Attendance booking**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Strip wedding OK. |
| Mkt | 2 | 2 | — |
| Ops | 6 | 6 | Table sẵn có giá trị. |
| UX | 5 | — | Đã gần chuẩn table; siết naming + toolbar check-in. |
**Verdict: Weak→OK pattern list.**

### D1. `ai-inbox` → **AI inbox**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Approve/reject OK. |
| Mkt | 5 | 5 | Queue. |
| Ops | 1 | 1 | — |
| UX | 3 | — | Split desktop h-scroll rủi ro; thiếu table; Approve toolbar. |
**Verdict: Weak.**

### D2. `campaign` → **Campaign**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Funnel simulate = BI giả. |
| Mkt | 3 | 3 | Cần members/config, không dashboard. |
| Ops | 1 | 1 | — |
| UX | 3 | — | Cắt funnel widgets. |
**Verdict: Fail (BI pollution) → sửa thành config list.**

### D3. `customer` → **Customer**
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | BP + roles wedding. |
| Mkt | 4 | 4 | — |
| Ops | 3 | 3 | — |
| UX | 6 | — | Tái dụng chuẩn nhất. |
**Verdict: OK-MVP (reuse).**

---

## 4. Tổng hợp điểm (trung bình 4 role · UI/Dụng)

| Form | Điểm | Verdict |
|------|------|---------|
| sale-team | 2.0 | Fail |
| sale-quota | 1.8 | Fail |
| event-hall | 4.0 | Weak |
| event-package | 4.0 | Weak |
| price-book | 3.5 | Weak |
| segment | 4.0 | Weak |
| sales-process (riêng) | 3.0 | Fail → merge |
| checklist-template | 3.0 | Fail → merge |
| payment-rule | 3.0 | Fail → merge |
| kpi-config/board | 1.5 | Cắt menu |
| lead | 4.5 | Weak |
| opportunity | 5.0 | Weak |
| activity | 4.0 | Weak |
| tour-booking | 4.0 | Weak |
| sale-quotation | 5.5 | Weak |
| event-hold | 4.0 | Weak |
| hall-calendar | 5.5 | Weak |
| contract | 4.5 | Weak |
| contract-payment | 4.0 | Weak |
| beo | 5.0 | Weak |
| attendance-booking | 5.0 | Weak |
| ai-inbox | 4.0 | Weak |
| campaign | 2.5 | Fail |
| customer | 5.5 | OK-MVP |

**Good = 0. Confirm G3 = chưa.**

---

## 5. Việc sửa prototype G3.4 (DoD demo)

1. Sentence case mọi Name/pageTitle/menu.  
2. Ẩn `kpi-board` (+ `kpi-config` khỏi menu Wedding).  
3. Gỡ insight/KPI strip kiểu BI trên team/quota/campaign/board.  
4. Shared list: data-table + cards + **toolbar toggle**.  
5. CTA chính → `app-toolbar`.  
6. CSS mobile: no overflow-x (trừ `.kanban-scroll` / calendar).  
7. Opp: 3 view list|cards|kanban; kanban `scrollx`.  
8. Redesign sale-team + sale-quota (CRUD mock, members, item policy, allocation FMCG).  
9. Merge process: 1 form DnD stage/checklist(+create doc)/payment.  
10. Campaign: bỏ funnel BI; list table + cards.

```
Gate: sửa xong → demo lại cho sponsor đánh giá (vẫn prototype mock)
```
