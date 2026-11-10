# Telco Customer Churn · Đề tài 01

Bản triển khai cho đồ án gồm dữ liệu IBM đã kiểm hash, EDA, baseline + hai mô hình, thí nghiệm cố định, Streamlit 5 trang, notebook và bằng chứng kiểm thử. Đã có [báo cáo Word](reports/BAOCAO-TTNT.docx), [PDF 67 trang](reports/BAOCAO-TTNT.pdf) và [21 slide PowerPoint](reports/BAO_VE_TELCO_CHURN.pptx). Thông tin nhóm/lớp/giảng viên để trống theo yêu cầu; nhóm cần ghi đóng góp thực và luyện bảo vệ.

## Nâng cấp theo hướng dẫn 6 trang

Xem [phân tích mức độ đáp ứng và nâng cấp](reports/PHAN_TICH_VA_NANG_CAP.md) theo ba nhóm 4–4–2 điểm; đây không phải điểm tự chấm. [Hồ sơ bảo vệ](docs/HO_SO_BAO_VE.md) có kịch bản demo, 13 câu hỏi và bài thực hành cho 5 thành viên.

- Bổ sung Wilson/paired bootstrap 95% từ prediction đã cố định; không fit/chọn lại mô hình theo test.
- Reliability diagram, Brier/log-loss và top-K/lift trên validation; giao diện cho khảo sát năng lực xem xét hồ sơ.
- **99 kiểm thử đạt ở cả hai venv**, bao gồm dữ liệu lỗi, hồi quy xác suất, CI/bootstrap, hash, giao diện và đóng gói.
- Báo cáo kiểm bằng Word: 67 trang, 19 hình, 28 bảng, 15 nguồn, 153 liên kết số trang. Slide mở và kiểm toàn bộ trong PowerPoint, có bảng/biểu đồ gốc và nguồn trong notes.

Test recall 80,75% có Wilson 95% 76,45–84,42%; precision 50,76% có khoảng 46,75–54,76%. Điểm quan sát không bảo đảm đạt ngưỡng trên quần thể mới. Top 20% validation gồm 282 hồ sơ, chứa 188/374 trường hợp churn (50,27%), lift 2,51; đây không phải số khách được giữ chân.

## Bản tối ưu ngày 10/11/2026

Trên máy kiểm thử Windows / Python 3.14.3, CSV 10.000 dòng đi từ đọc tệp đến dự đoán trong khoảng **0,31 giây**, so với **2,67 giây** trước tối ưu (trung vị 3 lần sau warm-up, nhanh hơn khoảng **8,7 lần**). Đây là phép đo cục bộ, không phải cam kết tốc độ trên mọi máy. Xem [chi tiết và cách đo lại](docs/TOI_UU_HOA.md).

- Kiểm tra đầu vào và cảnh báo ngoài khoảng train theo cột; đọc CSV có giới hạn, tránh kiểm tra từng ô hai lần.
- Kết quả dự đoán tự xóa khi thay hồ sơ, tệp CSV hoặc phiên bản/ngưỡng mô hình.
- Kiểm SHA-256 đầy đủ bằng luồng đọc; giữ nguyên model, dữ liệu, ngưỡng và thí nghiệm đã khóa.
- Bộ kiểm thử có hồi quy dữ liệu lỗi, CSV có dấu nháy/xuống dòng, dự đoán toàn bộ validation/test, giao diện và đóng gói.
- GitHub Actions chạy kiểm thử trên Windows khi push/PR; cache/venv/secrets không đưa vào Git.

## Lấy mã nguồn

~~~powershell
git clone https://github.com/maitamdev/telco_churn.git
cd telco_churn
~~~

Sau đó làm theo phần **Máy mới / môi trường sạch** bên dưới. Mô hình và dữ liệu cần để chạy demo đã nằm trong repository.

Đã rà soát trực tiếp theo hướng dẫn cuối kỳ ngày 10/11/2026. Xem [biên bản đối chiếu](reports/KIEM_TRA_YEU_CAU_CUOI_KY.md): ma trận 21 yêu cầu, bằng chứng kiểm tra, 5 câu hỏi đề tài và những phần còn thiếu. Trạng thái 18/18 bước kỹ thuật không có nghĩa bộ nộp đã hoàn tất.

[Cấu trúc báo cáo hiện tại](reports/DAN_Y_BAO_CAO_CHI_TIET.md) gồm 6 chương theo mẫu `reports/templates/MAU_BAO_CAO_GOC.docx`, thay cho dàn ý 8 chương trước khi nhận mẫu. Mục lục và danh mục hình/bảng tự động, không có phụ lục. [QA báo cáo](reports/evidence/report_qa.json) và [QA slide](reports/evidence/slides_qa.json) gắn với SHA-256 của file đã kiểm.

Giao diện đã nâng lên phiên bản 2.0 theo hướng TELCO Customer Operations: bảng khách hàng tìm kiếm/lọc được, mở hồ sơ điền sẵn, biểu đồ tương tác, biểu mẫu chia tab và kết quả đặt cạnh thông tin. Xem docs/GIAO_DIEN_V2.md và ảnh reports/evidence/ui_v2_*.jpg.

## Chạy demo ngay trên máy hiện tại

Mở PowerShell tại thư mục gốc dự án (`DU_AN_TELCO_CHURN` trên máy hiện tại hoặc `telco_churn` sau khi clone):

~~~powershell
.\.venv\Scripts\python.exe -X utf8 -m streamlit run app.py --server.port 8501
~~~

Mở http://127.0.0.1:8501. Không cần kích hoạt venv, API key, GPU hoặc dịch vụ đám mây. Dừng bằng Ctrl+C. Nếu cổng đang dùng do demo đã chạy, mở địa chỉ trên; hoặc chọn cổng 8502. Ứng dụng chỉ bind 127.0.0.1.

Có thể chạy file CHAY_DEMO.ps1 bằng PowerShell. Script không tự thay execution policy của Windows.

## Máy mới / môi trường sạch

Đã kiểm trên Windows và Python 3.14.3; các phiên bản thư viện được khóa trong requirements.txt. Không khẳng định đã kiểm các hệ điều hành hoặc bản Python khác.

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -X utf8 -m pytest -q
.\.venv\Scripts\python.exe -X utf8 -m streamlit run app.py
~~~

Gói kỹ thuật có sẵn dữ liệu và model. Chỉ việc cài thư viện cần Internet; sau đó demo không gọi dịch vụ bên ngoài. Giữ nguyên cấu trúc src, configs, data và artifacts. File joblib chỉ được nạp từ bundle của dự án, không nhận model do người dùng upload.

## Sáu phần, 18 bước

1. Môi trường: bước 01–02.
2. Dữ liệu và chia tập: bước 03–05.
3. EDA và nhận xét: bước 06–07.
4. Pipeline, mô hình, đánh giá, đóng gói: bước 08–12.
5. Streamlit: bước 13–14.
6. Kiểm thử, tái lập, bằng chứng và ZIP: bước 15–18.

Xem docs/18_BUOC_TRIEN_KHAI.md. Nhật ký append-only ở logs/NHAT_KY_THUC_HIEN.md; bản JSONL ở logs/events.jsonl. Trạng thái hiện tại ở configs/execution_status.json.

## Thí nghiệm đã chốt

- Dữ liệu gốc: 7.043 dòng × 21 cột; Churn Yes=1; 19 đặc trưng. customerID dùng truy vết.
- Train 4.225 / validation 1.409 / test 1.409, stratify, seed 42; ID/hash trong data/splits/split_manifest.json.
- 11 TotalCharges trống; train có 7. Chuyển NaN trong pipeline, median fit trong từng fold/train. Không xóa dòng.
- DummyClassifier most_frequent làm baseline. Logistic Regression 8 cấu hình, Random Forest 18 cấu hình, 5-fold CV trên train.
- Chọn bằng mean Average Precision (AP); std AP phá hòa. Không dùng test để chọn.
- Ngưỡng: precision≥0,50 rồi tối đa recall trên validation; mục tiêu recall≥0,80 là giả định nhóm.
- Khóa lựa chọn trước test; không refit train+validation sau chọn ngưỡng. Demo dùng đúng model này.
- configs/project_spec.json là snapshot bất biến của thiết kế ban đầu, bao gồm cờ trạng thái tại thời điểm lập kế hoạch. Các cờ đó không phải trạng thái thực thi; xem execution_status.json và metadata.

Random Forest được chọn: 300 cây, max_depth=None, min_samples_leaf=20, class_weight=balanced. CV AP=0,672568 ± 0,013939; LR=0,667818 ± 0,024414. Chênh lệch nhỏ, chưa chứng minh khác biệt có ý nghĩa thống kê.

| Trên test | Dummy gốc | LR, ngưỡng 0,5 | RF, ngưỡng chính thức 0,478803 |
|---|---:|---:|---:|
| Accuracy | 0,7346 | 0,7984 | 0,7410 |
| Precision churn | 0 | 0,6389 | 0,5076 |
| Recall churn | 0 | 0,5535 | 0,8075 |
| F1 churn | 0 | 0,5931 | 0,6233 |
| ROC-AUC | 0,5000 | 0,8425 | 0,8435 |
| AP | 0,2654 | 0,6285 | 0,6482 |

RF ở ngưỡng chính thức: TP=302, FP=293, FN=72, TN=742. Ưu tiên recall làm tăng báo động nhầm; không đồng nghĩa mô hình tốt nhất theo mọi mục tiêu. Đầy đủ cả 5 cấu hình vận hành trong artifacts/final_run/test_metrics.csv.

## Cấu trúc chính

| Đường dẫn | Nội dung |
|---|---|
| app.py, ui/ | 5 trang Streamlit |
| src/data.py, validation.py | Nguồn, chất lượng, split, hợp đồng đầu vào |
| src/preprocessing.py | Pipeline dùng chung cho huấn luyện và suy luận |
| src/train.py, evaluation.py | CV, khóa lựa chọn, đánh giá, chọn ngưỡng |
| src/inference.py | Kiểm hash và dự đoán cá nhân/CSV |
| src/eda.py, result_figures.py | Hình, bảng nguồn, nhận xét |
| data/raw, splits, samples | Dữ liệu gốc, phân hoạch và CSV demo |
| artifacts/eda | 8 PNG + CSV nguồn + nhận xét train |
| artifacts/final_run | Model, metadata, CV, prediction, metrics, importance, hình |
| src/diagnostics.py, artifacts/diagnostics | CI, reliability, Brier/log-loss, gain/lift; manifest nguồn |
| notebooks/01_telco_churn.ipynb | Notebook có output thực thi |
| tests/ | Unit, integration, Streamlit AppTest |
| reports/evidence | Test XML, screenshot, tái lập, kiểm notebook |
| reports/PHAN_TICH_KET_QUA.md | Nhận xét kết quả thực, phục vụ báo cáo |
| docs/BANG_CHUNG_CHO_BAO_CAO.md | Ánh xạ nội dung báo cáo tới bằng chứng |
| docs/AI_USAGE.md | Ghi nhận sử dụng AI và phần nhóm cần tự thực hiện |
| docs/BAO_VE_VA_DEMO.md | Kịch bản demo và câu hỏi bảo vệ |
| tools/ | Tạo notebook, tái lập, đóng gói/kiểm gói |

docs/planning_snapshot và docs/planning_documents là hồ sơ kế hoạch trước triển khai, giữ nguyên để truy vết.

## Dùng CSV

Tải data/samples/valid_customers.csv để thử; mixed_valid_invalid.csv có 1 dòng hợp lệ và 2 dòng lỗi. template.csv chỉ có tiêu đề để điền dữ liệu. Đủ 19 cột đặc trưng là bắt buộc, kể cả TotalCharges (giá trị cột này được phép thiếu). ID tùy chọn. Danh mục phải theo docs/DATA_DICTIONARY.md; SeniorCitizen nhận 0/1. Churn nếu có được giữ lại trong đầu ra nhưng không vào model và không tự tính accuracy.

Giới hạn 10 MiB, 10.000 dòng, UTF-8/BOM, dấu phẩy. Dòng lỗi không bị xóa và không có xác suất giả. Cột bổ sung được thông báo và bỏ khỏi model. Cột kết quả trùng tên bị từ chối để không ghi đè dữ liệu đầu vào.

## Tái lập và kiểm chứng

Kiểm tests, notebook và tái huấn luyện đầy đủ cùng cấu hình trong một bản sao riêng:

~~~powershell
.\.venv\Scripts\python.exe -X utf8 -m pytest -q --junitxml=reports/evidence/pytest_upgrade.xml
.\.venv\Scripts\python.exe -X utf8 -m tools.build_notebook
.\.venv\Scripts\python.exe -X utf8 -m tools.verify_reproduction
~~~

verify_reproduction tạo thư mục .reproduction/fixed_spec_... riêng, chạy lại 130 lần fit CV của hai mô hình cùng baseline/refit/importance, rồi đối chiếu lựa chọn, tham số, ngưỡng, CV và xác suất. Không ghi đè run chính. Đọc reports/evidence/full_reproduction.json.

Để xây mới từ đầu trong một thư mục chưa có final_run: python -m src.data → python -m src.eda → python -m src.train → python -m src.result_figures. src.train từ chối ghi đè run đã khóa. Không xóa selection_record chỉ để thử tối ưu theo test. Thiết kế mới cần lưu run riêng và quy trình đánh giá phù hợp.

Các bước sau chỉ tái dựng hình/nhận xét, không đổi model:

~~~powershell
.\.venv\Scripts\python.exe -X utf8 -m src.eda
.\.venv\Scripts\python.exe -X utf8 -m src.result_figures
.\.venv\Scripts\python.exe -X utf8 -m tools.build_diagnostics
~~~

Đóng gói yêu cầu hai báo cáo kiểm thử cùng bộ ca, đạt toàn bộ ở môi trường chính và môi trường kiểm chứng. Tạo báo cáo thứ hai trước khi đóng gói (venv này cài riêng cùng requirements.txt):

~~~powershell
python -m venv .venv_verify
.\.venv_verify\Scripts\python.exe -m pip install -r requirements.txt
.\.venv_verify\Scripts\python.exe -X utf8 -m pytest -q --junitxml=reports/evidence/pytest_upgrade_clean.xml
~~~

Đóng gói và kiểm hash gói; gói không chứa môi trường, cache hay secrets. Công cụ cũng yêu cầu chẩn đoán và SHA-256 báo cáo/PDF/slide khớp hồ sơ QA; nếu sửa tài liệu cần kiểm lại trước khi đóng gói:

~~~powershell
.\.venv\Scripts\python.exe -X utf8 -m tools.package_project
~~~

## Khắc phục lỗi thường gặp

- Thiếu thư viện: dùng đúng .venv\Scripts\python.exe và cài requirements.txt.
- Artifact sai hash: dùng lại bundle đầy đủ đúng phiên bản; không bỏ kiểm hash hoặc tạo dự đoán giả.
- scikit-learn khác phiên bản: cài requirements.txt vào venv sạch.
- Thiếu cột/danh mục CSV: dùng template và dictionary, không tự đoán cột thiếu.
- Terminal in tiếng Việt lỗi: thêm -X utf8 như các lệnh trên.
- Biểu đồ, model không tìm thấy: giữ cấu trúc thư mục khi giải nén và chạy tại root dự án.

## Giới hạn và việc còn lại

Dữ liệu là mẫu công ty hư cấu; mô hình snapshot không có kỳ dự báo tương lai đã được chứng minh. Xác suất chưa calibration. Chưa có chi phí thực, dữ liệu can thiệp, thời gian, hoặc đánh giá ngoài doanh nghiệp để khẳng định hiệu quả giữ chân. Báo cáo và slide đã có; còn thông tin, đóng góp thực và phần hiểu/bảo vệ của nhóm. Đợt nâng cấp áp dụng hướng dẫn 6 trang hiện có; không giả định thêm BM06.

Nhóm 5 người cần tự tham gia, kiểm chứng/chỉnh sửa và ghi đóng góp thực theo hướng dẫn môn học; không ghi nhận các phần do Codex làm như công sức đã có của sinh viên. Xem docs/AI_USAGE.md.

