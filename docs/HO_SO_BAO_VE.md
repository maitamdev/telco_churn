# Hồ sơ trình bày và luyện bảo vệ

Áp dụng hướng dẫn 6 trang hiện có, theo xác nhận của người dùng. Không tự thêm tiêu chí BM06 hoặc thời lượng bắt buộc. Bộ slide `reports/BAO_VE_TELCO_CHURN.pptx` có 21 trang: 1–18 là mạch trình bày chính, 19–21 là câu hỏi, bản đồ mã và nguồn. Các bảng và 3 biểu đồ là đối tượng PowerPoint có thể sửa; nguồn và gợi ý diễn giải nằm trong speaker notes.

## Kịch bản gợi ý 12–15 phút

Đây là thời lượng luyện tập đề xuất, không phải quy định của giảng viên. Nếu thời lượng được giao ngắn hơn, giữ bài toán, chia tập, lựa chọn mô hình/ngưỡng, ma trận nhầm lẫn, demo và giới hạn; dùng phần còn lại để trả lời câu hỏi.

| Thời gian gợi ý | Slide | Nội dung phải nói bằng lời của nhóm |
|---|---|---|
| 0:00–1:00 | 1–2 | Nhãn, 19 đầu vào, mục tiêu sàng lọc; precision/recall là giả định nghiên cứu |
| 1:00–3:00 | 3–5 | Nguồn IBM, thiếu/trùng, EDA, train/validation/test và rò rỉ dữ liệu |
| 3:00–5:00 | 6–8 | Dummy + LR + RF, pipeline, CV, chọn ngưỡng trên validation |
| 5:00–7:00 | 9–11 | Các điểm vận hành, TP/FP/FN/TN và nhóm bị bỏ sót |
| 7:00–9:00 | 12–14 | Khoảng tin cậy, chất lượng xác suất, danh sách top-K theo năng lực xử lý |
| 9:00–12:00 | 15–16 | Demo trực tiếp và bằng chứng kiểm thử |
| 12:00–14:00 | 17–18 | Giới hạn, hướng phát triển, công khai AI và đóng góp thật |

Không đọc toàn bộ bảng. Ví dụ ở slide 10: “595 hồ sơ được đánh dấu, gồm 302 trường hợp churn đúng và 293 báo động nhầm. 72 trường hợp churn bị bỏ sót.” Sau đó chỉ rõ recall = 302/374, precision = 302/595.

## Demo có kết quả đối chiếu

Khởi động từ root: `.\.venv\Scripts\python.exe -X utf8 -m streamlit run app.py`. Dùng dữ liệu mẫu có sẵn, tránh sửa bundle đã khóa.

1. Tổng quan: lọc một nhóm hợp đồng, mở một hồ sơ sang trang phân tích. Giải thích EDA dùng train; danh sách tham khảo không phải đánh giá triển khai tương lai.
2. Phân tích khách hàng: chạy dự đoán, đổi đầu vào và kiểm tra kết quả cũ được xóa. Nêu rằng điểm 0,6 chưa được chứng minh là xác suất churn trong tháng tới.
3. Nhập danh sách: dùng `data/samples/mixed_valid_invalid.csv`. Phải có 1 dòng hợp lệ, 2 dòng lỗi; lỗi có lý do và không có xác suất giả. Tải kết quả rồi đối chiếu số dòng.
4. Hiệu quả mô hình: đọc ma trận nhầm lẫn và phần chẩn đoán bổ sung. Tại năng lực 20%, validation chọn 282/1.409 hồ sơ, bao phủ 188/374 trường hợp churn (50,27%), precision 66,67%, lift 2,51. Đây là chất lượng xếp hạng, không phải số khách được giữ chân.
5. Ngưỡng và giải thích: đổi ngưỡng khảo sát; chỉ ra precision/recall thay đổi nhưng ngưỡng chính thức trong metadata vẫn 0,4788031716353531. AP/ROC-AUC của cùng vector điểm không thay đổi theo ngưỡng.

Nếu máy trình bày không chạy được, dùng ảnh đã kiểm trong `reports/evidence` và nói rõ đang trình bày bằng chứng ghi trước. Không gọi đó là demo trực tiếp. Chuẩn bị môi trường trước buổi bảo vệ; phần cài thư viện cần mạng, ứng dụng sau khi cài không gọi API ngoài.

## Năm vai trò thực hành — chưa phải phân công đã hoàn thành

Nhóm tự điền tên/MSSV và chỉ ký xác nhận sau khi làm. Mỗi người phải hiểu toàn bộ luồng ở mức cơ bản, không chỉ học thuộc slide của mình. Ghi bằng chứng vào bảng cuối `docs/AI_USAGE.md`.

| Vai trò gợi ý | Bài thực hành cụ thể | Bằng chứng cần lưu |
|---|---|---|
| 1. Dữ liệu/EDA | Tính lại tỷ lệ thiếu TotalCharges; chọn một hình, kiểm CSV nguồn và viết nhận xét của mình | Lệnh, output, nhận xét và commit |
| 2. Pipeline/mô hình | Chỉ ra imputer fit ở đâu; giải thích LR cần scaler; chạy kiểm thử chống fit holdout | Đoạn mã, test và giải thích |
| 3. Đánh giá | Tự tính precision/recall từ confusion; đổi ngưỡng khảo sát; diễn giải CI | Phép tính, output và nhận xét giới hạn |
| 4. Ứng dụng | Tạo một CSV sai có chủ đích; sửa lỗi đầu vào; kiểm đầu ra và kết quả cũ | CSV tự tạo, ảnh chạy thật, test liên quan |
| 5. Tái lập/hồ sơ | Cài venv riêng, chạy tests, đối chiếu hash; rà bảng/nguồn và luyện demo | Log máy của mình, commit, phiếu luyện tập |

Mỗi người chọn ít nhất một cải tiến có ý nghĩa trong phần phụ trách, giải thích trước/sau và chạy kiểm thử phù hợp. Thực hiện trên nhánh riêng. Không thay mô hình/ngưỡng dựa trên test hiện có; muốn thử mô hình mới phải thiết kế run và tập đánh giá mới. Không đổi tên biến để tạo vẻ như có đóng góp.

## Tám câu chung cần tự trả lời

| Câu hỏi | Ý chính có thể kiểm chứng |
|---|---|
| Bài toán và nhãn là gì? | Phân loại nhị phân Churn Yes=1; 19 đặc trưng; customerID chỉ truy vết. Snapshot chưa xác nhận một kỳ dự báo tương lai. |
| Thành công nghĩa là gì? | Chọn bằng CV AP; chọn ngưỡng validation tối đa recall với precision ≥0,50; recall ≥0,80 là mong muốn của nhóm, không phải bảo đảm. |
| Nguồn và chất lượng dữ liệu? | IBM mẫu công ty hư cấu; 7.043×21; 1.869 churn; 11 TotalCharges trống; không trùng ID/dòng; provenance có SHA-256. |
| Làm sạch vì sao như vậy? | Chuỗi trắng → NaN; median chỉ fit train/fold; không xóa 11 khách hoặc cắt ngoại lai hợp lệ theo nhãn. “No internet service” là một trạng thái. |
| Ngăn leakage thế nào? | Loại ID/nhãn; split theo ID không giao nhau; pipeline bên trong CV; threshold chỉ dùng validation; test không tham gia lựa chọn. Timestamp của từng trường vẫn chưa có. |
| Tại sao không dùng accuracy? | Dummy đạt 73,46% test accuracy nhưng recall churn bằng 0. AP đánh giá xếp hạng; precision/recall đánh giá quyết định ở ngưỡng cụ thể. |
| RF có hơn LR mọi mặt không? | RF thắng tiêu chí CV AP đã định; chênh lệch trung bình CV nhỏ. LR có Brier/log-loss validation thấp hơn. Khoảng bootstrap chênh AP test chỉ mô tả hai model đã cố định. |
| Giới hạn và cải tiến hợp lý? | Dữ liệu hư cấu/snapshot, chưa calibration, chưa chi phí/can thiệp. Cần dữ liệu thời gian, đánh giá ngoài mẫu, hiệu chỉnh trên dữ liệu riêng và thử nghiệm can thiệp. |

## Năm câu riêng đề tài Telco

| Câu hỏi | Trả lời và bằng chứng |
|---|---|
| Mất cân bằng ảnh hưởng gì? | Churn 26,54%; stratify giữ phân bố, đánh giá AP/recall/precision; class_weight được tuning trong CV. Không SMOTE toàn bộ dữ liệu trước chia tập. |
| Ưu tiên recall hay precision? | Thiết kế hiện tại ưu tiên recall có ràng buộc precision; test 80,75% và 50,76%. CI precision 46,75–54,76%, recall 76,45–84,42%; không chứng minh đạt ngưỡng tối thiểu trên mọi quần thể. |
| Thuộc tính quan trọng có ý nghĩa gì? | Contract, InternetService, tenure đứng đầu permutation importance validation; đây là mức phụ thuộc dự đoán, không phải nguyên nhân churn hoặc lời giải thích cá nhân. |
| Dùng ngưỡng/danh sách thế nào? | 0,478803 là ngưỡng chính thức chọn trước test. Top-K là phân tích bổ sung trên validation theo khả năng xem xét; không thay ngưỡng hoặc tính lợi nhuận giả. |
| Có đặc trưng sau churn không? | Không có churn reason/status/score trong 19 đầu vào; loại nhãn/ID. Nhưng không có timestamp nên chưa loại trừ toàn bộ leakage thời gian hoặc chứng minh dự báo sớm. |

Các câu dễ bị hỏi thêm: 9 khách churn có hợp đồng Two year trong test đều bị bỏ sót ở ngưỡng chính thức; mẫu nhỏ và phân tích hậu nghiệm nên không đổi ngưỡng chỉ vì nhóm này. Brier/log-loss thấp hơn không chứng minh riêng calibration tốt hơn, vì còn phụ thuộc khả năng phân biệt. Bootstrap 2.000 lần giả định hàng độc lập; không gồm bất định huấn luyện/tuning hoặc dịch chuyển dữ liệu.

## Trước khi nộp

- Điền thông tin thật vào bìa/slide khi nhóm muốn công khai; hiện để trống theo yêu cầu trước đó.
- Xác nhận đăng ký đề tài nếu giảng viên yêu cầu, ghi phân công và đóng góp thực, đọc lại toàn bộ phân tích và khai báo AI.
- Mỗi người tự chạy demo và trả lời câu hỏi/sửa mã; lưu bằng chứng thực tế, không đánh dấu hoàn thành trước.
- Chạy lại tests sau thay đổi. Nếu sửa báo cáo/slide, cập nhật mục lục và kiểm trang; QA hash cũ không chứng minh bản sửa mới.
- Thống nhất file nộp, mở thử DOCX/PPTX/ZIP trên máy trình bày. Tài liệu không cam kết điểm số hoặc thay cho đánh giá của giảng viên.

## Tái dựng các tài liệu bổ sung

`python -m tools.build_diagnostics` tính lại chẩn đoán từ prediction đã lưu, không fit model. `python -m tools.build_report` dựng DOCX từ nguồn; `tools/render_report_word.ps1` cập nhật fields và xuất PDF bằng Word trên Windows. Sau đó cần render và kiểm trang trước khi chạy `tools.verify_report` với hồ sơ visual review của đúng SHA-256.

Slide được tạo bằng `tools/build_slides.mjs` với thư viện `@oai/artifact-tool` của runtime Codex; không thuộc dependencies chạy demo. Khi có runtime tương thích, đặt `TELCO_PROJECT_ROOT`, `TELCO_PRESENTATION_SKILL`, `TELCO_ARTIFACT_PYTHON` và `RUNTIME_NODE_MODULES`, bảo đảm Node phân giải được package. Bản PPTX đã xuất có thể mở/chỉnh bằng PowerPoint mà không cần runtime này. `tools/render_slides_powerpoint.ps1` mở chỉ đọc, xuất PNG và kiểm các đối tượng bảng/biểu đồ gốc.
