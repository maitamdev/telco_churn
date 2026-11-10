**ĐẶC TẢ DỮ LIỆU VÀ THÍ NGHIỆM**

Trạng thái: protocol trước huấn luyện. Thông số có cấu trúc ở planning/project_spec.json. Mọi thay đổi lựa chọn nghiên cứu phải ghi lại trước lần mở test cuối.

**A. Dữ liệu và ý nghĩa bài toán**

Nguồn CSV đề xuất: [IBM Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv). Bản đã kiểm tra trong lượt nghiên cứu: 7.043 dòng, 21 cột, 1.869 Yes/5.174 No, 11 TotalCharges trống, không trùng nguyên dòng, 7.043 ID duy nhất. M1 phải tải/copy bản gốc vào dự án và kiểm lại SHA-256, không coi kế hoạch là một lần chạy dữ liệu chính thức.

Một dòng là một khách trong snapshot mẫu. Churn ánh xạ No=0, Yes=1. Bộ dữ liệu không cung cấp chuỗi thời điểm đầy đủ để kiểm chứng dự báo 30 ngày tới. Mục tiêu học thuật là phân loại theo nhãn có sẵn và minh họa cách hỗ trợ lựa chọn khách cần rà soát. Không nói mô hình đã được kiểm chứng trên khách Việt Nam hay rằng một ưu đãi chắc chắn giữ được khách.

**B. Hợp đồng dữ liệu cho 21 cột**

| Cột | Vai trò/kiểu sau chuẩn hóa | Miền và chính sách |
|---|---|---|
| customerID | ID chuỗi | Bắt buộc/duy nhất ở dữ liệu nghiên cứu; tùy chọn trong CSV dự đoán; không vào X |
| gender | Phân loại | Female, Male |
| SeniorCitizen | Phân loại nhị phân | 0, 1; nhận số hoặc chuỗi tương ứng, chuẩn hóa nhất quán |
| Partner | Phân loại | No, Yes |
| Dependents | Phân loại | No, Yes |
| tenure | Số nguyên tháng | Hữu hạn, không âm; cảnh báo nếu ngoài miền quan sát train |
| PhoneService | Phân loại | No, Yes |
| MultipleLines | Phân loại | No, Yes, No phone service |
| InternetService | Phân loại | DSL, Fiber optic, No |
| OnlineSecurity | Phân loại | No, Yes, No internet service |
| OnlineBackup | Phân loại | No, Yes, No internet service |
| DeviceProtection | Phân loại | No, Yes, No internet service |
| TechSupport | Phân loại | No, Yes, No internet service |
| StreamingTV | Phân loại | No, Yes, No internet service |
| StreamingMovies | Phân loại | No, Yes, No internet service |
| Contract | Phân loại | Month-to-month, One year, Two year |
| PaperlessBilling | Phân loại | No, Yes |
| PaymentMethod | Phân loại | Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic) |
| MonthlyCharges | Số thực | Hữu hạn, không âm; xác minh đơn vị nguồn, không tự đổi sang VND |
| TotalCharges | Số thực hoặc thiếu | Strip; chuỗi rỗng thành NaN; chuỗi không phải số là lỗi; không âm khi có giá trị |
| Churn | Nhãn | No, Yes trong dữ liệu học; nếu xuất hiện trong upload thì loại khỏi X và thông báo |

Đầu vào dự đoán bắt buộc có đủ 19 tên cột đặc trưng. Ô trống chỉ hỗ trợ ở TotalCharges trong phiên bản giao diện đầu tiên; không được điền im lặng một cột bị thiếu hẳn. Các imputer ở những nhánh khác là phòng vệ trong pipeline, không thay thế validation hợp đồng đầu vào.

Quan hệ liên cột: PhoneService=No thì MultipleLines=No phone service, PhoneService=Yes thì MultipleLines không được bằng No phone service. InternetService=No thì cả sáu dịch vụ kèm theo phải là No internet service; khi có Internet thì các cột đó chỉ No/Yes. Form có thể hướng dẫn/điều chỉnh trạng thái khi đổi dịch vụ, nhưng phải cho người dùng thấy giá trị sẽ gửi. CSV mâu thuẫn phải được chỉ rõ dòng/cột.

Đặc trưng bị loại: customerID và Churn. Nếu vô tình dùng bản dữ liệu mở rộng, kiểm tra Churn Label/Value/Reason/Score, trạng thái tài khoản đã đóng, ngày hủy và mọi biến biết sau sự kiện. Không tự thêm chúng vào mô hình. Đối với snapshot, ghi hạn chế khi thời điểm ghi nhận của cột không thể chứng minh.

**C. Trình tự xử lý**

1. Lưu raw nguyên trạng, SHA-256, ngày tải, URL, điều kiện sử dụng và data dictionary.
2. Chạy kiểm kê cấu trúc, dtype, thiếu (kể cả khoảng trắng), nhãn và ID; tìm lỗi cú pháp/logic, không khảo sát test để chọn mô hình.
3. Kiểm tra trùng. Chỉ khử trùng nguyên bản khi có lý do rõ và log. Khách khác ID nhưng cùng hồ sơ có thể hợp lệ. ID trùng nhiều snapshot đòi hỏi kế hoạch chia theo nhóm/thời gian mới.
4. Tạo split cố định: tách 20% test, rồi tách 25% phần còn lại thành validation; cả hai stratify theo y và seed 42. Xuất ID từng tập, tỷ lệ nhãn và hash split. Không hứa số lượng chính xác trước khi chạy/kiểm tra chất lượng.
5. EDA, quyết định cắt ngoại lai/chọn đặc trưng và mọi lựa chọn nghiên cứu dùng train. Mặc định không loại/cắt ngoại lai hợp lệ.
6. Pipeline gồm chuẩn hóa cú pháp xác định trước, ColumnTransformer và classifier. Transformer tự viết đặt trong module có thể import để joblib tải lại được, không để class ở __main__ của notebook.
7. Nhánh số 3 cột: SimpleImputer median + missing indicator; LR có StandardScaler, RF không cần scaler. Nhánh phân loại 16 cột: imputer most_frequent phòng vệ + one-hot, drop=None, sparse_output=False, handle_unknown='ignore'. Cổng validation của app vẫn từ chối nhãn sai, không dùng ignore để che lỗi người nhập.
8. Không SMOTE, không PCA và không chọn đặc trưng theo thống kê trong phiên bản cốt lõi. Mọi mở rộng phải nằm đúng fold nếu thêm sau này.

Toàn bộ fit imputer/scaler/encoder nằm trong pipeline được GridSearchCV clone và fit trong từng fold. Median của TotalCharges không tính trước khi chia tập. Không thay TotalCharges bằng 0 chỉ vì đã thấy tenure=0; nếu nghiên cứu phương án đó phải ghi giả định và thử trên train/validation.

**D. Bộ thí nghiệm đã định nghĩa**

Baseline: DummyClassifier(strategy='most_frequent'), không tuning threshold; bảo toàn chiến lược luôn đoán lớp đa số. Constant scores có ROC-AUC 0,5 khi cả hai lớp hiện diện, AP bằng tỷ lệ positive của tập đánh giá. Khi không có dự đoán positive, precision/F1 dùng quy ước zero_division=0 và giải thích trong báo cáo.

| Mô hình | Cố định | Grid |
|---|---|---|
| Logistic Regression | lbfgs, L2 qua l1_ratio=0 trên sklearn 1.9.1, max_iter=2000, seed 42 | C ∈ {0,01;0,1;1;10}; class_weight ∈ {None,balanced}: 8 cấu hình |
| Random Forest | 300 cây, max_features=sqrt, seed 42; n_jobs=1 khi search song song | depth ∈ {4,8,None}; min_samples_leaf ∈ {1,5,20}; class_weight ∈ {None,balanced}: 18 cấu hình |

Kiểm tra API sau khi tạo môi trường. Signature sklearn 1.9.1 hiện có trên máy cho thấy penalty đã deprecated; không sao chép tham số cũ vào phiên bản khác mà không kiểm tra. Nếu môi trường phải đổi, sửa cấu hình tương đương trước huấn luyện và ghi lại. [API LogisticRegression chính thức](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

CV: StratifiedKFold(5,shuffle=True,random_state=42) chỉ trên train. Tổng cộng 26 cấu hình × 5 fold = 130 lần fit ứng viên, chưa tính baseline và refit. Search dùng tối đa 4 worker hoặc ít hơn tùy máy để tránh song song lồng nhau. Đọc cảnh báo hội tụ; cho phép tăng max_iter LR lên 10000 một lần trước test và ghi việc đó, không âm thầm coi cảnh báo là đã đạt.

Metric tuyển chọn: mean Average Precision cao nhất; hòa thì std AP thấp hơn; hòa chính xác giữa hai họ thì ưu tiên Logistic Regression đơn giản hơn. Lưu từng fold, toàn bộ cv_results, best_params và thời gian. Các chỉ số khác gồm ROC-AUC, precision, recall, F1, accuracy tại ngưỡng mặc định. Std CV mô tả biến động fold, không gọi là khoảng tin cậy 95%; best CV score đã qua tuyển chọn, không gọi là test score.

Chọn họ mô hình từ train CV trước khi xem test. Validation dùng chọn ngưỡng và kiểm tra khả năng đạt mục tiêu; không xem test rồi đổi người thắng. Không bắt RF phải thắng LR.

**E. Ngưỡng quyết định và trường hợp không đạt**

Mỗi mô hình đã chốt cấu hình được fit trên 60% train, tạo P(Churn=Yes) cho validation bằng đúng chỉ số classes_ của lớp 1. Quy ước y_pred=1 khi p >= threshold.

Tập ngưỡng ứng viên là các xác suất validation duy nhất cộng 0 và 1. Tính precision/recall/F1 và số bị gắn cờ ở từng ngưỡng. Chỉ xét ứng viên có ít nhất một cảnh báo và precision ≥0,50. Trong các ứng viên hợp lệ, tối đa recall, rồi precision, rồi threshold cao hơn nếu còn hòa. Recall 0,80 là kỳ vọng tự đặt; báo đạt/chưa đạt riêng.

Nếu không có ngưỡng thỏa precision: đặt trạng thái precision_constraint_not_met, dùng 0,5 làm ngưỡng tham chiếu cho demo nghiên cứu và ghi rõ chưa đáp ứng chính sách chiến dịch. Không coi trường hợp dự đoán không ai là precision=1, không thay mục tiêu dựa vào test. Cả trường hợp recall không đạt 0,80 nhưng precision đạt cũng phải báo đúng.

class_weight thay mục tiêu huấn luyện, threshold thay cách chuyển điểm thành nhãn. Hai kỹ thuật không tương đương. Phần trăm hiển thị là xác suất ước lượng chưa được khẳng định calibration. Không tự suy ra chi phí/lợi nhuận từ điểm số. [Chọn ngưỡng trong scikit-learn](https://scikit-learn.org/stable/modules/classification_threshold.html).

**F. Đóng băng và đánh giá cuối**

Trước test, lưu selection_record.json có run_id, timestamp, dataset/spec/split hashes, danh sách đặc trưng, best params, mô hình tuyển chọn, ngưỡng từng ứng viên, lý do, trạng thái mục tiêu validation và phiên bản môi trường.

Sau đó chạy một đợt đánh giá test cho baseline và các ứng viên đã cố định, trình bày ngưỡng 0,5 và ngưỡng validation. Thông số của mô hình được chọn không thay theo bảng test. Tính accuracy, precision/recall/F1 lớp 1, ROC-AUC, AP, confusion counts và số cảnh báo. Lưu prediction từng dòng để có thể tính lại bảng. AP là average_precision_score, không gắn nhãn nhầm thành diện tích PR bằng hình thang.

Không refit trên train+validation trong phiên bản này: lưu đúng pipeline đã đánh giá và ngưỡng đi kèm. Việc sửa mã lỗi kỹ thuật sau test phải ghi tác động; nếu thay lựa chọn học từ dữ liệu thì kết quả đó là nghiên cứu tiếp theo, cần phân biệt với đánh giá cuối ban đầu.

**G. Giải thích và phân tích lỗi**

- Permutation importance trên validation, cột đầu vào gốc qua pipeline, AP scoring, 20 lần lặp, seed 42; báo mean/std và ảnh hưởng của cột tương quan. Không dùng kết quả này để tạo vòng chọn biến không khai báo sau test.
- Hệ số Logistic chỉ diễn giải khi nêu đơn vị, cách mã hóa và tương quan; full one-hot không cho một hệ số đơn lẻ thành odds ratio so với nhóm tham chiếu mặc định. Ưu tiên permutation cho phần giải thích chính.
- Chọn tối đa 10 ca test sai: FP/FN có xác suất tự tin nhất và gần ngưỡng nhất, theo quy tắc deterministic, ID làm tie-break. Nếu ít lỗi hơn thì báo số thực, không tạo ca lỗi giả.
- Bảng lỗi theo Contract/nhóm tenure/dịch vụ kèm n, số positive, TP/FP/FN/TN. Nhóm rất nhỏ chỉ mô tả, không kết luận xếp hạng chắc chắn.
- Không thay kết quả bằng số liệu trong slide khachhang.csv. Không suy luận nhân quả từ coefficients, importance hay kịch bản thay đầu vào.

**H. Tệp kết quả cần lưu mỗi run**

data_profile.json; cleaning_log.json; split_manifest.json; cv_results.csv; best_params.json; selection_record.json; validation_predictions.csv; threshold_sweep.csv; test_predictions.csv; metrics.json; permutation_importance.csv; error_cases.csv; subgroup_errors.csv; environment.json; figures/; models/churn_pipeline.joblib; models/metadata.json; artifact_manifest.json.

Notebook giải thích gọi module chung, không tạo thuật toán/tiền xử lý thứ hai. Mỗi hình/bảng dùng dữ liệu nguồn đã lưu và có run_id, tránh copy số bằng tay qua báo cáo/app.
