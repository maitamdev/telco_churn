# Kịch bản demo và chuẩn bị bảo vệ

Thời lượng dưới đây là gợi ý; điều chỉnh khi có yêu cầu giảng viên.

## Demo khoảng 6–8 phút

1. Tổng quan (1 phút): nguồn IBM, 7.043 khách, churn 26,5%; các tập 4.225/1.409/1.409; mở biểu đồ hợp đồng và tenure.
2. Mô hình (1 phút): baseline luôn No; LR/RF qua 5 fold; chọn RF bằng AP trong CV trên train, pipeline ngăn leakage.
3. Một khách hàng (1 phút): nhập form, dự đoán; giải thích xác suất ước lượng và ngưỡng. Thử không dùng Internet hoặc thiếu tổng cước.
4. CSV (1–2 phút): tải valid_customers.csv, dự đoán; tải mixed_valid_invalid.csv để thấy 1 dòng hợp lệ và 2 dòng lỗi, download toàn bộ kết quả.
5. Đánh giá (1 phút): recall 80,75%, precision 50,76%, FP=293/FN=72. Accuracy 74,10% không phải chỉ số duy nhất.
6. Ngưỡng (1 phút): tăng/giảm slider trên validation; chỉ ra ngưỡng chính thức không đổi. Importance toàn cục và giới hạn snapshot.

Chạy demo trước bảo vệ bằng môi trường đã khóa; giữ sẵn ZIP, ảnh giao diện, notebook và CSV mẫu. Không cần Internet sau khi cài xong thư viện.

## Câu hỏi cần hiểu và trả lời bằng lời của nhóm

| Câu hỏi | Ý chính cần giải thích |
|---|---|
| Bài toán dự đoán điều gì? | Nhãn Churn Yes/No của snapshot; chưa chứng minh dự báo trước 30 ngày. |
| Dữ liệu thật hay giả lập? | Mẫu công ty hư cấu từ IBM, không tự thu thập hay xác minh doanh nghiệp thực. |
| Vì sao accuracy không đủ? | Dummy đạt 73,46% accuracy trên test nhưng recall churn=0. |
| Vì sao 11 ô TotalCharges trống không xóa? | Giữ khách mới; median học trong từng fold/train, không giả định trống nghĩa là 0. |
| Ngăn leakage bằng cách nào? | ID/target không vào X; không fit preprocessing trên toàn dữ liệu; CV toàn pipeline; mở test sau khi khóa selection record. |
| Ba tập dùng làm gì? | Train để học/CV; validation chọn ngưỡng và importance; test đánh giá cố định. |
| LR và RF khác nhau thế nào? | LR mô hình log-odds tuyến tính có regularization; RF tổng hợp cây bagging, nắm tương tác/phi tuyến. |
| Vì sao scale chỉ cho LR? | Regularization và tối ưu nhạy với thang đo; cây tách theo ngưỡng không cần scale theo cùng lý do. |
| class_weight giải quyết gì? | Thay trọng số lỗi của các lớp trong fit; không tạo khách mới, không bảo đảm xác suất được calibration. |
| Chọn RF vì sao? | AP CV 0,672568 nhỉnh hơn LR 0,667818; khác biệt nhỏ và chưa kiểm định ý nghĩa thống kê. |
| AP và ROC-AUC là gì? | AP tổng hợp precision với trọng số là mức tăng recall; ROC-AUC mô tả xếp hạng dương/âm. AP không đồng nhất với PR-AUC hình thang. |
| Tại sao không dùng ngưỡng 0,5? | Giả định ưu tiên recall với precision≥0,5; ngưỡng 0,478803 chốt trên validation. Chưa chứng minh tối ưu chi phí. |
| FP/FN có tác động gì? | 293 FP có thể tăng liên hệ không cần thiết; 72 FN bỏ sót churn. Chưa đủ dữ liệu tính ROI. |
| Importance có phải nguyên nhân? | Không; mức giảm AP khi hoán vị đo sự phụ thuộc của model. Các biến tương quan có thể chia sẻ thông tin. |
| Model nạp lại có giống không? | So xác suất toàn bộ validation sai khác 0; có hash và kiểm đối chiếu test; tái lập trong venv mới. |
| Tại sao không fit lại train+validation? | Ngưỡng gắn với model đã fit; refit có thể đổi thang xác suất. Giữ đúng bundle đã đánh giá. |
| Dữ liệu thật mới vào có hạn chế gì? | Thay đổi phân phối, drift, calibration, chất lượng và thời điểm thu thập; cần kiểm ngoài mẫu trước áp dụng. |
| AI hỗ trợ những gì? | Trình bày đúng docs/AI_USAGE.md và đóng góp thật; không nhận code/nhận xét của AI là tự làm. |

Các gợi ý là dàn ý, không phải kịch bản học thuộc. Nhóm cần diễn giải thuật toán, chỉ được file bằng chứng và tự xử lý tình huống giảng viên đổi đầu vào.

## Gợi ý chia phần cho 5 người — chưa phải phân công đã thực hiện

1. Bài toán, nguồn, từ điển và kiểm chất lượng.
2. EDA và giải thích nhận xét bằng bảng/hình.
3. Pipeline, LR/RF, CV/tuning, chống leakage.
4. Metrics, ngưỡng, error analysis, importance và giới hạn.
5. Streamlit, CSV, kiểm thử, đóng gói và tái lập.

Mỗi người cần nắm toàn luồng và ghi việc thật vào AI_USAGE/nhật ký nhóm; chưa tự gán tên hoặc mức đóng góp.

