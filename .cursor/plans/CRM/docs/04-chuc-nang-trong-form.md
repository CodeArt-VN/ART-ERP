# 04 — Chức năng trong form (G2 draft — chờ Confirm)

Quy ước: **R** = Required field/action · **C** = Config · **G** = Gate (chặn nếu thiếu).

---

## A. SETUP

### A1. Sale Team (`crm-sale-team`)
**Fields:** Branch/Venue, Team name, Type (Wedding/Corporate/Banquet), Leader, Members (AE), Active.  
**Chức năng:** CRUD · Assign member · Disable.  
**Ghi chú:** Lead/Opp bắt buộc Primary Owner ∈ team.

### A2. Sale Quota (`crm-sale-quota`)
**Fields:** Period (tháng/quý), Team/AE, Target Signed, Target Collected, Venue optional.  
**Chức năng:** CRUD · Copy kỳ · Báo cáo vs actual (đọc từ Contract/Payment).

### A3. Hall (`crm-event-hall`)
**Fields:** Branch, Code/Name, Capacity min/max, Ca (trưa/tối), MinSpend optional, Active.  
**Chức năng:** CRUD · Gắn calendar.

### A4. Package / Menu set (`crm-event-package`)
**Fields:** Hall (optional), Name, Pax/Bàn, Lines → WMS Item hoặc mô tả, BasePrice, Peak multipliers link.  
**Chức năng:** CRUD · Clone · Version.

### A5. Price book / Peak (`crm-price-book`)
**Fields:** Rule (ngày trong tuần / lễ / mùa), Surcharge % hoặc amount, EffectiveFrom/To.  
**Chức năng:** CRUD · Preview giá trên Quote.

### A6. Segment (`crm-segment`)
**Fields:** Code, Name, Priority SLA, Default process, Default checklist set.  
**Chức năng:** CRUD · Map rule (nguồn/budget/member).

### A7. Quy trình bán (`crm-sales-process`)
**Fields:** Name, Stages list (Inquiry…Nurture), Segment áp dụng, PaymentRuleId, ChecklistSetId, HoldHours.  
**Chức năng:** CRUD · Activate · Clone.  
**G:** Opp chạy theo 1 process active.

### A8. Checklist template (`crm-checklist-template`)
**Fields:** Process+Stage, Item text, Sort, **`IsRequired`**, Role thực hiện.  
**Chức năng:** CRUD · Reorder · Copy stage.  
**G:** Item Required chưa done → không đổi stage.

### A9. Payment rule — cọc/TT (`crm-payment-rule`)
**Fields từng milestone:** Name, Sort, **`IsRequired`**, MinPercent nullable, MinAmount nullable, DueRule (D-n / after stage), GateAction (Confirmed / HardBook / BEOLock / FreshPO).  
**Chức năng:** CRUD milestones · Validate (ít nhất một trong Min% / MinAmount nếu Required).  
**Chốt G1:** Required Y/N; min % **hoặc** min tiền — cấu hình theo quy trình.

### A10. KPI Config (`crm-kpi-config`)
**Fields:** MetricCode, Name, Source/Query hoặc formula, Filters, Board, Roles, Active.  
**Chức năng:** CRUD · Enable/Disable · Seed default metrics.  
**Chốt G1:** linh động, không hard-code UI cố định.

---

## B. PIPELINE

### B1. Lead (mở rộng)
**Fields R:** Name/Phone, Source, Campaign, Segment (auto/manual), Owner, Branch.  
Optional: EventDate dự kiến, Guests, Budget.  
**Chức năng:** CRUD · Assign · Convert→Opp · AI draft reply.  
**G:** Source+Campaign bắt buộc trước convert (config).

### B2. Opportunity
**Fields R:** Process, Stage, Owner, Contact, EventDate, Guests/Hall quan tâm, Amount estimate.  
**Tabs:** Checklist · Activities · Quotes · Holds · Contract · BEO.  
**Chức năng:** Stage move (**G** checklist Required) · Lose reason · Convert Quote.  
**Ký MVP:** Owner xác nhận stage (status).

### B3. Activity
**Fields:** Type, Regarding (Lead/Opp), Due, Note, Done.  
**Chức năng:** CRUD · Complete · Auto từ AI log.

### B4. Tour / Tasting
**Fields R:** Opp, DateTime, Hall, Result (Show/NoShow/Interested…).  
**Chức năng:** CRUD · Reminder · Update checklist Tour.

### B5. SALE Quotation (event mode)
**Fields R:** Opp, Package/lines, Peak applied, ValidUntil, Version.  
**Chức năng:** Draft · Send PDF · Revise · Submit discount Approval nếu vượt quyền · Convert Hold/Contract.  
**G:** Dòng từ price book (không invent giá).

### B6. Event Hold
**Fields R:** Opp, Hall, Date, Slot, Expiry, HoldType Soft/Hard.  
**Chức năng:** Hold · Extend · Release · Conflict check · Auto-expire job.  
**G:** Concurrent lock; Soft theo HoldHours process.

### B7. Hall Calendar
**View:** Tháng/tuần theo Hall — Free / Soft / Hard / Booked.  
**Chức năng:** Filter · Click mở Hold/Contract · Suggest alternate slot.

---

## C. CONTRACT & PAYMENT

### C1. Contract
**Fields R:** Opp, Quote ref, Contact, EventDate, Hall, Amount, Process, Owner.  
**Statuses (MVP Owner ký):** Draft → OwnerSigned/Confirmed → … (sau: multi APPROVAL).  
**Chức năng:** Create from Quote · Owner Sign (status) · Phụ lục · Generate SO.  
**G:** Payment milestones Required theo rule + checklist Contract Required.

### C2. Contract Payment schedule & tracking
**Fields:** Milestones từ Payment rule (copy vào HĐ), PaidAmount, Linked IncomingPayment, Status Due/Paid/Overdue.  
**Chức năng:** Record payment · Remind · Escalate Overdue · Hiển thị gate Ops.  
**G:** GateAction chỉ mở khi milestone Required = Paid (hoặc đủ min %/amount).

---

## D. OPS

### D1. BEO
**Sections R (Ops-ready):** Menu course×zone · Dietary/Allergen · Beverage · Table plan (file) · Timing · AV · Staffing · Vendor window · Deposit flag · Version.  
**Statuses MVP:** Draft → OpsOwnerSigned → Locked (D-7) → Executed.  
**Chức năng:** Edit · Owner Sign · Lock · Print kitchen (ẩn giá bán) · Change request sau lock.  
**G:** Checklist BEO Required; milestone Payment gắn BEOLock nếu config; sau → APPROVAL đồng ký Sales+Ops+Chef.

### D2. Attendance / Event day (mở rộng)
**Fields thêm:** IDOpp, IDContract, IDHall, ActualPax, Extras log.  
**Chức năng:** Check-in ops · Extra ký · Close → trigger invoice path.

---

## E. AI / MKT / KPI runtime

### E1. AI Inbox (P1)
Draft list · Approve/Reject send · Confidence · Link Lead/Opp. AutoSend off.

### E2. Campaign (siết)
Bắt buộc khi tạo Lead (config). Attribution fields.

### E3. KPI Board
Render widgets từ KPI Config · Filter period/team/venue.

---

## F. Ma trận quyền (rút gọn)

| Form | Sale | Leader | Mkt | Kitchen | Banquet | Accountant |
|------|------|--------|-----|---------|---------|------------|
| Quote/Hold | R/W own | R/W team | R | — | R calendar | — |
| Contract/Payment | R/W | Approve discount | — | — | R | R/W payment |
| BEO | R/W draft | R | — | R no price | R/W ops | R deposit |
| KPI Config | — | R | R | — | — | — |
| KPI Board | R own | R team | R mkt | — | — | R |
