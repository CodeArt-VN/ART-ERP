# G3.4 — phản biện 2 vòng với toàn bộ role + backlog sửa prototype

**Ngày:** 2026-07-28  
**Phạm vi:** đánh giá **cái đang làm hiện tại** so với nghiệp vụ thật; không phê bình DB cũ thiếu gì.  
**Role tham gia:** BA, Architect, PM, UX, Sales manager, Sales executive, Event ops, Finance/commercial control.

---

## 1. Điều đã loại khỏi scope theo sponsor

1. **Không** coi SalesOrder là trung tâm CRM.
2. **Bỏ qua** sync SAP — phân hệ khác lo.
3. **Bỏ qua** module `SalesOrderDraft` như một module riêng; approval ở phân hệ khác.
4. `LeadO2O` **không** phải target structure được chấp nhận; Lead mới phải absorb phần inbound này.
5. Import data cũ là việc **sau UAT**, nhưng các role phải hiểu cấu trúc DB cũ ngay từ bây giờ để tránh thiết kế sai.

---

## 2. Kết luận vòng 1

### 2.1 BA
- Lead hiện còn quá mỏng, chưa absorb inbound signal / channel / campaign / event intent.
- Opportunity chưa đủ semantics của Inquiry thực.
- Quote mới có version số học, chưa thể hiện **v1/v2 khác nhau ở đâu**.
- Hold / booking, payment gate, BEO vẫn còn demo-level.

### 2.2 Architect
- Domain đang đúng hướng hơn hệ cũ, nhưng vẫn còn leak ngôn ngữ SO ở checklist / contract.
- Quan hệ object cần xoay về:
  `Lead -> Opportunity -> Quote version -> Hold -> Contract/Payment -> BEO`
- Không nên overbuild schema trước khi BA chốt mapping cuối.

### 2.3 Sales / Ops / Finance / UX / PM
- Sales cần **một cockpit** ở Opportunity.
- Ops cần BEO đủ tin được.
- Finance cần gate payment có **business consequence**.
- UX cần một narrative nhất quán, không nhảy object.
- PM cần giữ demo focus, không dàn trải quá rộng.

---

## 3. Kết luận vòng 2 — backlog tối thiểu phải sửa

Sau khi phản biện lại, các role chốt chỉ sửa **7 outcome nhìn thấy ngay trong demo**:

1. **Inbound inquiry trở thành lead signal**
   - Lead phải hiện channel / campaign / hall / pax / event date / signal timeline.

2. **Opportunity là cockpit sau khi qualify**
   - Từ đây nhìn được stage, checklist blocker, quote, hold, payment gate, BEO readiness.

3. **Quote versioning nhẹ nhưng rõ**
   - Có v1/v2 và “what changed”.

4. **Bỏ ngôn ngữ SO khỏi mặt demo**
   - Đổi sang contract / booking / ops handoff.

5. **Hold + calendar phải giải thích được quyết định**
   - Free / Soft / Hard / Booked, conflict reason, expiry, next action.

6. **Payment gate phải có hậu quả nghiệp vụ**
   - Trả tiền mốc nào thì mở gate nào.

7. **BEO phải đủ tin cho ops handoff**
   - menu, allergen, run-of-show, staffing, beverage, table plan, lock/print.

---

## 4. Những gì vẫn để phase sau

- quote compare engine hoàn chỉnh
- rule engine hold thật
- migration mapping execution
- sync / integration
- approval workflow riêng
- audit trail production-grade

---

## 5. Những gì đã sửa trong prototype sau 2 vòng phản biện

### Lead
- thêm `Channel`, `Campaign`, `Guests`, `PreferredHall`, `EventDate`, `UTM`
- thêm **Recent inbound timeline**
- Lead absorb inbound signal thay vì tách O2O

### Opportunity
- giữ vai trò **cockpit**
- thêm phần:
  - quote delta
  - hold + payment gate summary
  - BEO readiness

### Quote
- có compare `v1 -> v2`
- có `ChangeReason`
- có delta theo line

### Hold / Calendar
- hold giải thích `RuleHint`, `Conflict`, `NextAction`
- calendar thể hiện đúng free/soft/hard/booked + tooltip

### Payment
- gate có `ImpactBlocked` / `Impact`
- record payment mở gate rõ hơn

### BEO
- đổi ngôn ngữ sang **Ops handoff**
- packet đủ: kitchen, critical, run-of-show, ops, bar, floor

### Remove SO language
- bỏ `SO generated`
- đổi `CreateSO` -> `OpenOpsHandoff`

---

## 6b. Option B follow-up (Lead/AI + cockpit + mapping)

1. **AI inbox** restyle ART list; triage `New/Reviewed/Applied/Discarded`; action chính = **Apply signal to lead** (không phải fake approval product).
2. **Lead** timeline có Apply/Open; list hiện Channel + Inbound count + event intent.
3. **Opportunity cockpit** có Commercial path + blockers + deep-link Tour/Quote/Hold/Contract/Payment/BEO; giữ Channel từ lead.
4. **Quote** create next version; Hold/Payment/BEO link ngược cockpit; BEO packet đủ bar/floor + gate BEOLock.
5. **Doc 17** khung mapping BA/Architect old→new (Import/Transform/Drop), import sau UAT.

---

## 6. Narrative demo đề xuất

1. AI / Zalo / FB inquiry -> **Lead inbound**
2. Qualify -> **Opportunity cockpit**
3. Negotiate -> **Quote version v1/v2**
4. Reserve -> **Hold + hall calendar**
5. Collect deposit -> **Payment gate**
6. Release to ops -> **BEO ops handoff**

---

## 7. Kết luận

Vấn đề chính của G3.4 trước khi sửa không phải là layout, mà là:

- thiếu narrative đúng của CRM
- vẫn còn một ít tư duy SO-centric
- chưa làm rõ quote version / hold rule / payment consequence / ops handoff

Sau 2 vòng phản biện, prototype được kéo lại đúng trọng tâm hơn:

**Lead absorb inbound -> Opportunity center -> Quote compare -> Hold decision -> Payment gate -> BEO handoff**
