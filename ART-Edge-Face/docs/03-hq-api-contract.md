# HQ / ERP API Contract (G1 confirmed scope)

Base: `{hq.api_base_url}`  
Auth: `Authorization: Bearer {EDGE_FACE_API_KEY}`

OpenAPI spec chuẩn cho team BE: [`05-be-openapi.yaml`](05-be-openapi.yaml)  
Summary ngắn: [`06-be-openapi-summary.md`](06-be-openapi-summary.md)

## 1. Edge → BE API: ingestion event

`POST /edge/face-events`

```json
{
  "branch_id": "HN-001",
  "event_type": "known_match",
  "user_id": "EMP-001",
  "unknown_face_id": null,
  "timestamp": 1710000000.123,
  "score": 0.91,
  "camera_id": "cam-entrance-01",
  "display_name": "Nguyen Van A",
  "meta": {
    "det_score": 0.88,
    "bbox": { "x1": 112, "y1": 50, "x2": 180, "y2": 132, "cx": 0.34, "cy": 0.28 },
    "frame_size": { "width": 640, "height": 480 }
  }
}
```

| HTTP | Nghĩa |
|------|-------|
| 200/201/202 | Accepted — Edge đánh dấu synced |
| 4xx/5xx / timeout | Edge giữ SQLite, retry |

### Unknown / manual mapping event

Khi Edge **không nhận diện được**, vẫn phải gửi event để BE/ERP manual map theo chi nhánh:

```json
{
  "branch_id": "HN-001",
  "event_type": "unknown_face",
  "user_id": null,
  "unknown_face_id": "UNK-7B8C9D0E11223344",
  "timestamp": 1710000000.123,
  "score": 0.0,
  "camera_id": "cam-entrance-01",
  "display_name": null,
  "meta": {
    "det_score": 0.72,
    "bbox": { "x1": 112, "y1": 50, "x2": 180, "y2": 132, "cx": 0.34, "cy": 0.28 },
    "frame_size": { "width": 640, "height": 480 }
  }
}
```

Idempotency đề xuất:

- `known_match`: dedupe `(branch_id, camera_id, user_id, timestamp_bucket_1s)`
- `unknown_face`: dedupe `(branch_id, camera_id, unknown_face_id)`

## 2. Edge ← BE API: gallery pull

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

Phân quyền:

- BE lưu vector sinh trắc học tập trung
- Edge chỉ clone bản cần thiết để match local cho nhanh
- Scope dữ liệu là **toàn chuỗi**, nhưng query / sync phải áp dụng **RBAC theo chi nhánh**

## 3. BE / ERP APIs theo scope anh đã chốt

### 3.1 Attendance / chấm công

| API | Mục đích |
|-----|----------|
| `GET /erp/attendance-events?branch_id=&from=&to=&user_id=` | Lịch sử điểm danh / nhận diện nhân viên |
| `POST /erp/attendance/manual-confirm` | Manual confirm `unknown_face` thành nhân viên theo branch |

### 3.2 Khách quen / VIP / khách lạ

| API | Mục đích |
|-----|----------|
| `GET /erp/visitor-events?branch_id=&from=&to=&class=` | Log `vip`, `familiar`, `stranger`, `unknown_face` |
| `POST /erp/visitor-mapping/manual-confirm` | Gán `unknown_face_id` → customer/contact/VIP |
| `POST /erp/face-gallery/upsert` | Đăng ký / cập nhật vector khuôn mặt nhân viên / VIP |
| `DELETE /erp/face-gallery/{user_id}` | Thu hồi / vô hiệu hóa vector |

### 3.3 Đếm người theo khu vực / heatmap

| API | Mục đích |
|-----|----------|
| `POST /edge/zone-analytics` | Edge đẩy aggregate theo vùng / khung giờ nếu bật |
| `GET /erp/zone-heatmap?branch_id=&from=&to=&camera_id=` | Trả heatmap / mật độ theo khu vực |
| `GET /erp/zone-counts?branch_id=&from=&to=&zone_id=` | Đếm người theo khu vực / timeslot |

> Hiện package Edge đã gửi `bbox.cx/cy` normalized trong `meta`; BE có thể aggregate heatmap từ raw events trước khi cần thêm luồng analytics riêng.

## 4. Mapping entities

- `user_id` ↔ HR Employee / CRM Contact VIP
- `branch_id` ↔ Outlet / Cost center
- `known_match` → Attendance punch / VIP walk-in / familiar-visitor touchpoint
- `unknown_face` → Hàng chờ manual mapping theo branch
- `meta.bbox.cx/cy` → nguồn để aggregate heatmap / zone density
- Vector gốc lưu ở **BE**, Edge giữ bản clone theo policy sync

## 5. Trạng thái confirm G1

Đã chốt từ anh:

1. **BE API**
2. Use cases: **điểm danh/chấm công**, **đếm người theo khu vực + heatmap**, **nhận diện khách lạ/quen/VIP**
3. **Vector sinh trắc học lưu ở BE**, clone về Edge để xử lý local; unknown vẫn phải log để manual mapping theo branch
4. Scope **toàn chuỗi**, có **phân quyền chi nhánh**

Chưa có:

- Pilot branch / RTSP mẫu
