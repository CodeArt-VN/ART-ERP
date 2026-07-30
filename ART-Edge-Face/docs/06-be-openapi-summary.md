# BE OpenAPI Summary

File spec chính: [`05-be-openapi.yaml`](05-be-openapi.yaml)

## Mục tiêu

Khóa chuẩn API cho 3 luồng nghiệp vụ anh đã chốt:

1. **Điểm danh / chấm công**
2. **Khách lạ / quen / VIP**
3. **Đếm người theo khu vực / heatmap**

## Nhóm API

### 1. Edge Ingestion

- `POST /edge/face-events`
  - ingest `known_match`
  - ingest `unknown_face`
- `GET /edge/face-gallery`
  - Edge pull gallery vectors theo `branch_id`
- `POST /edge/zone-analytics`
  - optional aggregate upload từ Edge

### 2. Attendance

- `GET /erp/attendance-events`
- `POST /erp/attendance/manual-confirm`

Use khi Edge nhận diện được nhân viên hoặc khi ERP manual confirm `unknown_face`.

### 3. Visitors

- `GET /erp/visitor-events`
- `POST /erp/visitor-mapping/manual-confirm`

Class support:

- `vip`
- `familiar`
- `stranger`
- `unknown_face`

### 4. Face Gallery

- `POST /erp/face-gallery/upsert`
- `DELETE /erp/face-gallery/{user_id}`

BE là source of truth cho vector; Edge chỉ clone theo branch scope.

### 5. Zone Analytics

- `GET /erp/zone-heatmap`
- `GET /erp/zone-counts`

## Data model chính

### FaceEvent

- `branch_id`
- `event_type`: `known_match` | `unknown_face`
- `user_id`
- `unknown_face_id`
- `timestamp`
- `score`
- `camera_id`
- `display_name`
- `meta.bbox.cx/cy`

### Rule quan trọng

- `known_match` bắt buộc có `user_id`
- `unknown_face` bắt buộc có `unknown_face_id`
- `bbox.cx/cy` normalized dùng để aggregate heatmap / zone density
- mọi API query theo branch phải qua **RBAC chi nhánh**

## Thứ tự code BE em khuyên

1. `POST /edge/face-events`
2. `GET /edge/face-gallery`
3. `POST /erp/face-gallery/upsert`
4. `GET /erp/attendance-events`
5. `POST /erp/attendance/manual-confirm`
6. `GET /erp/visitor-events`
7. `POST /erp/visitor-mapping/manual-confirm`
8. `GET /erp/zone-counts`
9. `GET /erp/zone-heatmap`
10. `POST /edge/zone-analytics` (optional fast path)

## Ghi chú implementation

- Nên lưu raw events append-only trước, rồi aggregate sang bảng attendance / visitor / heatmap
- Unknown face nên có queue riêng để ERP thao tác manual mapping
- Dedupe:
  - known: `(branch_id, camera_id, user_id, timestamp_bucket_1s)`
  - unknown: `(branch_id, camera_id, unknown_face_id)`
