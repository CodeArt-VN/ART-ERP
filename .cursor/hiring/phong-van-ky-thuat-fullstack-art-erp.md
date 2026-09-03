# Bộ câu hỏi phỏng vấn — Fullstack Developer ART-ERP (FE-first + AI BE)

**Mục đích:** Screen **Fullstack** theo đặc trưng team: FE là trọng tâm; BE do Cursor AI + anh; ứng viên ship UI + gắn API + UAT.  
**Thời lượng:** 60–75 phút (+ take-home 2–3 giờ).  
**Đi kèm:** `jd-fullstack-developer-art-erp.md`

---

## 0. Định nghĩa “pass fullstack” ở vị trí này

| Kỳ vọng | Có | Không |
|---------|----|-------|
| Angular/Ionic production | Bắt buộc | — |
| Gắn REST, xử lý lỗi nghiệp vụ trên UI | Bắt buộc | — |
| Làm việc với API AI gen | Bắt buộc | — |
| Viết C# / ASP.NET / EF hàng ngày | — | Không yêu cầu |
| ART-DMS / .NET 4.x | — | Không hỏi sâu |

---

## 1. Cấu trúc buổi

| Phần | Thời gian | Nội dung |
|------|-----------|----------|
| A. Warm-up | 5' | Giải thích mô hình AI BE; overview CV |
| B. Angular / TS / RxJS | 25' | Core FE |
| C. Ionic + ERP UI | 15' | Form, list, PageBase-style |
| D. Fullstack nhẹ (API + AI) | 15' | Contract, 409, flag, UAT |
| E. Live / take-home | 15–20' | Form + list + mock API |
| F. Q&A | 5' | |

**Pass tổng:** ≥ **70/100**, không fail knockout.

---

## 2. Knockout

| # | Câu hỏi | Pass | Fail |
|---|---------|------|------|
| K1 | Angular production? Version? | Có | Chưa ship |
| K2 | Reactive vs template-driven — khi nào reactive? | Đúng | Không biết |
| K3 | Search box: `switchMap` vs `mergeMap`? | switchMap | Không biết race |
| K4 | API do AI/người khác viết — cách làm việc? | Đọc contract, báo lỗi rõ | Đòi tự viết hết BE hoặc bỏ mặc |

Fail ≥ 2 → no hire Mid (Junior+ chỉ nếu K1–K2 pass + mentor).

---

## 3. Frontend — Angular / TypeScript / RxJS (40 điểm)

**F1.** `ngOnInit` vs `ngAfterViewInit` — load API?  
**F2.** Tránh memory leak subscribe?  
**F3.** `OnPush` — khi nào?  
**F4.** Lazy route — lợi ích ERP nhiều module?  
**F5.** Validator EndTime > StartTime (reactive)?  
**F6.** List 5k row — paging / `trackBy` / virtual scroll?  
**F7.** Interceptor: token + error toast?  
**F8.** DTO: `interface` vs `class`?

*Mid pass:* F1–F5 vững + ≥1 trong F6–F8.

---

## 4. Ionic + UI ERP (25 điểm)

**I1.** `ModalController` / navigation Ionic?  
**I2.** Base page (`PageBase`: `preLoadData`, paging) — lợi ích / kinh nghiệm tương tự?  
**I3.** Ẩn nút theo role?  
**I4.** UX: validation client vs 409 server vs empty state?  
**I5.** `ngx-translate`?

*Pass:* I1 + I3 + I4.

---

## 5. Fullstack nhẹ — API + AI collab (20 điểm)

Đây là phần “fullstack” đúng nghĩa vị trí — **không** phải viết controller .NET.

**A1.** `POST /holds` → 409 Conflict (trùng sảnh) — FE xử lý UX thế nào?  
**A2.** API thiếu field form cần — bước tiếp theo (không hardcode bẩn)?  
**A3.** Feature flag `CRM.HallHold=false` — FE làm gì?  
**A4.** Anh verify P0 trên staging: FE test gì vs nhờ AI/anh check BE?  
**A5.** (Optional) Nhìn JSON response → viết TypeScript interface trong 2 phút.

**A6. Culture check:** “BE hầu hết AI gen — anh/chị thấy rủi ro gì và tự bảo vệ thế nào ở FE?”  
*Pass:* nói được validation phía client, không trust response mù, escalate contract.

*Pass phần D:* A1 + A2 + A6 chấp nhận được.

---

## 6. Nghiệp vụ nhẹ (gộp vào communication)

**N1.** Lead → Opp → Quote → Hold → Contract — **màn hình** chính nào?  
**N2.** Hold sắp hết hạn — UX trên list?

---

## 7. Thực hành

### Take-home 2–3h (khuyến nghị)

**Event Hold (mock API)** — chứng minh fullstack FE-first:

- List + filter  
- Form tạo hold (reactive, End > Start)  
- Mock 409 → message rõ  
- README `ng serve`  
- (Plus) file `API-NOTES.md`: 2–3 chỗ anh/chị sẽ hỏi lại BE/AI nếu API thật thiếu

| Tiêu chí | Điểm |
|----------|------|
| List + filter | 20 |
| Form + validator | 25 |
| UX 409 | 20 |
| Code TS sạch | 20 |
| API-NOTES / README | 15 |

### Live 15'

Reactive form + validator End > Start.

### Review 10'

```typescript
this.items.forEach(id => {
  this.http.get('/api/opportunity/' + id).subscribe(r => this.rows.push(r));
});
```

Bug? (N+1, race, leak) — sửa?

---

## 8. Rubric (100)

| Hạng mục | Trọng số | Mid pass |
|----------|----------|----------|
| Angular / TS / RxJS | 40 | ≥ 28 |
| Ionic / ERP UI | 25 | ≥ 15 |
| API + AI fullstack collab | 20 | ≥ 14 |
| Communication / domain nhẹ | 15 | ≥ 10 |

| Điểm | Offer |
|------|-------|
| 85–100 | Mid–Senior Fullstack (FE-first) |
| 70–84 | Mid Fullstack (**target**) |
| 55–69 | Junior+ + mentor |
| < 55 | No hire |

**Cấm:** trừ điểm vì “không biết .NET / EF6 / DMS”.

---

## 9. Red / green flags

**Red:** Angular yếu; từ chối mô hình AI BE; expect code C# full-time; coi thường UAT.  
**Green:** Ionic/admin form-heavy; đã gắn API người khác viết; hỏi PageBase/gate G3; feedback API cụ thể.

---

## 10. Biên bản

```
Ứng viên:
Ngày:
Người PV:

Knockout: K1[ ] K2[ ] K3[ ] K4[ ]
Angular (/40):
Ionic-ERP (/25):
API-AI fullstack (/20):
Communication (/15):
Tổng (/100):

Take-home: [link] __

Quyết định:
[ ] Offer Mid Fullstack (FE-first + AI BE)
[ ] Offer Junior+ (mentor)
[ ] Hold / No hire

Ghi chú (có chấp nhận mô hình AI BE không?):
```

---

## 11. Map JD ↔ câu hỏi

| JD | Câu hỏi |
|----|---------|
| Angular production | K1, F1–F8 |
| Reactive forms | K2, F5, take-home |
| RxJS | K3, F2 |
| Ionic / PageBase | I1–I2 |
| Fullstack AI API | K4, A1–A6 |
| UAT / UX | A1, N1–N2 |
| Không yêu cầu .NET 4.x | — (không hỏi) |

---

## 12. Ghi chú screening CV

- CV “.NET mạnh, FE basic” → **không** fit đặc trưng vị trí này.  
- CV “Angular mạnh, từng gắn API, ít/không .NET” → **đúng profile**.  
- Title trên JD vẫn là **Fullstack Developer**; nội dung PV phản ánh FE-first + AI BE.

---

*Thay thế bộ PV fullstack kiểu .NET Framework/DMS trước đây.*
