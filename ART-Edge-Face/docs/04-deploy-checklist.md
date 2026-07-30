# Edge Face — Deploy POS checklist

## Hardware

- [ ] Windows 11 POS, Core i3 gen8+, RAM ≥ 8GB
- [ ] Intel UHD driver mới; OpenVINO thấy device `GPU`
- [ ] Không cần VGA rời

## Network / Camera

- [ ] 1–3 camera trọng điểm: cửa / quầy
- [ ] RTSP **sub-stream** 640x480 hoặc 1280x720, H.264, 3–5 FPS
- [ ] NVR recording giữ nguyên — Edge không ghi đè
- [ ] ROI đã khoanh trên `config.json`

## Software

- [ ] Python 3.10+ (hoặc embed runtime trong release zip)
- [ ] `pip install -r requirements.txt` + `pywin32`
- [ ] Models: YuNet + MobileFaceNet IR trong `models/`
- [ ] `config.json` từ `config.example.json`
- [ ] `EDGE_FACE_API_KEY` set ở system env
- [ ] Service `ARTEdgeFace` Running
- [ ] Log `logs/edge_face.log` không spam reconnect

## Verify

```powershell
python -m edge_face --dry-check-config -c C:\ART\EdgeFace\config.json
Get-Service ARTEdgeFace
# Sau khi nhân viên đi qua camera: HQ nhận JSON; hoặc SQLite pending=0
```

## Rollback

```powershell
python -m edge_face stop
python -m edge_face remove
```

NVR / POS bán hàng không bị ảnh hưởng (process tách biệt).
