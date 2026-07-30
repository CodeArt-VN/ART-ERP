# HQ / ERP API Contract (draft — chờ confirm G1)

Base: `{hq.api_base_url}`  
Auth: `Authorization: Bearer {EDGE_FACE_API_KEY}`

## 1. Edge → HQ: Face event

`POST /edge/face-events`

```json
{
  "branch_id": "HN-001",
  "user_id": "EMP-001",
  "timestamp": 1710000000.123,
  "score": 0.91,
  "camera_id": "cam-entrance-01",
  "display_name": "Nguyen Van A",
  "meta": { "det_score": 0.88 }
}
```

| HTTP | Nghĩa |
|------|-------|
| 200/201/202 | Accepted — Edge đánh dấu synced |
| 4xx/5xx / timeout | Edge giữ SQLite, retry |

Idempotency đề xuất (G1): HQ dedupe `(branch_id, camera_id, user_id, timestamp_bucket_1s)`.

## 2. Edge ← HQ: Gallery pull

`GET /edge/face-gallery?branch_id=HN-001`

```json
{
  "branch_id": "HN-001",
  "version": "2026-07-30T01:00:00Z",
  "identities": [
    {
      "user_id": "EMP-001",
      "display_name": "Nguyen Van A",
      "embedding": [0.01, 0.02],
      "tags": ["staff"]
    }
  ]
}
```

`embedding` length = 128 hoặc 512 (khớp model nhận diện).

## 3. ERP → HQ (đề xuất — ERP gọi API HQ)

| API | Mục đích |
|-----|----------|
| `GET /erp/face-events?branch_id=&from=&to=` | Báo cáo check-in / VIP walk-in |
| `POST /erp/face-gallery/upsert` | Đăng ký / cập nhật nhân viên–VIP + embedding |
| `DELETE /erp/face-gallery/{user_id}` | Thu hồi quyền nhận diện |

Mapping ERP entities (chờ BA confirm):

- `user_id` ↔ HR Employee / CRM Contact VIP
- `branch_id` ↔ Outlet / Cost center
- Event → optional Attendance punch hoặc CRM visit log

## 4. Câu hỏi cần anh confirm (G1)

1. HQ receiver = NAS custom API hay module mới trên ART-ERP-BE?
2. Event chỉ log hay tạo chứng từ chấm công / CRM lead?
3. Ai phát hành embedding (HQ enrollment app vs Edge enroll)?
4. Retention log HQ bao lâu (30/90/365 ngày)?
