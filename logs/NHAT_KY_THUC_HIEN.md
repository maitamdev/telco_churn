
## 03 · Nguồn dữ liệu

Thời điểm: 2026-11-10T09:28:29+07:00 (UTC+7).

Đã thực hiện:
- Tải/kiểm lại CSV IBM và hash SHA-256

Kết quả:
- 970457 bytes; hash trùng nguồn đã chốt

Tệp bằng chứng:
- `data/raw/Telco-Customer-Churn.csv`
- `artifacts/preparation/provenance.json`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 04 · Kiểm chất lượng

Thời điểm: 2026-11-10T09:28:30+07:00 (UTC+7).

Đã thực hiện:
- Kiểm schema, ID, nhãn, số, danh mục, nhất quán dịch vụ
- Ghi từ điển và lý do làm sạch

Kết quả:
- 7.043 dòng × 21 cột; không trùng ID/dòng
- 11 TotalCharges trống, đều tenure=0; giữ tất cả dòng

Tệp bằng chứng:
- `artifacts/preparation/data_profile.json`
- `artifacts/preparation/cleaning_log.json`
- `docs/DATA_DICTIONARY.md`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 05 · Cố định ba tập

Thời điểm: 2026-11-10T09:28:30+07:00 (UTC+7).

Đã thực hiện:
- Stratified 60/20/20, seed=42, lưu ID/hash
- Kiểm giao ID rỗng; tạo mẫu CSV từ train

Kết quả:
- train: 4225 dòng
- validation: 1409 dòng
- test: 1409 dòng

Tệp bằng chứng:
- `data/splits/split_manifest.json`
- `data/splits/train.csv`
- `data/splits/validation.csv`
- `data/splits/test.csv`
- `data/samples/`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 01 · Khởi tạo thư mục riêng

Thời điểm: 2026-11-10T09:29:16+07:00 (UTC+7).

Đã thực hiện:
- Tạo DU_AN_TELCO_CHURN và cấu trúc module
- Sao lưu toàn bộ tài liệu kế hoạch trước triển khai

Kết quả:
- Thư mục độc lập; tài liệu gốc giữ nguyên

Tệp bằng chứng:
- `docs/planning_snapshot`
- `docs/planning_documents`
- `docs/18_BUOC_TRIEN_KHAI.md`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 02 · Môi trường Python

Thời điểm: 2026-11-10T09:29:16+07:00 (UTC+7).

Đã thực hiện:
- Tạo .venv và cài thư viện
- Lưu requirements đúng phiên bản thực tế

Kết quả:
- {'numpy': '2.5.4', 'pandas': '3.1.1', 'scikit-learn': '1.9.1', 'matplotlib': '3.11.2', 'seaborn': '0.13.2', 'joblib': '1.6.0', 'streamlit': '1.67.0', 'pytest': '9.2.0', 'nbformat': '5.11.1', 'nbclient': '0.11.0'}

Tệp bằng chứng:
- `requirements.txt`
- `artifacts/preparation/environment.json`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 06 · Tám biểu đồ EDA

Thời điểm: 2026-11-10T09:29:53+07:00 (UTC+7).

Đã thực hiện:
- Tạo 8 biểu đồ có nhãn/trục, chỉ trên train
- Lưu CSV số liệu nguồn

Kết quả:
- 8 PNG; bảng nhóm, phân phối và thống kê số

Tệp bằng chứng:
- `artifacts/eda/`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 08 · Pipeline và baseline

Thời điểm: 2026-11-10T09:30:57+07:00 (UTC+7).

Đã thực hiện:
- Normalizer -> ColumnTransformer -> estimator
- Imputer/scaler/encoder fit trong từng fold; Dummy most_frequent giữ dự đoán gốc

Kết quả:
- Baseline CV AP=0.265325

Tệp bằng chứng:
- `src/preprocessing.py`
- `artifacts/final_run/baseline_cv.csv`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 06 · Tám biểu đồ EDA

Thời điểm: 2026-11-10T09:31:10+07:00 (UTC+7).

Đã thực hiện:
- Tạo 8 biểu đồ có nhãn/trục, chỉ trên train
- Lưu CSV số liệu nguồn

Kết quả:
- 8 PNG; bảng nhóm, phân phối và thống kê số

Tệp bằng chứng:
- `artifacts/eda/`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 09 · Tuning hai mô hình

Thời điểm: 2026-11-10T09:31:41+07:00 (UTC+7).

Đã thực hiện:
- 5-fold stratified CV trên train; 8 cấu hình LR + 18 RF
- Chọn bằng mean AP, dùng std AP phá hòa; lưu mọi cấu hình và train/CV score

Kết quả:
- baseline: AP=0.265325 ± 0.000473
- logistic_regression: AP=0.667818 ± 0.024414
- random_forest: AP=0.672568 ± 0.013939

Tệp bằng chứng:
- `artifacts/final_run/cv_summary.json`
- `artifacts/final_run/logistic_regression_cv_results.csv`
- `artifacts/final_run/random_forest_cv_results.csv`

Giới hạn / việc còn lại:
- Độ lệch chuẩn giữa fold không phải khoảng tin cậy.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 10 · Khóa mô hình và ngưỡng trước test

Thời điểm: 2026-11-10T09:31:41+07:00 (UTC+7).

Đã thực hiện:
- Chọn mô hình theo train CV
- Chọn ngưỡng trên validation; lưu selection_record trước khi đọc test

Kết quả:
- Mô hình: random_forest
- Ngưỡng: 0.4788031716
- {'threshold': 0.4788031716353531, 'status': 'precision_constraint_met', 'validation_metrics': {'n': 1409, 'threshold': 0.4788031716353531, 'accuracy': 0.7352732434350603, 'precision_churn': 0.5008319467554077, 'recall_churn': 0.8048128342245989, 'f1_churn': 0.6174358974358974, 'roc_auc': 0.838150042625746, 'average_precision': 0.6364938507722082, 'tn': 735, 'fp': 300, 'fn': 73, 'tp': 301, 'flagged_count': 601}, 'precision_floor': 0.5, 'aspirational_recall': 0.8, 'aspirational_recall_met': True, 'assumption': 'precision>=0.50 và mong muốn recall>=0.80 là giả định nhóm; không phải thang điểm môn học.'}

Tệp bằng chứng:
- `artifacts/final_run/selection_record.json`
- `artifacts/final_run/validation_predictions.csv`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 07 · Nhận xét và kiểm biểu đồ

Thời điểm: 2026-11-10T09:31:45+07:00 (UTC+7).

Đã thực hiện:
- Viết 8 nhận xét định lượng từ train
- Xem contact sheet: tiêu đề/trục/chú giải không bị cắt; màu và số rõ

Kết quả:
- 8/8 hình đọc được; có bảng nguồn để truy lại
- Đã sửa lỗi in Unicode của terminal Windows; chạy lại EDA thành công

Tệp bằng chứng:
- `artifacts/eda/NHAN_XET_EDA.md`
- `reports/evidence/eda_contact_sheet.png`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 11 · Đánh giá cố định và phân tích lỗi

Thời điểm: 2026-11-10T09:32:02+07:00 (UTC+7).

Đã thực hiện:
- Đánh giá test tại 0.5 và ngưỡng đã khóa
- Permutation importance trên validation, 20 lần; xuất FP/FN và thống kê nhóm

Kết quả:
- {'model': 'baseline', 'operating_point': 'native_most_frequent', 'n': 1409, 'threshold': 0.5, 'accuracy': 0.7345635202271115, 'precision_churn': 0.0, 'recall_churn': 0.0, 'f1_churn': 0.0, 'roc_auc': 0.5, 'average_precision': 0.2654364797728886, 'tn': 1035, 'fp': 0, 'fn': 374, 'tp': 0, 'flagged_count': 0}
- {'model': 'random_forest', 'operating_point': 'default_0.5', 'n': 1409, 'threshold': 0.5, 'accuracy': 0.752306600425834, 'precision_churn': 0.521891418563923, 'recall_churn': 0.7967914438502673, 'f1_churn': 0.6306878306878307, 'roc_auc': 0.8434511353948694, 'average_precision': 0.6482362911420345, 'tn': 762, 'fp': 273, 'fn': 76, 'tp': 298, 'flagged_count': 571}
- {'model': 'random_forest', 'operating_point': 'validation_selected', 'n': 1409, 'threshold': 0.4788031716353531, 'accuracy': 0.7409510290986515, 'precision_churn': 0.507563025210084, 'recall_churn': 0.8074866310160428, 'f1_churn': 0.6233230134158927, 'roc_auc': 0.8434511353948694, 'average_precision': 0.6482362911420345, 'tn': 742, 'fp': 293, 'fn': 72, 'tp': 302, 'flagged_count': 595}

Tệp bằng chứng:
- `artifacts/final_run/test_metrics.json`
- `artifacts/final_run/test_predictions.csv`
- `artifacts/final_run/permutation_importance_validation.csv`
- `artifacts/final_run/error_cases.csv`
- `artifacts/final_run/subgroup_metrics.csv`

Giới hạn / việc còn lại:
- Test dùng mô tả kết quả, không đổi mô hình/ngưỡng sau khi xem.
- Importance không chứng minh nhân quả; các biến tương quan có thể chia sẻ thông tin.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 12 · Đóng gói pipeline

Thời điểm: 2026-11-10T09:32:03+07:00 (UTC+7).

Đã thực hiện:
- Lưu toàn bộ pipeline và metadata/hash/environment
- Load lại và so toàn bộ xác suất validation

Kết quả:
- Sai khác lớn nhất=0.0
- Thời gian thí nghiệm=66.44 giây

Tệp bằng chứng:
- `artifacts/final_run/churn_pipeline.joblib`
- `artifacts/final_run/metadata.json`
- `artifacts/final_run/artifact_manifest.json`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 13 · Tổng quan và dự đoán cá nhân

Thời điểm: 2026-11-10T09:40:36+07:00 (UTC+7).

Đã thực hiện:
- Xây giao diện tiếng Việt, 19 trường, ràng buộc dịch vụ
- Nạp pipeline thật và kiểm hash; không có model giả dự phòng

Kết quả:
- Dự đoán form trên AppTest và trình duyệt thành công

Tệp bằng chứng:
- `app.py`
- `ui/overview.py`
- `ui/scoring.py`
- `reports/evidence/ui_single_prediction.jpg`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 14 · CSV và đánh giá

Thời điểm: 2026-11-10T09:40:36+07:00 (UTC+7).

Đã thực hiện:
- Thêm upload/download CSV, báo lỗi từng dòng
- Bảng test cố định, CV, lỗi, subgroup, validation threshold playground

Kết quả:
- Đủ 5 trang; không đổi ngưỡng chính thức qua slider
- CSV thực: 3 dòng, 1 hợp lệ, 2 lỗi; tải kết quả thành công

Tệp bằng chứng:
- `ui/results.py`
- `data/samples`
- `reports/evidence/ui_csv_result.jpg`
- `reports/evidence/browser_download_predictions.csv`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 15 · Kiểm thử tự động

Thời điểm: 2026-11-10T09:40:36+07:00 (UTC+7).

Đã thực hiện:
- Chạy unit/integration/Streamlit AppTest
- Sửa 2 lỗi fixture do pandas strict string dtype, không sửa thí nghiệm/model

Kết quả:
- 54/54 tests passed

Tệp bằng chứng:
- `tests`
- `logs/pytest.log`
- `reports/evidence/pytest.xml`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 16 · Kiểm trình duyệt thật

Thời điểm: 2026-11-10T09:44:42+07:00 (UTC+7).

Đã thực hiện:
- Mở demo localhost và kiểm bố cục/đầu ra
- Upload CSV qua file chooser; download và đọc lại kết quả
- Đối chiếu trang đánh giá và lưu ảnh

Kết quả:
- Form dự đoán thành công
- 3 dòng CSV giữ đủ: 1 hợp lệ, 2 lỗi đúng
- Không ghi nhận lỗi console tại thời điểm kiểm

Tệp bằng chứng:
- `reports/evidence/browser_check.json`
- `reports/evidence/ui_overview.jpg`
- `reports/evidence/ui_csv_result.jpg`
- `reports/evidence/ui_evaluation_top.jpg`
- `reports/evidence/browser_download_predictions.csv`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 17 · Môi trường sạch và tái lập

Thời điểm: 2026-11-10T09:44:42+07:00 (UTC+7).

Đã thực hiện:
- Tạo venv_verify từ requirements, pip check và chạy 54 tests
- Huấn luyện lại toàn bộ trong bản sao riêng với cấu hình cố định
- Thực thi 6 ô mã notebook bằng venv sạch; viết README và script chạy

Kết quả:
- 54/54 tests trong môi trường sạch
- Model/tham số/ngưỡng giống; sai khác CV/metrics/xác suất=0
- Notebook thực thi đầy đủ, đã đóng kernel

Tệp bằng chứng:
- `logs/clean_install.log`
- `logs/pytest_clean_env.log`
- `reports/evidence/pytest_clean_env.xml`
- `reports/evidence/full_reproduction.json`
- `reports/evidence/notebook_execution.json`
- `notebooks/01_telco_churn.ipynb`
- `README.md`
- `CHAY_DEMO.ps1`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T09:45:22+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 13 · Nâng giao diện doanh nghiệp 2.0

Thời điểm: 2026-11-10T10:02:37+07:00 (UTC+7).

Đã thực hiện:
- Thiết kế nhận diện TELCO, sidebar, màu, chữ, card và biểu đồ tương tác
- Thêm tìm/lọc/xuất hồ sơ train; chọn một dòng để điền sẵn trang phân tích
- Chia biểu mẫu thành ba tab, đặt kết quả cạnh thông tin

Kết quả:
- Tìm và mở 8499-BRXTD thành công; dự đoán 5,6% khớp pipeline

Tệp bằng chứng:
- `ui/styles.css`
- `ui/components.py`
- `ui/charts.py`
- `ui/data_views.py`
- `ui/overview.py`
- `ui/scoring.py`
- `reports/evidence/ui_v2_overview.jpg`
- `reports/evidence/ui_v2_single.jpg`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 14 · Đồng bộ ba trang còn lại theo giao diện 2.0

Thời điểm: 2026-11-10T10:02:37+07:00 (UTC+7).

Đã thực hiện:
- Làm gọn nhập CSV và bảng kết quả tiếng Việt
- Tổ chức trang hiệu quả theo bảng/ma trận và các tab chi tiết
- Dùng biểu đồ tương tác cho ngưỡng và importance

Kết quả:
- CSV 3 dòng giữ 1 hợp lệ và 2 lỗi
- Slider validation chạy đúng và không đổi ngưỡng chính thức

Tệp bằng chứng:
- `ui/results.py`
- `reports/evidence/ui_v2_csv.jpg`
- `reports/evidence/ui_v2_threshold.jpg`
- `docs/GIAO_DIEN_V2.md`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 15 · Kiểm thử hồi quy giao diện 2.0

Thời điểm: 2026-11-10T10:02:37+07:00 (UTC+7).

Đã thực hiện:
- Chạy lại toàn bộ tests trên hai môi trường sau chỉnh sửa
- Kiểm tìm kiếm, trạng thái rỗng và kiểm tính toàn vẹn model

Kết quả:
- 54/54 tests đạt ở mỗi môi trường
- Pipeline, split và kết quả mô hình vẫn khớp manifest

Tệp bằng chứng:
- `logs/pytest.log`
- `logs/pytest_clean_env.log`
- `reports/evidence/pytest.xml`
- `reports/evidence/pytest_clean_env.xml`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 16 · Kiểm trình duyệt giao diện 2.0

Thời điểm: 2026-11-10T10:02:37+07:00 (UTC+7).

Đã thực hiện:
- Thử tìm/chọn hồ sơ, điền sẵn, dự đoán
- Kiểm CSV, trang hiệu quả và slider; lưu ảnh thực tế

Kết quả:
- Luồng mới hoạt động; không ghi nhận lỗi console
- Để sẵn trang tổng quan trên localhost

Tệp bằng chứng:
- `reports/evidence/ui_v2_check.json`
- `reports/evidence/ui_v2_overview.jpg`
- `reports/evidence/ui_v2_single.jpg`
- `reports/evidence/ui_v2_csv.jpg`
- `reports/evidence/ui_v2_evaluation.jpg`
- `reports/evidence/ui_v2_threshold.jpg`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T10:02:40+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 13 · Bỏ viền trang trí theo phản hồi

Thời điểm: 2026-11-10T10:06:08+07:00 (UTC+7).

Đã thực hiện:
- Bỏ vạch xanh và shadow/outline trang trí ở menu chọn
- Bỏ đường bao KPI, panel, badge và expander; dùng nền nhẹ và khoảng cách
- Giữ nhận biết focus bàn phím bằng nền và gạch chân

Kết quả:
- Kiểm trực tiếp trên trình duyệt: menu, KPI và panel có border 0px, shadow none, outline none
- Lưu ảnh giao diện sau sửa; đây là chỉnh CSS, không thay logic dự đoán

Tệp bằng chứng:
- `ui/styles.css`
- `docs/GIAO_DIEN_V2.md`
- `reports/evidence/ui_v2_no_borders.jpg`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T10:06:30+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 13 · Dọn nội dung thừa trên cả năm trang

Thời điểm: 2026-11-10T10:12:05+07:00 (UTC+7).

Đã thực hiện:
- Bỏ toàn bộ subtitle của trang và panel, ghi chú KPI, breadcrumb và footer
- Bỏ khối model/run ID/trạng thái giả định ở sidebar
- Bỏ đoạn gợi ý chung, giải thích học thuật và hướng dẫn lặp dưới biểu mẫu/bảng
- Giữ nhãn thao tác, dữ liệu kết quả, số hồ sơ, giới hạn CSV và lỗi cần sửa

Kết quả:
- 10/10 Streamlit AppTest đạt; năm trang hoạt động
- Thông tin phục vụ báo cáo vẫn nằm trong tài liệu và artifact

Tệp bằng chứng:
- `app.py`
- `ui/components.py`
- `ui/overview.py`
- `ui/scoring.py`
- `ui/results.py`
- `logs/ui_copy_cleanup_test.log`
- `docs/GIAO_DIEN_V2.md`
- `reports/evidence/ui_v2_clean_copy.jpg`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T10:13:34+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 06 · Tám biểu đồ EDA

Thời điểm: 2026-11-10T10:28:09+07:00 (UTC+7).

Đã thực hiện:
- Tạo 8 biểu đồ có nhãn/trục, chỉ trên train
- Lưu CSV số liệu nguồn

Kết quả:
- 8 PNG; bảng nhóm, phân phối và thống kê số

Tệp bằng chứng:
- `artifacts/eda/`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 07 · Bổ sung bằng chứng chất lượng và nhận định EDA sau rà soát

Thời điểm: 2026-11-10T10:29:25+07:00 (UTC+7).

Đã thực hiện:
- Lập bảng kiểu ngữ nghĩa, số thiếu và tỷ lệ thiếu cho 21 cột
- Kiểm IQR ba biến số trên train và theo nhóm để diễn giải boxplot; giữ nguyên dữ liệu
- Bổ sung trung vị tổng cước và giới hạn diễn giải cho biểu đồ 07; dựng lại notebook trong venv sạch

Kết quả:
- TotalCharges thiếu 11/7043 = 0,156183%; không có dòng/ID trùng
- Nhóm Churn=Yes: tenure có 13 điểm, TotalCharges có 67 điểm ngoài rào IQR của nhóm; không cắt theo nhãn
- Notebook thực thi đủ 6 ô; model/ngưỡng không đổi

Tệp bằng chứng:
- `reports/evidence/data_quality_audit.csv`
- `reports/evidence/outlier_audit_train.csv`
- `src/eda.py`
- `artifacts/eda/NHAN_XET_EDA.md`
- `notebooks/01_telco_churn.ipynb`
- `logs/notebook_requirements_audit.log`

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 15 · Kiểm tra toàn bộ kỹ thuật theo hướng dẫn cuối kỳ

Thời điểm: 2026-11-10T10:29:25+07:00 (UTC+7).

Đã thực hiện:
- Đọc đủ 6 trang hướng dẫn gốc, xem trực quan trang 1–3
- Chạy lại toàn bộ pytest và pip check; tính lại 5 dòng metrics và đối chiếu dự đoán model
- Kiểm split đầy đủ không trùng, notebook, hình, source hash bản tái lập; thao tác trực tiếp 5 trang demo
- Ghi ma trận 21 yêu cầu, bộ câu hỏi và các phần chưa đủ để nộp

Kết quả:
- 54/54 tests đạt; pip check không lỗi
- Sai khác model/test probability = 0; metrics tối đa 1,11e-16
- Không phát hiện lỗi kỹ thuật ngăn demo trong phạm vi đã kiểm

Tệp bằng chứng:
- `reports/KIEM_TRA_YEU_CAU_CUOI_KY.md`
- `reports/evidence/requirements_audit.json`
- `reports/evidence/pytest_requirements_audit.xml`
- `logs/pytest_requirements_audit.log`
- `reports/evidence/audit_browser_check.json`
- `tools/audit_requirements.py`

Giới hạn / việc còn lại:
- Chưa có báo cáo cuối, slide, đóng góp tự thực hiện của nhóm, bằng chứng xác nhận đăng ký và BM06.
- Snapshot không chứng minh tất cả thuộc tính được đo trước thời điểm dự báo tương lai.
- 18/18 là bước kỹ thuật; không chứng nhận đủ điều kiện nộp hoặc điểm tối đa.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T10:29:27+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Báo cáo · Bước 1: Chốt bố cục và dàn ý chi tiết

Thời điểm: 2026-11-10T10:49:03+07:00 (UTC+7).

Đã thực hiện:
- Chốt tên đề tài và 8 chương; ngân sách 62 trang toàn tệp, mục tiêu 60–65 trang
- Viết mục tiêu/nội dung từng mục, 5 câu hỏi nghiên cứu và vị trí trả lời
- Ánh xạ 21 yêu cầu, 8 câu chung, 5 câu riêng đề tài 1; định danh 21 hình và nguồn bảng
- Ghi rõ 4 sơ đồ cần dựng và ảnh UI cần chụp đồng bộ; không coi là đã tạo
- Thống nhất README, bảng bằng chứng và trạng thái viết báo cáo theo dàn ý hiện hành
- Kiểm số chương, ngân sách trang, mã hình, độ phủ yêu cầu và mọi tệp nguồn được dẫn

Kết quả:
- Dàn ý phiên bản 1.0 đã sẵn sàng cho bản thảo
- 63 tham chiếu tệp tồn tại; model và ngưỡng không thay đổi
- Chưa tạo báo cáo DOCX/PDF hoặc slide; không ghi công việc dự kiến như đóng góp đã thực hiện

Tệp bằng chứng:
- `reports/DAN_Y_BAO_CAO_CHI_TIET.md`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `reports/evidence/report_outline_check.json`
- `README.md`

Giới hạn / việc còn lại:
- Font/lề/bìa theo mẫu chờ cung cấp; số trang là dự kiến.
- Nhóm 5 người cần bổ sung thông tin và đóng góp thật; chưa có BM06.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T10:49:06+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Chưa viết báo cáo DOCX/PDF và slides; chờ mẫu/thông tin nhóm.
- Nhóm cần thực sự kiểm chứng, chỉnh sửa và bổ sung đóng góp theo hướng dẫn AI của môn học.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Hoàn thiện báo cáo Word theo đúng mẫu và kiểm tra dàn trang

Thời điểm: 2026-11-10T12:40:39+07:00 (UTC+7).

Đã thực hiện:
- Dùng đúng mẫu MaiTranThienTam_2305CT2070.docx; sao chép thành reports/templates/MAU_BAO_CAO_GOC.docx, không sửa file trên Desktop.
- Giữ hai bìa, logo, bố cục bốn section, khổ A4, lề, phông, giãn dòng, kiểu tiêu đề và đánh số của mẫu; thay nội dung đề tài cũ.
- Để trống tên thành viên, lớp, khóa và giảng viên theo câu trả lời của người dùng; không tự ghi tên hoặc phân công.
- Viết báo cáo theo sáu chương của mẫu: tổng quan, cơ sở lý thuyết, phân tích/thiết kế, xây dựng, kiểm thử/đánh giá, kết luận/hướng phát triển.
- Đưa dữ liệu 7043 hồ sơ, 19 đầu vào, kiểm thiếu/trùng/ngoại lai, chia tập, 8 hình EDA và các nhận định vào báo cáo.
- Trình bày baseline, Logistic Regression, Random Forest, pipeline, 5-fold CV, tuning, lựa chọn ngưỡng validation và đánh giá test từ lần chạy đã khóa.
- Chèn 5 ảnh giao diện thật, các biểu đồ mô hình, 10 mẫu FP/FN và kết quả theo nhóm; không tạo kết quả thực nghiệm mới.
- Tạo 25 bảng từ dữ liệu/nguồn đã lưu và một bảng từ viết tắt; kiểm từng ô sau khi Word lưu.
- Đối chiếu 13 nguồn IBM/scikit-learn/Streamlit; trích dẫn theo lần xuất hiện đầu, nối với mục tài liệu tham khảo.
- Tạo mục lục Heading 1–3, danh mục hình/bảng bằng trường Word, caption SEQ theo chương và số trang PAGEREF.
- Mở Microsoft Word, cập nhật trường, lưu DOCX và xuất PDF nội bộ để kiểm tra vì máy không có soffice.exe cho render_docx.py.
- Sửa bảng ngắn bị tách trang, công thức F1 xuống dòng, hai trang ít nội dung cuối chương 1–2 và cách ngắt URL tham khảo; bổ sung nguồn StandardScaler.
- Kết xuất và xem toàn bộ 64 ảnh trang ở tmp/telco_report/render_v3; kiểm bìa, phông tiếng Việt, bảng/hình, caption, danh mục và phần cuối.
- Chạy tools.verify_report: đối chiếu 146 liên kết số trang, 25 bảng, 13 nguồn, 17 hình, cấu trúc/định dạng mẫu và SHA-256 file gốc.
- Xóa thông tin tác giả/cập nhật khỏi metadata bản đầu ra; không thay đổi document.xml sau bản PDF đã kiểm.
- Cập nhật dàn ý sáu chương, bản đồ bằng chứng, README, biên bản yêu cầu và trạng thái đóng gói; lưu dàn ý tám chương cũ để truy vết.

Kết quả:
- Báo cáo DOCX có 64 trang toàn tệp, gồm 2 bìa, 9 trang đầu đánh số La Mã và 53 trang nội dung đánh số Ả Rập.
- 6 chương; 17 hình; 25 bảng có số + 1 bảng ký hiệu; 13 tài liệu tham khảo được trích dẫn.
- 3 danh mục tự động đã cập nhật; 146 liên kết số trang khớp nội dung ở trang PDF tương ứng.
- Styles, fontTable và theme giữ nguyên byte; numbering giữ nguyên nội dung định dạng, chỉ khác tuần tự hóa XML của Word.
- Lề, khổ giấy và quy tắc đánh số trang khớp các section của mẫu; file mẫu gốc không bị thay đổi.
- Không có phụ lục, ghi chú biên tập, comment Word, tracked changes hoặc nội dung đề tài POS cũ trong báo cáo.
- Các bảng khớp dữ liệu nguồn; số liệu mô hình, ngưỡng và lần chạy không bị thay đổi.
- Nhật ký và bằng chứng kiểm tra nằm ngoài bản báo cáo.

Tệp bằng chứng:
- `reports/BAO_CAO_CUOI_KY_TELCO_CHURN.docx`
- `reports/templates/MAU_BAO_CAO_GOC.docx`
- `reports/evidence/report_build.json`
- `reports/evidence/report_qa.json`
- `reports/evidence/report_references.json`
- `tools/build_report.py`
- `tools/report_content.md`
- `tools/report_tables.py`
- `tools/verify_report.py`
- `reports/DAN_Y_BAO_CAO_CHI_TIET.md`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`

Giới hạn / việc còn lại:
- Người dùng sẽ bổ sung thông tin cá nhân/lớp/giảng viên; nhóm chưa ghi nhận đóng góp tự thực hiện.
- Slide và việc luyện bảo vệ chưa hoàn thành; không tuyên bố đạt điểm tối đa.
- Công cụ dựng/kiểm báo cáo dùng runtime tài liệu kèm ứng dụng; demo tiếp tục dùng môi trường .venv và requirements.txt hiện có.
- Nếu sửa nội dung/điền thông tin làm đổi dàn trang, cần cập nhật trường Word và kiểm lại số trang.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T12:41:00+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Báo cáo DOCX 64 trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu.
- Chưa có slide; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại báo cáo và chuẩn bị bảo vệ.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T13:22:35+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Báo cáo DOCX 64 trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu.
- Chưa có slide; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại báo cáo và chuẩn bị bảo vệ.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T13:25:42+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Báo cáo DOCX 64 trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu.
- Chưa có slide; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại báo cáo và chuẩn bị bảo vệ.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T14:28:51+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Báo cáo DOCX 68 trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu.
- Đã có 21 slide đã kiểm bằng PowerPoint; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại hồ sơ và luyện bảo vệ.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.

## 18 · Tổng hợp và đóng gói kỹ thuật

Thời điểm: 2026-11-10T14:31:13+07:00 (UTC+7).

Đã thực hiện:
- Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt
- Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên
- Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh

Kết quả:
- 18/18 bước kỹ thuật có bằng chứng
- ZIP kỹ thuật đã kiểm tính toàn vẹn

Tệp bằng chứng:
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.zip`
- `dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256`
- `dist/package_verification.json`
- `reports/evidence/package_manifest.json`
- `docs/BANG_CHUNG_CHO_BAO_CAO.md`
- `docs/AI_USAGE.md`

Giới hạn / việc còn lại:
- Báo cáo DOCX 68 trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu.
- Đã có 21 slide đã kiểm bằng PowerPoint; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại hồ sơ và luyện bảo vệ.

Thực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.
