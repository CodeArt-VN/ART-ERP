# Phản biện G3 Prototype — Sale / Marketing / Operator

**Ngày:** 2026-07-24  
**Tiêu chí sponsor:** (1) UI/UX hiện đại, thân thiện — tham chiếu Salesforce (2) Đầy đủ · theo dõi xuyên suốt · **thực dụng**, không phải form khai báo danh sách (3) Phản biện thật, không đếm checklist.

**Verdict chung:** Prototype v1 = **CRUD skeleton** (PageBase + data-table + form-control). Đủ để chứng minh *có route*, **không đủ** để Sale làm việc hàng ngày. Opp detail là ví dụ thất bại rõ nhất: Stage/Process chỉ là 2 ô text; Checklist/Related nằm tab riêng; không thấy tiến độ cọc, next step, path-to-close.

---

## 1. Sale (AE / Leader)

### Điểm đau khi mở 1 Opportunity
- Không thấy **path**: quy trình nào → stage nào trong chuỗi → %/gate còn lại.
- Không thấy **Next best action** (gọi ai, khi nào, checklist Required còn mấy).
- Không thấy **money path**: báo giá active, hold sảnh, HĐ, mốc cọc Paid/Due.
- List Opp = bảng phẳng — thiếu kanban / unhealthy deal (quá hạn tour, hold sắp hết).

### Chấm từng nhóm form

| Form | Điểm (UI/UX · Thực dụng) | Phản biện Sale |
|------|--------------------------|----------------|
| `opportunity` list | 3/10 · 2/10 | Bảng khai báo. Cần pipeline board + highlight SLA/hold expiry. |
| `opportunity` detail | 2/10 · 1/10 | **Core fail.** Field dump. Tab Related = link sang form khác = bắt Sale nhảy app. Phải là **workspace 360**. |
| `activity` | 3/10 · 3/10 | List độc lập, không timeline trên Opp. |
| `tour-booking` | 3/10 · 4/10 | Có fields nhưng không gắn kết quả vào checklist/stage. |
| `sale-quotation` | 3/10 · 3/10 | Bảng dòng giá OK kỹ thuật, thiếu compare version / “recommended package” / peak preview trên Opp. |
| `event-hold` | 4/10 · 4/10 | Hold type/expiry có nhưng conflict/calendar không nhúng Opp. |
| `hall-calendar` | 5/10 · 5/10 | Khá thực dụng hơn các form khác; thiếu click → tạo hold từ ô Free, filter team. |
| `contract` | 3/10 · 2/10 | Status OwnerSigned chỉ là select — không timeline ký + phụ lục. |
| `contract-payment` | 3/10 · 2/10 | Bảng mốc tách khỏi Opp/HĐ — Sale không “nhìn một mắt” đủ cọc chưa. |
| Setup (`sale-team`…`payment-rule`) | 4/10 · 5/10 | CRUD setup chấp nhận được ở MVP admin; UI vẫn thô. |
| `lead` / `campaign` | 4/10 · 4/10 | Có sẵn hệ thống; thiếu journey convert + attribution trên Opp. |
| `ai-inbox` / `kpi-board` | 3/10 · 3/10 | List draft/KPI — chưa actionable từ Opp. |

### Góp ý Sale (Salesforce-ish)
1. **Highlight panel** trên Opp: Process · Stage path · Amount · Close/Event date · Owner · Health.
2. **Path / Stage coach** ngang (Inquiry→…→Nurture), click stage chỉ khi gate OK.
3. **Right rail:** Next steps + Activity composer + Upcoming.
4. **Below:** Checklist stage hiện tại · Quotes · Hold · Contract & Payment progress · BEO status.
5. List: **Kanban by Stage** + list mode; card hiện EventDate, Hall, Amount, hold badge.

---

## 2. Marketing

### Điểm đau
- Không thấy Lead→Opp **attribution** (Campaign/Source/Segment) trên Opp workspace.
- Campaign vẫn form riêng; không funnel “campaign member → show rate tour → signed”.
- AI Inbox tách rời — không “đề xuất reply” gắn activity trên Opp/Lead.

### Chấm nhanh

| Form | UI/UX · Thực dụng | Phản biện Mkt |
|------|-------------------|---------------|
| `lead` | 4 · 4 | Thiếu journey strip + next touch. |
| `campaign` | 4 · 3 | Không dashboard ROI gắn wedding pipeline. |
| `segment` | 3 · 4 | Setup OK; không hiện segment badge trên Opp header. |
| `ai-inbox` | 3 · 2 | Draft list — cần approve-in-context trên Lead/Opp. |
| `kpi-board` | 3 · 3 | Metric rows ≠ board widgets (conversion by source). |
| Opp detail | 2 · 1 | Mất story marketing → sale. |

### Góp ý Mkt
- Opp header: Source · Campaign · Segment · Member level.
- Campaign: funnel widgets (Lead / Tour show / Quote / Signed).
- AI: panel “Suggested reply” trên Lead/Opp Activity.

---

## 3. Operator (Banquet / Kitchen / Coordinator)

### Điểm đau
- BEO = form textarea — **không** phải production order (zone×course, allergen flag, timing, lock countdown).
- Từ Opp không thấy BEO status / D-7 lock / deposit gate.
- Attendance chưa gắn Opp/Contract trên UI (chỉ G2 nói mở rộng).
- Calendar hữu ích nhưng Ops cần view “Booked hôm nay → mở BEO”.

### Chấm nhanh

| Form | UI/UX · Thực dụng | Phản biện Ops |
|------|-------------------|---------------|
| `beo` | 2 · 2 | Textarea = khai báo. Cần section cards + print kitchen (ẩn giá). |
| `attendance-booking` | 5 · 4 | Có sẵn; thiếu FK Opp/Contract trên UI. |
| `hall-calendar` | 5 · 5 | Nên deep-link Booked → BEO/Contract. |
| `contract-payment` | 3 · 3 | Gate BEOLock phải hiện đỏ trên BEO/Opp. |
| Opp detail | 2 · 1 | Ops mở Opp không biết tiệc đã sẵn sàng chưa. |

### Góp ý Ops
- BEO workspace: sections + version + lock state + deposit flag.
- Opp: strip “Ops readiness” (Hold Hard? Deposit BEOLock? BEO Locked?).
- Calendar: badge Booked click → BEO.

---

## 4. Tổng hợp ưu tiên redesign (G3.1)

| Prio | Thay đổi | Lý do 3 role |
|------|----------|--------------|
| **P0** | **Opportunity workspace 360** (path, checklist, activities/next, quotes, hold, contract+payment, BEO strip) | Core fail cả 3 role |
| **P0** | Opportunity **pipeline board** (kanban) + list | Sale daily |
| **P1** | Contract detail + **payment progress timeline** nhúng | Money path |
| **P1** | BEO detail **sectioned ops** + gate banner | Ops |
| **P1** | Hall calendar deep-link + legend actions | Sale+Ops |
| **P2** | Lead/Campaign attribution trên Opp header | Mkt |
| **P2** | AI inbox / KPI board widgets | Sau Confirm G3.1 |

**Không làm:** thêm form mới. **Làm:** đổi *cách dùng* form đã có từ “danh sách field” → “màn hình công việc”.

---

## 5. Definition of Done demo G3.1
Mở `#/opportunity/1001` phải **một màn** thấy:
1. Process = Wedding Standard + stage coach Tour (highlight)
2. Checklist Required còn mở + nút Move stage (gate)
3. Next step + 2–3 activities
4. Quote / Hold / Contract tóm tắt
5. Payment milestones progress (Paid/Due + Gate)
6. BEO status strip

Sale/Mkt/Ops ký nhận: *“đây là chỗ làm việc, không phải form master data.”*
