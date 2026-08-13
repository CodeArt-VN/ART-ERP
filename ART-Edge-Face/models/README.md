# Place OpenVINO IR / ONNX models here (not committed — binary size).

## Required files (config.example.json)

| File | Role |
|------|------|
| `face-detection-yunet-2023mar.onnx` (or `.xml`+`.bin`) | YuNet face detection |
| `mobilefacenet-arcface.xml` + `.bin` | MobileFaceNet 128-d embedding |

## Download helpers

```powershell
# From ART-Edge-Face root (Windows POS)
python scripts/download_models.py
```

YuNet (OpenCV Zoo):
https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet

Prefer OpenVINO-optimized IR for iGPU (`device: "GPU"` in config.json).
Convert ONNX → IR with `ovc` if needed:

```powershell
ovc models/face-detection-yunet-2023mar.onnx --output_model models/face-detection-yunet-2023mar
```

Gallery JSON format (`data/gallery.json`):

```json
{
  "identities": [
    {
      "user_id": "EMP-001",
      "display_name": "Nguyen Van A",
      "embedding": [0.01, 0.02]
    }
  ]
}
```

Embedding length must match `models.recognition.embedding_dim` (128 or 512).
