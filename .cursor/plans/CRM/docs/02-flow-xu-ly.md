# 02 — Flow xử lý (khóa từ G1)

```mermaid
flowchart TD
  Setup[Setup_Team_Quota_Menu_Segment_Checklist_PaymentRule_KPI]
  Setup --> A[Inquiry]
  A --> B[Tour_Tasting]
  B --> C[Quote]
  C --> D[Hold]
  D --> E[Contract_PaymentSchedule]
  E --> F[BEO]
  F --> G[Event_Day]
  G --> H[Final_Invoice]
  H --> I[Nurture]
  D -->|hold_expire| C
```

**Quy tắc chốt G1:**

1. Đổi stage: checklist mục **Required** phải xong.
2. Cọc/TT: theo **Payment rule config** của quy trình sale (`Required`, min %, min Amount).
3. Ký MVP: **Owner status**; sau → APPROVAL đồng ký.
4. KPI: config linh động.

Chi tiết nghiệp vụ: [g1-nghiep-vu-flow.md](g1-nghiep-vu-flow.md).
