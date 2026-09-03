# Job Description — Fullstack Developer (ART-ERP)

**Công ty / dự án:** CodeArt — ART-ERP  
**Vị trí:** Fullstack Developer  
**Hình thức:** [Full-time / Hybrid / Remote — điền theo thực tế]  
**Cấp bậc:** Mid (ưu tiên) · Junior+ có mentor (xem xét)  
**Báo cáo:** Tech Lead / PM module  
**Cập nhật:** 2026-03-03

---

## 1. Giới thiệu dự án

ART-ERP là hệ thống ERP doanh nghiệp đa module (CRM, Bán hàng, POS, Kế toán, WMS, HRM, Approval…), đang mở rộng các module mới trên nền codebase production:

| Repo | Vai trò |
|------|---------|
| `ART-ERP-FE` | Frontend Angular + Ionic + Capacitor |
| `ART-DMS` | Backend API chính (.NET Framework, Web API) |
| `ART-ERP-BE` | Backend bổ trợ |
| `ART-ERP-MCP` | Tích hợp AI / automation |

**Đặc điểm làm việc:**

- Mở rộng hệ thống **có sẵn** (không greenfield) — cần đọc hiểu legacy, additive change, feature flag.
- Quy trình theo **gate confirm**: nghiệp vụ → forms → prototype FE → code BE/FE + unit test → UAT → go-live.
- Domain phức tạp: CRM tiệc cưới/nhà hàng, kế toán (SAP B1-inspired), POS event day, approval workflow.

---

## 2. Mục tiêu tuyển dụng

Tuyển dev **làm được cả BE và FE** trong một sprint/module, tự triển khai API + màn hình theo pattern ART, viết unit/API test, và phối hợp PM/UAT — **không** cần mentor full-time cho từng task FE hoặc BE.

---

## 3. Trách nhiệm chính

### Backend

- Phát triển/mở rộng REST API trên `ART-DMS` (C#, ASP.NET Web API, Entity Framework 6).
- Thiết kế schema additive, stored procedure / query tối ưu khi cần.
- Tích hợp module: CRM, SALE, POS, AC (kế toán), APPROVAL, BANK…
- Bật/tắt tính năng qua **feature flag**; đảm bảo backward compatible.
- Viết unit test / API test; hỗ trợ production issue (RCA, hotfix).

### Frontend

- Xây dựng màn hình Angular + Ionic theo pattern `PageBase` (list, detail, tree, form phức tạp).
- Prototype UI (G3) rồi implement production (G4) gắn API thật.
- Xử lý auth, role, validation, i18n (`ngx-translate`), SignalR realtime khi module yêu cầu.
- Đảm bảo responsive / Capacitor-ready nếu module dùng mobile.

### Fullstack / chung

- Đọc hiểu plan nghiệp vụ (flow, forms, test cases) trước khi code.
- Map test case P0 (double-book, hold/deposit, concurrent booking…) sang test tự động.
- Review code đồng nghiệp; commit theo submodule (`ART-ERP-FE`, `ART-DMS`).
- Tham gia UAT demo, sửa lỗi theo feedback sponsor.

---

## 4. Yêu cầu bắt buộc (Must-have)

### Kinh nghiệm

- **Tối thiểu 2 năm** làm web enterprise (hoặc 1.5 năm + project ERP/CRM thực tế phức tạp).
- Đã **ship** ít nhất 1 sản phẩm có cả API và UI do mình làm (không chỉ CRUD demo).

### Backend

| Kỹ năng | Mức yêu cầu |
|---------|-------------|
| C# | Thành thạo |
| ASP.NET Web API hoặc ASP.NET Core Web API | Thành thạo ít nhất một |
| SQL Server (hoặc Oracle/PostgreSQL + sẵn sàng chuyển) | Viết query, index, transaction |
| REST, JWT/OAuth, DI | Đã dùng production |
| Entity Framework (6 hoặc Core) | CRUD + migration/schema change |
| Git | Branch, PR, submodule hoặc monorepo |

### Frontend

| Kỹ năng | Mức yêu cầu |
|---------|-------------|
| **Angular** (v15+) | Component, service, routing, reactive form |
| **TypeScript** | Type-safe, RxJS cơ bản |
| HTML/CSS/SCSS | Layout form/list enterprise |
| Gọi REST API từ FE | Interceptor, error handling |

### Tư duy

- Đọc code người khác, sửa legacy **không phá** hành vi cũ.
- Viết test cho logic nghiệp vụ quan trọng (không chỉ happy path).
- Giao tiếp tiếng Việt tốt; tiếng Anh đọc tài liệu kỹ thuật.

---

## 5. Yêu cầu ưu tiên (Strong plus)

- **Ionic** (v7/v8) — list/detail mobile, modal, popover.
- **.NET Framework 4.x** + EF6 (ART-DMS đang dùng .NET Framework 4.7.2).
- Kinh nghiệm **ERP / CRM / POS / Kế toán** — hiểu flow bán hàng, hợp đồng, cọc, invoice.
- **SignalR**, Firebase push, Capacitor.
- Feature flag, staging/prod rollout, additive DB migration.
- n8n / workflow automation / tích hợp LLM (module AI Sales).
- Đã làm việc với submodule Git hoặc multi-repo.

---

## 6. Nice to have

- SAP Business One hoặc hệ kế toán VN (MISA, Fast…).
- Jasmine/Karma hoặc Jest cho FE; NUnit/xUnit cho BE.
- Docker, CI/CD (GitHub Actions, GitLab CI).
- FullCalendar, gridster, báo cáo/dashboard.

---

## 7. Không phù hợp nếu

- Chỉ có backend .NET, **chưa từng** làm Angular/TypeScript production.
- Chỉ có React/Vue, chưa Angular — cần thời gian ramp-up ≥ 2 tháng (chỉ xem xét nếu BE rất mạnh).
- Chỉ làm CRUD template, chưa gặp form nhiều role / approval / concurrent transaction.
- Không chấp nhận quy trình gate confirm (prototype trước, code sau).

---

## 8. Tech stack tham chiếu (đối chiếu CV)

```
Frontend:  Angular 20 · Ionic 8 · TypeScript 5.8 · Capacitor 8 · RxJS · ngx-translate · SignalR
Backend:   C# · .NET Framework 4.7.2 · ASP.NET Web API · Entity Framework 6 · SQL Server
Mobile:    Capacitor (iOS/Android) · Firebase push
Process:   Feature flag · Unit/API test · Gate G1–G6 · Git submodule
```

---

## 9. Mẫu đánh giá nhanh CV (screening 5 phút)

| Tiêu chí | Pass | Fail |
|----------|------|------|
| Angular + TypeScript production | Có project/job rõ ràng | Chỉ HTML/JS basic |
| C# Web API production | ≥ 1 năm | Chỉ console/winform |
| SQL / DB | Tối ưu query hoặc schema design | Chỉ SELECT đơn giản |
| ERP/enterprise | CRM, booking, accounting, inventory… | Chỉ todo/blog app |
| Legacy / maintain | Refactor, production support | Chỉ project mới 100% |

**Quy tắc thumb:** thiếu **Angular production** → loại khỏi fullstack; chuyển sang track **Backend-only** nếu BE mạnh.

---

## 10. Quy trình tuyển dụng đề xuất

1. **Screen CV** (HR + Tech lead 15 phút) — bảng mục 9.
2. **Phỏng vấn kỹ thuật** (60–90 phút) — xem file `phong-van-ky-thuat-fullstack-art-erp.md`.
3. **Bài thực hành** (optional, 2–4 giờ): mini module CRM Hold hoặc fix bug có sẵn trong repo sandbox.
4. **Vòng culture / PM** (30 phút): làm việc theo gate, ước lượng task, giao tiếp blocker.
5. **Offer** — level Mid hoặc Junior+ kèm mentor 3 tháng.

---

## 11. Mức lương / level (placeholder — PM điền)

| Level | Điều kiện | Ghi chú |
|-------|-----------|---------|
| **Junior+** | 1–2 năm, Angular cơ bản, BE ok | Bắt buộc mentor FE |
| **Mid** | 2–4 năm, Angular + .NET production | Target cho fullstack ART-ERP |
| **Senior** | 4+ năm, ERP domain + lead nhỏ | Review arch, không chỉ code |

---

## 12. Quyền lợi (placeholder)

- [Lương gross / thưởng / BHXH]
- [Hybrid / remote ngày]
- [Laptop / màn hình]
- [Ngân sách học Angular/Ionic nếu Junior+]

---

## 13. Cách ứng tuyển

Gửi email **[email HR]** với tiêu đề: `[ART-ERP] Fullstack Developer — Họ tên`

**Đính kèm:**

1. CV (PDF) — **ghi rõ** project Angular + .NET, vai trò cá nhân, link GitHub nếu có.
2. Trả lời ngắn 3 câu:
   - Module ERP/CRM nào anh/chị đã làm? Vai trò BE hay FE?
   - Angular version đã dùng? Có Ionic không?
   - Có kinh nghiệm .NET Framework (EF6) hay chỉ .NET Core?

---

*Tài liệu nội bộ — đối chiếu stack từ repo `ART-ERP` (submodules FE/DMS) và plan CRM/AC.*
