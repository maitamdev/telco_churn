# Nhận xét EDA từ số liệu thật

Phạm vi: train; không dùng validation/test để chọn đặc trưng.

1. Tập train có 4,225 khách; churn 1,121 (26.53%). Accuracy cần so với tỷ lệ lớp đa số 73.47%.

2. Contract: nhóm Month-to-month có tỷ lệ churn 43.08% (n=2326), so với 2.51% (n=1034) ở Two year. Đây là tương quan, không chứng minh nguyên nhân.

3. InternetService: nhóm Fiber optic có tỷ lệ churn 42.32% (n=1843), so với 7.27% (n=908) ở No. Đây là tương quan, không chứng minh nguyên nhân.

4. PaymentMethod: nhóm Electronic check có tỷ lệ churn 45.60% (n=1410), so với 15.07% (n=909) ở Credit card (automatic). Đây là tương quan, không chứng minh nguyên nhân.

5. Median tenure: churn=10.00, không churn=37.00. Các phân bố vẫn chồng lấp; không thể quyết định từ một biến.

6. Median MonthlyCharges: churn=79.75, không churn=64.38. Các phân bố vẫn chồng lấp; không thể quyết định từ một biến.

7. Median TotalCharges: churn=679.30, không churn=1677.85 (đơn vị gốc). Tổng cước còn liên quan thời gian sử dụng, không suy ra tổng cước thấp gây churn. Các điểm ngoài râu hộp chưa đủ bằng chứng là dữ liệu sai nên được giữ lại. Train có 7 TotalCharges thiếu; hình bỏ qua ô thiếu để mô tả, mô hình điền median trong fold/train và không xóa khách.

8. tenure–TotalCharges có tương quan Pearson 0.834; biến liên quan có thể chia sẻ độ quan trọng. Pearson không mô tả đầy đủ quan hệ phi tuyến.

Không suy diễn quan hệ nhân quả từ dữ liệu quan sát. Không thực hiện cắt outlier hoặc xóa đặc trưng theo biểu đồ.
