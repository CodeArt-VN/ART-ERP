# Edge Face — Flow xử lý

## 1. Boot service

1. Load `config.json` (`EDGE_FACE_CONFIG`)
2. Init SQLite `data/edge_face.db`
3. Load gallery local; nếu trống → GET HQ `/edge/face-gallery?branch_id=`
4. Compile OpenVINO models trên iGPU
5. Mở 1–3 RTSP sub-stream (buffer=1)

## 2. Frame loop (mỗi camera)

1. Throttle theo `fps_target` (3–5 FPS)
2. Crop ROI
3. Detect faces (YuNet)
4. Crop + embed (MobileFaceNet → L2 vector)
5. FAISS cosine (`IndexFlatIP` trên vector đã chuẩn hóa)
6. Nếu `score >= confidence_threshold`:
   - Emit `known_match`
   - Dedupe theo `(camera_id, user_id)` trong `dedupe_window_seconds`
   - Publish event → BE; nếu fail → SQLite `synced=0`
7. Nếu **không match**:
   - Sinh `unknown_face_id`
   - Emit `unknown_face` để manual mapping trên ERP theo branch
   - Kèm `bbox.cx/cy` normalized để BE aggregate heatmap / zone counts

## 3. Sync bù

Background mỗi `sync_interval_seconds`: POST lần lượt pending rows cho đến khi BE OK hoặc lỗi mạng.

## 4. ERP

ERP **không** nhận RTSP. ERP gọi BE API để:

- Tra cứu lịch sử nhận diện / điểm danh theo chi nhánh / ngày
- Aggregate khách lạ / quen / VIP
- Tính toán heatmap / đếm người theo khu vực
- Đồng bộ master nhân viên–VIP → BE đẩy gallery xuống Edge (hoặc Edge pull)

Chi tiết contract: [03-hq-api-contract.md](03-hq-api-contract.md).
