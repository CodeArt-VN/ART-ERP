# ART Edge Face

Headless **Windows Service** nhận diện khuôn mặt tại POS nhà hàng (Edge), sync log về HQ/ERP.

## Kiến trúc (theo Technical Brief)

```
Camera IP (sub-stream) → Edge POS (OpenVINO @ Intel iGPU)
                              ├─ YuNet detect
                              ├─ MobileFaceNet embed
                              ├─ FAISS cosine match (RAM gallery)
                              └─ JSON event → HQ NAS API
                                   └─ offline: SQLite → sync bù
NVR 24/7 recording: không đụng (giữ đầu ghi cũ)
```

## Resource targets

| Metric | Target |
|--------|--------|
| RAM | ≤ 300 MB |
| CPU (Core i3) | ≤ 10% (AI trên iGPU) |
| Cameras | 1–3 trọng điểm, sub-stream 3–5 FPS |
| Confidence | ≥ 0.75 |
| Event payload | ~1 KB JSON |

## Quick start (dev / console)

```bash
cd ART-Edge-Face
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
cp config.example.json config.json   # sửa RTSP + HQ URL
python scripts/download_models.py    # YuNet; thêm MobileFaceNet IR thủ công
pytest -q
python -m edge_face --dry-check-config -c config.json
python -m edge_face -c config.json   # console (không phải service)
```

## Windows Service (POS)

```powershell
# Admin PowerShell
.\scripts\install_service.ps1 -InstallDir C:\ART\EdgeFace
# hoặc:
python -m edge_face install
python -m edge_face start
```

Env:

- `EDGE_FACE_CONFIG` — đường dẫn `config.json`
- `EDGE_FACE_API_KEY` — Bearer token HQ (tên field cấu hình được trong config)

## Event payload (HQ webhook)

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
    "bbox": { "cx": 0.34, "cy": 0.28 }
  }
}
```

Ngoài `known_match`, Edge còn phát `unknown_face` để BE/ERP manual mapping theo chi nhánh.

BE API contract chi tiết:

- `docs/03-hq-api-contract.md`
- `docs/05-be-openapi.yaml`
- `docs/06-be-openapi-summary.md`

## Layout

```
ART-Edge-Face/
  edge_face/           # service + pipeline
  config.example.json
  models/              # IR/ONNX (gitignored binaries)
  data/                # sqlite + gallery
  scripts/             # install + model download
  tests/
  docs/
```

## BA / Plan

Kế hoạch module & gate confirm: `.cursor/plans/EDGE-FACE/plan.md`.
