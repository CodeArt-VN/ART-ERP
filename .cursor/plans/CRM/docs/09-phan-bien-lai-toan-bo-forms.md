# Phản biện LẠI — TOÀN BỘ forms (vòng 3 · sau G3.2)

**Ngày:** 2026-07-24  
**Đối tượng:** 25/25 forms CRM Wedding (list + detail nếu có) — **không chỉ Opportunity**.  
**Cơ sở chấm:** code Angular hiện tại trong `ART-ERP-FE/src/app/pages/CRM` (sau lớp skin `.crm-ws`), không chấm theo ý định / backlog cũ.

**Vì sao làm lại:** Doc `08` chấm *trước* redesign; G3.2 đã phủ hero/card/chip lên nhiều màn. Sponsor vẫn thấy **tệ** → cần phản biện lại theo **trải nghiệm thật khi mở form**, không đếm “đã có section mock”.

---

## 0. Kết luận thẳng (đọc trước)

| Câu hỏi | Trả lời |
|---------|---------|
| G3.2 có đẹp / hiện đại như Salesforce không? | **Không.** Cùng một lớp skin mỏng (hero + card + chip teal), copy-paste SCSS ~36 file. Trông như wireframe có màu, không phải product UI. |
| Đã “làm việc được” chưa? | **Chưa.** Hầu hết CTA = `routerLink` / mock data cứng. Không edit lines, không drag stage, không record payment thật, không convert lead. |
| Opp có phải ngoại lệ? | **Có — nhưng chỉ tương đối.** Opp list (kanban) + detail (workspace) là màn dày nhất; vẫn thiếu density, sticky money/BEO, composer activity, polish. |
| Forms “có sẵn” (lead/campaign/customer/attendance)? | **Vẫn CRUD bảng cũ** — gần như không đụng wedding UX. |
| Verdict hệ thống | **Fail tổng thể.** Skin ≠ workspace. Không đủ Confirm G3 nếu tiêu chí là “thực dụng · theo dõi xuyên suốt · UI hiện đại”. |

**Đếm sau vòng 3 (trung bình 3 role):**  
`Fail` **14** · `Weak` **9** · `OK-MVP` **2** (`opportunity`, `hall-calendar`) · `Good` **0**.

---

## 1. Cách chấm (cứng)

Mỗi form bị hỏi 4 câu. Fail bất kỳ câu P0 → không được `OK-MVP`.

1. **Mở list:** 5 giây có biết *việc gì cần làm hôm nay* không? (không = Fail list)
2. **Mở detail:** có **Highlight + Action + Working canvas** thật không, hay chỉ field/hero trang trí?
3. **Xuyên suốt:** thao tác trên form này có đẩy trạng thái sang Opp / HĐ / BEO / Calendar không, hay chỉ nhảy link?
4. **UI:** typography/spacing/density có đọc được như app bán hàng không, hay “card mock demo”?

Thang: UI 1–10 · Thực dụng 1–10 · Verdict `Fail` / `Weak` / `OK-MVP` / `Good`.

---

## 2. Lỗi hệ thống (áp dụng gần như mọi form G3.2)

Ba role đều chạm cùng một tường:

| # | Lỗi | Hệ quả |
|---|-----|--------|
| S1 | **Skin đồng phục** — `.crm-ws` copy từng page, không design system token dùng chung | Nhìn “một kiểu demo”; không có hierarchy thương hiệu / density chuẩn ERP |
| S2 | **Mock hardcode** — roster, lines, milestones, widgets gắn trong `.ts` | Không tin được khi demo; không chứng minh flow end-to-end |
| S3 | **Action giả** — Approve/Send/Activate/Record payment thường không đổi state bền | Sale/Ops cảm giác “bấm cho vui” |
| S4 | **List = chồng card** thay datatable nhưng **thiếu sort/filter/bulk/empty/skeleton** | Không scale; Leader không triage |
| S5 | **Không related-in-context có edit** | Mọi thứ “xem rồi `routerLink`” = nhảy form như G3.0 |
| S6 | **Lead / Campaign / Customer / Attendance bỏ quên** | Phễu đầu và ngày tiệc đứt khỏi wedding UX |
| S7 | **Mobile / compact** không thiết kế | Hero + nhiều card xếp dọc = scroll mệt trên tablet AE |

> Phản biện meta: vòng 2 bảo “làm Highlight + Canvas”; vòng 3 thấy team **vẽ đúng khung nhưng không đổ nghiệp vụ vào khung**. Sponsor đúng khi vẫn thấy tệ.

---

## 3. Phản biện theo form — Sale / Marketing / Operator

### A. SETUP

#### A1. `sale-team` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | List có insight + OpenOpps — tốt hơn CRUD. Detail roster/deals **đọc-only mock**; không add/remove AE, không drill deal thật theo Id. |
| Mkt | 3 | 2 | Không map team ↔ segment/venue cho routing lead. |
| Ops | 2 | 1 | Không thấy ai liên hệ khi tiệc gần. |
**Verdict: Weak.** Skin có; **không phải team console**. Cần: CRUD roster, deep-link Opp đúng Id, quota pace live.

#### A2. `sale-quota` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Progress bar Signed/Collected = đúng hướng Leader. Drill “pipeline” = link chung `/opportunity`, không filter theo team/period. |
| Mkt | 2 | 2 | Không đối chiếu lead volume / campaign cost. |
| Ops | 1 | 1 | — |
**Verdict: Weak.** Thiếu traffic-light kỳ, breakdown theo AE, click-through filtered.

#### A3. `event-hall`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Card capacity + upcoming text — tạm. Không preview slot trống trong tuần. |
| Mkt | 3 | 2 | Không asset/story venue. |
| Ops | 5 | 5 | Min/max/slot có trên card; detail vẫn mỏng so với ops master. |
**Verdict: Weak.** Cần week strip + deep-link calendar đã filter hall.

#### A4. `event-package` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Lines table có nhưng **không edit**, không version, “Preview on quote” hardlink `/sale-quotation/1`. |
| Mkt | 3 | 3 | Không gói “hero” cho campaign. |
| Ops | 4 | 4 | Lines → bếp chỉ là text; không flag allergen/vendor. |
**Verdict: Fail.** Package bán hàng phải **soạn được line** + clone version, không phải poster.

#### A5. `price-book` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Simulator date+base → surcharge: **một trong ít interaction thật**. Rule vẫn 1 dòng text, không matrix ngày/season. |
| Mkt | 2 | 2 | — |
| Ops | 2 | 2 | — |
**Verdict: Weak.** Simulator OK-MVP cục bộ; rule engine UI vẫn Fail.

#### A6. `segment`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Card hiện default process/SLA — tốt hơn field dump. Không preview gate khi gán segment lên Opp. |
| Mkt | 5 | 5 | Xương journey — UI vẫn list card, không funnel members. |
| Ops | 3 | 3 | SLA không hiện runtime trên Opp path. |
**Verdict: Weak.**

#### A7. `sales-process` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Stage rail + bindings Payment/Checklist/HoldHours — **đúng câu chuyện**. Rail không kéo-thả, không thêm/xóa stage, Activate không đổi trạng thái bền. |
| Mkt | 4 | 3 | Segment name hiển thị; không thấy process nào apply segment nào trên list. |
| Ops | 4 | 4 | HoldHours chìm trong bind text. |
**Verdict: Weak (critical setup vẫn chưa “designer”).** Cần process designer thật, không poster rail.

#### A8. `checklist-template` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Detail = **1 item** + gate preview — **không** board theo stage như đã hứa P0. List vẫn hàng item. |
| Mkt | 2 | 2 | — |
| Ops | 4 | 5 | Required chip có; thiếu group Role × Stage. |
**Verdict: Fail.** Đây là setup gate — phải nhìn được **cả set theo stage**, drag sort, bulk required.

#### A9. `payment-rule` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Milestone cards + Gate chip — đọc được hơn bảng. Không timeline ngang, không validate tổng Min%, không edit inline. |
| Mkt | 1 | 1 | — |
| Ops | 5 | 5 | BEOLock nhìn được trên card; runtime vẫn phải qua form khác. |
**Verdict: Weak.** Gần OK nội dung; UX vẫn “stack card”, chưa rule designer.

#### A10. `kpi-config`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 3 | Enable/Disable card — admin tạm. Leader không dùng hàng ngày. |
| Mkt | 4 | 4 | Board chip có; thiếu seed funnel metrics. |
| Ops | 3 | 3 | — |
**Verdict: Weak.** Chấp nhận admin MVP nếu `kpi-board` đủ mạnh (hiện không).

---

### B. PIPELINE

#### B1. `lead` (list + detail có sẵn)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | **Datatable cũ.** Không next touch, không Convert→Opp, không wedding fields nổi. |
| Mkt | 4 | 4 | Campaign field có sẵn hệ thống nhưng không journey / attribution widget. |
| Ops | 1 | 1 | — |
**Verdict: Fail.** Đầu phễu vẫn “CRM generic” — lệch hoàn toàn tone wedding workspace.

#### B2. `opportunity` (list + detail) — màn dày nhất
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 7 | 7 | **List kanban + health + next** = đúng việc AE. Detail: hero, path, checklist gate, commercial, payment, BEO, next steps — **đủ khung 360**. Vẫn: path không sticky; payment/BEO dưới fold; activity không composer; Move stage/mock; Fields tab thô; không related hover/density SF. |
| Mkt | 5 | 5 | Chip Source/Campaign/Segment có — **không** funnel ngược về campaign. |
| Ops | 5 | 5 | Ops strip mỏng; Lock/gate chỉ text + link BEO. |
**Verdict: OK-MVP (duy nhất gần đạt).** Không phải Good. Confirm G3 *chỉ nhờ Opp* là **không công bằng** với 24 form còn lại.

#### B3. `activity`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Today/Overdue filter + Complete + Regarding link — **đúng hướng inbox**. Không tạo activity inline, không calendar, không sync về Opp timeline tự refresh. |
| Mkt | 3 | 3 | AI touch không vào queue này. |
| Ops | 3 | 3 | — |
**Verdict: Weak.**

#### B4. `tour-booking`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Card Result + Impact text — **Impact chỉ chữ**, không tick checklist/stage Opp. |
| Mkt | 4 | 4 | Show/NoShow là metric — không capture → KPI. |
| Ops | 3 | 3 | Không check conflict hall. |
**Verdict: Fail.** Tour không đẩy trạng thái = tour vô dụng với pipeline.

#### B5. `sale-quotation` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Hero + lines + Send/Hold/Contract — **trông như quote workspace**. Lines read-only mock; Send PDF không PDF; version compare không có; peak chỉ label. |
| Mkt | 2 | 2 | — |
| Ops | 3 | 3 | Package lines không đẩy BEO. |
**Verdict: Fail (critical sell).** Poster quote ≠ báo giá làm việc.

#### B6. `event-hold`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Countdown + Conflict trên card — tốt. Extend/Release trên detail? Chủ yếu xem. |
| Mkt | 1 | 1 | — |
| Ops | 5 | 5 | Conflict text; calendar vẫn tách — chưa panel xung đột thật. |
**Verdict: Weak.**

#### B7. `hall-calendar`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 6 | Grid ngày + status + click hold — **thực dụng**. Không week/month thật, không filter team, UI thô hơn Opp. |
| Mkt | 2 | 2 | — |
| Ops | 6 | 6 | Booked→BEO deep-link cần rõ trên cell. |
**Verdict: OK-MVP.**

---

### C. CONTRACT / PAYMENT / OPS

#### C1. `contract` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 6 | 6 | List PayPct bar tốt. Detail sign path + payment — khá. Thiếu phụ lục, dual-sign, link BEO/Attendance. |
| Mkt | 2 | 2 | — |
| Ops | 4 | 4 | Không cầu nối ngày tiệc / attendance. |
**Verdict: Weak → sát OK list; detail chưa Good.**

#### C2. `contract-payment` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Insight Due + BEOLock + card màu — **console nhẹ**. Không Record payment modal, không group theo HĐ, không ledger. |
| Mkt | 1 | 1 | — |
| Ops | 5 | 5 | Gate alert có chữ; chưa chặn Lock BEO thật. |
**Verdict: Weak.** Gần P0; chưa phải payment console.

#### C3. `beo` (+ detail)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | List Lock chip tốt. Detail section grid + Lock D-7 — **đúng hướng ops**. Section body text giả; không change-request, không vendor window, không version diff. |
| Mkt | 1 | 1 | — |
| Ops | 6 | 6 | Màn Ops mạnh nhất sau calendar; vẫn thiếu checklist sản xuất theo giờ. |
**Verdict: Weak / sát OK-MVP detail.**

#### C4. `attendance-booking`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Form ops **cũ**, không strip Opp/Contract/Hall wedding. |
| Mkt | 2 | 2 | — |
| Ops | 6 | 6 | Có giá trị F&B sẵn; **đứt khỏi deal**. |
**Verdict: Fail (gap tích hợp).** Không phải Fail nghiệp vụ attendance — Fail **mối nối wedding**.

---

### D. AI / MKT / KPI / MASTER

#### D1. `ai-inbox`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 5 | 5 | Split draft + Approve/Reject — đúng pattern. State không bền; Regarding hardlink Opp 1001; không queue SLA. |
| Mkt | 5 | 5 | Confidence hiện; thiếu channel filter, A/B copy, assign. |
| Ops | 1 | 1 | — |
**Verdict: Weak.** Pattern OK; độ tin cậy demo thấp.

#### D2. `campaign`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 3 | 3 | Datatable cũ — không members→tour→signed. |
| Mkt | 3 | 3 | **Fail Mkt nặng:** không funnel wedding. |
| Ops | 1 | 1 | — |
**Verdict: Fail.**

#### D3. `customer` (business-partner)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | BP generic — thiếu Bride/Groom/Planner, related Opp. |
| Mkt | 4 | 3 | — |
| Ops | 3 | 3 | — |
**Verdict: Weak (reuse chưa gắn wedding).**

#### D4. `kpi-board`
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 4 | 4 | Widget grid mock Q3 — nhìn “dashboard” giả. Không filter period/team thật, không drill. |
| Mkt | 4 | 4 | — |
| Ops | 3 | 3 | — |
**Verdict: Fail.** Card số ≠ board điều hành.

---

## 4. Ma trận tổng (điểm trung bình 3 role · **sau G3.2**)

| # | Form | UI | Dụng | Verdict vòng 2 (doc 08) | Verdict vòng 3 (nay) | Delta |
|---|------|----|------|-------------------------|----------------------|-------|
| 1 | sale-team | 3 | 3 | Fail | **Weak** | ↑ skin |
| 2 | sale-quota | 3 | 3 | Fail | **Weak** | ↑ skin |
| 3 | event-hall | 4 | 4 | Weak | **Weak** | ≈ |
| 4 | event-package | 4 | 4 | Fail | **Fail** | skin ≠ edit |
| 5 | price-book | 4 | 4 | Fail | **Weak** | ↑ simulator |
| 6 | segment | 4 | 4 | Weak | **Weak** | ≈ |
| 7 | sales-process | 4 | 4 | Fail | **Weak** | ↑ poster rail |
| 8 | checklist-template | 3 | 4 | Weak | **Fail** | xuống — sai hình dạng |
| 9 | payment-rule | 4 | 4 | Fail | **Weak** | ↑ cards |
| 10 | kpi-config | 4 | 3 | Weak | **Weak** | ≈ |
| 11 | lead | 3 | 3 | Weak | **Fail** | xuống — bỏ quên |
| 12 | opportunity | 6 | 6 | OK-MVP | **OK-MVP** | ≈ (vẫn chưa Good) |
| 13 | activity | 4 | 4 | Fail | **Weak** | ↑ inbox |
| 14 | tour-booking | 4 | 4 | Fail | **Fail** | impact giả |
| 15 | sale-quotation | 5 | 5 | Fail | **Fail** | skin ≠ quote |
| 16 | event-hold | 4 | 4 | Weak | **Weak** | ≈ |
| 17 | hall-calendar | 6 | 6 | OK-MVP | **OK-MVP** | ≈ |
| 18 | contract | 5 | 5 | Weak | **Weak** | ↑ list bar |
| 19 | contract-payment | 4 | 4 | Fail | **Weak** | ↑ console nhẹ |
| 20 | beo | 5 | 5 | Weak | **Weak** | ↑ |
| 21 | attendance-booking | 4 | 4 | Weak | **Fail** | xuống — đứt FK |
| 22 | ai-inbox | 5 | 5 | Fail | **Weak** | ↑ split |
| 23 | campaign | 3 | 3 | Weak | **Fail** | xuống — bỏ quên |
| 24 | customer | 4 | 4 | Weak | **Weak** | ≈ |
| 25 | kpi-board | 4 | 4 | Fail | **Fail** | số mock |

**Tóm tắt delta:** G3.2 **kéo ~8 form Fail→Weak** bằng skin + mock interaction. **Không tạo thêm Good.** Một số form **tụt** vì lộ ra là bỏ quên (`lead`, `campaign`, `attendance`) hoặc làm sai hình (`checklist-template` detail 1 item).

---

## 5. Phản biện theo ROLE (tổng hợp ngang)

### 5.1 Sale (AE / Leader)
- **Làm được gần đúng:** pipeline board Opp, mở 1 deal thấy path/checklist/money skeleton, calendar giữ chỗ.
- **Vẫn bó tay hàng ngày:** soạn quote, convert lead, ghi nhận tour→stage, thu cọc, coaching quota theo AE.
- **Cảm giác UI:** “nhiều card giống nhau”, thiếu density Lightning (compact highlight, related lists, inline edit).
- **Chấm Sale tổng:** UI **4.5/10** · Thực dụng **4/10**.

### 5.2 Marketing
- **Gần như không có nhà:** `campaign`/`lead` CRUD cũ; Opp chỉ chip attribution; AI inbox chưa phải queue campaign.
- **Không trả lời được:** campaign X → bao nhiêu tour show → bao nhiêu signed.
- **Chấm Mkt tổng:** UI **3/10** · Thực dụng **2.5/10**.

### 5.3 Operator
- **Có điểm tựa:** BEO detail, hall-calendar, payment gate chữ, attendance form cũ (lệch ngữ cảnh).
- **Thiếu:** change-request BEO, conflict thật, attendance gắn HĐ/Opp, print/kitchen tin được.
- **Chấm Ops tổng:** UI **4.5/10** · Thực dụng **4.5/10**.

---

## 6. Backlog tổng hợp G3.3 (làm thật, không skin thêm)

### Nguyên tắc chốt
1. **Một form = một quyết định.** Nếu CTA không đổi state object → cấm ship trong demo Confirm.
2. **Shared design tokens** — gom `.crm-ws` vào 1 partial; densify; bỏ copy 36 SCSS.
3. **Opp là hub** — form vệ tinh phải *ghi ngược* Opp (không chỉ link tới).
4. **Không Confirm G3** khi còn `Fail` ở P0 critical: quote, checklist-template, tour impact, lead convert, payment record, campaign funnel.

### P0 — critical path bán tiệc (bắt buộc trước Confirm)
| # | Form | Việc cụ thể (DoD) |
|---|------|-------------------|
| 1 | `sale-quotation` | Inline edit lines · peak apply · version compare · CTA tạo Hold/Contract **tạo record mock bền** |
| 2 | `checklist-template` | Board theo Stage (không detail 1 dòng) · drag sort · Required toggle · preview gate trên process |
| 3 | `tour-booking` | Result Show/NoShow/Cancel → tick checklist + optional stage suggestion trên Opp |
| 4 | `contract-payment` | Group theo HĐ · **Record payment** đổi Paid/Due · cập nhật % trên Opp/Contract |
| 5 | `lead` | Highlight + Next touch + **Convert→Opp** wizard (segment/process) |
| 6 | `opportunity` | Sticky bar Payment% + BEO lock · activity composer · Move stage chỉ khi Required Done (state bền) |
| 7 | `sales-process` | Add/reorder stage · bind picker thật · Activate đổi IsActive trên list |
| 8 | `campaign` | Funnel strip Lead→Tour→Signed · bắt buộc gắn lead source |

### P1 — hoàn thiện vận hành
- `event-package` line editor + clone version  
- `payment-rule` timeline + validate tổng %  
- `sale-team` / `sale-quota` drill filter pipeline  
- `event-hold` Extend/Release + conflict panel  
- `beo` change-request + version diff  
- `attendance-booking` strip FK Opp/Contract/Hall  
- `ai-inbox` queue filter + state bền + regarding đúng object  
- `kpi-board` filter period/team + drill  
- `customer` roles Bride/Groom + related Opp  
- `hall-calendar` week header + team filter  

### P2 / không làm trong G3
- Floor plan, multi-sign Approval, Zalo OA sâu, PDF engine thật (stub có chủ đích).

---

## 7. Definition of Done — Confirm G3 (siết)

Sponsor mở **toàn bộ 25 form**. Với mỗi form P0 ở §6:

> *“Trên màn này tôi đang **quyết định / thay đổi** gì?”*  
> Nếu câu trả lời là “xem card / điền field / bấm link sang chỗ khác” → **chưa Confirm**.

Checklist nhanh:
- [ ] Quote soạn line được và thấy peak  
- [ ] Tour Show làm checklist Opp đổi  
- [ ] Record 1 payment → % Opp/Contract đổi  
- [ ] Lead Convert tạo Opp nằm đúng stage  
- [ ] Campaign thấy funnel số  
- [ ] Checklist template nhìn được cả set theo stage  
- [ ] Opp sticky thấy cọc + BEO không cần scroll hết trang  

```
Gate note: G3 CHƯA Confirm — vòng 3 phản biện lại toàn forms
Trạng thái: Fail tổng thể (OK-MVP chỉ opportunity + hall-calendar)
Next: G3.3 theo backlog §6 — làm state thật, không skin thêm
```
