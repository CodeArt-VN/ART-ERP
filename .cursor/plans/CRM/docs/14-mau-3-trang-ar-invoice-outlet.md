# Chuẩn 3 trang mẫu — phân tích ar-invoice / outlet + đánh giá lại

**Ngày:** 2026-07-24  
**Phạm vi lần này:** chỉ **Sale team · Lead · Opportunity** — anh duyệt rồi mới làm lại toàn bộ.

---

## 1. Phân tích form chuẩn ART-ERP

### 1.1 `ar-invoice` (list)
| Thành phần | Cách làm | Áp vào CRM |
|------------|----------|------------|
| Toolbar | `app-toolbar` + nút icon (Create e-invoice, Sync…) khi select / theo quyền | Toggle list/cards/(kanban) · Add · Convert · Save |
| Title | `app-page-title` — **không** hero marketing | Giữ |
| List | `app-data-table` + `responsive` | Giữ |
| **Cột gom thông tin** | Cột Customer: **tên** + taxid `small` + remark màu warning — 1 cột nhiều dòng | Name = tên + meta (ngày/sảnh/pax hoặc source/next touch) |
| Status | `ion-badge` màu `_Status.Color` | Opp/Lead dùng **status bar** kiểu outlet (tracking đoạn) |

### 1.2 `ar-invoice-detail`
| Thành phần | Cách làm |
|------------|----------|
| Toolbar | Action theo trạng thái (Approve, Create e-invoice) |
| Header | `ion-grid` + `ion-row.hr-group`: cột label trái + `app-form-control` phải |
| Body | `row-full shadow full-screen` + `ion-toolbar primary` + **`ion-segment`** (Items / Other…) |
| Không | Card hero teal, insight KPI, sticky CTA trùng toolbar |

### 1.3 `outlet` (list) — **status bar tracking**
```html
<span class="bar-holder">
  <ion-text class="bar-title" [color]="i.StatusColor">{{i.StatusText}}</ion-text>
  <span class="bar" *ngFor="let s of statusList"
        [ngClass]="{active: s.Code==i.Status}"
        [ngStyle]="{'background-color': 'var(--ion-color-'+s.Color+')'}"
        [title]="s.Name"></span>
</span>
```
- Mỗi thanh nhỏ = 1 bước quy trình; **active** = đang đứng đoạn đó.
- Cột Name gom: tên uppercase + địa chỉ/SĐT `ion-text medium` nhiều dòng.
- Mobile: ẩn cột phụ (`col-saleMan`), không phá layout.

**Kết luận UX:** đây mới là “chuẩn ART” — không phải skin `.crm-ws` G3.2/G3.3.

---

## 2. Đánh giá lại (4 role) — chỉ 3 form mẫu sau khi làm lại

### Sale team
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 7 | 7 | List table + cột gom Name/Leader/Products; detail Members·Products·Quota; CRUD mock. Chưa phân bổ quota sâu trên trang này (tab Quota link) — chấp nhận mẫu. |
| Mkt | 4 | 3 | Ít đụng; product allow-list phục vụ routing sau. |
| Ops | 3 | 2 | — |
| UX | 7 | — | Đúng toolbar + page-title + data-table + bar status; bỏ hero BI. |
**Verdict mẫu: OK-MVP (chờ anh duyệt).**

### Lead
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 7 | 7 | Cột Name gom remark/source/next; status bar New→Converted; Convert trên toolbar. |
| Mkt | 6 | 6 | Source/Segment nhìn được trên list. |
| Ops | 2 | 1 | — |
| UX | 7 | — | ART list pattern + bar; cards toggle phụ. |
**Verdict mẫu: OK-MVP.**

### Opportunity (Cơ hội)
| Role | UI | Dụng | Phản biện |
|------|----|------|-----------|
| Sale | 8 | 8 | List: Name gom event/hall/next + **stage bar** full path; kanban `scrollx`; detail ar-invoice grid + segment Workspace/Checklist/Fields + stage bar. |
| Mkt | 5 | 5 | Attribution trong Fields/workspace. |
| Ops | 6 | 6 | BEO/payment trong workspace — vận hành, không BI chart. |
| UX | 8 | — | Gần nhất chuẩn ar-invoice + outlet bar + task kanban scroll. |
**Verdict mẫu: OK-MVP / sát Good list.**

---

## 3. Mapping yêu cầu cũ → 3 trang mẫu

| Yêu cầu anh | Đã áp trên 3 trang? |
|-------------|---------------------|
| Sentence case tên form | Có (`Sale team`, `Lead`, `Opportunity`) |
| Toolbar action + reuse component | Có |
| data-table + cards toggle | Có (Opp thêm kanban) |
| Cột gom nhiều thông tin | Có |
| Status bar tracking (outlet) | Có (Lead status, Opp stage, Team Active/Inactive) |
| Không BI trên form | Có (đã gỡ insight/collected chart) |
| Mobile no h-scroll (trừ kanban) | Có |
| Detail kiểu ar-invoice | Có |

---

## 4. Demo duyệt

```
/#/sale-team
/#/sale-team/1
/#/lead
/#/opportunity          (toolbar: list | cards | kanban)
/#/opportunity/1001
```

**Sau khi anh Confirm 3 trang mẫu →** clone pattern sang toàn bộ forms còn lại (G3.4 full).
