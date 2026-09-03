# Job Description — Fullstack Developer (ART-ERP)

**Công ty / dự án:** CodeArt — ART-ERP  
**Vị trí:** Fullstack Developer  
**Hình thức:** [Full-time / Hybrid / Remote — điền theo thực tế]  
**Cấp bậc:** Mid (ưu tiên) · Junior+ có mentor (xem xét)  
**Báo cáo:** Sponsor / PM module  
**Cập nhật:** 2026-03-03  

**Đặc trưng vị trí (quan trọng):**  
Đây là fullstack theo mô hình **FE-first + AI-assisted BE** — không phải fullstack .NET truyền thống.

| Phần | Ai làm | Vai trò ứng viên |
|------|--------|------------------|
| **Frontend** (~85–90%) | Người | Angular/Ionic production, prototype → UAT |
| **Backend** (~10–15%) | Cursor AI + anh | Ứng viên **đọc/gắn API**, feedback contract; **không** viết BE hàng ngày |
| Legacy `ART-DMS` / .NET 4.x | Đang thay thế | **Không** yêu cầu |

---

## 1. Giới thiệu dự án

ART-ERP — ERP đa module (CRM, SALE, POS, Kế toán, WMS, HRM, Approval…), mở rộng trên codebase production:

| Repo | Vai trò |
|------|---------|
| `ART-ERP-FE` | Frontend chính — Angular + Ionic + Capacitor (**trọng tâm job**) |
| `ART-ERP-BE` | Backend mới ASP.NET Core — **AI gen**, người review/gắn |
| `ART-DMS` | Backend legacy — đang bỏ; không phải skill tuyển |
| `ART-ERP-MCP` | AI / automation |

**Cách team ship module:**

1. Anh confirm nghiệp vụ / forms (G1–G2)  
2. Ứng viên prototype FE (G3)  
3. AI gen BE theo form/TC đã chốt; ứng viên gắn API + bắt lỗi UI/nghiệp vụ (G4)  
4. UAT với anh (G5) → go-live theo lệnh anh (G6)

---

## 2. Mục tiêu tuyển dụng

Tuyển **1 Fullstack Mid** đủ năng lực FE để ship màn hình ERP, đồng thời làm việc thành thạo với API do AI sinh — **end-to-end ownership phía sản phẩm** (UI + contract + UAT), không cần hire thêm BE dev.

**Không** tìm người code C#/.NET Framework full-time.  
**Có** tìm người chịu trách nhiệm “màn hình chạy được với API thật” và escalate BE đúng cách.

---

## 3. Trách nhiệm chính

### A. Frontend (trọng tâm)

- Màn Angular + Ionic theo pattern `PageBase` (list, detail, tree, form phức tạp).
- Prototype mock (G3) → production gắn API (G4).
- Reactive forms, validation cross-field, role/permission, `ngx-translate`.
- Paging server, `trackBy`, virtual scroll khi list lớn.
- Capacitor / mobile layout khi module cần.
- SignalR hoặc push phía client khi có yêu cầu.

### B. Fullstack với AI-assisted BE (bắt buộc, nhẹ về code)

- Đọc API contract (OpenAPI / JSON) do AI gen; map TypeScript model.
- Xử lý status/UX: 400 validation, **409 Conflict** (vd. double-book hold), 401/403.
- Feedback BE cụ thể (thiếu field, sai status, thiếu filter) để AI/anh sửa — **không** im lặng workaround bẩn.
- Viết test FE cho validator / flow quan trọng; hỗ trợ verify API P0 trên staging (Postman/curl/HTTP client — đủ mức dùng).
- Hiểu feature flag: ẩn menu FE khi flag off; không gọi API chết.

### C. Không thuộc scope hàng ngày

- Viết/maintain controller C#, EF, migration DB production.
- Làm việc chuyên sâu `ART-DMS` / .NET Framework 4.x.

---

## 4. Must-have

### Kinh nghiệm

- **≥ 2 năm** Angular production (hoặc 1.5 năm + app form-heavy/ERP).
- Đã ship sản phẩm có **cả UI và tích hợp API** (fullstack theo nghĩa sản phẩm — không bắt buộc tự viết mọi API).

### Kỹ năng

| Kỹ năng | Mức |
|---------|-----|
| **Angular** 15+ (ưu tiên 17–20) | Thành thạo |
| **TypeScript** + RxJS | `switchMap`, unsubscribe / async pipe |
| **Reactive Forms** | Cross-field validation |
| HTML/SCSS | Form/list enterprise, responsive |
| REST từ FE | Interceptor, error, loading |
| Làm việc với API có sẵn / AI gen | Đọc contract, báo lỗi rõ |
| Git | Branch, PR |

### Soft

- Chấp nhận mô hình **AI viết BE, người ship FE + UAT**.  
- Tiếng Việt tốt; đọc doc Angular tiếng Anh.

---

## 5. Strong plus

- **Ionic** 7/8.  
- ERP / CRM / admin multi-role.  
- Pattern base page (`preLoadData`, paging…).  
- Đã dùng Cursor/Copilot — review code/API AI gen.  
- Biết đọc sơ ASP.NET Core / JSON schema (không cần code C#).  
- SignalR client, Capacitor, `ngx-translate`.

---

## 6. Nice to have

- Viết được snippet API đơn giản (bất kỳ stack) khi AI blocker — **không** phải .NET 4.x.  
- Jasmine/Karma, CI chạy FE.  
- FullCalendar, gridster.

---

## 7. Không phù hợp nếu

- FE chỉ HTML/JS basic, chưa Angular production.  
- Chỉ React/Vue, chưa Angular (ramp dài — không ưu tiên).  
- Chỉ muốn làm BE .NET; từ chối gắn API người/AI khác viết.  
- Expect fullstack = 50% C# + 50% Angular trên ART-DMS.  
- Không chấp nhận gate confirm (G1–G3 trước code production).

---

## 8. Tech stack

```
FE (core):   Angular 20 · Ionic 8 · TypeScript 5.8 · Capacitor · RxJS · ngx-translate · SignalR
BE (AI):     ART-ERP-BE — ASP.NET Core — ứng viên consume + feedback
Legacy:      ART-DMS — đang thay thế — không yêu cầu
Process:     Gate G1–G6 · Feature flag · Git submodule ART-ERP-FE
```

---

## 9. Screening CV 5 phút

| Tiêu chí | Pass | Fail |
|----------|------|------|
| Angular production | Có version + project | Không / chỉ tutorial |
| UI + gọi API thật | Có | Chỉ UI tĩnh / chỉ BE |
| Form phức tạp / admin | Có | Chỉ landing |
| Ionic | Plus | Không bắt buộc nếu Angular mạnh |
| .NET / C# sâu | **Không cần** | Đừng loại vì thiếu |
| “Fullstack” trên CV nhưng FE basic | Cân nhắc kỹ | Thường **fail** vị trí này |

**Thumb rule:** Angular yếu → loại. Thiếu .NET → vẫn pass.

---

## 10. Quy trình tuyển

1. Screen CV (mục 9).  
2. PV kỹ thuật — `phong-van-ky-thuat-fullstack-art-erp.md` (FE nặng + API/AI).  
3. Take-home: list + form + xử lý 409 (mock API).  
4. Culture: làm việc với AI BE, UAT với anh.  
5. Offer Mid Fullstack (FE-first) hoặc Junior+ + mentor.

---

## 11. Level (placeholder lương)

| Level | Điều kiện |
|-------|-----------|
| Junior+ | Angular 1–2 năm, form cơ bản | Mentor pattern ART |
| **Mid** | Angular 2–4 năm, ship UI+API | **Target** |
| Senior FE-leaning | Lead UI ERP + review AI output | Ít cần |

---

## 12. Quyền lợi (placeholder)

- [Lương / thưởng / BHXH] · [Hybrid/remote] · [Laptop]

---

## 13. Ứng tuyển

**[email HR]** — `[ART-ERP] Fullstack Developer — Họ tên`

Trả lời ngắn kèm CV:

1. Angular version production? Có Ionic không?  
2. Project nào anh/chị **tự gắn UI với API** (kể cả API người khác viết)?  
3. Sẵn sàng mô hình AI gen BE + người ship FE/UAT không?

---

*Nội bộ — Fullstack FE-first, AI-assisted BE. Không tuyển .NET Framework/DMS.*
