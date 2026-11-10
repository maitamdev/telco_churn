# Dàn ý báo cáo chi tiết — Đề tài 01

Phiên bản 1.0 — chốt cấu trúc nội dung ngày 10/11/2026 theo yêu cầu người dùng.

**Tên đề tài:** Dự đoán khách hàng rời dịch vụ viễn thông bằng học máy và xây dựng ứng dụng Streamlit.

**Trạng thái:** Dàn ý đã sẵn sàng để viết bản thảo; chưa phải báo cáo hoàn chỉnh. Mẫu bìa, font, lề và thông tin nhóm chờ người dùng cung cấp. Khi nhận mẫu sẽ ánh xạ cấu trúc này vào mẫu, giữ đầy đủ nội dung bắt buộc.

Đây là dàn ý chính thức dùng từ giai đoạn viết báo cáo. Thay thế bố cục dự kiến trong các bản kế hoạch cũ về thứ tự chương và mã hình/bảng. Các tệp trong thư mục planning vẫn là lịch sử chuẩn bị. Không sửa cấu hình thí nghiệm đã khóa chỉ để đổi kế hoạch viết.

Căn cứ: `../Huong_Dan_Do_An_CuoiKy.pdf` (yêu cầu chung, sản phẩm và đề tài 1 ở trang 1–3), `reports/KIEM_TRA_YEU_CAU_CUOI_KY.md`, cùng dữ liệu/kết quả đã kiểm chứng trong dự án.

## A. Quy mô và cấu trúc toàn báo cáo

Mục tiêu khoảng **60–65 trang toàn tệp**, ngân sách làm việc **62 trang**, luôn dưới 100 trang theo yêu cầu người dùng. Đây là dự toán khi chưa có mẫu; không kéo dài nội dung để đủ số trang. Hướng dẫn môn học không bắt buộc số chương hoặc số trang này.

| Phần | Nội dung | Trang dự kiến |
|---|---|---:|
| Phần đầu | Bìa, tóm tắt, mục lục, danh mục hình/bảng và thuật ngữ | 6 |
| Chương 1 | Giới thiệu bài toán và mục tiêu | 4 |
| Chương 2 | Dữ liệu và tiền xử lý | 6 |
| Chương 3 | Khám phá và trực quan hóa dữ liệu | 8 |
| Chương 4 | Cơ sở phương pháp và thiết kế thực nghiệm | 9 |
| Chương 5 | Kết quả thực nghiệm và so sánh mô hình | 7 |
| Chương 6 | Giải thích mô hình, phân tích lỗi và giới hạn | 5 |
| Chương 7 | Xây dựng ứng dụng Streamlit và kiểm thử | 6 |
| Chương 8 | Kết luận và hướng phát triển | 2 |
| Phần cuối 1 | Phân công thực tế và khai báo công cụ hỗ trợ | 2 |
| Phần cuối 2 | Tài liệu tham khảo | 2 |
| Phụ lục | Từ điển đầy đủ, ca lỗi, hướng dẫn chạy và đối chiếu yêu cầu | 5 |
| **Tổng** | **47 trang nội dung chính + 15 trang các phần còn lại** | **62** |

Phần đầu gồm bìa chính; bìa phụ/lời cảm ơn/cam đoan chỉ nếu mẫu yêu cầu; tóm tắt khoảng 200–300 từ; mục lục tự động; danh mục hình, bảng; danh mục từ viết tắt. Viết tóm tắt sau khi hoàn thiện các chương. Không tự điền tên, MSSV, lớp, giảng viên hoặc lời cam đoan về công việc nhóm chưa thực hiện.

Thuật ngữ cần thống nhất: Churn, EDA, LR, RF, CV, TP/FP/FN/TN, Precision, Recall, F1, ROC-AUC, AP, Pipeline. Dùng tiếng Việt giải thích ở lần xuất hiện đầu tiên.

## B. Dàn ý từng chương

### Chương 1. Giới thiệu bài toán và mục tiêu — 4 trang

Mục đích: người đọc hiểu cần giải quyết việc gì, hệ thống phục vụ ai, đầu ra là gì và đánh giá thành công bằng cách nào.

| Mục | Nội dung phải viết |
|---|---|
| **1.1. Bối cảnh và lý do chọn đề tài** | Vấn đề khách rời dịch vụ; nguồn lực chăm sóc có giới hạn; nhu cầu lựa chọn hồ sơ cần xem xét. Không thêm số liệu thị trường/doanh thu khi chưa có nguồn. |
| **1.2. Phát biểu bài toán** | Học có giám sát, phân loại nhị phân; một dòng là một khách; X có 19 thuộc tính, y là Churn; Yes=1, No=0; ID không làm đặc trưng. Đầu ra là xác suất ước lượng và nhãn theo ngưỡng. |
| **1.3. Mục tiêu của dự án** | Hiểu dữ liệu; xây dựng quy trình không fit holdout; so sánh baseline/LR/RF; đánh giá lỗi và giới hạn; xây dựng demo dùng đúng mô hình; tái lập được. |
| **1.4. Các câu hỏi nghiên cứu** | Trình bày đủ năm câu Q1–Q5 trong bảng bên dưới; mỗi câu gắn với phần trả lời cụ thể. |
| **1.5. Baseline và tiêu chí thành công** | Dummy luôn dự đoán lớp đa số. Chọn mô hình theo AP CV; ưu tiên recall với precision≥0,50 trên validation; recall≥0,80 là mục tiêu mong muốn của nhóm. Phân biệt tiêu chí khoa học/phần mềm với mục tiêu nghiệp vụ giả định. |
| **1.6. Đối tượng sử dụng và phạm vi** | Nhân viên/phân tích viên xem xét danh sách khách; demo local. Dữ liệu IBM dạng snapshot của công ty hư cấu; không chứng minh dự báo sớm theo kỳ hạn hoặc hiệu quả giữ chân thực tế. |

| Mã | Câu hỏi nghiên cứu được chốt | Nơi trả lời chính |
|---|---|---|
| Q1 | Nhãn churn mất cân bằng bao nhiêu và vì sao accuracy có thể gây hiểu nhầm? | 3.2, 4.7, 5.4 |
| Q2 | Hợp đồng, thời gian sử dụng, cước phí và dịch vụ có liên hệ với churn thế nào? | 3.3–3.9, đối chiếu 6.1 |
| Q3 | LR và RF cải thiện so với baseline ở những độ đo nào? | 5.2, 5.4–5.5 |
| Q4 | Chọn ngưỡng nào trên validation để ưu tiên recall khi precision tối thiểu 50%; kết quả test và đánh đổi ra sao? | 4.9, 5.3, 5.6 |
| Q5 | Mô hình dựa nhiều vào thông tin nào, thường sai ở những hồ sơ nào và còn giới hạn gì? | 6.1–6.5 |

Hình/bảng: Hình 1.1 mô tả luồng hồ sơ → ước lượng nguy cơ → danh sách xem xét; Bảng 1.1 là năm câu hỏi nghiên cứu và cách kiểm chứng. Hình 1.1 cần dựng khi viết bản thảo.

Bằng chứng: `configs/project_spec.json`, `README.md`, `reports/KIEM_TRA_YEU_CAU_CUOI_KY.md`.

### Chương 2. Dữ liệu và tiền xử lý — 6 trang

Mục đích: chứng minh nhóm hiểu dữ liệu, biết các vấn đề chất lượng và giải thích được từng quyết định xử lý.

| Mục | Nội dung phải viết |
|---|---|
| **2.1. Nguồn và xuất xứ dữ liệu** | Tên bộ IBM Telco, URL gốc, ngày kiểm nguồn và SHA-256; dữ liệu mẫu công ty hư cấu. Phân biệt nguồn công khai và ghi chú giấy phép trong provenance; ghi công IBM. |
| **2.2. Cấu trúc và ý nghĩa các thuộc tính** | 7.043 dòng × 21 cột; 19 đầu vào gồm 3 biến số và 16 biến phân loại; 1 ID và 1 nhãn. Giải thích tenure, MonthlyCharges, TotalCharges, Contract và các nhóm dịch vụ; đơn vị tiền giữ nguyên theo nguồn. |
| **2.3. Kiểm tra chất lượng ban đầu** | Kiểu đọc và kiểu ngữ nghĩa; thiếu từng cột; nhãn hợp lệ; ID duy nhất; số dòng trùng; tính nhất quán giữa dịch vụ chính và dịch vụ kèm. Tổng cước có 11 ô trống, 0,156183%; các cột khác không thiếu theo kiểm tra đã thực hiện. |
| **2.4. Các quyết định làm sạch** | Chuyển khoảng trắng tổng cước thành NaN; giữ 11 khách mới; không tự thay bằng 0. SeniorCitizen là danh mục; giữ No internet service/No phone service. Tách ID/nhãn khỏi X. Thống kê điền thiếu chỉ học trong fold/train; mô tả cơ chế chi tiết ở 4.2. |
| **2.5. Kiểm tra ngoại lai và quyết định giữ dữ liệu** | Trình bày miền hợp lệ và kiểm IQR trên train. Toàn train: không có điểm ngoài rào IQR chung của 3 biến số. Riêng Churn=Yes có 13 điểm tenure và 67 điểm TotalCharges ngoài rào nhóm; không cộng hai số thành số khách và không dùng nhãn để cắt dữ liệu. Chưa có bằng chứng các điểm là lỗi nên giữ. |
| **2.6. Phân hoạch và phạm vi sử dụng dữ liệu** | Stratify, seed 42; train 4.225, validation 1.409, test 1.409. Nêu số Yes/No từng tập; ID không giao nhau; train dùng EDA/CV/fit, validation dùng ngưỡng/importance, test dùng đánh giá cuối. |

Hình/bảng: Bảng 2.1 mô tả dữ liệu/nhóm thuộc tính; Bảng 2.2 kiểm chất lượng và tỷ lệ thiếu từng cột; Bảng 2.3 quyết định xử lý kèm lý do/số dòng trước sau; Bảng 2.4 quy mô và nhãn ba tập; Hình 2.1 sơ đồ chia tập và vai trò từng tập (cần dựng).

Bằng chứng: `artifacts/preparation/provenance.json`, `artifacts/preparation/data_profile.json`, `artifacts/preparation/cleaning_log.json`, `docs/DATA_DICTIONARY.md`, `reports/evidence/data_quality_audit.csv`, `reports/evidence/outlier_audit_train.csv`, `data/splits/split_manifest.json`, `src/data.py`, `src/validation.py`.

### Chương 3. Khám phá và trực quan hóa dữ liệu — 8 trang

Mục đích: trả lời Q1–Q2 bằng quan sát có số liệu. Toàn bộ tám hình EDA chính dùng **train n=4.225**. Hình đánh giá mô hình và ảnh demo không được tính thay cho tám hình này.

| Mục | Hình | Nội dung cần phân tích |
|---|---|---|
| **3.1. Phạm vi và cách đọc EDA** | — | Giới thiệu train, mẫu số khi tính tỷ lệ, khác biệt tương quan/nhân quả; dữ liệu thiếu trong mô tả được xử lý thế nào. |
| **3.2. Phân bố nhãn churn** | 3.1 | 1.121 Yes và 3.104 No, khoảng 26,53%/73,47%; hệ quả đối với baseline và chọn độ đo. |
| **3.3. Churn theo loại hợp đồng** | 3.2 | Hợp đồng tháng 43,08%, một năm khoảng 10,8%, hai năm 2,51%; trình bày cả cỡ nhóm; không suy ra kéo dài hợp đồng tự động giữ khách. |
| **3.4. Churn theo dịch vụ Internet** | 3.3 | So sánh Fiber optic, DSL, No; phân biệt đặc điểm nhóm với chất lượng dịch vụ thực tế chưa đo. |
| **3.5. Churn theo phương thức thanh toán** | 3.4 | Electronic check có tỷ lệ cao hơn trong dữ liệu; không khẳng định phương thức thanh toán gây churn. |
| **3.6. Phân bố thời gian sử dụng** | 3.5 | Trung vị nhóm churn 10 tháng, không churn 37 tháng; mô tả độ chồng lấp. Đây là thâm niên khách, không phải chuỗi thời gian theo tháng lịch. |
| **3.7. Phân bố cước tháng** | 3.6 | Trung vị nhóm churn 79,75, nhóm không churn 64,38; giữ đơn vị nguồn; không quyết định từ một biến. |
| **3.8. Phân bố tổng cước** | 3.7 | Trung vị 679,30 so với 1.677,85; quan hệ với thời gian sử dụng; giải thích boxplot, điểm ngoài râu và 7 ô thiếu trên train. |
| **3.9. Tương quan các biến số** | 3.8 | Pearson tenure–TotalCharges khoảng 0,834; giải thích dấu/độ lớn; tương quan cao không chứng minh nhân quả hoặc bắt buộc xóa biến. |
| **3.10. Các phát hiện và hệ quả cho mô hình** | — | Tổng hợp mất cân bằng, nhóm đáng chú ý, biến tương quan và nhu cầu mô hình đa biến; không tạo quy tắc chắc chắn từ biểu đồ. |

Mẫu viết dưới mỗi hình: **quan sát có số liệu → ý nghĩa đối với bài toán → giới hạn diễn giải**, khoảng 2–4 câu; có trục, chú giải, đơn vị và phạm vi mẫu. Tên file và thứ tự hình nằm ở mục C.

Bằng chứng: `artifacts/eda/NHAN_XET_EDA.md`, `artifacts/eda/01_class_balance.csv`, `artifacts/eda/02_Contract.csv`, `artifacts/eda/03_InternetService.csv`, `artifacts/eda/04_PaymentMethod.csv`, `artifacts/eda/numeric_summary.csv`, `artifacts/eda/08_correlation.csv`, `src/eda.py`.

### Chương 4. Cơ sở phương pháp và thiết kế thực nghiệm — 9 trang

Mục đích: trình bày cách làm và lý do chọn cách làm. Chương này mô tả quy trình; số liệu kết quả đo được trình bày ở Chương 5.

| Mục | Nội dung phải viết |
|---|---|
| **4.1. Quy trình học máy tổng thể** | Chuẩn hóa kiểu không học thống kê → tiền xử lý học trên train → mô hình → xác suất → ngưỡng → đánh giá/lưu → suy luận. Nêu ranh giới train/CV/validation/test. |
| **4.2. Chuẩn bị đặc trưng trong pipeline** | Median có missing indicator cho biến số; StandardScaler chỉ cho LR; OneHotEncoder cho biến danh mục; imputer danh mục dự phòng. Giải thích ColumnTransformer và tránh fit trước CV. Kiểm đầu vào ngoài ứng dụng vẫn từ chối danh mục sai dù encoder có handle_unknown=ignore. |
| **4.3. Mô hình đường cơ sở** | DummyClassifier most_frequent; lý do luôn đoán No; giữ dự đoán gốc, không tuning ngưỡng baseline. |
| **4.4. Logistic Regression** | Sigmoid, xác suất lớp 1, hàm mất mát phân loại và regularization L2; ý nghĩa C; ưu/nhược với dữ liệu bảng; vì sao chuẩn hóa biến số. Toán gắn với cấu hình thực tế, không trình bày thuật toán không dùng. |
| **4.5. Random Forest** | Cây quyết định, phép chia theo độ không thuần nhất, bootstrap, chọn tập con đặc trưng; tổng hợp xác suất các cây. Ý nghĩa số cây, max_depth và min_samples_leaf. |
| **4.6. Mất cân bằng và trọng số lớp** | Thử None/balanced bên trong CV; class_weight đổi mức phạt khi học, không tạo thêm khách; khác với đổi ngưỡng. Không tuyên bố đã dùng SMOTE/PCA vì triển khai không có. |
| **4.7. Các độ đo và lý do sử dụng** | Ma trận nhầm lẫn; công thức accuracy, precision, recall, F1; vai trò ROC-AUC và AP. Vì sao AP dùng để chọn mô hình, recall/precision dùng cho quyết định đánh dấu. AP không đồng nhất PR-AUC tính hình thang. |
| **4.8. Kiểm định chéo và tinh chỉnh** | StratifiedKFold 5 phần; 8 cấu hình LR, 18 RF; 130 fit CV cho hai mô hình, chưa tính baseline/refit. Pipeline được fit riêng mỗi fold. Xếp theo mean AP cao, std thấp; LR khi hai họ hòa tuyệt đối. |
| **4.9. Chọn ngưỡng trên validation** | Dự đoán Yes khi p≥t. Xét ngưỡng thỏa precision≥0,50 và có ít nhất một hồ sơ được đánh dấu; tối đa recall, rồi precision, rồi ngưỡng cao hơn. Nêu mục tiêu recall≥0,80 và fallback 0,5 khi không có ngưỡng phù hợp. Đây là giả định của nhóm. |
| **4.10. Kiểm soát rò rỉ và khả năng tái lập** | Seed/phiên bản, khóa model/ngưỡng trước khi đánh giá test, lưu selection record, giữ cùng pipeline cho app; không refit train+validation sau chọn ngưỡng. Phân biệt chống leakage do xử lý dữ liệu với giới hạn thời điểm thu thập ở 6.4. |

Hình/bảng: Hình 4.1 sơ đồ pipeline và ranh giới fit/transform (cần dựng); Bảng 4.1 phép biến đổi từng nhóm đặc trưng; Bảng 4.2 lưới tham số đã chạy và tham số cố định; Bảng 4.3 độ đo, công thức ngắn và ý nghĩa nghiệp vụ.

Bằng chứng: `src/preprocessing.py`, `src/train.py`, `src/evaluation.py`, `configs/project_spec.json`, `artifacts/final_run/selection_record.json`. Khi viết lý thuyết, dùng bài giảng đã có và tài liệu chính thức phù hợp phiên bản, ghi trích dẫn thật.

### Chương 5. Kết quả thực nghiệm và so sánh mô hình — 7 trang

Mục đích: cho thấy quy trình ở Chương 4 tạo ra kết quả gì, tốt hơn baseline ở đâu và phải đánh đổi điều gì.

| Mục | Nội dung phải viết |
|---|---|
| **5.1. Thiết lập thực nghiệm** | Python/thư viện/môi trường thực; run dùng trong báo cáo; cỡ tập, positive class. Không tự điền cấu hình phần cứng chưa thu thập. |
| **5.2. Kết quả kiểm định chéo và lựa chọn mô hình** | Bảng baseline/LR/RF mean±std AP, các độ đo bổ sung, tham số tốt nhất. RF AP 0,672568±0,013939; LR 0,667818±0,024414. Chênh lệch nhỏ, chưa kiểm định ý nghĩa thống kê. RF được chọn bằng train CV. |
| **5.3. Kết quả chọn ngưỡng trên validation** | Ngưỡng RF 0,4788031716; precision 50,08%, recall 80,48%. Bảng ngưỡng của LR/RF và đường precision/recall theo ngưỡng; kiểm mục tiêu đạt/chưa đạt trên validation. |
| **5.4. Đánh giá cuối trên test** | Trình bày đủ 5 dòng: Dummy gốc; LR 0,5 và ngưỡng validation; RF 0,5 và ngưỡng validation. Cùng test n=1.409; không trộn số train/validation. Diễn giải baseline accuracy cao nhưng recall 0. |
| **5.5. Ma trận nhầm lẫn và đường cong đánh giá** | Ma trận RF tại 0,5 và ngưỡng chọn; ROC và Precision–Recall so cả ba phương án. Đọc TP/FP/FN/TN bằng số khách và giải thích AUC/AP không phải phần trăm dự đoán đúng. |
| **5.6. Đánh đổi và ý nghĩa sử dụng** | Tại ngưỡng chính thức: đánh dấu 595, đúng 302, báo động nhầm 293, bỏ sót 72. So ngưỡng 0,5: phát hiện thêm 4 nhưng tăng 20 báo động nhầm. Phân biệt recall tăng với F1/accuracy có thể giảm; không gọi ngưỡng tối ưu mọi độ đo hoặc tối ưu chi phí. |

Số liệu đối soát cho RF chính thức trên test: accuracy **74,10%**, precision **50,76%**, recall **80,75%**, F1 **0,6233**, ROC-AUC **0,8435**, AP **0,6482**; TN=742, FP=293, FN=72, TP=302. Bản thảo phải lấy lại từ JSON/CSV thay vì chép nhiều lần từ dàn ý.

Hình/bảng: Bảng 5.1 kết quả CV và cấu hình chọn; Bảng 5.2 ngưỡng/metrics validation; Bảng 5.3 đủ năm thiết lập trên test; Hình 5.1 đường chọn ngưỡng validation, Hình 5.2 confusion test, Hình 5.3 ROC và PR test.

Bằng chứng: `artifacts/final_run/environment.json`, `artifacts/final_run/cv_summary.json`, `artifacts/final_run/cv_summary.csv`, `artifacts/final_run/logistic_regression_cv_results.csv`, `artifacts/final_run/random_forest_cv_results.csv`, `artifacts/final_run/selection_record.json`, `artifacts/final_run/test_metrics.json`, `artifacts/final_run/test_metrics.csv`, `artifacts/final_run/test_predictions.csv`, `reports/PHAN_TICH_KET_QUA.md`.

### Chương 6. Giải thích mô hình, phân tích lỗi và giới hạn — 5 trang

Mục đích: cho thấy nhóm hiểu mô hình có thể sai, biết dựa vào bằng chứng để diễn giải và giới hạn được các kết luận.

| Mục | Nội dung phải viết |
|---|---|
| **6.1. Mức độ quan trọng của đặc trưng** | Permutation importance trên validation, AP giảm khi xáo trộn một cột, 20 lần, mean/std. Contract, InternetService, tenure đứng đầu. Đối chiếu EDA; chỉ là mức phụ thuộc toàn cục của model, không phải nguyên nhân hoặc lời giải thích cá nhân. |
| **6.2. Các trường hợp dự đoán sai** | Định nghĩa FP/FN và tác động nghiệp vụ. Lưu 10 ca tự động: mỗi loại 3 ca xa ngưỡng nhất và 2 ca gần ngưỡng nhất, bỏ trùng. Nội dung chính minh họa 1 xa + 1 gần ngưỡng mỗi loại; phụ lục giữ đủ 10. Không gán nguyên nhân churn cá nhân khi dữ liệu không có. |
| **6.3. Hiệu quả theo nhóm khách** | Contract, InternetService, gender, SeniorCitizen: luôn có n cùng các độ đo/đếm lỗi. Xem khác biệt và cỡ mẫu; chưa coi đây là chứng nhận công bằng. |
| **6.4. Rò rỉ theo thời điểm thu thập** | ID/target và cột tiết lộ nhãn rõ ràng không vào X; nhưng snapshot chưa xác minh từng trường trước thời điểm dự đoán. Chú ý thời điểm chốt tenure, tổng cước và hợp đồng. Không tuyên bố dự báo trước 30/60/90 ngày. |
| **6.5. Giới hạn và phạm vi kết luận** | Dữ liệu mẫu một nguồn, chưa kiểm ngoài doanh nghiệp; chia ngẫu nhiên không thay đánh giá theo thời gian; xác suất chưa calibration; một split/seed; biến liên quan chia sẻ importance; chưa có chi phí/can thiệp nên chưa tính được ROI hoặc hiệu quả giữ chân. |

Hình/bảng: Hình 6.1 importance; Bảng 6.1 các ca FP/FN tiêu biểu theo quy tắc đã nêu; Bảng 6.2 kết quả theo nhóm. Tách rõ giả thuyết giải thích với sự kiện quan sát được.

Bằng chứng: `artifacts/final_run/permutation_importance_validation.csv`, `artifacts/final_run/permutation_repeats_validation.csv`, `artifacts/final_run/error_cases.csv`, `artifacts/final_run/subgroup_metrics.csv`, `reports/PHAN_TICH_KET_QUA.md`, `reports/KIEM_TRA_YEU_CAU_CUOI_KY.md`.

### Chương 7. Xây dựng ứng dụng Streamlit và kiểm thử — 6 trang

Mục đích: chứng minh mô hình được tích hợp thành ứng dụng hoạt động thật và cho kết quả nhất quán với thực nghiệm.

| Mục | Nội dung phải viết |
|---|---|
| **7.1. Người dùng và yêu cầu chức năng** | Xem dữ liệu, phân tích một hồ sơ, nhập danh sách, xem chất lượng mô hình, thử ngưỡng và xem importance. Mô tả đầu vào/đầu ra, không đưa chi tiết lập trình vào lời hướng dẫn cho người sử dụng. |
| **7.2. Kiến trúc ứng dụng** | app.py điều phối; ui trình bày; src.validation kiểm đầu vào; src.inference kiểm bundle và dự đoán; artifacts chứa mô hình/kết quả. Có sơ đồ và luồng dữ liệu, không chép nguyên mã vào chương. |
| **7.3. Năm màn hình chính** | 7.3.1 Tổng quan; 7.3.2 Phân tích khách hàng; 7.3.3 Nhập danh sách; 7.3.4 Hiệu quả mô hình; 7.3.5 Ngưỡng & giải thích. Mỗi màn hình một ảnh thực và mô tả ngắn thao tác/kết quả. |
| **7.4. Kiểm tra dữ liệu và xử lý lỗi** | Đủ 19 cột; ID tùy chọn; giới hạn tệp; miền số/danh mục và dịch vụ nhất quán; ô tổng cước được thiếu. CSV giữ dòng lỗi/thứ tự và báo lỗi; xuất kết quả. Dữ liệu upload không có nhãn đáng tin không tự tạo accuracy. |
| **7.5. Nhất quán giữa demo và mô hình đánh giá** | Nạp toàn pipeline, kiểm hash/schema/phiên bản; dùng cùng ngưỡng chính thức. Thanh trượt chỉ thay đánh giá minh họa trên validation; không ghi đè model/ngưỡng. Bấm dự đoán không huấn luyện lại. |
| **7.6. Kết quả kiểm thử** | Tổng hợp 54 tests và các nhóm kiểm tra; 5 trang, form/CSV, đầu vào lỗi, parity và ngưỡng độc lập; kiểm trình duyệt; notebook; bằng chứng cài môi trường sạch và tái lập. Trình bày ngày/phạm vi, không gọi đây là chứng nhận sản phẩm vận hành thực. |
| **7.7. Chạy demo và bàn giao** | Môi trường đã kiểm, chạy local, data/model đi kèm, requirements/README; mô tả gói kỹ thuật. Lệnh đầy đủ ở phụ lục. Demo hoạt động offline sau khi cài thư viện, không cần public deployment. |

Hình/bảng: Hình 7.1 kiến trúc (cần dựng); Hình 7.2–7.6 năm màn hình; Bảng 7.1 chức năng/đầu vào/đầu ra; Bảng 7.2 kịch bản kiểm thử, mong đợi, thực tế và bằng chứng.

Ảnh đã có dùng làm nguồn tham khảo; khi viết bản cuối chụp lại cùng một phiên bản giao diện, tránh trộn ảnh cũ có ghi chú đã bỏ. Ảnh ngưỡng phải ghi đúng 0,479 minh họa nếu dùng mặc định; nó khác ngưỡng chính thức 0,4788031716 và có thể cho số khách khác.

Bằng chứng: `app.py`, `ui/overview.py`, `ui/scoring.py`, `ui/results.py`, `src/inference.py`, `src/validation.py`, `artifacts/final_run/metadata.json`, `reports/evidence/pytest_requirements_audit.xml`, `reports/evidence/audit_browser_check.json`, `reports/evidence/full_reproduction.json`, `reports/evidence/notebook_execution.json`, `README.md`.

### Chương 8. Kết luận và hướng phát triển — 2 trang

| Mục | Nội dung phải viết |
|---|---|
| **8.1. Trả lời các câu hỏi nghiên cứu** | Trả lời Q1–Q5 bằng kết quả đã trình bày; dẫn lại bảng/hình tương ứng, không bổ sung kết quả mới chưa có thực nghiệm. |
| **8.2. Những kết quả đạt được** | Hoàn thành quy trình dữ liệu, EDA, baseline + LR/RF, pipeline, CV/tuning, đánh giá và ứng dụng. Nêu giá trị hỗ trợ sàng lọc cùng giới hạn thực tế, không tự cam kết điểm số. |
| **8.3. Hướng phát triển** | Ưu tiên dữ liệu theo thời gian và mốc trước sự kiện; đánh giá ngoài mẫu; calibration và ngưỡng theo chi phí; thử nghiệm chiến dịch có đối chứng. Đây là đề xuất tương lai, chưa ghi như chức năng đã có. |

Bảng 8.1: Q1–Q5, câu trả lời ngắn, bằng chứng, giới hạn còn lại.

## C. Danh mục hình đã chốt

Các hình “cần dựng” là công việc của giai đoạn viết bản thảo, chưa có file và chưa được coi là hoàn thành. Không thêm biểu đồ mới chỉ để tăng số trang.

| Hình | Tên dự kiến | Nguồn / trạng thái |
|---|---|---|
| 1.1 | Bài toán và luồng sử dụng dự đoán | Cần dựng từ quy trình hiện có |
| 2.1 | Phân hoạch dữ liệu và vai trò ba tập | Cần dựng từ split manifest |
| 3.1 | Phân bố nhãn churn trên train | `artifacts/eda/01_class_balance.png` |
| 3.2 | Tỷ lệ churn theo hợp đồng trên train | `artifacts/eda/02_Contract.png` |
| 3.3 | Tỷ lệ churn theo Internet trên train | `artifacts/eda/03_InternetService.png` |
| 3.4 | Tỷ lệ churn theo phương thức thanh toán trên train | `artifacts/eda/04_PaymentMethod.png` |
| 3.5 | Phân bố thời gian sử dụng theo nhãn trên train | `artifacts/eda/05_tenure.png` |
| 3.6 | Phân bố cước tháng theo nhãn trên train | `artifacts/eda/06_MonthlyCharges.png` |
| 3.7 | Tổng cước theo nhãn trên train | `artifacts/eda/07_TotalCharges.png` |
| 3.8 | Tương quan Pearson trên train | `artifacts/eda/08_correlation.png` |
| 4.1 | Pipeline và ranh giới fit/transform | Cần dựng từ pipeline thực tế |
| 5.1 | Precision/recall/F1 theo ngưỡng validation | `artifacts/final_run/evaluation_threshold.png` |
| 5.2 | Ma trận nhầm lẫn RF trên test ở hai ngưỡng | `artifacts/final_run/evaluation_confusion.png` |
| 5.3 | ROC và Precision–Recall trên test | `artifacts/final_run/evaluation_curves.png` |
| 6.1 | Permutation importance trên validation | `artifacts/final_run/evaluation_importance.png` |
| 7.1 | Kiến trúc ứng dụng và luồng suy luận | Cần dựng từ các module hiện có |
| 7.2 | Màn hình Tổng quan | Tham khảo `reports/evidence/ui_v2_clean_copy.jpg`; chụp lại khi chốt bản cuối |
| 7.3 | Dự đoán một khách hàng | Tham khảo `reports/evidence/ui_v2_single.jpg`; ảnh lịch sử, cần chụp lại bản giao diện hiện tại |
| 7.4 | Dự đoán danh sách và dòng lỗi | Tham khảo `reports/evidence/audit_csv.jpg`; chụp lại khi chốt bản cuối |
| 7.5 | Màn hình đánh giá mô hình | Tham khảo `reports/evidence/audit_evaluation.jpg`; chụp lại khi chốt bản cuối |
| 7.6 | Thử ngưỡng và giải thích | Tham khảo `reports/evidence/audit_threshold.jpg`; ghi đúng ngưỡng minh họa |

Tổng dự kiến 21 hình: 8 EDA, 4 hình kết quả/giải thích, 5 ảnh ứng dụng và 4 sơ đồ cần dựng. Hình 5.3 là một hình hai ô (a) ROC, (b) PR, không tự đếm thành hai hình để làm sai danh mục. Caption và đánh số sẽ dùng chức năng của Word khi dàn trang.

## D. Phân công, tài liệu tham khảo và phụ lục

### Phân công và khai báo công cụ hỗ trợ

Một bảng có các cột: họ tên/MSSV; phần phụ trách; công việc thực sự đã thực hiện; file hoặc bằng chứng tự chạy/chỉnh sửa; thời điểm; người kiểm tra chéo. Không mặc định chia 20% mỗi người khi chưa có dữ liệu đóng góp.

Phương án để nhóm nhận nhiệm vụ, **chưa phải phân công đã thực hiện**:

| Vai trò dự kiến | Nội dung phụ trách chính | Việc phải hiểu và kiểm chứng |
|---|---|---|
| Thành viên 1 | Chương 1–2, nguồn và từ điển | Dữ liệu, nhãn, kiểm thiếu/trùng/ngoại lai, split |
| Thành viên 2 | Chương 3 | Tự chạy EDA, đọc bảng nguồn và viết nhận xét |
| Thành viên 3 | Chương 4 và phần CV ở Chương 5 | Pipeline, LR/RF, tuning, ngăn leakage do xử lý |
| Thành viên 4 | Phần test ở Chương 5 và Chương 6 | Tính metrics, chọn ngưỡng, đọc lỗi/importance và giới hạn |
| Thành viên 5 | Chương 7, tích hợp Chương 8 và định dạng | Chạy app, thử lỗi, đối chiếu số liệu, tổng hợp từ cả nhóm |

Mọi người vẫn phải hiểu toàn bộ luồng. Nội dung khai báo AI bám `docs/AI_USAGE.md`; ghi đúng phần Codex hỗ trợ và phần nhóm đã làm, không đổi bản hỗ trợ thành lời cam đoan tự thực hiện toàn bộ.

### Tài liệu tham khảo

Nhóm nguồn cần dùng: hướng dẫn/bài giảng môn học; nguồn dữ liệu IBM; tài liệu chính thức scikit-learn về pipeline, LR/RF, CV, metrics, threshold và permutation importance; tài liệu chính thức Streamlit cho phần ứng dụng. Khi viết, kiểm đúng trang đã sử dụng, phiên bản và ngày truy cập; không tự tạo tác giả, năm hoặc DOI.

Kiểu trích dẫn áp theo mẫu người dùng cung cấp. Trong lúc soạn nội dung giữ nguồn gắn với từng luận điểm; số liệu thực nghiệm dẫn tới bảng/hình do dự án tạo và ghi phạm vi mẫu.

### Phụ lục chọn lọc — khoảng 5 trang

- **Phụ lục A:** Từ điển đầy đủ 21 cột, vai trò ID/target/feature, miền giá trị và đơn vị; phần thân trình bày nhóm thuộc tính, tránh lặp nguyên bảng.
- **Phụ lục B:** Đủ 10 ca FP/FN đã lưu; tham chiếu CSV cho lưới tham số và kết quả chi tiết, không in toàn bộ 130 lượt fit.
- **Phụ lục C:** Hướng dẫn cài/chạy demo, cấu trúc gói nộp, cách mở notebook và đường dẫn bằng chứng kiểm thử/tái lập.
- **Phụ lục D:** Bảng đối chiếu yêu cầu và câu hỏi vấn đáp; trích phần nhật ký cần thiết. Nhật ký/mã nguồn đầy đủ nằm trong gói dự án, không chèn hàng chục trang code vào báo cáo.

## E. Đối chiếu yêu cầu và câu hỏi của giảng viên

### Các yêu cầu trong bản rà soát

| Mã | Nơi thể hiện trong báo cáo / sản phẩm |
|---|---|
| RQ01 | Bìa, 1.4, bảng phân công; xác nhận đăng ký do nhóm bổ sung |
| RQ02 | 1.2–1.5, 4.3 |
| RQ03 | 2.1–2.3, Phụ lục A |
| RQ04 | 2.4–2.5 |
| RQ05 | 3.1–3.10 và tám hình EDA |
| RQ06 | 4.2, 4.10, 7.5 |
| RQ07 | 2.6, 4.8 |
| RQ08 | 4.3–4.5, 5.2, 5.4 |
| RQ09 | 1.5, 4.7, 5.6 |
| RQ10 | 5.5, 6.2 |
| RQ11 | 4.8, 5.2 |
| RQ12 | Chương 6, 8.3 |
| RQ13 | Chương 7 và demo thực tế |
| RQ14 | Toàn bộ báo cáo theo dàn ý này; DOCX/PDF chưa được tạo |
| RQ15 | 7.6–7.7, Phụ lục C và gói mã nguồn |
| RQ16 | 2.1, Phụ lục C và dữ liệu đi kèm |
| RQ17 | Slide và buổi bảo vệ là công việc riêng sau báo cáo; không coi dàn ý là slide |
| RQ18 | 7.6–7.7, Phụ lục C và ZIP |
| RQ19 | 4.8, 4.10, 5.1 |
| RQ20 | Phần phân công/AI, nhật ký và việc tự kiểm chứng của nhóm |
| RQ21 | 2.1, 6.5 và tài liệu tham khảo |

### Tám câu hỏi chung — hướng dẫn trang 3

| Câu | Nội dung | Nơi trả lời |
|---|---|---|
| G1 | Loại bài toán và nhãn | 1.2, 2.2 |
| G2 | Tiêu chí thành công và baseline | 1.5, 4.3 |
| G3 | Nguồn, quy mô, tỷ lệ thiếu | 2.1–2.3 |
| G4 | Vấn đề làm sạch và quyết định xử lý | 2.4–2.5 |
| G5 | Phòng tránh rò rỉ | 2.6, 4.2, 4.10, 6.4 |
| G6 | Chọn độ đo và lý do | 4.7, 5.6 |
| G7 | So baseline và ca dự đoán sai | 5.4–5.5, 6.2 |
| G8 | Giới hạn và cải tiến | 6.5, 8.3 |

### Năm câu hỏi riêng đề tài 1 — hướng dẫn trang 3

| Câu | Nội dung | Nơi trả lời |
|---|---|---|
| T1 | Mất cân bằng; accuracy so với precision/recall/F1 | 3.2, 4.7, 5.4 |
| T2 | Ưu tiên recall hay precision, vì sao | 1.5, 4.9, 5.6 |
| T3 | Hợp đồng/cước/dịch vụ có quan trọng, kiểm chứng bằng gì | 3.3–3.9, 6.1 |
| T4 | Cách doanh nghiệp dùng dự đoán và đặt ngưỡng | 1.6, 4.9, 5.6, 7.3 |
| T5 | Rủi ro đặc trưng chỉ biết sau khi khách rời | 2.2, 4.10, 6.4 |

Cụm 4 điểm dữ liệu/EDA/chuẩn bị được trình bày chủ yếu ở Chương 1–4; cụm 4 điểm mô hình/đánh giá ở Chương 4–6; cụm 2 điểm trình bày/demo/vấn đáp được hỗ trợ bởi Chương 7, slide và việc thực hành của nhóm. Đây là ánh xạ nội dung, không phải tự chia điểm nhỏ hoặc bảo đảm điểm tối đa. Chưa có BM06 chi tiết.

## F. Quy tắc viết và thứ tự triển khai tiếp theo

1. Viết Chương 2–3 trước vì số liệu và hình đã có; mỗi nhận định có bảng/hình chứng minh.
2. Viết Chương 4, sau đó Chương 5–6 để khớp phương pháp với kết quả và giới hạn.
3. Viết Chương 7, dựng bốn sơ đồ còn thiếu và chụp đồng bộ năm màn hình. Các sơ đồ phải phản ánh mã thực tế.
4. Hoàn thiện Chương 1, Chương 8 và tóm tắt sau khi phần kết quả ổn định; Q1–Q5 đã chốt từ dàn ý, không đổi câu hỏi để chọn kết quả có lợi.
5. Nhóm kiểm chứng/chỉnh sửa nội dung, điền đóng góp thật; hoàn thiện tham khảo và áp mẫu báo cáo.
6. Xuất DOCX/PDF cùng nội dung, kiểm từng trang, bảng/hình/mục lục và tổng trang dưới 100. Chỉ đánh dấu báo cáo hoàn thành sau bước này.

Quy tắc biên tập: phân biệt train/CV/validation/test ở caption; phần trăm làm tròn 2 chữ số khi cần, AP/AUC/F1 4 chữ số; ngưỡng chính thức ghi đủ để tái lập. Mean±std CV không phải khoảng tin cậy; importance không phải nhân quả; recall 80,75% không phải accuracy 80,75%; không suy ra dự báo tương lai hoặc ROI từ snapshot.

Số liệu thuộc run `telco_20261110T093056_0700`. Thay đổi nội dung báo cáo không được ghi đè run, chọn lại mô hình hoặc ngưỡng dựa trên test. Mẫu báo cáo và thông tin nhóm chưa có không cản việc viết bản thảo nội dung nhưng phải để chờ, không tự bịa.
