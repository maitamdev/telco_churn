# Từ điển dữ liệu

Churn: No=0, Yes=1. customerID: mã truy vết, không vào mô hình.

| Cột | Ý nghĩa | Kiểu và miền hợp lệ |
|---|---|---|
| tenure | Thời gian sử dụng (tháng) | số nguyên không âm |
| MonthlyCharges | Cước tháng (đơn vị gốc) | số hữu hạn không âm |
| TotalCharges | Tổng cước (đơn vị gốc) | số hữu hạn không âm; được thiếu |
| gender | Giới tính | Female, Male |
| SeniorCitizen | Thuộc nhóm cao tuổi | 0, 1 |
| Partner | Có bạn đời | No, Yes |
| Dependents | Có người phụ thuộc | No, Yes |
| PhoneService | Dịch vụ điện thoại | No, Yes |
| MultipleLines | Nhiều đường dây | No, Yes, No phone service |
| InternetService | Loại Internet | DSL, Fiber optic, No |
| OnlineSecurity | Bảo mật trực tuyến | No, Yes, No internet service |
| OnlineBackup | Sao lưu trực tuyến | No, Yes, No internet service |
| DeviceProtection | Bảo vệ thiết bị | No, Yes, No internet service |
| TechSupport | Hỗ trợ kỹ thuật | No, Yes, No internet service |
| StreamingTV | Truyền hình trực tuyến | No, Yes, No internet service |
| StreamingMovies | Phim trực tuyến | No, Yes, No internet service |
| Contract | Loại hợp đồng | Month-to-month, One year, Two year |
| PaperlessBilling | Hóa đơn điện tử | No, Yes |
| PaymentMethod | Phương thức thanh toán | Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic) |

Đơn vị tiền giữ nguyên theo dữ liệu nguồn; không quy đổi sang VND. Dữ liệu dạng snapshot, không có timestamp để chia theo thời gian.