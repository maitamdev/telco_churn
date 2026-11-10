# Phân tích kết quả thực nghiệm

Run: telco_20261110T093056_0700. Mô hình được chọn bằng train CV: **random_forest**; test không tham gia lựa chọn.

Ngưỡng **0.4788031716** chọn trên validation với precision≥0,50, tối đa recall. Đây là giả định nghiệp vụ, chưa có chi phí giữ chân thực.

Validation: precision=50.08%, recall=80.48%; mục tiêu recall≥80%: đạt.

Test n=1409: AP=0.6482; ROC-AUC=0.8435; accuracy=74.10%; precision=50.76%; recall=80.75%; F1=0.6233.

Test: TP=302, FP=293, FN=72, TN=742. Đánh dấu 595 khách để xem xét; không tự động kết luận phải giữ chân.

FP: 293 khách không churn vẫn bị đánh dấu; có thể làm tăng chi phí liên hệ. FN: 72 khách churn bị bỏ sót; có thể mất cơ hội hỗ trợ. Chưa có dữ liệu can thiệp để suy ra ROI hay hiệu quả giữ chân.

Ba biến có mean permutation importance lớn nhất trên validation: Contract (0.0777 ± 0.0174), InternetService (0.0541 ± 0.0135), tenure (0.0366 ± 0.0079). Đo mức phụ thuộc của mô hình, không phải nguyên nhân churn. Std là độ dao động qua 20 lần hoán vị.

Ví dụ lỗi được lấy tự động: mỗi loại FP/FN gồm 3 lỗi xa ngưỡng nhất và 2 gần ngưỡng nhất, loại trùng; không tuyển chọn thủ công để làm đẹp kết quả.

- 2545-EBUPK: FP, xác suất ước lượng=0.9333, nhãn=No, tenure=2, Contract=Month-to-month, InternetService=Fiber optic. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 8739-XNIKG: FP, xác suất ước lượng=0.9232, nhãn=No, tenure=5, Contract=Month-to-month, InternetService=Fiber optic. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 8161-QYMTT: FP, xác suất ước lượng=0.9226, nhãn=No, tenure=7, Contract=Month-to-month, InternetService=Fiber optic. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 5804-HYIEZ: FP, xác suất ước lượng=0.4801, nhãn=No, tenure=70, Contract=Month-to-month, InternetService=Fiber optic. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 1194-SPVSP: FP, xác suất ước lượng=0.4815, nhãn=No, tenure=1, Contract=Month-to-month, InternetService=No. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 8580-QVLOC: FN, xác suất ước lượng=0.0467, nhãn=Yes, tenure=72, Contract=Two year, InternetService=DSL. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 3705-PSNGL: FN, xác suất ước lượng=0.0718, nhãn=Yes, tenure=45, Contract=One year, InternetService=No. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 3400-ESFUW: FN, xác suất ước lượng=0.0784, nhãn=Yes, tenure=55, Contract=Two year, InternetService=DSL. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 4695-VADHF: FN, xác suất ước lượng=0.4758, nhãn=Yes, tenure=18, Contract=Month-to-month, InternetService=DSL. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

- 6646-QVXLR: FN, xác suất ước lượng=0.4757, nhãn=Yes, tenure=62, Contract=One year, InternetService=Fiber optic. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.

## Giới hạn và hướng phát triển

- Dữ liệu mẫu công ty hư cấu; chưa xác minh khả năng áp dụng cho doanh nghiệp Việt Nam.

- Snapshot không có timestamp, không chứng minh dự báo trước một khoảng thời gian cụ thể; ngẫu nhiên stratified không thay thế validation theo thời gian.

- Xác suất chưa hiệu chỉnh calibration. Ngưỡng có thể lệch khi tỷ lệ churn/chi phí thay đổi; cần validation mới.

- Có nhóm nhân khẩu học; bảng subgroup có cỡ mẫu nhưng chưa chứng minh công bằng hoặc tác động thực tế.

- Chênh lệch CV giữa hai mô hình chỉ là ước lượng trên một split/seed; chưa kiểm định khác biệt thống kê.

- Sau khi xem test, không sửa để tối ưu trên test này. Nếu thay thiết kế, cần thí nghiệm mới và tập đánh giá mới phù hợp.

- Đề xuất hỗ trợ nhóm hợp đồng tháng/tenure thấp chỉ là giả thuyết để kiểm tra bằng thử nghiệm can thiệp có kiểm soát.
