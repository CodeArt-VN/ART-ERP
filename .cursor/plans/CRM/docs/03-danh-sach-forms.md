# 03 — Danh sách forms (G2 draft — chờ Confirm)

**Phạm vi:** màn hình cần có cho CRM Wedding MVP (sau G1).  
**Chú thích:** `Mới` = chưa có UI/entity đủ · `Mở rộng` = có sẵn cần bổ sung · `Có` = tái dùng gần như nguyên.

| # | Mã form / Route đề xuất | Tên | Nhóm | Trạng thái | Ưu tiên |
|---|-------------------------|-----|------|------------|---------|
| 1 | `crm-sale-team` | Sale Team | Setup | Mới | P0 |
| 2 | `crm-sale-quota` | Sale Quota | Setup | Mới | P0 |
| 3 | `crm-event-hall` | Sảnh / Hall | Setup | Mới | P0 |
| 4 | `crm-event-package` | Package / Menu set | Setup | Mới | P0 |
| 5 | `crm-price-book` | Price book / Peak rule | Setup | Mới | P0 |
| 6 | `crm-segment` | Segment / Phân hạng KH | Setup | Mới | P0 |
| 7 | `crm-sales-process` | Quy trình bán hàng | Setup | Mới | P0 |
| 8 | `crm-checklist-template` | Checklist template (stage) | Setup | Mới | P0 |
| 9 | `crm-payment-rule` | Quy tắc cọc / TT tiến độ | Setup | Mới | P0 |
| 10 | `crm-kpi-config` | Cấu hình KPI linh động | Setup | Mới | P0 |
| 11 | `crm/lead` | Lead | Pipeline | Có — mở rộng | P0 |
| 12 | `crm/opportunity` | Opportunity / Deal | Pipeline | Mới UI (BE có) | P0 |
| 13 | `crm/activity` | Activity | Pipeline | Mới UI (BE có) | P1 |
| 14 | `crm-tour-booking` | Tour / Tasting | Pipeline | Mới (hoặc Attendance type) | P0 |
| 15 | `sale/quotation` (event) | Báo giá sự kiện | Quote | Mở rộng SALE_Quotation | P0 |
| 16 | `crm-event-hold` | Giữ chỗ sảnh | Quote/Hold | Mới | P0 |
| 17 | `crm-hall-calendar` | Lịch sảnh | Quote/Hold | Mới | P0 |
| 18 | `crm/contract` | Hợp đồng | Contract | Mới UI (BE có) + mở rộng | P0 |
| 19 | `crm-contract-payment` | Lịch & theo dõi TT/cọc | Contract | Mới | P0 |
| 20 | `crm-beo` | BEO | Ops | Mới | P0 |
| 21 | `crm/attendance-booking` | Event day / Attendance | Ops | Có — mở rộng FK | P0 |
| 22 | `crm-ai-inbox` | AI Sales inbox / draft | AI | Mới | P1 |
| 23 | `crm/campaign` | Campaign | Mkt | Có — siết bắt buộc gắn Lead | P0 |
| 24 | `crm/customer` | Contact / KH | Master | Có | P0 |
| 25 | `crm-kpi-board` | KPI Board (runtime) | Báo cáo | Mới | P1 |

**Tái dùng không tạo form mới:** `BANK_IncomingPayment`, `SALE_Order`, `APPROVAL` (phase sau đồng ký), WMS Item (menu lines).

**Phase 2 (không MVP):** Floor plan kéo-thả, Approval multi-sign BEO/Contract, Zalo OA sâu.
