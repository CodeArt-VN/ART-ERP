import React, { CSSProperties } from "react";
import {
  Button,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Code,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Link,
  Pill,
  Row,
  Spacer,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
  useCanvasState,
  CollapsibleSection,
  TodoListCard
} from "cursor/canvas";

export default function CRMTestStrategy() {
  const theme = useHostTheme();
  const [activeTab, setActiveTab] = useCanvasState<string>("activeTab", "scope");

  const containerStyle: CSSProperties = {
    padding: "24px",
    backgroundColor: theme.bg.editor,
    minHeight: "100vh",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
  };

  const tabs = [
    { id: "scope", label: "Phạm Vi (Epic Scope)" },
    { id: "testcases", label: "Kịch Bản Trọng Yếu" },
    { id: "data", label: "Dữ Liệu & Phân Quyền" },
    { id: "automation", label: "Tự Động Hóa" },
    { id: "uat", label: "Kịch Bản UAT" },
    { id: "ac", label: "Khung AC Template" },
    { id: "docs", label: "Danh Mục Tài Liệu" }
  ];

  const renderScope = () => {
    const epics = [
      {
        id: "epic-lead",
        title: "EPIC 1: LEAD (Tiềm Năng)",
        desc: "Phễu tiếp nhận yêu cầu tiệc cưới/sự kiện từ Website, Hotline, Social Media. Tự động gán lead cho sales và phân tích nhu cầu ban đầu.",
        items: [
          "Thu thập thông tin cô dâu chú rể, số điện thoại, ngày cưới dự kiến.",
          "Phân loại độ nóng của Lead (Lead Scoring) dựa trên ngân sách và sảnh mong muốn.",
          "Luật gán Lead tự động (Round-robin hoặc theo hiệu suất của sales).",
          "Tự động đặt lịch nhắc nhở gọi điện/chăm sóc (Follow-up Reminders)."
        ]
      },
      {
        id: "epic-quotation",
        title: "EPIC 2: QUOTATION (Báo Giá)",
        desc: "Tính toán báo giá động theo bàn, thực đơn (Set menu/Buffet) và các dịch vụ cộng thêm (Decoration, MC, Âm thanh ánh sáng).",
        items: [
          "Bảng giá động theo thứ trong tuần, cuối tuần hoặc mùa cao điểm.",
          "Quy tắc tính chiết khấu (Discount) tự động theo số lượng bàn hoặc tổng giá trị.",
          "Luồng phê duyệt (Approval Workflow) khi sales báo giá dưới giá sàn cấu hình.",
          "Xuất báo giá sang định dạng PDF chuẩn hóa gửi khách hàng."
        ]
      },
      {
        id: "epic-booking",
        title: "EPIC 3: BOOKING/CONTRACT (Đặt Chỗ & Hợp Đồng)",
        desc: "Quy trình giữ chỗ sảnh tạm thời, đóng cọc giữ chân và ký kết hợp đồng pháp lý ràng buộc.",
        items: [
          "Khóa sảnh tạm thời (Hold sảnh) với cơ chế chống trùng lặp.",
          "Theo dõi tiến độ nộp cọc (Thường chia 3 đợt: Cọc giữ sảnh, Cọc chốt menu, Thanh toán đợt cuối).",
          "Tự động chuyển đổi từ Báo giá chốt sang Hợp đồng nháp.",
          "Ràng buộc các điều khoản phạt hủy tiệc tự động tính toán."
        ]
      },
      {
        id: "epic-ops",
        title: "EPIC 4: EVENT OPS (Vận Hành Sự Kiện)",
        desc: "Chuyển giao thông tin từ Sales xuống bộ phận Vận hành (Sảnh, Bếp, Trang trí) để chuẩn bị chu đáo trước ngày tiệc.",
        items: [
          "Xuất định lượng món ăn (BOM) tự động cho Bếp trưởng dựa trên số bàn chốt.",
          "Danh sách trang thiết bị và checklist bàn giao sảnh cho Banquet Manager.",
          "Quản lý ca làm việc và phân công nhân sự phục vụ (Full-time & Part-time).",
          "Sơ đồ sảnh (Floor Plan) hiển thị chi tiết số bàn và cách bố trí."
        ]
      },
      {
        id: "epic-post",
        title: "EPIC 5: POST-EVENT (Sau Sự Kiện)",
        desc: "Quyết toán tiệc, khảo sát khách hàng và ghi nhận doanh thu thực tế.",
        items: [
          "Ghi nhận đồ uống/dịch vụ phát sinh ngoài hợp đồng ngay tại tiệc.",
          "Quyết toán cuối tiệc, hoàn trả cọc (nếu có) và xuất hóa đơn VAT.",
          "Tự động tính hoa hồng (Commission) cho nhân viên kinh doanh.",
          "Khảo sát đánh giá độ hài lòng của khách hàng (CSAT) tự động qua SMS/Zalo."
        ]
      },
      {
        id: "epic-ai",
        title: "EPIC 6: AI SALES ASSISTANT",
        desc: "Trợ lý ảo hỗ trợ sales tăng tốc quy trình tư vấn và báo giá tiệc cưới.",
        items: [
          "Đọc hiểu nội dung chat/email của khách hàng để tự động điền Form Lead.",
          "Gợi ý gói thực đơn và trang trí tối ưu dựa trên ngân sách và số bàn khách mô tả.",
          "Tự động tạo dự thảo Báo giá nháp (Draft Quotation) chỉ sau 1 câu lệnh.",
          "Phân tích phản hồi khách hàng để gợi ý câu trả lời thuyết phục cho Sales."
        ]
      }
    ];

    return (
      <Stack gap={16}>
        <H2>Phạm Vi Kiểm Thử (6 Epics CRM Wedding ERP)</H2>
        <Text tone="secondary">
          Chiến lược kiểm thử tập trung vào chuỗi giá trị khép kín từ lúc nhận thông tin khách hàng tiềm năng đến khi quyết toán tiệc cưới.
        </Text>
        <Grid columns={2} gap={16}>
          {epics.map(epic => (
            <Card key={epic.id}>
              <CardHeader>{epic.title}</CardHeader>
              <CardBody>
                <Stack gap={12}>
                  <Text weight="semibold">{epic.desc}</Text>
                  <Divider />
                  <Stack gap={6}>
                    <Text size="small" weight="medium" tone="secondary">Nội dung kiểm thử chính:</Text>
                    {epic.items.map((item, idx) => (
                      <Row key={idx} gap={8} align="start">
                        <Text tone="tertiary" size="small">•</Text>
                        <Text size="small" tone="secondary">{item}</Text>
                      </Row>
                    ))}
                  </Stack>
                </Stack>
              </CardBody>
            </Card>
          ))}
        </Grid>
      </Stack>
    );
  };

  const renderTestCases = () => {
    const tableHeaders = ["TC ID", "Tình Huống Trọng Yếu", "Given (Bối cảnh)", "When (Hành động)", "Then (Kết quả mong đợi)"];
    const tableRows = [
      [
        <Code>TC-CRM-01</Code>,
        <Text weight="semibold">Double Booking Hall (Trùng Sảnh)</Text>,
        "Sảnh 'Diamond' đã được chốt giữ chỗ (Hold/Booked) cho Trưa ngày 25/12/2026.",
        "Sales B cố gắng chọn Sảnh 'Diamond' Trưa 25/12/2026 trên một báo giá mới và lưu giữ chỗ.",
        "Hệ thống hiển thị cảnh báo sảnh đã bị trùng lịch, chặn việc lưu thông tin và đề xuất các sảnh trống khác hoặc ca tối."
      ],
      [
        <Code>TC-CRM-02</Code>,
        <Text weight="semibold">Deposit Overdue (Cọc Quá Hạn)</Text>,
        "Phiếu giữ sảnh tạm thời (Hold) có thời hạn cọc là 48 tiếng (tạo lúc 10:00 ngày 23/07/2026).",
        "Đến 10:01 ngày 25/07/2026 hệ thống không ghi nhận bất kỳ chứng từ đặt cọc nào từ kế toán.",
        "Cron job tự động chuyển trạng thái sảnh sang 'Quá hạn', giải phóng sảnh trở lại danh sách trống để Sales khác bán."
      ],
      [
        <Code>TC-CRM-03</Code>,
        <Text weight="semibold">Menu Change After Contract</Text>,
        "Hợp đồng tiệc đã ký, Set Menu A trị giá 5.000.000đ/bàn đã được chốt và đồng bộ xuống bếp.",
        "Khách yêu cầu đổi sang Set Menu B trị giá 5.500.000đ/bàn trước ngày cưới 7 ngày.",
        "Hệ thống tạo Phụ lục hợp đồng, tính chênh lệch thanh toán, gửi thông báo khẩn cấp đồng bộ thực đơn mới cho bộ phận Bếp."
      ],
      [
        <Code>TC-CRM-04</Code>,
        <Text weight="semibold">AI Wrong Quote (AI Sai Lệch)</Text>,
        "Khách yêu cầu tiệc 30 bàn tại sảnh Diamond cuối tuần (giá sàn cấu hình tối thiểu là 6.000.000đ/bàn).",
        "AI Sales Assistant đọc email và tự động tạo báo giá nháp với giá 5.000.000đ/bàn (dưới giá sàn).",
        "Hệ thống kích hoạt Price Guardrail, gắn cờ cảnh báo đỏ và bắt buộc gửi yêu cầu phê duyệt đến Sale Manager trước khi cho phép xuất gửi khách."
      ],
      [
        <Code>TC-CRM-05</Code>,
        <Text weight="semibold">Concurrency Booking (Đồng Thời)</Text>,
        "Sảnh 'Ruby' đang trống duy nhất ngày 12/12/2026 ca tối.",
        "Sales A và Sales B cùng mở Form và nhấn nút 'Giữ sảnh' (Hold) đúng cùng 1 giây (11:46:00).",
        "Hệ thống áp dụng Lock chặn đồng thời, chỉ 1 Sales thao tác trước 1/1000s thành công, người còn lại nhận báo lỗi và tự động làm mới lịch sảnh."
      ]
    ];

    return (
      <Stack gap={16}>
        <H2>Kịch Bản Kiểm Thử Trọng Yếu & Biên (Edge Cases)</H2>
        <Callout tone="warning" title="Lưu ý Đặc Thù Ngành Tiệc Cưới">
          Đối với ngành tiệc cưới, trùng sảnh (Double Booking) và sai lệch giá thực đơn sau ký hợp đồng là hai rủi ro nghiêm trọng nhất, có thể dẫn đến đền bù thiệt hại thương hiệu nặng nề. Do đó, các kịch bản này được xếp hạng ưu tiên kiểm thử mức P0.
        </Callout>
        <Table
          headers={tableHeaders}
          rows={tableRows}
          columnAlign={["center", "left", "left", "left", "left"]}
          rowTone={["danger", "warning", "info", "warning", "danger"]}
          striped
        />
      </Stack>
    );
  };

  const renderDataAndRoles = () => {
    const tableHeaders = ["Vai Trò (Role)", "Quyền Hạn Chính Trong CRM", "Yêu Cầu Dữ Liệu Test (Test Data)", "Mục Tiêu Kiểm Thử Quyền (Test Purpose)"];
    const tableRows = [
      [
        <Text weight="semibold">Sale (Kinh Doanh)</Text>,
        "Tạo Lead, tạo Báo giá, gửi duyệt chiết khấu, giữ sảnh tạm thời (Hold) cho khách của mình.",
        "Tài khoản Sales test độc lập; danh sách 10 sảnh trống; bộ dữ liệu menu tiệc mẫu.",
        "Đảm bảo sales không xem/sửa được khách hàng của sales khác (Kiểm thử cô lập dữ liệu)."
      ],
      [
        <Text weight="semibold">Sale Manager (Trưởng Phòng)</Text>,
        "Duyệt báo giá dưới sàn/chiết khấu cao, phân bổ Lead tự động, xem báo cáo doanh thu toàn phòng.",
        "Tài khoản Manager; 5 báo giá chờ duyệt vượt hạn mức; danh sách Sales hoạt động để phân bổ.",
        "Kiểm tra luồng phê duyệt (Approval Workflow) và tính chính xác của thuật toán chia Lead."
      ],
      [
        <Text weight="semibold">Kitchen (Bộ phận Bếp)</Text>,
        "Xem danh sách món ăn tiệc cưới đã chốt, quản lý định lượng nguyên liệu (BOM). Không xem thông tin tiền.",
        "Hợp đồng tiệc đã ký có trạng thái 'Đã chốt Menu'; danh mục 100 món ăn kèm định lượng nguyên liệu.",
        "Xác minh thông tin nhạy cảm (giá cả, chiết khấu) hoàn toàn bị ẩn khỏi màn hình nhà bếp."
      ],
      [
        <Text weight="semibold">Banquet Manager (Quản lý sảnh)</Text>,
        "Xem sơ đồ bố trí sảnh, sắp xếp bàn tiệc, quản lý checklist thiết bị và phân công phục vụ.",
        "Sơ đồ sảnh Diamond/Ruby; danh sách 50 trang thiết bị (Micro, Projector, Sân khấu); danh sách nhân viên phục vụ.",
        "Xác nhận sơ đồ bàn tiệc hiển thị chính xác theo cấu hình số khách của hợp đồng."
      ],
      [
        <Text weight="semibold">Accountant (Kế Toán)</Text>,
        "Xác nhận đặt cọc (Deposit), ghi nhận phiếu thu, lập hóa đơn quyết toán đồ uống phát sinh và hư hỏng đồ.",
        "Tài khoản kế toán kết nối cổng thanh toán giả lập; báo giá tiệc cưới trạng thái 'Chờ đóng cọc'.",
        "Đảm bảo trạng thái tiệc chuyển từ 'Hold' sang 'Booked' ngay khi kế toán nhấn xác nhận đã nhận cọc."
      ],
      [
        <Text weight="semibold">Admin (Quản trị hệ thống)</Text>,
        "Cấu hình sảnh (dung tích, đơn giá sàn theo mùa), quản trị danh mục thực đơn, phân quyền tài khoản.",
        "Quyền tối cao (SuperAdmin); bảng cấu hình tham số hệ thống.",
        "Kiểm thử khả năng phục hồi dữ liệu và chặn đổi quyền trái phép."
      ]
    ];

    return (
      <Stack gap={16}>
        <H2>Yêu Cầu Dữ Liệu Kiểm Thử & Ma Trận Phân Quyền</H2>
        <Text tone="secondary">
          Bảng dưới đây định nghĩa phân quyền truy cập dữ liệu CRM Wedding ERP và dữ liệu giả lập cần chuẩn bị để chạy thử nghiệm.
        </Text>
        <Table
          headers={tableHeaders}
          rows={tableRows}
          columnAlign={["left", "left", "left", "left"]}
          striped
        />
      </Stack>
    );
  };

  const renderAutomation = () => {
    return (
      <Stack gap={16}>
        <H2>Phân Khai Thử Nghiệm: Automation (API, E2E) vs Manual Exploratory</H2>
        <Grid columns={2} gap={16}>
          <Card style={{ flex: 1 }}>
            <CardHeader trailing={<Pill active>API & E2E</Pill>}>
              KỊCH BẢN NÊN TỰ ĐỘNG HÓA (AUTOMATION CANDIDATES)
            </CardHeader>
            <CardBody>
              <Stack gap={12}>
                <Text weight="semibold">Tập trung vào logic nghiệp vụ cốt lõi, công thức tính toán và các tác vụ nền:</Text>
                <Divider />
                <Stack gap={10}>
                  <Text weight="medium" tone="primary">1. API Kiểm Tra Sảnh Trống (Hall Availability API)</Text>
                  <Text size="small" tone="secondary">
                    - Kiểm tra khả năng trả về danh sách sảnh trống dựa trên ngày/ca.
                    - Tần suất gọi lớn từ mobile/web, cần tự động hóa kiểm thử hiệu năng (Performance Test).
                  </Text>
                  
                  <Text weight="medium" tone="primary">2. Core Engine Tính Giá Tiệc (Pricing & Promo Engine)</Text>
                  <Text size="small" tone="secondary">
                    - Unit/Integration Test cho công thức: [Tổng tiền = (Giá bàn x Số bàn) + Dịch vụ + Phát sinh - Chiết khấu + VAT].
                    - Chạy tự động hóa với bộ dữ liệu kiểm thử biên đầu vào lớn để tránh sai sót kế toán.
                  </Text>

                  <Text weight="medium" tone="primary">3. Luồng Quá Hạn Cọc (Deposit Expiry Cron Job)</Text>
                  <Text size="small" tone="secondary">
                    - Chạy tự động hóa giả lập thời gian để đảm bảo sảnh tự động giải phóng sau 48h quá hạn cọc mà không có phiếu thu.
                  </Text>

                  <Text weight="medium" tone="primary">4. E2E Luồng Happy Path Khép Kín</Text>
                  <Text size="small" tone="secondary">
                    - Luồng: Nhận Lead -> Tạo Báo giá -> Xác nhận Hold sảnh -> Thanh toán cọc đợt 1 -> Tự động sinh hợp đồng pháp lý.
                  </Text>
                </Stack>
              </Stack>
            </CardBody>
          </Card>

          <Card style={{ flex: 1 }}>
            <CardHeader trailing={<Pill active>Manual Exploratory</Pill>}>
              KỊCH BẢN NÊN KIỂM THỬ THỦ CÔNG (EXPLORATORY TESTING)
            </CardHeader>
            <CardBody>
              <Stack gap={12}>
                <Text weight="semibold">Tập trung vào trải nghiệm người dùng, độ nhạy của AI và tương tác phần cứng:</Text>
                <Divider />
                <Stack gap={10}>
                  <Text weight="medium" tone="primary">1. Giao Diện Sơ Đồ Sảnh Kéo Thả (Floor Plan UI/UX)</Text>
                  <Text size="small" tone="secondary">
                    - Thao tác kéo thả bàn tiệc, đổi vị trí sân khấu, lối đi cô dâu chú rể.
                    - Rất khó viết script E2E ổn định; nên test thủ công trên nhiều trình duyệt khác nhau để kiểm tra giật lag.
                  </Text>

                  <Text weight="medium" tone="primary">2. Khả năng Nhận Diện của AI Assistant</Text>
                  <Text size="small" tone="secondary">
                    - Gửi các đoạn chat lộn xộn, viết tắt, không dấu, sai ngữ pháp từ khách hàng ("đặt tiệc cưới tầm 40 mâm ở sảnh kim cương tối chủ nhật tuần sau tầm bn xiền e").
                    - Kiểm thử độ nhạy bén và độ chính xác của AI trong việc phân tích ý định (Intent Extraction) để sinh báo giá nháp.
                  </Text>

                  <Text weight="medium" tone="primary">3. Hiển thị Mobile Responsive Ngoài Thực Địa</Text>
                  <Text size="small" tone="secondary">
                    - Banquet Manager điều phối sảnh bằng iPad, Nhân viên bếp xem danh sách món trên điện thoại.
                    - Kiểm thử thủ công trên các thiết bị thực tế dưới ánh sáng mạnh/yếu của sảnh tiệc.
                  </Text>
                </Stack>
              </Stack>
            </CardBody>
          </Card>
        </Grid>
      </Stack>
    );
  };

  const renderUAT = () => {
    return (
      <Stack gap={16}>
        <H2>Kịch Bản Thử Nghiệm Chấp Nhận Người Dùng (UAT Scenarios)</H2>
        <Text tone="secondary">
          Dành riêng cho Đội ngũ Kinh doanh tiệc (Wedding Sales Team) giả lập một ngày làm việc thực tế tại nhà hàng.
        </Text>
        <Stack gap={12}>
          <Card>
            <CardHeader trailing={<Pill>Kịch Bản UAT 1</Pill>}>
              BÁN HÀNG DỒN DẬP & GIỮ CHỖ TRỰC TIẾP (High-Pressure Live Sale)
            </CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text weight="semibold">Mô tả tình huống:</Text>
                <Text tone="secondary">
                  Nhà hàng đang tổ chức ngày hội cưới (Wedding Fair), khách hàng đến xem và chốt sảnh dồn dập tại quầy. Sales phải tư vấn sảnh trống tức thì và in báo giá trong vòng 3 phút để không mất khách.
                </Text>
                <Divider />
                <Text weight="medium">Các bước Sales thực hiện thử nghiệm:</Text>
                <Text size="small" tone="secondary">
                  1. Mở nhanh Dashboard lịch sảnh để xem sảnh "Diamond" còn trống ngày 25/12/2026 ca trưa hay không.<br />
                  2. Khách chốt giữ sảnh, Sales click trực tiếp vào ô lịch sảnh đó để mở Form tạo nhanh báo giá.<br />
                  3. Chọn gói Set Menu 6.500.000đ/bàn, áp dụng chương trình khuyến mãi Wedding Fair (Tặng bia, miễn phí thử món).<br />
                  4. Nhấn lưu để khóa sảnh Diamond trong vòng 48 giờ.<br />
                  5. Nhấn xuất file PDF báo giá và in gửi trực tiếp khách ký nháp giữ chỗ.
                </Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader trailing={<Pill>Kịch Bản UAT 2</Pill>}>
              BIẾN ĐỘNG YÊU CẦU LIÊN TỤC TRƯỚC NGÀY CƯỚI (Dynamic Changes Workflow)
            </CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text weight="semibold">Mô tả tình huống:</Text>
                <Text tone="secondary">
                  Cách ngày cưới 10 ngày, cô dâu chú rể bất ngờ đổi ngày tiệc vì lý do gia đình, giảm quy mô từ 50 bàn xuống còn 40 bàn, đồng thời yêu cầu thay đổi 3 món trong thực đơn Set Menu đã ký để phục vụ khách ăn chay.
                </Text>
                <Divider />
                <Text weight="medium">Các bước Sales thực hiện thử nghiệm:</Text>
                <Text size="small" tone="secondary">
                  1. Tìm kiếm và mở Hợp đồng tiệc cưới của khách hàng.<br />
                  2. Thao tác đổi ngày tiệc trên hệ thống, kiểm tra xem hệ thống có tự động báo sảnh mới còn trống hay không.<br />
                  3. Thay đổi số lượng bàn từ 50 xuống 40 bàn. Kiểm tra xem hệ thống có tự động áp dụng lại mức phạt giảm số lượng bàn ngoài quy định tối thiểu hay không.<br />
                  4. Mở danh sách món ăn, xóa món thịt heo quay, thay bằng món nấm xào rau củ. Kiểm tra đơn giá bàn tiệc tự động cập nhật chênh lệch.<br />
                  5. Hệ thống tự động tạo Phụ lục hợp đồng (Addendum), tự động tính toán lại số tiền cọc đợt 2 kế toán cần thu.<br />
                  6. Gửi duyệt phụ lục hợp đồng lên Sale Manager duyệt nhanh.
                </Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader trailing={<Pill>Kịch Bản UAT 3</Pill>}>
              GIỜ G: PHÁT SINH CUỐI TIỆC & THANH TOÁN QUYẾT TOÁN (Real-time Settlement)
            </CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text weight="semibold">Mô tả tình huống:</Text>
                <Text tone="secondary">
                  Tiệc cưới đang diễn ra sôi động, khách phát sinh thêm 3 bàn dự phòng (bàn dự bị) ngoài hợp đồng gốc, đồng thời gọi thêm 15 két bia Heineken và làm vỡ 2 chiếc ly thủy tinh cao cấp của nhà hàng. Sales và Banquet Manager phải quyết toán nhanh để tiệc xong khách thanh toán ngay tại sảnh.
                </Text>
                <Divider />
                <Text weight="medium">Các bước Banquet & Sales thực hiện thử nghiệm:</Text>
                <Text size="small" tone="secondary">
                  1. Trong lúc tiệc đang chạy, Banquet Manager sử dụng iPad mở app ERP, chọn tiệc đang diễn ra và nhấn nút "Thêm bàn dự phòng" (+3 bàn).<br />
                  2. Bộ phận bếp nhận thông báo tức thì trên tablet nhà bếp để lập tức chuẩn bị thêm 3 bàn ăn chay/mặn tương ứng.<br />
                  3. Banquet Manager ghi nhận đồ uống phát sinh thực tế tiêu thụ (+15 két bia) và ghi nhận hư hại tài sản (+2 ly vỡ).<br />
                  4. Ngay khi tiệc kết thúc, Sales nhấn nút "Quyết Toán Tiệc" (Settlement). Hệ thống tính toán toàn bộ số tiền cọc đã đóng, trừ đi chi phí gốc, cộng thêm bàn phát sinh, đồ uống và tiền đền bù ly vỡ để ra con số thanh toán đợt cuối.<br />
                  5. Sales xuất hóa đơn quyết toán chuẩn xác, in hóa đơn ngay tại sảnh và cùng kế toán quầy thu tiền khách cưới trước khi họ ra về.
                </Text>
              </Stack>
            </CardBody>
          </Card>
        </Stack>
      </Stack>
    );
  };

  const renderAC = () => {
    return (
      <Stack gap={16}>
        <H2>Khung Tiêu Chí Nghiệm Thu (Acceptance Criteria Template)</H2>
        <Text tone="secondary">
          Tất cả các Form và chức năng trong module CRM Wedding ERP bắt buộc phải được thiết kế tài liệu nghiệp vụ (BA) và kiểm thử (QA) dựa trên cấu trúc tiêu chuẩn dưới đây:
        </Text>
        <Card>
          <CardHeader>MẪU KHUNG AC TIÊU CHUẨN (User Story & Gherkin Format)</CardHeader>
          <CardBody>
            <Stack gap={12}>
              <H3>1. Mô Tả Tổng Quan (User Story)</H3>
              <Code style={{ display: "block", padding: "12px", whiteSpace: "pre-wrap" }}>
                {`AS A [Vai trò người dùng - e.g. Nhân viên Sales tiệc]
I WANT TO [Hành động muốn thực hiện - e.g. Tạo một báo giá tiệc cưới mới]
SO THAT [Giá trị nghiệp vụ đem lại - e.g. Có thể gửi thông tin chi phí chuẩn xác cho khách hàng]` }
              </Code>
              
              <H3>2. Các Tiêu Chí Nghiệm Thu Chi Tiết (Acceptance Criteria)</H3>
              
              <Text weight="semibold" tone="primary">AC 1: Ràng buộc nhập liệu dữ liệu (Data & Form Validation)</Text>
              <Text size="small" tone="secondary">
                - Hệ thống phải hiển thị dấu sao đỏ (*) tại các trường bắt buộc: Tên khách hàng, Số điện thoại, Sảnh tiệc cưới, Ngày tiệc dự kiến, Số lượng bàn tối thiểu.<br />
                - Các trường số điện thoại phải được validate đúng định dạng số (10 chữ số).<br />
                - Ngày tiệc cưới dự kiến phải lớn hơn ngày hiện tại ít nhất 3 ngày (Quy tắc nhà hàng không nhận tiệc cưới khẩn cấp dưới 3 ngày chuẩn bị).
              </Text>

              <Text weight="semibold" tone="primary">AC 2: Logic xử lý nghiệp vụ (Business Rules Logic)</Text>
              <Text size="small" tone="secondary">
                - Đơn giá bàn tiệc mặc định phải tự động lấy từ danh mục Set Menu đã chọn.<br />
                - Nếu ngày tiệc cưới rơi vào ngày thứ Bảy hoặc Chủ Nhật, hệ thống phải tự động cộng thêm phụ phí cuối tuần là 10% trên đơn giá bàn tiệc.<br />
                - Nếu tổng giá trị dịch vụ phụ trợ đạt trên 20.000.000đ, hệ thống tự động áp dụng mã giảm giá 5% cho tổng hóa đơn.
              </Text>

              <Text weight="semibold" tone="primary">AC 3: Phân quyền hành động (Role-based Actions)</Text>
              <Text size="small" tone="secondary">
                - Nhân viên Sales chỉ được chọn mức chiết khấu tối đa 5%. Mọi mức chiết khấu {">"} 5% phải bị khóa mờ nút "Gửi Báo Giá", thay vào đó hiển thị nút "Gửi Trưởng Phòng Phê Duyệt".<br />
                - Trưởng phòng Sales (Sale Manager) mới có quyền nhấn nút "Phê Duyệt" để kích hoạt báo giá có mức chiết khấu cao.
              </Text>

              <Text weight="semibold" tone="primary">AC 4: Tích hợp hệ thống (System Integration)</Text>
              <Text size="small" tone="secondary">
                - Khi báo giá được xác nhận trạng thái "Khách Chốt", hệ thống phải tự động đồng bộ trạng thái sảnh cưới tương ứng trên giao diện "Lịch Quản Lý Sảnh" thành trạng thái "Giữ sảnh tạm thời (Hold)" trong 48 giờ.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Stack>
    );
  };

  const renderDocs = () => {
    const todos = [
      { id: "doc-ug-step", content: "User Guide: Tài liệu hướng dẫn từng bước (Step-by-step) chi tiết cho 6 vai trò sử dụng hệ thống.", status: "completed" as const },
      { id: "doc-ug-faq", content: "User Guide: Danh mục câu hỏi thường gặp (FAQ) và phương án xử lý nhanh sự cố thao tác (Ví dụ: Thanh toán lỗi).", status: "completed" as const },
      { id: "doc-pf-bpmn", content: "Process Flow: Sơ đồ quy trình nghiệp vụ BPMN 2.0 thể hiện luồng dữ liệu khép kín từ Lead -> Quyết toán.", status: "completed" as const },
      { id: "doc-pf-swim", content: "Process Flow: Phân tách rõ ràng trách nhiệm xử lý giữa các phòng ban bằng Swimlanes (Kinh doanh, Kế toán, Bếp, Sảnh).", status: "completed" as const },
      { id: "doc-fl-list", content: "Form List: Bảng kê danh mục toàn bộ biểu mẫu/giao diện sử dụng trong phân hệ CRM (Mã form, epic cha, quyền sử dụng).", status: "completed" as const },
      { id: "doc-ff-fields", content: "Form Functions: Đặc tả chi tiết cấu trúc trường dữ liệu của từng Form (Field name, Type, Validation rule).", status: "completed" as const },
      { id: "doc-ff-con", content: "Form Functions: Quy tắc xử lý các nút bấm hành động (Ví dụ: Sử dụng Pessimistic Locking cho nút 'Hold sảnh' để chống tranh chấp).", status: "completed" as const },
      { id: "doc-tc-suit", content: "Test Cases: Tập kịch bản kiểm thử chi tiết bao gồm cả Happy Path và 100% các tình huống biên nguy cơ cao.", status: "completed" as const }
    ];

    return (
      <Stack gap={16}>
        <H2>Checklist Danh Mục Tài Liệu Bắt Buộc (BA & QA Deliverables)</H2>
        <Text tone="secondary">
          Để bàn giao dự án CRM ERP thành công, toàn bộ tài liệu dưới đây phải được viết đầy đủ, chuẩn hóa và lưu trữ trên Wiki dự án để phục vụ bảo trì và đào tạo nhân sự mới.
        </Text>
        <TodoListCard
          todos={todos}
          defaultExpanded
        />
      </Stack>
    );
  };

  return (
    <div style={containerStyle}>
      <Stack gap={24}>
        <Row align="center" gap={12}>
          <Stack gap={4}>
            <H1 style={{ margin: 0 }}>Chiến Lược & Quy Trình Kiểm Thử CRM Wedding ERP</H1>
            <Row gap={8} align="center">
              <Pill active>QA Lead / Test BA Deliverable</Pill>
              <Text tone="secondary" size="small">Phân hệ quản lý khách hàng tiệc cưới & sự kiện nhà hàng</Text>
            </Row>
          </Stack>
        </Row>

        <Divider />

        <Row gap={8} wrap>
          {tabs.map(tab => (
            <Pill
              key={tab.id}
              active={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </Pill>
          ))}
        </Row>

        <Card variant="borderless" style={{ backgroundColor: theme.fill.quaternary, padding: "16px", borderRadius: "8px" }}>
          <CardBody style={{ padding: 0 }}>
            {activeTab === "scope" && renderScope()}
            {activeTab === "testcases" && renderTestCases()}
            {activeTab === "data" && renderDataAndRoles()}
            {activeTab === "automation" && renderAutomation()}
            {activeTab === "uat" && renderUAT()}
            {activeTab === "ac" && renderAC()}
            {activeTab === "docs" && renderDocs()}
          </CardBody>
        </Card>
      </Stack>
    </div>
  );
}