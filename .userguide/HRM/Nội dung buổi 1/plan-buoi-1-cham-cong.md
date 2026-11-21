# HRM — Buổi 1: Chấm công end-to-end

| | |
|---|---|
| **Thời lượng** | 3.5–4 giờ |
| **Mục tiêu** | Setup → chấm → tính được bảng công kỳ mẫu |
| **Output** | 1 kỳ đã **Tính bảng chấm công**, có **Dữ liệu chấm công** đối soát được |
| **Không làm** | C&B, thuế, BH, payroll (Buổi 2–3) |

---

## 1. Vị trí buổi 1 trong lộ trình 3 buổi

```mermaid
flowchart LR
  B1["Buổi 1<br/>Chấm công"] --> B2["Buổi 2<br/>Cơ sở C&B / đầu vào lương"]
  B2 --> B3["Buổi 3<br/>Tính lương & Payslip"]

  style B1 fill:#1B6CA8,color:#fff,stroke:#0E3A5C
  style B2 fill:#E8EEF4,color:#222,stroke:#8AA0B5
  style B3 fill:#E8EEF4,color:#222,stroke:#8AA0B5
```

---

## 2. Sơ đồ luồng nghiệp vụ buổi 1

```mermaid
flowchart TD
  A[Nhân sự - Staff] --> B[Ca làm việc - Shift]
  B --> C[Bảng chấm công - Timesheet]
  C --> D[Đăng ký NV - Staff timesheet]
  D --> E[Cổng check-in + User device]
  E --> F[Phân ca - Scheduler]
  F --> G[Check-in]
  G --> H[Check-in log / Timesheet log]
  H --> I{Nghỉ / OT / Lễ / Work rule?}
  I -->|Đã duyệt / áp dụng| J[Mẫu bảng công - Timesheet template]
  I -->|Không| J
  J --> K[Kỳ chấm công - Timesheet cycle]
  K --> L[Tính bảng chấm công]
  L --> M[Dữ liệu chấm công - Timesheet record]

  style A fill:#E8F4FC,stroke:#1B6CA8
  style B fill:#E8F4FC,stroke:#1B6CA8
  style C fill:#E8F4FC,stroke:#1B6CA8
  style D fill:#E8F4FC,stroke:#1B6CA8
  style E fill:#FFF4E0,stroke:#C47E00
  style F fill:#FFF4E0,stroke:#C47E00
  style G fill:#FFF4E0,stroke:#C47E00
  style H fill:#FFF4E0,stroke:#C47E00
  style I fill:#F5F0FF,stroke:#6B5B95
  style J fill:#E6F7ED,stroke:#1F7A45
  style K fill:#E6F7ED,stroke:#1F7A45
  style L fill:#1F7A45,color:#fff,stroke:#0F4A28
  style M fill:#1F7A45,color:#fff,stroke:#0F4A28
```

### Thứ tự demo bắt buộc (đừng đảo)

`Staff → Shift → Timesheet (+ enrollment) → Gate/Device → Scheduler → Check-in → Template → Cycle → Calculate → Record`

---

## 3. Ba lớp dữ liệu cần phân biệt

```mermaid
flowchart TB
  subgraph L1["Lớp 1 — Log thô"]
    CL[Check-in log]
    TL[Timesheet log]
  end

  subgraph L2["Lớp 2 — Công đã tính"]
    TR[Timesheet record<br/>chi tiết / tổng hợp]
  end

  subgraph L3["Lớp 3 — Lương - Buổi 3"]
    PR[Staff payroll / Payslip]
  end

  CL --> TR
  TL --> TR
  TR -.->|Buổi 3| PR

  style L1 fill:#FFF4E0,stroke:#C47E00
  style L2 fill:#E6F7ED,stroke:#1F7A45
  style L3 fill:#F0F0F0,stroke:#999,stroke-dasharray: 5 5
```

| Lớp | Ý nghĩa | Buổi |
|-----|---------|------|
| Log thô | Giờ vào/ra thực tế | 1 |
| Công đã tính | Số công, OT, đi muộn… sau **Calculate** | 1 |
| Lương | Áp C&B + công thức payroll | 3 |

---

## 4. Agenda

| # | Phần | Thời lượng | Output checkpoint |
|---|------|------------|-------------------|
| 0 | Khai mạc + sơ đồ luồng | 15' | Học viên nắm end-to-end |
| 1 | Master chấm công | 50' | Shift + Timesheet + Enrollment |
| 2 | Cổng & thiết bị | 25' | Gate (+ device) sẵn |
| 3 | Phân ca & chấm thực tế | 45' | Có ca + có log trong kỳ |
| 4 | Nghỉ / OT / lễ / work rule (góc công) | 30' | Biết nguồn nào đổ vào tính công |
| 5 | Mẫu công → kỳ → tính công | 55' | Kỳ đã calculate + có record |
| 6 | Lab + checklist + Q&A | 30–40' | Lab pass + checklist tick đủ |

```mermaid
gantt
  title Buổi 1 — Timeline gợi ý
  dateFormat mm
  axisFormat %M'

  section Khai mạc
  Sơ đồ luồng           :a0, 00, 15m

  section Setup
  Master chấm công      :a1, after a0, 50m
  Cổng và thiết bị      :a2, after a1, 25m

  section Vận hành
  Phân ca và check-in   :a3, after a2, 45m
  Nghỉ OT lễ work rule  :a4, after a3, 30m

  section Tính công
  Template kỳ Calculate :a5, after a4, 55m
  Lab checklist Q&A     :a6, after a5, 35m
```

---

## 5. Chuẩn bị trước buổi

- Môi trường demo + 2–3 NV test  
- 1 chi nhánh / workplace có tọa độ hoặc IP gate  
- Data mẫu: 1 ca HC (VD 08:00–17:00) nếu muốn rút phần setup  
- Quyền menu HRM liên quan buổi 1:

| Route / màn | Tên VN |
|-------------|--------|
| `staff` | Nhân sự |
| `shift` | Ca làm việc |
| `timesheet` | Bảng chấm công |
| `staff-timesheet` | Bảng chấm công nhân viên |
| `checkin-gate` | Cổng check-in |
| `user-device` | Thiết bị người dùng |
| `scheduler` | Phân ca làm việc |
| `checkin` | Check-in |
| `checkin-log` | Nhật ký check-in |
| `timesheet-log` | Timesheet log |
| `leave-type` / `staff-time-off-request` | Loại nghỉ / Đơn nghỉ |
| `overtime-policy` / `overtime-request` | Chính sách OT / Phiếu OT |
| `holiday-policy` | Chính sách nghỉ lễ |
| `work-rule` (+ group / violation) | Quy định làm việc |
| `timesheet-template` | Mẫu bảng công |
| `timesheet-cycle` | Kỳ chấm công |
| `timesheet-record` | Dữ liệu chấm công |

---

## 6. Nội dung chi tiết theo phần

### 0. Khai mạc (15')

**Giảng**
- Mục tiêu buổi & output  
- Sơ đồ mục §2  
- Phân biệt log thô / công đã tính / lương (§3)

**Demo:** Chỉ menu HRM liên quan — chưa click sâu.

---

### 1. Master chấm công (50')

```mermaid
flowchart LR
  S[Staff] --> SH[Shift]
  SH --> TS[Timesheet]
  TS --> EN[Staff timesheet<br/>enrollment]

  style S fill:#E8F4FC,stroke:#1B6CA8
  style SH fill:#E8F4FC,stroke:#1B6CA8
  style TS fill:#E8F4FC,stroke:#1B6CA8
  style EN fill:#1B6CA8,color:#fff,stroke:#0E3A5C
```

#### 1.1 Nhân sự — `staff` (10')
- Field ảnh hưởng chấm: chi nhánh, workplace, trạng thái, gắn user  
- NV nghỉ việc / chưa active → không vào bảng công  

#### 1.2 Ca làm việc — `shift` (15')
- Giờ vào–ra, loại ca, nghỉ giữa ca  
- Mã ca không trùng loại nghỉ  

#### 1.3 Bảng chấm công — `timesheet` (15')
Trên detail nhấn mạnh:
- **Template** (`IDTimesheetTemplate`)  
- **Check-in policy**  
- **Shift list**  
- Workplace / office  
- Số ca/ngày, giờ công/ngày  
- **Check-out required**  

#### 1.4 Đăng ký NV — `staff-timesheet` (10')
- Ai thuộc bảng công nào, khoảng thời gian  
- **Thiếu enrollment** = có log vẫn có thể không ra dòng công  

**Checkpoint:** Có Shift + Timesheet + Staff enrollment.

---

### 2. Cổng & thiết bị (25')

```mermaid
flowchart LR
  G[Check-in gate<br/>tọa độ / IP] --> D[User device]
  D --> OK{Đủ điều kiện chấm?}
  OK -->|Có| CI[Cho phép check-in]
  OK -->|Không| ERR[IP / địa điểm / thiết bị lỗi]

  style G fill:#FFF4E0,stroke:#C47E00
  style D fill:#FFF4E0,stroke:#C47E00
  style CI fill:#1F7A45,color:#fff
  style ERR fill:#B33A3A,color:#fff
```

#### 2.1 Cổng — `checkin-gate` (15')
- Tọa độ, bán kính, IP wifi công ty  
- Lỗi hay gặp: IP invalid, phải chấm đúng địa điểm  

#### 2.2 Thiết bị — `user-device` (10')
- Đăng ký / duyệt thiết bị (nếu policy yêu cầu)  

**Checkpoint:** Gate (+ device nếu bắt buộc) sẵn sàng.

---

### 3. Phân ca & chấm thực tế (45')

```mermaid
sequenceDiagram
  participant HR as HR / Quản lý
  participant Sch as Scheduler
  participant NV as Nhân viên
  participant CI as Check-in
  participant Log as Check-in log

  HR->>Sch: Phân ca theo ngày / NV
  NV->>CI: Check-in / Check-out
  CI->>CI: Kiểm tra gate, giờ, device
  alt Hợp lệ
    CI->>Log: Ghi log thô
  else Không hợp lệ
    CI-->>NV: Message lỗi (IP / ngoài giờ / sai chỗ)
  end
  HR->>Log: Đối soát Timesheet log
```

#### 3.1 Phân ca — `scheduler` (20')
- Gán ca theo ngày / NV / bảng công  
- Chưa phân ca vs đã phân ca: ảnh hưởng đi muộn / về sớm  

#### 3.2 Check-in — `checkin` (10')
- Vào / ra; đúng chỗ, đúng giờ; checkout bắt buộc hay không  
- Demo 1 case success + 1 case fail  

#### 3.3 Nhật ký — `checkin-log` + `timesheet-log` (15')
- Check-in log = dữ liệu thô  
- Timesheet log = góc đối soát theo công  
- Bổ sung / sửa log khi quên chấm *(đúng quy trình công ty)*  

**Checkpoint:** Có phân ca + có log trong kỳ.

---

### 4. Nghỉ / OT / lễ / work rule — góc công (30')

> Không đi sâu C&B. Chỉ: **đã duyệt / áp dụng thì công tính thế nào**.

```mermaid
flowchart TD
  subgraph Nguồn ảnh hưởng công
    LV[Đơn nghỉ đã duyệt]
    OT[Đơn OT đã duyệt]
    HL[Ngày lễ - Holiday policy]
    WR[Work rule violation<br/>đi muộn / về sớm]
  end

  LV --> CALC[Calculate timesheet]
  OT --> CALC
  HL --> CALC
  WR --> CALC
  LOG[Check-in log + Scheduler] --> CALC
  CALC --> REC[Timesheet record]

  style CALC fill:#1F7A45,color:#fff
  style REC fill:#E6F7ED,stroke:#1F7A45
```

| Chủ đề | Màn hình | Nội dung giảng (gọn) |
|--------|----------|----------------------|
| Loại nghỉ / đơn nghỉ | `leave-type`, `staff-time-off-request` | Nghỉ duyệt → trừ công / công phép |
| PTO | `paid-time-off-policy`, `ptos-enrollment` | Nhắc enrollment; chi tiết Buổi 2 |
| OT | `overtime-policy`, `overtime-request` | OT duyệt → giờ OT vào công |
| Ngày lễ | `holiday-policy` | Ngày lễ vs ngày thường |
| Work rule | `work-rule`, group, violation | Đi muộn / về sớm → violation / trừ công |

**Demo gợi ý (chọn 2/3):** 1 đơn nghỉ duyệt · 1 đơn OT duyệt · 1 ngày lễ trên policy.

**Checkpoint:** Học viên biết nguồn nào “đổ” vào tính công.

---

### 5. Mẫu công → kỳ → tính công (55')

```mermaid
flowchart TD
  TPL[Timesheet template<br/>cột / UDF / công thức] --> TS2[Timesheet gắn Template]
  TS2 --> CY[Timesheet cycle<br/>From - To]
  CY --> ATT[Gắn bảng công vào kỳ]
  ATT --> CFG[Cấu hình cột theo kỳ<br/>cycle-config]
  CFG --> RUN[Tính bảng chấm công]
  RUN --> REC2[Timesheet record]
  REC2 --> EXP[Export chi tiết / tổng hợp]
  REC2 --> LOCK{Đóng / Reopen kỳ?}

  style TPL fill:#E6F7ED,stroke:#1F7A45
  style CY fill:#E6F7ED,stroke:#1F7A45
  style RUN fill:#1F7A45,color:#fff
  style REC2 fill:#1F7A45,color:#fff
```

#### 5.1 Mẫu bảng công — `timesheet-template` (15')
- Cột công, UDF  
- Template gắn vào Timesheet  
- Đổi template / reload cột giữa kỳ → rủi ro lệch dữ liệu  

#### 5.2 Kỳ chấm công — `timesheet-cycle` (20')
- Tạo kỳ From–To  
- Chọn working schedule / bảng công  
- Cấu hình cột theo kỳ (nút options / cycle-config)  
- Message cần biết:
  - *Timesheet is not attached to this cycle*
  - *No timesheet cycle found for this date*
  - *No timesheet template available*

#### 5.3 Calculate + Record (15')
- Action **Tính bảng chấm công**  
- Xem **Timesheet record** (chi tiết / tổng hợp)  
- Export; reopen kỳ khi cần sửa bộ cột đã đóng băng  

#### 5.4 Đối soát nhanh (5')

```mermaid
flowchart LR
  Q1[Scheduler<br/>Có ca?] --> Q2[Check-in log<br/>Có vào/ra?]
  Q2 --> Q3[Đơn nghỉ/OT<br/>Đã duyệt?]
  Q3 --> Q4[Timesheet record<br/>Số công đúng?]
```

**Checkpoint:** Kỳ đã calculate; có record xuất được.

---

## 7. Lab thực hành (30–40')

1. Gắn 1 NV vào bảng công  
2. Phân ca 3 ngày  
3. Ít nhất 2 ngày có log  
4. 1 ngày có nghỉ hoặc OT *(tuỳ data)*  
5. Tính công kỳ  
6. Đọc 1 dòng record và giải thích số liệu  

```mermaid
flowchart TD
  L1[1. Enrollment] --> L2[2. Phân ca 3 ngày]
  L2 --> L3[3. Có log ≥ 2 ngày]
  L3 --> L4[4. Nghỉ hoặc OT]
  L4 --> L5[5. Calculate]
  L5 --> L6[6. Giải thích 1 dòng record]

  style L5 fill:#1F7A45,color:#fff
  style L6 fill:#1B6CA8,color:#fff
```

---

## 8. Checklist chốt buổi 1

- [ ] Shift hợp lệ  
- [ ] Timesheet có template + shift list + policy  
- [ ] Staff timesheet enrollment đủ  
- [ ] Gate (+ device nếu cần)  
- [ ] Scheduler có ca trong kỳ  
- [ ] Có check-in log  
- [ ] Nghỉ / OT / lễ liên quan đã duyệt *(nếu có)*  
- [ ] Timesheet cycle gắn đúng bảng công  
- [ ] Đã **Calculate timesheet**  
- [ ] Timesheet record đối soát OK  

---

## 9. Lỗi thường gặp

| Triệu chứng | Nguyên nhân thường gặp |
|-------------|------------------------|
| Không tính được công | Thiếu kỳ / bảng công chưa gắn kỳ |
| Có log nhưng không ra dòng NV | Thiếu staff-timesheet enrollment |
| Check-in fail | Sai IP, sai địa điểm, ngoài giờ, device chưa duyệt |
| Công lệch giờ | Chưa phân ca / sai ca / quên checkout |
| Thiếu OT / nghỉ trên record | Đơn chưa duyệt trước khi calculate |
| Lệch cột sau khi tính | Đổi / reload template giữa kỳ |

---

## 10. Tài liệu phát học viên

1. File này (sơ đồ + checklist)  
2. Bảng màn hình ↔ việc cần làm (§5)  
3. 5 screenshot gợi ý: Timesheet detail · Scheduler · Check-in log · Cycle calculate · Timesheet record  

---

## Liên kết lộ trình

| Buổi | Folder | Nội dung |
|------|--------|----------|
| 1 | `.userguide/HRM/Nội dung buổi 1/` | Chấm công *(file này)* |
| 2 | *(sẽ tạo)* | Cơ sở C&B — thuế — BH — HĐ — PTO — payroll template/config |
| 3 | *(sẽ tạo)* | Tính lương & Payslip |
