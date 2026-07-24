# 03 — Danh sách forms (G2 draft — **chưa Confirm**, đang review)

**Phạm vi:** màn hình CRM Wedding MVP (sau G1).  
**Mã form:** không dùng prefix `crm-` / `crm/`.  
**Chú thích:** `Mới` · `Mở rộng` · `Có` = tái dùng gần như nguyên.

| # | Mã form | Tên | Nhóm | Trạng thái | Ưu tiên |
|---|---------|-----|------|------------|---------|
| 1 | `sale-team` | Sale Team | Setup | Mới | P0 |
| 2 | `sale-quota` | Sale Quota | Setup | Mới | P0 |
| 3 | `event-hall` | Sảnh / Hall | Setup | Mới | P0 |
| 4 | `event-package` | Package / Menu set | Setup | Mới | P0 |
| 5 | `price-book` | Price book / Peak rule | Setup | Mới | P0 |
| 6 | `segment` | Segment / Phân hạng KH | Setup | Mới | P0 |
| 7 | `sales-process` | Quy trình bán hàng | Setup | Mới | P0 |
| 8 | `checklist-template` | Checklist template (stage) | Setup | Mới | P0 |
| 9 | `payment-rule` | Quy tắc cọc / TT tiến độ | Setup | Mới | P0 |
| 10 | `kpi-config` | Cấu hình KPI linh động | Setup | Mới | P0 |
| 11 | `lead` | Lead | Pipeline | Có — mở rộng | P0 |
| 12 | `opportunity` | Opportunity / Deal | Pipeline | Mới UI (BE có) | P0 |
| 13 | `activity` | Activity | Pipeline | Mới UI (BE có) | P1 |
| 14 | `tour-booking` | Tour / Tasting | Pipeline | Mới (hoặc Attendance type) | P0 |
| 15 | `sale-quotation` | Báo giá sự kiện | Quote | Mở rộng SALE_Quotation | P0 |
| 16 | `event-hold` | Giữ chỗ sảnh | Quote/Hold | Mới | P0 |
| 17 | `hall-calendar` | Lịch sảnh | Quote/Hold | Mới | P0 |
| 18 | `contract` | Hợp đồng | Contract | Mới UI (BE có) + mở rộng | P0 |
| 19 | `contract-payment` | Lịch & theo dõi TT/cọc | Contract | Mới | P0 |
| 20 | `beo` | BEO | Ops | Mới | P0 |
| 21 | `attendance-booking` | Event day / Attendance | Ops | Có — mở rộng FK | P0 |
| 22 | `ai-inbox` | AI Sales inbox / draft | AI | Mới | P1 |
| 23 | `campaign` | Campaign | Mkt | Có — siết bắt buộc gắn Lead | P0 |
| 24 | `customer` | Contact / KH | Master | Có | P0 |
| 25 | `kpi-board` | KPI Board (runtime) | Báo cáo | Mới | P1 |

**Tái dùng không tạo form mới:** `BANK_IncomingPayment`, `SALE_Order`, `APPROVAL` (phase sau đồng ký), WMS Item (menu lines).

**Phase 2:** Floor plan kéo-thả, Approval multi-sign BEO/Contract, Zalo OA sâu.

> Route Angular thực tế có thể vẫn nằm dưới module `pages/CRM/` — **mã form / SYS_Form.Code** dùng bảng trên (không prefix `crm`).
