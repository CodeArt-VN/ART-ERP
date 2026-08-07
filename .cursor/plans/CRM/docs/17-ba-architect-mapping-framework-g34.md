# G3.4 — BA / Architect mapping framework (old → new)

**Ngày:** 2026-07-28  
**Mục đích:** khung mapping để các role hiểu DB cũ **ngay từ bây giờ**, nhưng **không execute import** trước UAT.  
**Phạm vi:** ownership entity + lifecycle + rule Import / Transform / Drop.  
**Không làm trong doc này:** ETL script, data clean, cutover plan chi tiết, SAP sync.

---

## 1. Luật cứng từ sponsor (áp dụng mapping)

| # | Luật | Hệ quả mapping |
|---|------|----------------|
| 1 | CRM center **không** phải SalesOrder | SO không phải master lifecycle CRM |
| 2 | Ignore SAP sync | Không map SAP object vào CRM target schema |
| 3 | Ignore module `SalesOrderDraft` riêng | Draft chỉ là status; approval ở phân hệ khác |
| 4 | `LeadO2O` **không** phải target structure | Absorb vào Lead (+ AI inbox signal) |
| 5 | Quote versioning + compare **bắt buộc** | Giữ history version; không flatten 1 quote |
| 6 | Import cũ **sau UAT** | Doc này = design readiness, chưa migration run |

---

## 2. Target lifecycle (new)

```text
Inbound signal (AI inbox)
        ↓ apply
Lead (absorb channel/campaign/pax/hall/date/UTM)
        ↓ convert
Opportunity (commercial cockpit / Inquiry thực)
        ↓
Quote versions (v1/v2… + change reason)
        ↓
Hold / Booking (soft → hard by payment gate)
        ↓
Contract + Payment milestones
        ↓
BEO (ops handoff packet)
        ↓
Event / Attendance / Invoice / Nurture
```

Ownership gợi ý:

| Domain object | Owner role chính | Consumer |
|---------------|------------------|----------|
| Lead + inbound signal | Sales + Marketing | Sales manager |
| Opportunity | Sales | Sales manager / Finance (read gates) |
| Quote version | Sales | Customer / Finance |
| Hold + calendar | Sales + Ops | Ops |
| Contract + payment gate | Sales + Finance | Ops (unlock) |
| BEO | Ops / Banquet | Kitchen / Floor / Bar |

---

## 3. Mapping matrix (old → new)

> Cột **Decision**: `Import` = mang data sang sau transform · `Transform` = reshape trước khi gắn target · `Drop` = không đưa vào CRM target (có thể giữ ở phân hệ khác).

| Old concept (In Holdings / as-is) | New target | Decision | Transform rule (draft) | Notes |
|-----------------------------------|------------|----------|------------------------|-------|
| Lead (basic contact) | `Lead` | Import | Map name/phone/email/owner; normalize status → New/Warm/Hot/Converted | Keep as CRM front door |
| LeadO2O / O2O inquiry rows | `Lead` + `AI inbox signal` | Transform | Channel, campaign, UTM, hall intent, pax, event date → Lead fields; raw message → inbox signal timeline | **Không** tạo entity O2O riêng |
| Inquiry (sales case) | `Opportunity` | Transform | Inquiry header → Opportunity; stage start = Inquiry; keep source/campaign from lead | Opportunity = Inquiry thực sau qualify |
| Quotation / quote lines | `Sale quotation` versions | Transform | Group by quote code; version asc; keep change reason if recoverable else `Migrated baseline` | Compare v(n)/v(n+1) required |
| Booking / soft reserve | `Event hold` | Transform | Soft/Hard/Booked/Free semantics; expiry; conflict text | Calendar consumes hold state |
| Confirmed booking after deposit | `Event hold` (Hard) + payment gate Paid | Transform | Only promote Hard when deposit gate evidence exists | Do not invent Hard without payment |
| Contract / agreement | `Contract` | Import | Link OppId + QuoteCode | Sign steps keep as status trail |
| Deposit / milestone payments | `Contract payment` | Transform | Map milestone → GateAction (Confirmed / HardBook / BEOLock) | Gate consequence bắt buộc |
| BEO / banquet order sheets | `BEO` | Transform | Packet sections: menu, allergen, run-of-show, staffing, beverage, floor | Ops handoff language, not SO |
| SalesOrder (wedding path) | Contract handoff / ops context | Drop (as CRM center) | If needed later: reference link only, not lifecycle driver | Finance/ops outside CRM core |
| SalesOrderDraft module | Quote/Contract status only | Drop (as module) | Status `Draft` stays on existing docs | Approval subsystem riêng |
| SAP sync objects | — | Drop | Out of CRM mapping scope | Separate subsystem |
| Activity / call logs | `Activity` | Import | Regarding → Lead or Opportunity | Keep chronology |
| Campaign membership | `Campaign` + Lead/Opp Campaign field | Import | Attribution fields required on convert | MembersCount may recompute |
| Hall / venue master | `Event hall` | Import | Capacity + slot + min spend | Calendar source |
| Customer roles (bride/groom/planner) | Contact roles on Opportunity/Lead | Transform | Role enum preserve | Multi-stakeholder |

---

## 4. Field-level absorb rules (LeadO2O → Lead)

| Old O2O-ish field | Lead field | Required on apply? |
|-------------------|------------|--------------------|
| Channel / social source | `Channel` | Yes |
| Campaign / ad set | `Campaign` | Preferred |
| Guest count / pax | `Guests` | Yes if present |
| Preferred venue/hall | `PreferredHall` | Yes if present |
| Event date intent | `EventDate` | Yes if present |
| UTM / landing | `UTM` | Preferred |
| Raw message / thread | AI inbox `DraftBody` + timeline | Keep as signal evidence |
| Confidence / AI score | Inbox `Confidence` | Optional |

**Apply semantics (prototype đã demo):**  
`Apply signal to lead` copies hall/pax/date/campaign/channel/UTM onto Lead, marks signal `Applied`. Discard does **not** delete history — only triage out of open queue.

---

## 5. Opportunity absorb rules (Inquiry → cockpit)

| Inquiry/old sales case | Opportunity | Rule |
|------------------------|-------------|------|
| Case title | `Name` | Required |
| Owner | `Owner` | Required to move stage |
| Event date / hall / pax | Event fields | Carry from Lead on convert |
| Source / campaign / channel | Demand source | Preserve on convert — **do not** overwrite with `Source=Lead` |
| Current stage | `Stage` | Map to Wedding/Corp process stages |
| Open tasks | Checklist + Activities | Checklist is gate; activity is chronology |
| Commercial docs | Related Tour / Quote / Hold / Contract / Payment / BEO | Cockpit must deep-link, not duplicate BI |

---

## 6. Drop / park list (explicit)

1. **SAP objects** — park outside CRM.
2. **SalesOrder as CRM spine** — park; if referenced, only as downstream document link.
3. **SalesOrderDraft as separate CRM module** — park; keep draft as status.
4. **LeadO2O entity** — drop as target; absorb into Lead + inbox signals.
5. **Fake local AI approval product** — inbox is triage/apply queue, not approval workflow product.

---

## 7. Import readiness checklist (after business chốt)

BA:

- [ ] Chốt dictionary old table/column ↔ new object/field (finalize §3).
- [ ] Chốt status mapping Lead / Opp / Quote / Hold / Payment / BEO.
- [ ] Chốt rule “missing event date / hall / pax” = quarantine vs default.

Architect:

- [ ] Chốt FK graph: Lead→Opp→QuoteVersion→Hold→Contract→Payment→BEO.
- [ ] Chốt idempotent import keys (Code / external Id).
- [ ] Chốt soft-delete / reopen / version append policy for quotes.
- [ ] Không overbuild schema trước khi BA chốt dictionary cuối.

PM / UAT:

- [ ] Import chỉ sau UAT business path pass.
- [ ] Pilot 1 brand/outlet trước full cutover.
- [ ] Rollback = freeze new writes + restore snapshot (plan riêng).

---

## 8. Demo evidence already aligned

Prototype G3.4 Option B đang thể hiện hướng mapping này:

1. AI inbox → Apply → Lead fields + timeline.
2. Lead convert → Opportunity giữ Source/Campaign/Channel + event intent.
3. Opportunity cockpit deep-link Tour/Quote/Hold/Contract/Payment/BEO + blockers.
4. Quote version compare + create next version.
5. Hold rule hint / conflict / next action.
6. Payment Impact / ImpactBlocked unlocks gates.
7. BEO ops packet + lock gated by BEOLock payment.

---

## 9. Next after business confirm

1. BA điền dictionary cột thật từ DB document (table-level, không chỉ concept).
2. Architect phát hành ERD target + migration staging tables.
3. PM xếp UAT → import pilot — **không** đảo thứ tự.
