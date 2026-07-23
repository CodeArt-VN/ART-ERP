# 05 — Test cases (draft G2 — khóa trước G4)

## P0

| ID | Given | When | Then |
|----|-------|------|------|
| TC-CRM-01 | Hall Diamond Trưa 25/12 đã Hold/Booked | Sale B hold cùng slot | Chặn + gợi ý slot khác |
| TC-CRM-02 | Soft hold hết Expiry, chưa đủ milestone Required | Job chạy | Release slot; Opp về Quote/Lost theo process |
| TC-CRM-05 | Hai sale Hold cùng slot cùng lúc | Concurrent save | Chỉ 1 thành công |
| TC-CRM-06 | Checklist stage có mục Required chưa done | Đổi stage | Chặn + liệt kê mục thiếu |
| TC-CRM-07 | Payment rule: milestone Required min 30% hoặc 10tr | Confirm Contract khi chưa đạt | Chặn Confirmed/HardBook theo GateAction |
| TC-CRM-08 | Payment rule Required=false cho mốc | Bỏ qua thu | Cho qua gate tương ứng |
| TC-CRM-09 | BEO thiếu section Required (allergen) | Lock BEO | Chặn lock |
| TC-CRM-10 | Kitchen role | Xem BEO | Không thấy giá bán/margin |
| TC-CRM-04 | AI draft quote dưới sàn | Gửi khách | Guardrail + cần duyệt (AutoSend off) |
| TC-CRM-03 | Contract đã ký, đổi menu | Lưu | Phụ lục + sync BEO/notify ops |

## P1

| ID | Case |
|----|------|
| TC-CRM-11 | Quota actual = collected từ payment Paid |
| TC-CRM-12 | KPI Config tắt metric → Board không hiện |
| TC-CRM-13 | Owner Sign Contract (status) — chưa cần APPROVAL multi |
| TC-CRM-14 | Lead thiếu Campaign/Source → không convert (nếu config bật) |
| TC-CRM-15 | Peak surcharge áp đúng T7 trên Quote |

## UAT (G5)

1. Wedding fair: lead → tour → quote PDF &lt; 3 phút.  
2. Đổi ngày/pax sau cọc: phụ lục + payment chênh.  
3. Event day extras → quyết toán.

*(Bổ sung chi tiết khi Confirm G2 / trước G4.)*
