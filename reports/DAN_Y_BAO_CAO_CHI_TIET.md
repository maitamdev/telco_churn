# Cấu trúc báo cáo theo mẫu đã nhận

Phiên bản nâng cấp ngày 10/11/2026. Báo cáo `reports/BAOCAO-TTNT.docx` và PDF: 68 trang, 6 chương, 19 hình, 28 bảng và 15 nguồn tham khảo.

Mẫu gốc: `reports/templates/MAU_BAO_CAO_GOC.docx`. Giữ định dạng mẫu; thông tin cá nhân/lớp/giảng viên để trống theo yêu cầu. Hai bìa, lời cảm ơn, lời cam đoan, mục lục và danh mục hình/bảng tự động, danh mục từ viết tắt; tài liệu tham khảo ở cuối, không có phụ lục.

## Dàn ý đã triển khai

- 1. TỔNG QUAN ĐỀ TÀI
  - 1.1. Đặt vấn đề
  - 1.2. Mục tiêu đề tài
    - 1.2.1. Mục tiêu tổng quát
    - 1.2.2. Mục tiêu cụ thể
    - 1.2.3. Câu hỏi nghiên cứu
  - 1.3. Đối tượng và phạm vi đề tài
    - 1.3.1. Đối tượng nghiên cứu
    - 1.3.2. Phạm vi thực hiện
  - 1.4. Phương pháp thực hiện
  - 1.5. Cấu trúc báo cáo
- 2. CƠ SỞ LÝ THUYẾT
  - 2.1. Bài toán phân loại khách hàng rời dịch vụ
  - 2.2. Tiền xử lý dữ liệu dạng bảng
    - 2.2.1. Xử lý giá trị thiếu và chuẩn hóa
    - 2.2.2. Mã hóa thuộc tính phân loại
    - 2.2.3. Pipeline và phòng tránh rò rỉ dữ liệu
  - 2.3. Các mô hình phân loại
    - 2.3.1. Mô hình đối chứng DummyClassifier
    - 2.3.2. Logistic Regression
    - 2.3.3. Random Forest
  - 2.4. Kiểm định chéo và lựa chọn siêu tham số
  - 2.5. Các độ đo đánh giá
    - 2.5.1. Ma trận nhầm lẫn
    - 2.5.2. Accuracy, precision, recall và F1
    - 2.5.3. ROC-AUC và Average Precision
  - 2.6. Độ quan trọng thuộc tính
  - 2.7. Công nghệ xây dựng ứng dụng
- 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
  - 3.1. Phân tích yêu cầu hệ thống
    - 3.1.1. Yêu cầu chức năng
    - 3.1.2. Yêu cầu phi chức năng
  - 3.2. Nguồn dữ liệu và cấu trúc thuộc tính
    - 3.2.1. Nguồn và quy mô
    - 3.2.2. Kiểu dữ liệu và giá trị thiếu
  - 3.3. Thiết kế quy trình chuẩn bị dữ liệu
    - 3.3.1. Làm sạch và kiểm tra ngoại lai
    - 3.3.2. Chia tập dữ liệu
    - 3.3.3. Phòng tránh sử dụng thông tin không phù hợp
  - 3.4. Phân tích khám phá dữ liệu
    - 3.4.1. Phân bố nhãn churn
    - 3.4.2. Churn theo loại hợp đồng
    - 3.4.3. Churn theo dịch vụ Internet
    - 3.4.4. Churn theo phương thức thanh toán
    - 3.4.5. Thời gian sử dụng và churn
    - 3.4.6. Cước hàng tháng và tổng cước
    - 3.4.7. Tương quan giữa các thuộc tính số
  - 3.5. Thiết kế kiến trúc hệ thống
  - 3.6. Thiết kế luồng xử lý và giao diện
    - 3.6.1. Luồng phân tích một khách hàng
    - 3.6.2. Luồng xử lý danh sách
    - 3.6.3. Luồng xem hiệu quả và khảo sát ngưỡng
- 4. XÂY DỰNG HỆ THỐNG
  - 4.1. Môi trường phát triển và tổ chức mã nguồn
    - 4.1.1. Môi trường thực nghiệm
    - 4.1.2. Tổ chức mã nguồn
  - 4.2. Xây dựng pipeline tiền xử lý
  - 4.3. Huấn luyện và lựa chọn mô hình
    - 4.3.1. Thiết lập tìm kiếm siêu tham số
    - 4.3.2. Cấu hình được chọn
    - 4.3.3. Lựa chọn ngưỡng trên validation
    - 4.3.4. Lưu mô hình và cố định lựa chọn
  - 4.4. Xây dựng ứng dụng Streamlit
    - 4.4.1. Màn hình tổng quan
    - 4.4.2. Màn hình phân tích khách hàng
    - 4.4.3. Màn hình nhập danh sách
    - 4.4.4. Màn hình hiệu quả mô hình
    - 4.4.5. Màn hình ngưỡng và giải thích
  - 4.5. Cấu hình và vận hành demo
  - 4.6. Phạm vi hỗ trợ của công cụ AI
- 5. KIỂM THỬ VÀ ĐÁNH GIÁ
  - 5.1. Mục tiêu và phạm vi đánh giá
  - 5.2. Kết quả kiểm định chéo
  - 5.3. Kết quả đánh giá trên test
    - 5.3.1. So sánh các mô hình và ngưỡng
    - 5.3.2. Ma trận nhầm lẫn và khối lượng sàng lọc
    - 5.3.3. Đường ROC và precision–recall
  - 5.4. Đánh giá lựa chọn ngưỡng
  - 5.5. Phân tích độ quan trọng thuộc tính
  - 5.6. Phân tích các trường hợp dự đoán sai
    - 5.6.1. Các trường hợp báo động nhầm
    - 5.6.2. Các trường hợp bỏ sót
  - 5.7. Đánh giá theo nhóm khách hàng
    - 5.7.1. Hợp đồng và loại dịch vụ Internet
    - 5.7.2. Giới tính và nhóm tuổi
  - 5.8. Độ bất định của kết quả đánh giá
  - 5.9. Độ tin cậy của xác suất dự đoán
  - 5.10. Khả năng ưu tiên hồ sơ theo năng lực xử lý
  - 5.11. Kiểm thử chức năng và tính tái lập
    - 5.11.1. Bộ kiểm thử tự động
    - 5.11.2. Kiểm thử giao diện và tình huống dữ liệu
    - 5.11.3. Kiểm chứng số liệu và môi trường sạch
  - 5.12. Đánh giá tổng hợp
- 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
  - 6.1. Kết luận
  - 6.2. Kết quả đạt được
  - 6.3. Giới hạn phạm vi của đề tài
  - 6.4. Hướng phát triển
    - 6.4.1. Bổ sung dữ liệu và xác định thời điểm dự báo
    - 6.4.2. Cải tiến đánh giá và lựa chọn mô hình
    - 6.4.3. Hoàn thiện khả năng sử dụng

## Danh mục hình

- Hình 3.1. Phân bố nhãn Churn trên tập train
- Hình 3.2. Tỷ lệ churn theo loại hợp đồng trên train
- Hình 3.3. Tỷ lệ churn theo dịch vụ Internet trên train
- Hình 3.4. Tỷ lệ churn theo phương thức thanh toán trên train
- Hình 3.5. Phân bố thời gian sử dụng theo Churn trên train
- Hình 3.6. Phân bố cước hàng tháng theo Churn trên train
- Hình 3.7. Phân bố tổng cước theo Churn trên train
- Hình 3.8. Ma trận tương quan các biến số trên train
- Hình 4.1. Màn hình tổng quan khách hàng
- Hình 4.2. Màn hình phân tích một khách hàng
- Hình 4.3. Màn hình xử lý danh sách khách hàng từ CSV
- Hình 4.4. Màn hình đánh giá hiệu quả mô hình
- Hình 4.5. Màn hình khảo sát ngưỡng phân loại
- Hình 5.1. Ma trận nhầm lẫn của Random Forest trên test
- Hình 5.2. Đường ROC và precision–recall trên test
- Hình 5.3. Precision và recall theo ngưỡng trên validation
- Hình 5.4. Độ quan trọng thuộc tính trên validation
- Hình 5.5. Độ tin cậy của xác suất trên validation
- Hình 5.6. Khả năng bao phủ churn theo tỷ lệ hồ sơ được xem xét trên validation

## Danh mục bảng

- Bảng 1.1. Mục tiêu và tiêu chí đánh giá của đề tài
- Bảng 2.1. Ý nghĩa các kết quả phân loại trong bài toán churn
- Bảng 3.1. Các yêu cầu chức năng của hệ thống
- Bảng 3.2. Tổng quan bộ dữ liệu sử dụng
- Bảng 3.3. Từ điển dữ liệu Telco Customer Churn
- Bảng 3.4. Kết quả kiểm tra chất lượng và cách xử lý dữ liệu
- Bảng 3.5. Phân bố dữ liệu sau khi chia tập
- Bảng 3.6. Các thành phần trong kiến trúc hệ thống
- Bảng 4.1. Các thành phần chính của môi trường thực nghiệm
- Bảng 4.2. Tổ chức các thành phần mã nguồn và dữ liệu
- Bảng 4.3. Cấu hình các bước tiền xử lý
- Bảng 4.4. Không gian tìm kiếm siêu tham số
- Bảng 4.5. Kết quả lựa chọn ngưỡng trên validation
- Bảng 5.1. Kết quả kiểm định chéo trên tập train
- Bảng 5.2. Precision, recall và F1 của các cấu hình trên test
- Bảng 5.3. Accuracy, ROC-AUC và AP của các cấu hình trên test
- Bảng 5.4. Khối lượng sàng lọc của Random Forest theo hai ngưỡng
- Bảng 5.5. Mười thuộc tính có mức giảm AP trung bình cao nhất
- Bảng 5.6. Một số trường hợp FP trên test
- Bảng 5.7. Một số trường hợp FN trên test
- Bảng 5.8. Kết quả test theo hợp đồng và dịch vụ Internet
- Bảng 5.9. Kết quả test theo giới tính và nhóm tuổi
- Bảng 5.10. Khoảng ước lượng 95% trên test của các mô hình đã cố định
- Bảng 5.11. Brier và log loss trên validation
- Bảng 5.12. Đánh đổi giữa năng lực xử lý và khả năng bao phủ churn
- Bảng 5.13. Kết quả bộ kiểm thử tự động theo nhóm
- Bảng 5.14. Các tình huống kiểm tra chức năng ứng dụng
- Bảng 5.15. Kết quả kiểm chứng tính nhất quán và tái lập

## Kiểm chứng và phần nhóm cần làm

QA báo cáo kiểm 155 liên kết số trang, tất cả bảng với artifact và các thành phần định dạng với mẫu. 68 trang được xuất bằng Word và kiểm trực quan; SHA-256 trong `reports/evidence/report_qa.json`.

Các phần mới: 4.6 khai báo AI; 5.8 độ bất định; 5.9 chất lượng xác suất; 5.10 năng lực xử lý; kiểm thử/tái lập ở 5.11. Bộ slide riêng gồm 21 trang ở `reports/BAO_VE_TELCO_CHURN.pptx`, có QA bằng PowerPoint.

Nhóm đọc lại, điền thông tin thật, ghi đóng góp tự thực hiện và luyện demo/vấn đáp theo `docs/HO_SO_BAO_VE.md`. Dàn ý 8 chương trước khi nhận mẫu được giữ ở `docs/planning_snapshot` để truy vết.
