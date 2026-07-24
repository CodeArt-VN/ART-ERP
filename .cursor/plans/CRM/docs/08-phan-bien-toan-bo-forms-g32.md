# Phản biện TOÀN BỘ forms G3 — Sale / Marketing / Operator (vòng 2)

**Ngày:** 2026-07-24  
**Bối cảnh:** Sponsor chấm G3.1 vẫn **tệ**. Vòng 1 nghiêng Opp; vòng 2 đánh giá **25/25 forms** theo tiêu chí:

1. **UI/UX hiện đại, thân thiện, đẹp** (tham chiếu Salesforce Lightning: highlight panel, path, related lists trong context, action bar — không phải master-data CRUD).  
2. **Thực dụng · theo dõi xuyên suốt** — mở form là làm việc / ra quyết định, không phải “khai báo danh sách field”.  
3. **Phản biện thật** — nói rõ vì sao fail, cần gì; không đếm tick chức năng.

**Thang:** UI/UX 1–10 · Thực dụng 1–10 · Verdict: `Fail` / `Weak` / `OK-MVP` / `Good`.

---

## A. SETUP (admin cấu hình — vẫn phải thực dụng)

### A1. `sale-team`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | List tên team. Không roster AE, không thấy pipeline/quota gắn team, không “ai đang giữ deal nào”. |
| Mkt | 3 | 2 | Không map team ↔ segment/venue cho routing lead. |
| Ops | 2 | 1 | Ít liên quan; nếu cần liên hệ AE theo tiệc thì form này vô dụng. |
**Verdict: Fail.** Cần: roster members, leader, type Wedding/Corp, link quota + active deals count.

### A2. `sale-quota`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Có target số nhưng không % đạt, không drill xuống Opp/HĐ. Leader không coaching được. |
| Mkt | 2 | 2 | Không đối chiếu volume lead/campaign. |
| Ops | 1 | 1 | — |
**Verdict: Fail.** Cần: progress bars Signed/Collected vs Actual, kỳ, traffic-light, link actual records.

### A3. `event-hall`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Capacity text; không preview availability. |
| Mkt | 2 | 2 | Không gắn story venue cho content. |
| Ops | 4 | 4 | Cần min/max, ca, min spend — đang phẳng. |
**Verdict: Weak.** Cần: capacity band, slots, deep-link calendar, upcoming bookings strip.

### A4. `event-package`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Không dòng món / giá peak preview khi bán. |
| Mkt | 3 | 3 | Không “hero package” cho campaign. |
| Ops | 3 | 4 | Thiếu lines → bếp không chuẩn hóa. |
**Verdict: Fail.** Cần: line items table, base price, clone version, “preview on quote”.

### A5. `price-book`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Rule text; không simulator “ngày X + package Y = giá”. |
| Mkt | 2 | 2 | — |
| Ops | 2 | 2 | — |
**Verdict: Fail.** Cần: rule cards + **price simulator** (input date/package → surcharge).

### A6. `segment`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Không thấy default process/checklist khi gán segment. |
| Mkt | 4 | 5 | Segment là xương sống journey — UI vẫn CRUD. |
| Ops | 2 | 2 | SLA không hiện trên Opp. |
**Verdict: Weak.** Cần: default process/checklist/payment-rule chips + SLA badge preview.

### A7. `sales-process`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Stages là textarea — **không phải process designer**. |
| Mkt | 3 | 3 | Không thấy segment áp dụng. |
| Ops | 3 | 3 | HoldHours/PaymentRule chìm trong field. |
**Verdict: Fail (critical setup).** Cần: visual stage rail, bind PaymentRule + ChecklistSet + HoldHours, Activate/Clone.

### A8. `checklist-template`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Flat rows; không group theo stage; không cảm nhận gate. |
| Mkt | 2 | 2 | — |
| Ops | 4 | 5 | Required items cho BEO/Contract phải rõ role. |
**Verdict: Weak.** Cần: board theo Stage, drag sort, Required toggle nổi, preview gate.

### A9. `payment-rule`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Bảng mốc tách; không timeline gate. |
| Mkt | 1 | 1 | — |
| Ops | 4 | 5 | BEOLock/HardBook phải nhìn là hiểu. |
**Verdict: Fail (critical money).** Cần: milestone timeline + GateAction badges + validate min%/amount.

### A10. `kpi-config`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 2 | 2 | Config list ≠ thứ Leader dùng hàng ngày. |
| Mkt | 3 | 3 | Thiếu metric funnel. |
| Ops | 2 | 2 | — |
**Verdict: Weak.** Cần: enable cards theo Board (Sales/Mkt/Ops), seed defaults.

---

## B. PIPELINE

### B1. `lead` (có sẵn — mở rộng)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Form cũ; thiếu next touch, convert wizard, Opp preview. |
| Mkt | 4 | 5 | Campaign có field nhưng không journey. |
| Ops | 2 | 1 | — |
**Verdict: Weak.** Cần: highlight + activity strip + Convert→Opp CTA + attribution.

### B2. `opportunity` (đã G3.1 workspace)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 7 | Đúng hướng 360; vẫn thiếu polish SF (compact density, related hover, composer activity inline). Payment/BEO dễ bị fold dưới fold. |
| Mkt | 5 | 5 | Đã có chip Source/Campaign/Segment — chưa funnel ngược campaign. |
| Ops | 5 | 5 | Ops strip còn mỏng. |
**Verdict: OK-MVP (duy nhất).** Cần tiếp: sticky action bar, payment/BEO luôn visible, inline activity.

### B3. `activity`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Inbox việc độc lập; không Today/Overdue; không Regarding card. |
| Mkt | 3 | 3 | AI log không vào đây. |
| Ops | 3 | 3 | — |
**Verdict: Fail.** Cần: Today focus, Regarding link chip, complete-in-list, filter My/Team.

### B4. `tour-booking`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | CRUD lịch; Result không đẩy checklist/stage Opp. |
| Mkt | 3 | 4 | Show/NoShow = funnel metric — UI không capture sạch. |
| Ops | 3 | 3 | Hall conflict không check. |
**Verdict: Fail.** Cần: result outcomes → update Opp checklist; calendar conflict hint.

### B5. `sale-quotation`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Không line editor, peak, version compare, PDF/send. |
| Mkt | 2 | 2 | — |
| Ops | 2 | 2 | Package lines không về BEO. |
**Verdict: Fail (critical sell).** Cần: header Opp + lines table + peak applied + version + CTA Hold/Contract.

### B6. `event-hold`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 4 | Soft/Hard/Expiry text; countdown & conflict yếu. |
| Mkt | 1 | 1 | — |
| Ops | 4 | 4 | Calendar tách. |
**Verdict: Weak.** Cần: countdown, conflict panel, Extend/Release actions, link calendar cell.

### B7. `hall-calendar`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 6 | Thực dụng hơn hẳn; thiếu tuần/tháng thật, filter team. |
| Mkt | 2 | 2 | — |
| Ops | 5 | 6 | Booked→BEO có deep-link; cần rõ hơn. |
**Verdict: OK-MVP.** Cải thiện: tooltip, filter, week header.

---

## C. CONTRACT / PAYMENT / OPS

### C1. `contract`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | G3.1 có sign path + payment — list vẫn bảng. |
| Mkt | 2 | 2 | — |
| Ops | 4 | 4 | Thiếu link BEO/Attendance. |
**Verdict: Weak→OK list fail.** List cần status/payment %; detail đã khá hơn.

### C2. `contract-payment`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Bảng mốc tách HĐ — không phải **payment console**. |
| Mkt | 1 | 1 | — |
| Ops | 4 | 5 | Gate BEOLock phải alert. |
**Verdict: Fail.** Cần: console theo HĐ, record payment CTA, overdue red, gate impact.

### C3. `beo`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Detail sectioned OK; **list** vẫn phẳng. |
| Mkt | 1 | 1 | — |
| Ops | 6 | 6 | Đúng hướng production; thiếu change-request, vendor window. |
**Verdict: OK-MVP detail / Fail list.**

### C4. `attendance-booking` (có sẵn)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 3 | Chưa thấy IDOpp/Contract trên UI. |
| Mkt | 2 | 2 | — |
| Ops | 6 | 6 | Form ops sẵn có giá trị; cần FK wedding. |
**Verdict: Weak (gap FK).** Thêm strip Opp/Contract/Hall trên detail.

---

## D. AI / MKT / KPI / MASTER

### D1. `ai-inbox`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | List draft; không approve/reject cạnh nội dung; không mở Lead. |
| Mkt | 4 | 4 | Cần confidence + channel queue. |
| Ops | 1 | 1 | — |
**Verdict: Fail.** Cần: split pane draft | meta | Approve/Reject; link Regarding.

### D2. `campaign`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 3 | Có sẵn; thiếu funnel wedding. |
| Mkt | 4 | 4 | Cần members → tour show → signed widgets. |
| Ops | 1 | 1 | — |
**Verdict: Weak.** Thêm funnel strip trên detail.

### D3. `customer` (= business-partner)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Tái dùng BP — thiếu role bride/groom/planner trên wedding context. |
| Mkt | 4 | 4 | — |
| Ops | 3 | 3 | — |
**Verdict: Weak (reuse).** UDF roles + related Opp list (G4 nếu nặng).

### D4. `kpi-board`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 2 | 2 | Rows metric ≠ dashboard. |
| Mkt | 3 | 3 | — |
| Ops | 2 | 2 | — |
**Verdict: Fail.** Cần: widget grid từ kpi-config, filter period/team.

---

## E. Ma trận tổng (UI / Thực dụng / Verdict)

| Form | UI | Dụng | Verdict |
|------|----|------|---------|
| sale-team | 3 | 3 | Fail |
| sale-quota | 3 | 4 | Fail |
| event-hall | 3 | 4 | Weak |
| event-package | 3 | 3 | Fail |
| price-book | 3 | 4 | Fail |
| segment | 3 | 4 | Weak |
| sales-process | 3 | 4 | Fail |
| checklist-template | 3 | 4 | Weak |
| payment-rule | 3 | 4 | Fail |
| kpi-config | 2 | 2 | Weak |
| lead | 4 | 4 | Weak |
| opportunity | 6 | 7 | OK-MVP |
| activity | 3 | 3 | Fail |
| tour-booking | 3 | 3 | Fail |
| sale-quotation | 3 | 3 | Fail |
| event-hold | 3 | 4 | Weak |
| hall-calendar | 5 | 6 | OK-MVP |
| contract | 5 | 5 | Weak |
| contract-payment | 3 | 3 | Fail |
| beo | 5 | 5 | Weak/OK detail |
| attendance-booking | 5 | 4 | Weak |
| ai-inbox | 3 | 3 | Fail |
| campaign | 4 | 4 | Weak |
| customer | 5 | 5 | Weak |
| kpi-board | 2 | 2 | Fail |

**Đếm:** Fail 12 · Weak 11 · OK-MVP 2 (`opportunity`, `hall-calendar`).  
→ Prototype vẫn **hệ thống form khai báo**; chỉ 2 màn chạm mức làm việc.

---

## F. Tổng hợp ưu tiên redesign G3.2 (toàn hệ)

### Nguyên tắc bắt buộc (Salesforce-ish)
Mỗi form **list**: insight strip (KPI/health) + primary object cards hoặc enriched rows — không chỉ datatable trần.  
Mỗi form **detail**: Highlight panel + Action bar + 1 “working canvas” (timeline/lines/roster/funnel) + related context — field dump xuống tab Fields.

### P0 — làm ngay (unblock cảm nhận “dùng được”)
1. `sales-process` — visual stages + binds  
2. `payment-rule` — milestone timeline + gates  
3. `checklist-template` — group by stage  
4. `sale-quotation` — lines + peak + CTA  
5. `contract-payment` — payment console  
6. `activity` — today/regarding  
7. `tour-booking` — result outcomes  
8. `ai-inbox` — approve split pane  
9. `kpi-board` — widget grid  
10. `sale-quota` — progress vs actual  
11. `event-package` — line items  
12. `price-book` — simulator  
13. `sale-team` — roster  
14. List enrich: `contract`, `beo`, `event-hold`, `lead` insight  

### P1
- `segment`, `event-hall`, `kpi-config`, `campaign` funnel, `lead` convert strip, `attendance` FK strip, `customer` roles note  
- Opp sticky payment/BEO  

### Không làm
Thêm form mới. Không HTML mock tách source.

---

## G. Definition of Done G3.2
Sponsor mở lần lượt **mọi form P0** và với mỗi form trả lời được câu:  
*“Tôi đang làm việc gì / quyết định gì trên màn này?”* — nếu câu trả lời là “điền field” → **vẫn Fail**.

```
Gate note: G3.2 redesign theo phản biện toàn bộ forms
Sponsor: Confirm G3 sau khi review all P0
```
