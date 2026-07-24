# Phản biện G3.4 — theo phản hồi sponsor + 4 role (gồm UX Designer)

**Ngày:** 2026-07-24  
**Phạm vi:** **toàn bộ forms** CRM Wedding (kể cả form anh chưa nói — em tự soi lỗi cùng lớp để khỏi phải nhắc lại).  
**Chuẩn tham chiếu code:** `ACCOUNTANT/ar-invoice` (+ detail), `PM/task` kanban (`app-board` + `scrollx`).  
**Tham chiếu design (UX):** Behance “Deals Pipeline CRM Kanban”, Salesforce Lightning Opportunity Kanban / Path, pattern list↔board toggle.

> **Invalidate điểm G3.3 ≥7:** điểm cũ đo “workspace mock làm việc được”. Bộ rule mới của anh là **chuẩn sản phẩm ART-ERP** → chấm lại từ đầu. Prototype mock vẫn OK; **sai pattern hệ thống = Fail**.

---

## 0. Luật cứng từ phản hồi anh (áp dụng mọi form)

| # | Luật | Hệ quả nếu vi phạm |
|---|------|-------------------|
| R1 | **Title case câu:** chỉ viết hoa chữ đầu câu; từ sau viết thường trừ **từ khóa** (KPI, BEO, SLA, PDF, SO…). VD: `Sale team`, `Event hall`, `Payment rule`, `AI inbox`. | Fail UX copy |
| R2 | **Responsive mobile:** không thanh cuộn ngang trừ bất khả kháng. | Fail mobile |
| R3 | **Kanban = buộc cuộn ngang** theo pattern `PM/task` board (`scrollx` + kanban lib / cột fixed-width). Không “ép fit” làm vỡ card. | Fail pipeline |
| R4 | **Không nhét báo cáo / insight KPI giả BI** vào từng form — BI đã có phân hệ riêng. Form = cấu hình + vận hành. | Fail kiến trúc |
| R5 | **Nút chức năng lên `app-toolbar`** (như `ar-invoice`); tận dụng PageBase + component sẵn (`app-data-table`, `app-form-control`, `app-page-title`…). Không action bar “hero custom” trùng toolbar. | Fail chuẩn ERP |
| R6 | **Mọi form list:** bắt buộc **data-table** + giữ **cards** (nếu có giá trị). **Toggle view trên toolbar** (list ↔ cards; riêng Opp thêm kanban). | Fail list pattern |
| R7 | Form setup phải **CRUD thật (mock OK)**: tạo/sửa/xóa, gán quan hệ — không chỉ poster đọc. | Fail nghiệp vụ |

**Áp dụng lan tỏa (anh chưa nói nhưng cùng lỗi):** mọi form G3.2/G3.3 đang Title Case menu, insight/KPI strip kiểu BI, CTA trong hero thay toolbar, cards-only không data-table, mobile overflow → **cùng backlog**, không chờ anh nhắc từng form.

---

## 1. Role mới — Chuyên viên thiết kế giao diện phần mềm

### Tiêu chí chấm
- Hierarchy & density theo ERP (toolbar → title → content), không landing-page marketing.
- Mobile-first: 1 cột, tap target ≥44px, không horizontal scroll (trừ kanban).
- Typography: sentence case (R1); tránh ALL CAPS eyebrow trừ brand hệ thống.
- Pattern nhất quán với ART-ERP (`ar-invoice`), không skin `.crm-ws` “app khác sống nhờ ERP”.
- Tham chiếu: Salesforce Lightning list/kanban toggle; Behance deals pipeline (card gọn, stage cột cuộn ngang); Dribbble “CRM mobile dashboard” (bottom nav / stacked sections, không multi-column desktop nhồi mobile).

### Phán quyết UX Designer (hệ thống hiện tại)
| Hạng mục | Điểm | Phản biện |
|----------|------|-----------|
| Visual system vs ART-ERP | 3/10 | `.crm-ws` hero/card tách biệt `ar-invoice`; nhìn như prototype gắn vào shell. |
| Typography / naming | 2/10 | Menu & heading Title Case hàng loạt (`Sale Team`, `Price Book`…). |
| Mobile | 2/10 | Board Opp / grid3 / split pane dễ overflow ngang; không breakpoint nghiêm. |
| Toolbar & actions | 3/10 | Nút nằm hero/sticky trong content — lệch chuẩn `app-toolbar`. |
| List pattern | 2/10 | Nhiều form **chỉ cards**; thiếu data-table + toggle. |
| Kanban | 4/10 | Có board Opp nhưng tự chế; chưa reuse `PM/task` kanban/`scrollx`. |
| BI pollution | 2/10 | Insight KPI trên team/quota/kpi-board trùng BI. |
| **Tổng UX Designer** | **≈ 2.5/10** | **Fail.** Phải G3.4 align ART-ERP trước khi nói “đẹp”. |

---

## 2. Phản hồi cụ thể anh đã nêu

### 2.1 Sale team / Sale quota — **thiết kế lại nghiệp vụ**

**Anh cần (không phải dashboard):**
1. CRUD team (tạo/sửa/xóa).
2. Gán nhân viên vào team (roster).
3. Khai báo **quota target** + **items** (chỉ tiêu theo sản phẩm/nhóm).
4. **Sản phẩm được bán / không được bán** + **SL tối đa**.
5. Chỉ tiêu team **phân bổ xuống nhân viên**.
6. Mở rộng FMCG: **số khách · doanh số · số lượng** (metric chỉ tiêu — không phải báo cáo BI).
7. **Cấm** nhúng báo cáo tiến độ kiểu BI trên form này.

| Role | Phản biện |
|------|-----------|
| Sale | Form hiện tại = roster mock + progress bar “báo cáo nhẹ” → **sai việc**. Cần master data + allocation matrix. |
| Mkt | Ít đụng; nếu routing theo team/product allow-list thì cần đọc config, không cần chart. |
| Ops | Không liên quan sâu. |
| UX | 2 tab/segment trên detail: `Thành viên` · `Sản phẩm & hạn mức` · `Phân bổ chỉ tiêu` (FMCG metrics). List = data-table teams; toolbar: Add / Delete / (toggle list-card). |

**Đề xuất model (G2/G4):**
- `SaleTeam` 1–n `SaleTeamMember` (Staff)
- `SaleTeam` 1–n `SaleTeamItemPolicy` (Item/ItemGroup, Allow|Deny, MaxQty)
- `SaleQuota` header (Team, Period, MetricType: Revenue|Qty|CustomerCount|…)
- `SaleQuotaLine` theo Item/ItemGroup
- `SaleQuotaAllocation` theo Staff (sum staff ≤ team target)

### 2.2 Gộp `sales-process` + `checklist-template` + `payment-rule` → **1 form**

**Tên đề xuất (R1):** `Sales process` (code giữ `sales-process`; deprecate route riêng checklist/payment-rule → redirect).

**Canvas 1 màn (kéo-thả):**
1. **Stage rail** (drag reorder) — như process designer.
2. Mỗi stage expand:
   - Checklist items (drag reorder) — Required / Role.
   - **On-complete actions:** tạo document: báo giá · phiên bản BG · booking/hold · SO · task · (mở rộng sau).
3. Tab/section **Payment rule** gắn process: milestone drag reorder + Min% + Gate (Confirmed / HardBook / BEOLock…).

| Role | Phản biện |
|------|-----------|
| Sale | 1 chỗ hiểu “đi stage nào · làm checklist gì · sinh doc gì · cọc mở gate gì”. Hiện 3 form rời = Fail. |
| Mkt | Segment → default process vẫn trỏ 1 form. |
| Ops | BEOLock nhìn trong cùng process. |
| UX | DnD bắt buộc; mobile = list reorder nút ↑↓ + long-press nếu kanban-lib nặng. Tham chiếu task board DnD. |

### 2.3 UI chung (title, mobile, kanban, toolbar, list/card, no BI)

Đã thành luật R1–R6. **Mọi form** dưới đây bị chấm Fail/Weak nếu còn vi phạm — kể cả anh chưa nêu tên.

---

## 3. Ma trận toàn forms (4 role · sau luật mới)

Thang: UI (UX Designer trọng số cao) · Dụng (Sale/Mkt/Ops trung bình) · Verdict.

| Form | UI | Dụng | Verdict | Lỗi cùng lớp (tự soi) |
|------|----|------|---------|------------------------|
| sale-team | 2 | 3 | **Fail** | Thiếu CRUD/policy/allocation; có “báo cáo” nhẹ; cards-only; Title Case; nút ngoài toolbar |
| sale-quota | 2 | 3 | **Fail** | Progress = BI giả; thiếu target items + phân bổ NV + FMCG metrics |
| event-hall | 3 | 5 | **Weak** | Cards-only; Title Case; thiếu data-table + toggle; mobile grid |
| event-package | 3 | 5 | **Weak** | Nút trong hero; thiếu toolbar pattern; list cards |
| price-book | 3 | 5 | **Weak** | Simulator OK; thiếu list table + toolbar |
| segment | 3 | 5 | **Weak** | Cards-only; naming |
| sales-process | 3 | 4 | **Fail** | Phải **merge**; DnD chưa chuẩn task |
| checklist-template | 3 | 4 | **Fail** | Merge vào process; board tự chế |
| payment-rule | 3 | 4 | **Fail** | Merge vào process |
| kpi-config | 2 | 2 | **Fail** | Gần BI config — cân nhắc **bỏ khỏi Wedding MVP** hoặc chỉ deep-link BI |
| kpi-board | 1 | 1 | **Fail / Cắt** | **Trùng BI** — đề xuất **loại khỏi CRM Wedding forms** |
| lead | 4 | 5 | **Weak** | Có table cũ + cards; dual UI; Title; Convert chưa toolbar |
| opportunity | 4 | 6 | **Weak** | Kanban tự chế ≠ task; thiếu data-table toggle chuẩn; sticky/hero actions; insight BI-ish |
| activity | 3 | 5 | **Weak** | Cards-only; thiếu data-table; filter chưa toolbar |
| tour-booking | 3 | 5 | **Weak** | Cards-only; Result chips trong content |
| sale-quotation | 4 | 6 | **Weak** | Workspace tốt nhưng lệch `ar-invoice` detail (segment + toolbar); thiếu list table toggle |
| event-hold | 3 | 5 | **Weak** | Cards-only; Extend trong content |
| hall-calendar | 5 | 6 | **Weak** | Calendar = exception scroll; vẫn cần list holds phụ + mobile |
| contract | 4 | 6 | **Weak** | List cards; detail lệch ar-invoice |
| contract-payment | 3 | 5 | **Weak** | Console cards; thiếu data-table; insight kiểu BI |
| beo | 4 | 6 | **Weak** | Naming BEO OK (keyword); list cards; actions trong hero |
| attendance-booking | 5 | 5 | **Weak** | Đã data-table; bổ sung wedding strip OK; check naming/toolbar |
| ai-inbox | 3 | 5 | **Weak** | Split desktop; mobile?; thiếu table + toolbar Approve |
| campaign | 3 | 4 | **Weak** | Funnel simulate ≈ báo cáo; cắt funnel BI; giữ config + members |
| customer | 5 | 5 | **OK-MVP pattern** | Tái dụng BP; chỉ siết wedding roles; naming |
| *(mới)* sales-process gộp | — | — | **P0 redesign** | Thay 3 form |

**Đếm (luật mới):** Fail **9** · Weak **14** · OK-MVP pattern **1** (`customer` tái dụng) · Cắt/đề xuất bỏ **1–2** (`kpi-board`, cân `kpi-config`).  
**Good = 0.** Không Confirm G3 dưới luật mới.

---

## 4. Phản biện theo role (ngắn)

### Sale
- Team/quota hiện tại **không cấu hình được** việc bán — Fail nghiệp vụ.
- Process tách 3 form + checklist không khai báo “sinh document” → AE không hiểu hệ quả bấm Done.
- Muốn list/table để filter-sort như hóa đơn; cards chỉ khi triage nhanh.

### Marketing
- Campaign đang nghiêng “funnel giả BI” → cắt; giữ gắn lead/source.
- Segment chỉ cần default process (form gộp).

### Operator
- BEO/calendar/attendance: bỏ KPI strip; actions lên toolbar; mobile 1 cột.
- Gate thanh toán nằm trong **sales process** gộp — dễ hơn form payment-rule riêng.

### UX Designer
- Align ART-ERP trước “Salesforce đẹp”.
- Menu/pageTitle sentence case.
- Toolbar toggle: `list | cards | (kanban nếu có)`.
- Kanban Opp: học `PM/task` (`scrollx`, cột không co ép).
- Mobile: cấm `grid3` cứng; stack; kanban mới được overflow-x.

---

## 5. Backlog G3.4 (ưu tiên — làm hết lớp lỗi)

### P0 — luật hệ thống (mọi form)
1. Đổi **Name/title** sentence case (menu bootstrap + `pageTitle` + heading). Giữ KPI, BEO, SLA, AI (chữ đầu), SO…
2. Gỡ **insight/KPI/widget báo cáo** khỏi form vận hành; `kpi-board` → **remove khỏi Wedding menu** (deep-link BI nếu cần).
3. Mọi list: `app-data-table` + cards; **toggle trên `app-toolbar`** (pattern chung `viewMode`).
4. Chuyển CTA chính vào **`app-toolbar`** / `pageConfig` Show* như `ar-invoice`.
5. CSS: `overflow-x: hidden` content; chỉ region kanban/calendar được `scrollx`.
6. Opp kanban: refactor hướng `PM/task` board (cuộn ngang bắt buộc).

### P0 — nghiệp vụ anh đã chỉ
7. **Redesign `sale-team` + `sale-quota`:** CRUD, roster, item allow/deny + MaxQty, quota lines, allocation xuống NV, metrics FMCG (khách/DS/SL) — **không chart BI**.
8. **Merge** `sales-process` + `checklist-template` + `payment-rule` → 1 form; **drag-drop** stage/checklist/milestone; checklist **OnComplete → create doc** (quote / quote version / booking / SO / task…).

### P1 — soi sẵn (anh chưa nói)
9. `sale-quotation` / `contract` / `beo` detail → layout gần `ar-invoice-detail` (grid + segment + toolbar).
10. `lead` / `campaign` / `activity` / `tour` / `hold` / `payment` / `ai-inbox`: bỏ dual-UI lệch; table mặc định; cards secondary.
11. `event-package` / `price-book` / `segment` / `event-hall`: table + toolbar Save/Add; bỏ poster-only.
12. Mobile QA checklist từng form (no h-scroll screenshot).

### Không làm trong CRM Wedding
- Báo cáo/dashboard nhúng form (đã có BI).
- Skin marketing tách design system ERP.

---

## 6. Naming đề xuất (R1) — menu

| Code | Name mới |
|------|----------|
| sale-team | Sale team |
| sale-quota | Sale quota |
| event-hall | Event hall |
| event-package | Event package |
| price-book | Price book |
| segment | Segment |
| sales-process | Sales process *(gộp checklist + payment rule)* |
| checklist-template | *(redirect → sales-process)* |
| payment-rule | *(redirect → sales-process)* |
| kpi-config | KPI config *(hoặc cắt)* |
| kpi-board | *(cắt — dùng BI)* |
| lead | Lead |
| opportunity | Opportunity |
| activity | Activity |
| tour-booking | Tour / tasting |
| sale-quotation | Sale quotation |
| event-hold | Event hold |
| hall-calendar | Hall calendar |
| contract | Contract |
| contract-payment | Contract payment |
| beo | BEO |
| attendance-booking | Attendance booking |
| ai-inbox | AI inbox |
| campaign | Campaign |
| customer | Customer |

---

## 7. Definition of Done G3.4 (trước Confirm)

- [ ] Không form nào Title Case trái R1  
- [ ] Mobile: không h-scroll (trừ kanban/calendar)  
- [ ] Opp kanban cuộn ngang kiểu task  
- [ ] Không KPI/insight BI trên form nghiệp vụ; kpi-board khỏi menu Wedding  
- [ ] Toolbar chứa action chính; reuse component ART  
- [ ] Mọi list: data-table + toggle cards  
- [ ] Sale team/quota đủ CRUD + item policy + allocation FMCG  
- [ ] 1 form Sales process: stage + checklist(+create doc) + payment rule, có kéo thả  

```
Gate note: G3 CHƯA Confirm — luật mới từ sponsor invalidate điểm G3.3
Next: G3.4 theo §5 — align ART-ERP + merge process + redesign team/quota
```
