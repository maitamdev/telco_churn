# Giao diện doanh nghiệp · phiên bản 2.0

Điều chỉnh nội dung giao diện: đã bỏ mô tả phụ dưới tiêu đề/panel, các đoạn gợi ý chung, giải thích học thuật, chú thích KPI, breadcrumb, footer phiên bản và khối thông tin kỹ thuật ở sidebar trên cả 5 trang. Giữ nhãn trường/nút, số hồ sơ, phạm vi số liệu, giới hạn CSV, mã khách đang xem và lỗi đầu vào. Các nhận xét/phương pháp/giới hạn của thí nghiệm vẫn có trong hồ sơ báo cáo; không hiển thị lặp lại trong luồng thao tác.

Điều chỉnh theo phản hồi tiếp theo: bỏ vạch xanh bên trái menu đang chọn, bỏ khung focus khi bấm chuột và các đường bao trang trí ở KPI, panel, badge, expander. Dùng nền nhẹ và chữ đậm để nhận biết mục chọn; điều hướng bàn phím được nhận biết bằng nền và gạch chân.

Yêu cầu: làm lại Streamlit theo hướng công cụ nội bộ doanh nghiệp, gọn và dễ thao tác. Triển khai trên chính dự án; dùng dữ liệu và pipeline hiện có.

## Những gì đã thay đổi

- Nhận diện TELCO Customer Operations; thanh điều hướng bên trái, đường dẫn trang, nền xám sáng, khối nội dung trắng, xanh trầm làm màu nhấn.
- Chuẩn hóa cỡ chữ, khoảng cách, bảng, biểu mẫu, nhãn trạng thái và nút hành động. Không thêm tên nhân viên, doanh thu hoặc biểu đồ thời gian không có trong dữ liệu.
- Tổng quan: KPI có phạm vi dữ liệu rõ ràng; biểu đồ tương tác theo hợp đồng và thâm niên được tính từ train.
- Bảng hồ sơ: tìm mã, lọc hợp đồng/trạng thái, xuất danh sách đã lọc; chọn một dòng để điền sẵn trang phân tích.
- Phân tích khách hàng: ba tab Hồ sơ / Dịch vụ / Thanh toán; kết quả nằm cạnh biểu mẫu. Dự đoán chỉ chạy khi bấm nút.
- Nhập danh sách: khu vực chọn CSV, mẫu tải xuống, số dòng hợp lệ/lỗi và bảng kết quả với thanh xác suất, tên cột tiếng Việt.
- Hiệu quả mô hình: bảng so sánh, ma trận nhầm lẫn và ý nghĩa FP/FN; các bằng chứng chi tiết chia thành tab.
- Ngưỡng & giải thích: biểu đồ tương tác, chỉ số cập nhật theo slider, importance và quy tắc chọn ngưỡng.
- Giữ nhãn dữ liệu mẫu IBM và giới hạn của xác suất để giao diện không tạo ấn tượng đây là dữ liệu doanh nghiệp đang vận hành.

## Tệp triển khai

app.py; .streamlit/config.toml; ui/styles.css; ui/components.py; ui/charts.py; ui/data_views.py; ui/overview.py; ui/scoring.py; ui/results.py.

Công nghệ: Streamlit 1.67.0, CSS riêng và Altair 6.3.0 đã có trong requirements. Không đổi framework, không thêm dịch vụ bên ngoài. CSS dùng thuộc tính data-testid của phiên bản Streamlit đã khóa; cần kiểm lại giao diện nếu nâng thư viện.

## Kiểm chứng thực tế

- 54 tests đạt trên venv chính và 54 tests trên venv sạch.
- Tìm 8499-BRXTD trả đúng 1 hồ sơ; mã không tồn tại trả thông báo không có kết quả.
- Trình duyệt: chọn hồ sơ 8499-BRXTD → Phân tích hồ sơ → tự điền mã, giới tính, tenure=18 và thông tin dịch vụ/thanh toán.
- Dự đoán hồ sơ đó hiển thị 5,6%, khớp xác suất 0,055513879... của pipeline.
- CSV mẫu có lỗi vẫn cho 3 dòng: 1 hợp lệ, 2 lỗi; cột kết quả hiển thị đúng.
- Slider về 0 trên validation: precision 26,5%, recall 100%, đánh dấu 1.409 khách; ngưỡng chính thức vẫn 0,478803.
- Trang hiệu quả hiển thị precision 0,508, recall 0,807, F1 0,623, ROC-AUC 0,843 và TP=302/FP=293/FN=72/TN=742.
- Không ghi nhận lỗi console ở các trang đã kiểm. Ảnh ở reports/evidence/ui_v2_*.jpg.
- Dữ liệu, split, pipeline và kết quả mô hình tiếp tục khớp manifest của thí nghiệm.

## Nhật ký và gói bàn giao

Nhật ký bổ sung tại logs/NHAT_KY_THUC_HIEN.md. Bộ ZIP kỹ thuật được cập nhật; bản trước đổi giao diện được giữ tại dist/DU_AN_TELCO_CHURN_KY_THUAT_V1.zip. Gói ZIP không chứa venv hay bản sao thử nghiệm.

Đây là bản nâng giao diện và thao tác của demo đồ án. Báo cáo và đóng góp tự thực hiện của nhóm vẫn theo trạng thái đã ghi nhận trước đó.

