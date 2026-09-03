# Bộ câu hỏi phỏng vấn kỹ thuật — Fullstack ART-ERP

**Mục đích:** Screen ứng viên fullstack cho ART-ERP (Angular/Ionic + .NET + SQL).  
**Thời lượng:** 60–90 phút (+ 2–4 giờ take-home nếu cần).  
**Người phỏng vấn:** Tech Lead + (optional) PM.  
**Đi kèm:** `jd-fullstack-developer-art-erp.md`

---

## 1. Cấu trúc buổi phỏng vấn

| Phần | Thời gian | Nội dung |
|------|-----------|----------|
| A. Warm-up | 5 phút | Giới thiệu dự án ART-ERP, hỏi overview CV |
| B. Backend | 25 phút | C#, Web API, EF, SQL, legacy |
| C. Frontend | 25 phút | Angular, Ionic, TypeScript, form ERP |
| D. Fullstack / nghiệp vụ | 15 phút | API↔UI, CRM scenario, feature flag |
| E. Thực hành ngắn | 15–20 phút | Live coding hoặc review đoạn code ART |
| F. Q&A | 5 phút | Ứng viên hỏi lại |

**Pass tổng thể:** ≥ **70/100** và **không fail** mục knockout (mục 2).

---

## 2. Câu hỏi knockout (Fail ngay nếu trả lời sai cơ bản)

| # | Câu hỏi | Pass | Fail |
|---|---------|------|------|
| K1 | Anh/chị đã deploy Angular app lên môi trường thật chưa? Version? | Có, nêu được version & build | Chưa từng / chỉ học tutorial |
| K2 | REST API anh/chị thiết kế: GET list có phân trang/filter không? Làm thế nào? | Query params / body filter, paging | Không biết paging |
| K3 | SQL: transaction dùng khi nào? Ví dụ nghiệp vụ cần transaction. | Chuyển tiền, booking, order+c payment | Không biết ACID |
| K4 | Angular: difference giữa `template-driven` và `reactive` form? Khi nào dùng reactive? | Form phức tạp, validation động → reactive | Không phân biệt được |

> **Lưu ý:** Fail ≥ 2 câu knockout → **không** offer fullstack; có thể chuyển track BE nếu phần B rất mạnh.

---

## 3. Backend (.NET + SQL)

### 3.1 C# & ASP.NET Web API

**B1.** Middleware pipeline ASP.NET Core khác gì `HttpModule`/`Global.asax` .NET Framework?  
- *Pass:* Biết ít nhất authentication, routing, exception handling nằm ở đâu.  
- *Strong:* Đã maintain cả Framework 4.x lẫn Core.

**B2.** `[Authorize]` + JWT: flow từ login đến gọi API protected? Refresh token có không?  
- *Pass:* Login → token → header `Authorization: Bearer` → validate claims.  
- *Red flag:* Lưu password plain text; token không expiry.

**B3.** Dependency Injection: register `Scoped` vs `Singleton` vs `Transient` — ví dụ cho `DbContext` và service nghiệp vụ.  
- *Pass:* DbContext thường Scoped; Singleton cẩn thận state.

**B4.** Làm sao version API mà không breaking mobile app cũ?  
- *Pass:* URL versioning, header, additive fields, feature flag.

**B5.** (ART-DMS context) Controller trả về `IHttpActionResult` / custom wrapper `{ data, error }` — ưu/nhược?  
- *Pass:* Consistent envelope giúp FE; cần HTTP status đúng chuẩn.

### 3.2 Entity Framework & database

**B6.** EF6 `DbContext` vs EF Core — khác biệt anh/chị từng gặp?  
- *Pass:* Biết EF6 gắn .NET Framework; migration khác; lazy loading.

**B7.** N+1 query là gì? Cách phát hiện và fix?  
- *Pass:* Include/Eager loading, projection Select, log SQL.

**B8.** Thêm cột mới bảng production 10M rows — anh/chị làm gì?  
- *Pass:* Additive nullable/default, index online, deploy off-peak, không drop/rename bừa.

**B9.** Stored procedure vs LINQ — khi nào chọn SP?  
- *Pass:* Báo cáo nặng, batch, tái sử dụng DBA tuning.

**B10.** Scenario ART-ERP: **double-book sảnh tiệc cưới** — thiết kế DB + API chống trùng.  
- *Pass:* Unique constraint (hall_id, event_date, slot) hoặc serializable transaction / row lock; check hold trước confirm.  
- *Strong:* Optimistic concurrency token, queue hold TTL 48h.

### 3.3 Legacy & production

**B11.** Kể incident production: RCA và fix — ví dụ thật.  
- *Listen:* Log, reproduce, root cause không đổ lỗi, rollback plan.

**B12.** Refactor controller 2000 dòng — bước đầu tiên?  
- *Pass:* Test cover critical path, extract service, không big bang.

---

## 4. Frontend (Angular + Ionic + TypeScript)

### 4.1 Angular core

**F1.** Lifecycle hook: `ngOnInit` vs `ngAfterViewInit` — load data API nên đặt đâu?  
- *Pass:* Init data thường `ngOnInit`; DOM/view child `AfterViewInit`.

**F2.** RxJS: `switchMap` vs `mergeMap` khi user gõ search box?  
- *Pass:* `switchMap` hủy request cũ — tránh race.

**F3.** Change detection: default vs `OnPush` — khi nào dùng OnPush?  
- *Pass:* Input immutable, performance list lớn.

**F4.** Lazy loading module routing — lợi ích trên app ERP nhiều module?  
- *Pass:* Giảm bundle initial, load CRM/SALE khi cần.

**F5.** Reactive form: validate số khách ≥ sức chứa sảnh, cross-field validation?  
- *Pass:* Validator function / `updateValueAndValidity`, error hiển thị template.

### 4.2 Ionic & UI ERP

**F6.** Ionic page vs Angular component — `NavController` dùng khi nào?  
- *Pass:* Mobile navigation stack; modal `ModalController`.

**F7.** (ART pattern) Page kế thừa base class chung (`PageBase`): lợi ích?  
- *Pass:* DRY list/detail, paging, sort, permission; *Strong:* đọc được `preLoadData`, `loadedData`.

**F8.** List 5000 dòng CRM Lead — render performance?  
- *Pass:* Virtual scroll, server paging, trackBy.

**F9.** `ngx-translate`: đổi ngôn ngữ runtime, load file JSON thế nào?  
- *Pass:* TranslateService, HttpLoader hoặc custom loader.

**F10.** Gọi API có loading + error toast — implement outline (interceptor hay service)?  
- *Pass:* HTTP interceptor global loading; catchError map message.

### 4.3 TypeScript & tooling

**F11.** `interface` vs `class` cho model API response?  
- *Pass:* Interface cho DTO; class nếu cần method/transform.

**F12.** Strict null check: optional chaining `?.` — ví dụ nested CRM contact.

---

## 5. Fullstack & nghiệp vụ ART-ERP

**FS1.** Mô tả flow: **Lead → Opportunity → Quotation → Hold → Contract → Deposit** — anh/chị thiết kế màn hình và API?  
- *Listen:* Entity relationship, status machine, ai được chuyển stage.

**FS2.** Feature flag `CRM.HallHold` off trên prod — dev test thế nào?  
- *Pass:* Staging bật, config per tenant, không hardcode.

**FS3.** BE trả lỗi 409 Conflict (hold trùng) — FE hiển thị và xử lý UX?  
- *Pass:* Message rõ, suggest slot khác, không crash form.

**FS4.** Unit test vs API test vs E2E — TC double-book test ở tầng nào?  
- *Pass:* Unit logic conflict; API integration 2 concurrent hold; E2E optional UAT.

**FS5.** Submodule Git: sửa FE và BE cùng feature — quy trình commit?  
- *Pass:* Branch feature, commit từng submodule, parent repo pointer update.

**FS6.** SignalR: notify sales khi có hold sắp hết hạn — kiến trúc?  
- *Pass:* Hub server push; FE subscribe; fallback polling.

---

## 6. Bài thực hành

### Option A — Take-home (khuyến nghị, 3 giờ)

**Đề:** Mini **Event Hold API + màn list/detail**

**Yêu cầu BE (.NET Core hoặc Framework — ứng viên chọn):**

- Entity: `Hall`, `EventHold` (HallId, EventDate, StartTime, EndTime, Status, ExpiresAt).
- `POST /holds` — tạo hold; reject nếu trùng slot (409).
- `GET /holds?date=&hallId=` — list filter.
- 1 unit test case concurrent double-book.

**Yêu cầu FE (Angular standalone hoặc module):**

- Page list holds + form tạo hold.
- Hiển thị lỗi 409 thân thiện.
- Reactive form validation (End > Start).

**Chấm:**

| Tiêu chí | Điểm |
|----------|------|
| API đúng REST + status code | 20 |
| Chống double-book đúng | 25 |
| FE form + list hoạt động | 25 |
| Test + README chạy được | 15 |
| Code structure, naming | 15 |

### Option B — Live coding (15 phút, không Google)

**Đề ngắn (BE):** Viết C# method `bool IsSlotAvailable(hallId, date, start, end, IEnumerable<existing>)`.

**Đề ngắn (FE):** Viết Angular reactive form 3 field (date, start, end) + custom validator.

### Option C — Code review (15 phút)

Đưa đoạn bug có chủ ý (ART-style):

```typescript
// FE: subscribe không unsubscribe, gọi API trong loop
this.items.forEach(id => {
  this.http.get('/api/opportunity/' + id).subscribe(r => this.rows.push(r));
});
```

```csharp
// BE: check hold không transaction
var exists = db.Holds.Any(h => h.HallId == hallId && h.Date == date);
if (!exists) db.Holds.Add(newHold);
db.SaveChanges();
```

Hỏi: bug gì? sửa thế nào?

---

## 7. Rubric chấm điểm (100)

| Hạng mục | Trọng số | Mid pass |
|----------|----------|----------|
| Backend | 35 | ≥ 25 |
| Frontend | 35 | ≥ 25 |
| Fullstack / domain | 20 | ≥ 12 |
| Communication | 10 | ≥ 7 |

**Thang level:**

| Điểm | Đề xuất |
|------|---------|
| 85–100 | Mid–Senior fullstack |
| 70–84 | Mid fullstack |
| 55–69 | Junior+ BE-heavy hoặc FE-heavy + mentor |
| < 55 | Không hire fullstack |

---

## 8. Câu hỏi theo level ứng viên

### Nếu CV kiểu Võ Thị Mỹ Tiên (BE mạnh, FE basic)

Ưu tiên hỏi sâu B1–B12, F1–F5 cơ bản.  
**Câu then chốt:** “Anh/chị cam kết ramp Angular/Ionic bao lâu? Có side project Angular không?”  
→ Nếu không có kế hoạch học Angular 1–2 tháng → **không** fullstack.

### Mid fullstack target

Phải pass F6–F10 và FS1–FS3.

### Senior

Thêm: thiết kế feature flag rollout, schema migration zero-downtime, mentee review.

---

## 9. Red flags (ghi nhận trong feedback)

- Không biết Angular nhưng apply fullstack.
- Mọi project đều “team làm”, không nêu được phần việc cá nhân.
- Coi thường test / “PM test giúp”.
- Không hỏi gì về nghiệp vụ CRM/ERP.
- Trả lời SQL không transaction cho booking/hold.

---

## 10. Green flags

- Đã làm .NET Framework production + tự học Angular có demo.
- Kể được bug concurrent/race đã fix.
- Hỏi về gate confirm, feature flag, submodule workflow.
- Nhận legacy code là bình thường, không đòi rewrite.

---

## 11. Template biên bản phỏng vấn

```
Ứng viên:
Ngày:
Người PV:

Knockout: K1 [ ] K2 [ ] K3 [ ] K4 [ ]
Backend (/35):
Frontend (/35):
Fullstack (/20):
Communication (/10):
Tổng (/100):

Take-home / live: [Link repo] — điểm: __

Quyết định:
[ ] Offer Mid Fullstack
[ ] Offer Junior+ (mentor FE ___ tháng)
[ ] Offer Backend only
[ ] Hold / No hire

Ghi chú:
```

---

## 12. Đối chiếu nhanh — CV vs bộ câu hỏi

| Hạng mục JD | Câu hỏi tương ứng |
|-------------|-------------------|
| Angular production | K1, F1–F8 |
| .NET Web API | K2, B1–B5 |
| SQL / transaction | K3, B7–B10 |
| Ionic / mobile | F6 |
| ERP CRM flow | FS1, B10 |
| Feature flag | FS2 |
| Legacy .NET FW | B5, B6, B12 |
| Unit test | FS4, Take-home |

---

*Tài liệu nội bộ PM/Tech — cập nhật khi stack ART-ERP nâng version.*
