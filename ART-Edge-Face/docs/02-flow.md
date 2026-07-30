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
   - Dedupe theo `(camera_id, user_id)` trong `dedupe_window_seconds`
   - Publish event → HQ; nếu fail → SQLite `synced=0`

## 3. Sync bù

Background mỗi `sync_interval_seconds`: POST lần lượt pending rows cho đến khi HQ OK hoặc lỗi mạng.

## 4. ERP

ERP **không** nhận RTSP. ERP gọi API HQ để:

- Tra cứu lịch sử nhận diện theo chi nhánh / ngày
- Đồng bộ master nhân viên–VIP → HQ đẩy gallery xuống Edge (hoặc Edge pull)

Chi tiết contract: [03-hq-api-contract.md](03-hq-api-contract.md).
