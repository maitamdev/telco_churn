# Kiểm tra đối chiếu hướng dẫn cuối kỳ

Ngày kiểm tra: 10/11/2026. Thực hiện: OpenAI Codex theo yêu cầu người dùng.

Nguồn chuẩn: `../Huong_Dan_Do_An_CuoiKy.pdf`, 6 trang. Đã đọc toàn bộ nội dung, đối chiếu hình ảnh đầy đủ trang 1–3 chứa yêu cầu chung, sản phẩm nộp, thang điểm và đề tài 1. Trang 4–6 là các đề tài khác, không áp yêu cầu riêng của các đề tài đó cho Telco.

SHA-256 hướng dẫn: `6d9cc9630c84ad1c33e55182f867b473dd721e809c411b996fa4c95c33b2b893`.

**Cập nhật sau nâng cấp:** đã có `BAOCAO-TTNT.docx` và PDF 68 trang, 6 chương theo mẫu người dùng gửi, giữ định dạng gốc. Đã kiểm toàn bộ trang, 19 hình, 28 bảng, 15 nguồn và 155 liên kết số trang. Có `BAO_VE_TELCO_CHURN.pptx` gồm 21 slide, bảng/biểu đồ chỉnh sửa được, đã mở và kiểm từng slide trong PowerPoint. Bằng chứng gắn SHA-256 ở `evidence/report_qa.json` và `evidence/slides_qa.json`. Thông tin cá nhân/lớp/giảng viên để trống theo yêu cầu; báo cáo công khai phạm vi AI hỗ trợ.

**Kết luận: phần kỹ thuật, báo cáo và slide có bằng chứng thực nghiệm; nghĩa vụ của nhóm trước khi nộp CHƯA được xác nhận hoàn tất.** Còn thông tin/phân công, đóng góp thực và luyện bảo vệ; chưa có bằng chứng giảng viên xác nhận đăng ký. Người dùng xác nhận áp dụng hướng dẫn 6 trang hiện có. Không tự thêm tiêu chí BM06 hoặc chứng nhận 10/10. Lượt nâng cấp không huấn luyện lại/chọn lại mô hình; xem `PHAN_TICH_VA_NANG_CAP.md` và `../docs/HO_SO_BAO_VE.md`.

## 1. Phạm vi kiểm chứng thực tế

- Đọc mã dữ liệu, tiền xử lý, huấn luyện, đánh giá, dự đoán, EDA, giao diện và công cụ tái lập/đóng gói; đối chiếu với artifact, không coi kế hoạch là kết quả đã làm.
- Chạy lại 99 tests trên mã hiện tại trong cả hai venv: đều đạt, 0 lỗi, 0 bỏ qua. `pip check` không phát hiện phụ thuộc hỏng ở cả hai môi trường.
- Kiểm hash bundle và mô hình; so dự đoán của model đã lưu với toàn bộ test: sai khác lớn nhất 0.
- Tính lại 5 dòng đánh giá (baseline; LR/RF ở ngưỡng mặc định và ngưỡng validation): sai khác số thực lớn nhất khoảng 1,11e-16, trong sai số làm tròn máy.
- Ghép lại 3 tập bằng ID: đủ 7.043 hồ sơ, không trùng giữa các tập, từng giá trị khớp dữ liệu gốc.
- Kiểm 8 ảnh EDA, nhận xét và số liệu nguồn; notebook có đủ 6 ô mã đã chạy và không có output lỗi.
- Giữ bằng chứng cài mới/tái huấn luyện của đợt ban đầu. Lượt mới đối chiếu trực tiếp prediction và chạy bộ test hiện tại; một số mã kiểm đầu vào/đánh giá đã thay đổi nên không gọi toàn bộ mã hiện tại giống bản tái huấn luyện cũ. Chi tiết hash trong requirements_audit.json. Không huấn luyện hoặc chọn lại ngưỡng.
- Bằng chứng 5 luồng cũ ở `reports/evidence/audit_browser_check.json`. Lượt mới kiểm 3 thẻ chẩn đoán; thanh trượt 20% → 40% đổi 282 → 564 hồ sơ, recall 50,3% → 78,1%, lift 2,51 → 1,95; không thay ngưỡng chính thức. Xem `reports/evidence/ui_upgrade_*.png` và `upgrade_browser_check.json`.
- Bổ sung bảng thiếu/kiểu dữ liệu và kiểm ngoại lai; bổ sung nhận định định lượng cho biểu đồ tổng cước. Loại thư mục tạm khỏi gói kỹ thuật.

Bằng chứng hiện tại: `reports/evidence/requirements_audit.json`, `pytest_upgrade.xml`, `pytest_upgrade_clean.xml`, `data_quality_audit.csv`, `outlier_audit_train.csv`, `artifacts/diagnostics/manifest.json`. XML 54/76 tests và log cũ giữ lại để truy vết lịch sử, không dùng làm chứng nhận số ca hiện tại.

## 2. Ma trận yêu cầu và trạng thái

Các nội dung chuyên môn đã được đưa vào báo cáo 6 chương. Bằng chứng kỹ thuật không tự chứng minh nhóm đã đọc, kiểm chứng hoặc bảo vệ được.

| Mã | Yêu cầu và vị trí trong hướng dẫn | Bằng chứng hiện có | Kết luận / việc còn lại |
|---|---|---|---|
| RQ01 | Nhóm 3–5; đăng ký nguồn và ít nhất 3 câu hỏi; tr.1 mục 2 | Người dùng xác nhận 5 người; notebook có các câu hỏi; bộ 5 câu ở mục 3 dưới đây | Quy mô phù hợp; chưa có tên/phân công thật hoặc bằng chứng giảng viên xác nhận đăng ký |
| RQ02 | Bài toán, nhãn, tiêu chí thành công, baseline; tr.1 bước 1 | Churn Yes=1; 19 đầu vào; Dummy; mục tiêu trong spec/README | Đã trình bày ở Chương 1 và đối chiếu ở Chương 5 |
| RQ03 | Nguồn, số dòng/cột, kiểu, tỷ lệ thiếu; tr.1 bước 2 | provenance, data profile, dictionary, data_quality_audit.csv | Đã bổ sung tỷ lệ thiếu và kiểu ngữ nghĩa cho từng cột |
| RQ04 | Thiếu, sai kiểu, trùng, ngoại lai và lý do; tr.1 bước 3 | cleaning_log, validation.py, outlier_audit_train.csv | Có bằng chứng; giữ ngoại lai hợp lệ, không cắt theo nhãn |
| RQ05 | Ít nhất 5 biểu đồ đủ nhãn, mỗi hình có nhận định; tr.1 bước 4 | 8 PNG train, CSV nguồn, NHAN_XET_EDA.md | 8 hình và nhận định định lượng đã đưa vào Chương 3 |
| RQ06 | Pipeline/ColumnTransformer, chỉ fit train; tr.1 bước 5, tr.2 mục 5 | FeatureNormalizer + ColumnTransformer + estimator; median/fold tests | Đủ bằng chứng chống rò rỉ do tiền xử lý; giới hạn thời gian ở mục 4 |
| RQ07 | Chia train/test đúng; tr.1 bước 6 | Train 4.225 / validation 1.409 / test 1.409; stratify, seed 42; split manifest | Các tập không trùng khách, đầy đủ dữ liệu gốc |
| RQ08 | Ít nhất 2 mô hình so với baseline; tr.1 bước 6 | Dummy + Logistic Regression + Random Forest; cv/test tables | Đủ; Dummy được tính riêng, không tính là một trong hai mô hình |
| RQ09 | Chọn và giải thích độ đo; tr.1 bước 7, tr.2 mục 5 | AP chọn mô hình; recall/precision chọn ngưỡng; FP/FN; metrics/report notes | Đã trình bày lập luận ở Chương 2 và Chương 5; không dùng accuracy đơn độc |
| RQ10 | Ma trận nhầm lẫn cho phân loại; tr.1 bước 7 | evaluation_confusion.png, test_metrics.json, màn hình đánh giá | Đã tính lại TN=742, FP=293, FN=72, TP=302 |
| RQ11 | Kiểm định chéo và tuning trong pipeline; tr.1 bước 7 | 5-fold; 8 cấu hình LR và 18 RF; toàn bộ cv_results | Đủ bằng chứng thực nghiệm |
| RQ12 | Mẫu sai, giới hạn, cải tiến; tr.1 bước 8 | 10 FP/FN cases, subgroup metrics, PHAN_TICH_KET_QUA.md | Đã phân tích 10 FP/FN ở Chương 5; giới hạn/cải tiến ở Chương 6 |
| RQ13 | Demo, lưu pipeline; tr.1 bước 9 + yêu cầu người dùng | Streamlit 5 trang, joblib, metadata, tests và kiểm trình duyệt | Có demo hoạt động thật; vẫn phải trình bày trực tiếp khi bảo vệ |
| RQ14 | Báo cáo PDF hoặc DOCX; tr.2 mục 4/7 | BAOCAO-TTNT.docx, BAOCAO-TTNT.pdf; evidence/report_qa.json | Đã viết và kiểm 68 trang theo mẫu; thông tin nhóm/giảng viên để trống để người dùng bổ sung |
| RQ15 | Notebook hoặc module chạy được; requirements, README; tr.2 mục 4 | Module, notebook đã chạy, dependencies khóa phiên bản, hướng dẫn | Có; notebook trình bày bằng chứng, module chịu trách nhiệm huấn luyện từ đầu |
| RQ16 | Dữ liệu hoặc liên kết; tr.2 mục 4 | data/raw, split, sample, URL IBM và SHA-256 | Có dữ liệu và nguồn đối chiếu |
| RQ17 | Slide, trình bày, demo, vấn đáp; tr.2 mục 4/8 | 21 slide PPTX, speaker notes, HO_SO_BAO_VE.md; demo local | Slide đã kiểm; từng thành viên cần thực sự tập trình bày và sửa mã |
| RQ18 | Git hoặc ZIP; chạy môi trường sạch; tr.2 mục 4 | Git; ZIP kiểm manifest/CRC/hash; 99 tests ở venv kiểm chứng; tái huấn luyện lịch sử | Có DOCX/PDF/PPTX; còn hồ sơ đóng góp và xác nhận của nhóm trước khi chốt bộ nộp |
| RQ19 | Seed và phiên bản; tr.2 mục 5 | Seed 42, requirements, environment, selection/metadata | Có; hash nguồn mới/cũ được báo riêng, prediction hiện tại được đối chiếu trực tiếp |
| RQ20 | Khai báo AI, đóng góp và hiểu/sửa mã; tr.1 mục 2, tr.2 mục 6 | docs/AI_USAGE.md mô tả hỗ trợ của Codex | Mới có khai báo; CHƯA có đóng góp tự thực hiện của nhóm, chưa đủ để coi là hoàn thành yêu cầu này |
| RQ21 | Nguồn dữ liệu, quyền sử dụng, riêng tư; tr.2 mục 6 | Nguồn IBM công khai, mẫu công ty hư cấu, file gốc/hash, provenance | Có truy xuất nguồn và phạm vi dữ liệu; không tự gọi giấy phép mã của repo là giấy phép riêng cho dataset; giữ ghi công nguồn trong báo cáo |

## 3. Câu hỏi nghiên cứu và câu hỏi vấn đáp

Bộ câu hỏi cụ thể tổng hợp từ đề tài và notebook hiện có, dùng khi hoàn thiện đề cương/báo cáo; việc có bộ câu hỏi không thay cho xác nhận đăng ký của giảng viên:

1. Tỷ lệ churn mất cân bằng bao nhiêu và vì sao accuracy có thể gây hiểu nhầm?
2. Hợp đồng, thời gian sử dụng, cước và dịch vụ có liên hệ với churn thế nào trên train?
3. LR và RF có cải thiện so với baseline theo AP, precision, recall và F1 không?
4. Chọn ngưỡng nào để tăng recall khi yêu cầu precision tối thiểu 50% trên validation; kết quả khi áp ngưỡng cố định lên test ra sao?
5. Những hồ sơ nào bị dự đoán sai, và mô hình phụ thuộc nhiều vào thuộc tính nào?

Năm câu riêng đề tài 1 (tr.3) đã có cơ sở trả lời:

| Câu định hướng | Câu trả lời dựa trên kết quả đã kiểm |
|---|---|
| Mất cân bằng và độ đo | Churn 1.869/7.043 = 26,54%; Dummy test accuracy 73,46% nhưng recall 0; cần precision/recall/F1 và AP |
| Ưu tiên recall hay precision | Ưu tiên phát hiện khách cần xem xét, có ràng buộc precision≥50% để kiểm soát báo động nhầm; đây là giả định của nhóm, chưa phải tối ưu chi phí |
| Thuộc tính quan trọng và bằng chứng | EDA trên train; permutation importance trên validation, 20 lần; Contract, InternetService, tenure đứng đầu; không suy ra nhân quả |
| Cách dùng và ngưỡng | Sàng lọc danh sách để nhân viên xem xét; ngưỡng 0,478803 chọn trên validation. Test: 595 người bị đánh dấu, 302 đúng, 293 báo động nhầm, bỏ sót 72 |
| Rủi ro đặc trưng xuất hiện sau churn | Đã loại ID/target và không có churn reason/status/score trong 19 đầu vào; pipeline tránh fit holdout. Tuy nhiên chưa có timestamp trước sự kiện cho từng cột, nên không chứng nhận dự báo sớm hay loại hết rủi ro thời gian |

Tám câu chung (tr.3) được bao phủ như sau: loại bài toán/nhãn → RQ02; tiêu chí/baseline → RQ02/RQ09; nguồn/quy mô/thiếu → RQ03/RQ21; làm sạch → RQ04; leakage → RQ06/RQ07 và mục 4; độ đo → RQ09; so baseline/lỗi → RQ08/RQ10/RQ12; giới hạn/cải tiến → RQ12 và mục 4. Đây là bản đồ bằng chứng, chưa chứng minh các thành viên đã hiểu.

## 4. Những điểm được làm rõ trong đợt kiểm tra

### Chất lượng và ngoại lai

`TotalCharges` có 11 ô trống, tương đương 0,156183% toàn bộ dữ liệu; 20 cột khác không thiếu theo kiểm tra ô trống. Không có dòng trùng hoàn toàn hoặc ID trùng. Bảng mới ghi cả kiểu đọc từ CSV và kiểu ngữ nghĩa để không nhầm SeniorCitizen với một biến số liên tục.

Trên toàn bộ train, cả ba biến số không có điểm vượt rào 1,5×IQR chung. Khi mô tả riêng nhóm Churn=Yes, tenure có 13 điểm và TotalCharges có 67 điểm vượt rào của nhóm. Hai con số này có thể chồng lấp khách; không cộng thành số khách riêng biệt. Rào theo nhóm chỉ phục vụ đọc biểu đồ, tuyệt đối không dùng nhãn để cắt dữ liệu trước huấn luyện. Các giá trị vẫn nằm trong miền hợp lệ và chưa có bằng chứng lỗi thu thập, nên giữ lại. “Không cắt ngoại lai” không đồng nghĩa “không kiểm ngoại lai”.

Biểu đồ 07 được bổ sung nhận định: trung vị tổng cước nhóm churn 679,30, nhóm không churn 1.677,85 (đơn vị gốc); phải đọc cùng thời gian sử dụng. Các số này là train, không phải toàn bộ dữ liệu.

### Giới hạn về thời điểm thu thập

Có hai vấn đề khác nhau: (1) rò rỉ do dùng holdout để fit imputer/scaler/encoder hoặc chọn mô hình; (2) một thuộc tính chỉ biết sau thời điểm cần dự đoán. Dự án có kiểm chứng phòng tránh (1). Với (2), dữ liệu snapshot không cung cấp lịch sử đo từng trường trước thời điểm rời bỏ. Đặc biệt cần kiểm lại thời điểm chốt tenure, TotalCharges và trạng thái hợp đồng/dịch vụ nếu đưa vào doanh nghiệp thực.

Vì vậy câu “không dùng thông tin tương lai” trong nhật ký làm sạch ban đầu phải hiểu là chủ đích thiết kế và không đưa các cột tiết lộ nhãn rõ ràng vào X; nó không phải bằng chứng kiểm chứng thời gian của tất cả cột. Báo cáo cần giữ giới hạn này; không tuyên bố đã dự báo trước 30/60/90 ngày. Lượt rà soát không thay đặc trưng hoặc tối ưu lại theo test.

### Yêu cầu nào thuộc hướng dẫn, yêu cầu nào của nhóm?

- Hướng dẫn yêu cầu ít nhất 2 mô hình và baseline, không bắt phải có mạng nơ-ron, deep learning, SVM, PCA hay SMOTE cho đề tài 1.
- Precision≥50%, recall mục tiêu≥80%, chia 60/20/20, 8 biểu đồ và 5 trang là lựa chọn triển khai; không phải mức điểm bắt buộc của giảng viên.
- Demo ở bước 9 được ghi tùy chọn, nhưng bảng điểm có demo/vấn đáp; người dùng đã yêu cầu Streamlit nên dự án vẫn phải có demo.
- Báo cáo dưới 100 trang là ràng buộc người dùng. Hướng dẫn không quy định con số trang cụ thể.
- Hướng dẫn yêu cầu PDF HOẶC DOCX; làm cả hai là kế hoạch bàn giao của dự án. Slide là sản phẩm phải có; liên kết demo công khai chỉ được khuyến khích. Không cần tự deploy để đáp ứng yêu cầu nộp local.

Trang thử ngưỡng mặc định làm tròn thanh trượt thành 0,479, trong khi ngưỡng chính thức là 0,4788031716. Do đó số validation trên thanh trượt (600 được đánh dấu, 74 bỏ sót) có thể khác số tại ngưỡng chính thức (601 được đánh dấu, 73 bỏ sót). Phải ghi đúng ngưỡng khi chụp hình đưa vào báo cáo; không dùng số minh họa thay cho kết quả validation đã khóa.

## 5. Phần còn lại trước khi nộp

1. Xác nhận việc đăng ký đề tài/nguồn/câu hỏi với giảng viên; bổ sung yêu cầu mới nếu có. Chưa có bằng chứng này trong workspace, không kết luận nhóm chưa từng đăng ký.
2. Nhóm đọc và kiểm chứng bản báo cáo 68 trang; bổ sung tên/MSSV/lớp/giảng viên và ghi đóng góp thực. Thông tin được để trống theo chỉ dẫn người dùng.
3. Đọc 21 slide và speaker notes; thực hành kịch bản demo, 13 câu hỏi và bài tập từng vai trò trong HO_SO_BAO_VE.md.
4. Ghi đóng góp thực của 5 thành viên và khai báo AI trung thực. Trang 2 mục 6 nêu: “Không nộp bài mà mã nguồn hoặc phần phân tích do AI sinh ra toàn bộ”; mỗi thành viên phải giải thích và chỉnh sửa được mã. Bản hiện tại có phần đáng kể do Codex sinh, không được ghi toàn bộ là công sức tự làm của sinh viên. Việc có file AI_USAGE chưa tự đáp ứng yêu cầu này.
5. Sau khi có báo cáo/slide, rà lại định dạng, số liệu, nguồn trích dẫn và gói nộp; luyện bảo vệ toàn bộ quy trình, không chỉ phần chia cho từng người.

## 6. Đối chiếu thang điểm, không tự chấm điểm

| Phần | Điểm trong hướng dẫn | Đánh giá bằng chứng hiện tại |
|---|---:|---|
| Câu 1: dữ liệu, khám phá, chuẩn bị, báo cáo/mã tái lập | 4,0 | Có dữ liệu, làm sạch, 8 hình EDA, pipeline và báo cáo theo mẫu; việc cho điểm phụ thuộc đánh giá của giảng viên |
| Câu 2: mô hình, đánh giá, CV/tuning, lỗi | 4,0 | Có bằng chứng, bổ sung CI, chẩn đoán xác suất và top-K; điểm phụ thuộc giải thích đúng phương pháp/giới hạn |
| Câu 3: trình bày, demo, vấn đáp từng thành viên | 2,0 | Demo hoạt động, slide đã kiểm; phần bảo vệ/đóng góp thật cần nhóm hoàn thành |

PDF tr.3 dẫn tới Đáp án BM06 nhưng workspace chưa có BM06; lượt này theo hướng dẫn 6 trang như người dùng xác nhận. Không tự quy đổi 99 tests hay 18 bước kỹ thuật thành điểm môn học, không cam kết 10/10. Dòng “18/18” là tiến độ triển khai kỹ thuật, không xác nhận đã xong nghĩa vụ của nhóm.
