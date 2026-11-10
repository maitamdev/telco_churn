**KẾ HOẠCH TỔNG THỂ — PHIÊN BẢN 1.0**

Ngày lập: 10/11/2026. Phạm vi lượt hiện tại: chuẩn bị đầy đủ trước triển khai. Trạng thái kỹ thuật: chưa huấn luyện/chưa có app. Nội dung công việc chi tiết ở 06_CONG_VIEC_VA_TIEN_DO.md, thông số ở planning/project_spec.json.

**Kết quả người dùng sẽ nhận**

| Mã | Sản phẩm cuối dự kiến | Điều kiện bàn giao |
|---|---|---|
| D01 | Dữ liệu gốc hoặc cách tải có kiểm chứng, data dictionary, nhật ký làm sạch | Nguồn/hash được ghi; mọi số liệu chạy lại được |
| D02 | Module Python và notebook giải thích | Chạy từ đầu, tách trách nhiệm, không phụ thuộc thứ tự bấm ô |
| D03 | Kết quả thí nghiệm | Baseline + 2 mô hình, CV/tuning, threshold, test, phân tích lỗi |
| D04 | Pipeline joblib + metadata + manifest | Tải lại đúng; schema/ngưỡng/phiên bản/training run có thể đối soát |
| D05 | Ứng dụng Streamlit tiếng Việt | 5 trang, dự đoán thật, CSV, đánh giá, ngưỡng và giải thích |
| D06 | Bản báo cáo DOCX và PDF | Cùng nội dung, theo mẫu sẽ nhận, tối đa 99 trang toàn tệp |
| D07 | Slide PPTX, kịch bản demo, bộ câu hỏi vấn đáp | Nội dung khớp báo cáo, từng thành viên thực hành |
| D08 | README, requirements và gói ZIP | Cài mới/chạy được; có tệp mẫu; không đưa môi trường ảo vào gói |

DOCX và PDF là hai định dạng của cùng một báo cáo. Hướng dẫn cho phép PDF hoặc DOCX; chuẩn bị cả hai để thuận tiện chỉnh sửa và nộp. Không tạo nội dung giả để điền số trang.

**Phạm vi đã quyết định**

- Bài toán phân loại nhị phân, nhãn Churn=Yes là positive. Demo hỗ trợ ưu tiên rà soát khách hàng có nguy cơ.
- Dữ liệu tabular IBM Telco; không mở rộng sang chatbot, dữ liệu ảnh hay dự báo doanh thu.
- Bộ cốt lõi gồm baseline, Logistic Regression và Random Forest. Không gọi Dummy là một trong hai mô hình học máy.
- Tám hình EDA có nhận định, cùng các hình riêng cho đánh giá và giải thích mô hình.
- Pipeline duy nhất cho biến đổi học từ dữ liệu và inference. Giao diện không có phiên bản tiền xử lý khác.
- Không dùng test chọn đặc trưng, siêu tham số, mô hình hay ngưỡng. Test dùng để xác nhận cuối và mô tả lỗi.
- Không cam kết accuracy, số điểm môn học hay khả năng giữ chân khách thực tế trước khi có bằng chứng.
- Không tự publish/deploy/push. Các hoạt động local, viết/sửa/kiểm thử trong phạm vi đã giao không cần hỏi lại từng bước.

**Mục tiêu đo được**

Mục tiêu quy trình: đáp ứng đủ ma trận yêu cầu; app/report dùng cùng run; cài mới và tái lập được; nhóm hiểu và chỉnh sửa được các phần đã dùng.

Mục tiêu mô hình: AP vượt baseline, báo cả precision/recall/F1 và các lỗi. Giả định chiến dịch ban đầu là precision tối thiểu 0,50, chọn ngưỡng để recall cao nhất trong tập thỏa điều kiện; hướng tới recall 0,80. Đây là mục tiêu nghiên cứu tự đặt, không phải yêu cầu giảng viên hay kết quả bảo đảm. Trạng thái đạt/chưa đạt được báo thật; quy trình fallback được quy định trước ở tài liệu thí nghiệm.

**Các mốc thực hiện, không gắn deadline**

| Mốc | Nội dung | Điều kiện chuyển mốc |
|---|---|---|
| M0 | Đặc tả và chuẩn bị | Các tài liệu khớp nhau; checklist có thể kiểm tra; thông tin chưa có được đánh dấu |
| M1 | Môi trường, nguồn, schema, chia tập | Cài tương thích; raw hash đúng; quality log và split manifest |
| M2 | EDA và bản thảo dữ liệu | 8 hình có bảng nguồn, nhận định, nhãn và cỡ mẫu |
| M3 | Pipeline, baseline, CV, tuning | ≥2 mô hình thật; log CV/tuning; không rò rỉ; model selection theo quy tắc |
| M4 | Ngưỡng, đóng băng lựa chọn, test, giải thích | Có selection record trước test; metrics và artifacts nhất quán |
| M5 | Streamlit và kiểm tra chức năng | Form/CSV/module cùng kết quả; trang đánh giá đọc kết quả đã lưu |
| M6 | Nội dung báo cáo và áp dụng mẫu | Mẫu đã có cho định dạng cuối; mọi bảng/hình dẫn được về kết quả; <100 trang |
| M7 | Slide, tái lập môi trường sạch, bảo vệ, đóng gói | Kiểm tra đạt, hồ sơ đủ, nhóm thực hành giải thích |

Có thể soạn phần bài toán/phương pháp, mẫu bảng và kịch bản bảo vệ từ sớm. Không viết kết quả/kết luận thực nghiệm trước M4. M6 về nội dung không phải đợi mẫu; chỉ bước định dạng cuối cần mẫu người dùng gửi.

**Phân công đề xuất cho 5 người**

| Vai trò | Chủ trì | Phải hiểu thêm | Minh chứng |
|---|---|---|---|
| R1 | Bài toán, nguồn, schema, làm sạch | Leakage, split, cột TotalCharges | Data dictionary, cleaning log, giải thích quyết định |
| R2 | EDA, hình/bảng và nhận định | Tỷ lệ nhóm, cỡ mẫu, tương quan/nhân quả | Notebook và hình đã đối soát |
| R3 | Pipeline, baseline, CV, tuning | Ngưỡng, AP, chọn mô hình | Code chạy lại, CV logs, cấu hình |
| R4 | Đánh giá, threshold, phân tích lỗi | Cơ chế LR/RF và dataset | Metrics, error cases, diễn giải nghiệp vụ |
| R5 | Streamlit, tích hợp, kiểm thử, đóng gói | Pipeline, schema, cách báo cáo metric | App, test evidence, README |

Tất cả cùng viết/rà soát báo cáo và tập vấn đáp toàn bài. Đây là phân công dự kiến theo vị trí, chưa phải khai báo ai đã làm. Tên/MSSV/lớp/GV chờ bổ sung, không ngăn triển khai kỹ thuật.

**Phần nâng cao, chỉ làm khi nền tảng đã đạt**

| Hạng mục | Khi nào có ích | Điều kiện |
|---|---|---|
| Gradient Boosting | Muốn thêm đối chứng phi tuyến | Khai báo trước khi mở test; cùng split/CV/metric |
| Hiệu chỉnh xác suất | Cần diễn giải xác suất theo tần suất đáng tin hơn | Đánh giá calibration; mọi calibration trong train/CV, không dùng test |
| Bootstrap CI | Cần thể hiện bất định test | Chốt trước cách tính, không dùng CI để tinh chỉnh sau test |
| SHAP | Có nhu cầu giải thích từng khách | Kiểm tra đúng không gian đặc trưng; phân biệt giải thích với nguyên nhân |
| MLP/PCA/phân cụm | Mục tiêu nghiên cứu mới có lý do | Không tự thêm chỉ để đủ thuật toán đã học |

Không mở rộng theo test score. Sau khi xem test, thay đổi mang tính nghiên cứu mới cần cách kiểm chứng độc lập mới; không gọi test đã tái sử dụng là kiểm tra cuối chưa từng thấy.

**Rủi ro đã có phương án**

- Streamlit chưa cài trong Python hiện tại: tạo venv và kiểm tra dependencies ở M1, không giả định môi trường đang sẵn.
- PDF/slide không thống nhất về cuối kỳ: theo PDF hướng dẫn cuối kỳ và yêu cầu hiện tại; lịch/mẫu có thể bổ sung.
- Dữ liệu nguồn đổi: dừng ở kiểm tra hash, ghi phiên bản mới trước khi tiếp tục, không thay dữ liệu im lặng.
- Không đạt mục tiêu recall/precision: giữ kết quả thật, phân tích giới hạn, không tìm ngưỡng trên test để làm đẹp số.
- Mẫu báo cáo đến muộn: soạn nội dung có cấu trúc, hình/bảng tách riêng, áp style sau.
- Demo lỗi mạng: app dùng model và mẫu local sau cài đặt; không phụ thuộc API ngoài.

Thay đổi đặc tả được ghi ngày, lý do, ảnh hưởng, trạng thái đã xem test hay chưa. Kiểm tra tiến độ bằng bằng chứng đầu ra, không chỉ đánh dấu đã viết code.
