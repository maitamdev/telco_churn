**DANH SÁCH CÔNG VIỆC VÀ TIẾN ĐỘ**

Ngày cập nhật: 10/11/2026. Có 53 công việc cốt lõi và 4 lựa chọn mở rộng chưa chọn. Tiến độ theo mốc, không gán ngày nộp. Nguồn có cấu trúc ở planning/tasks.json.

done nghĩa là đã có bằng chứng của đúng công việc; planned là chưa triển khai; not_selected là phần mở rộng chưa nằm trong phạm vi. R1-R5 là vai trò dự kiến của 5 người, chưa gán tên hay đóng góp thực tế.

Việc hiện tại chỉ hoàn thành M0. M1-M7 chưa có kết quả thực nghiệm/ứng dụng/báo cáo. Mẫu báo cáo và tên thành viên chỉ ảnh hưởng các bước hoàn thiện liên quan, không chặn chuẩn bị kỹ thuật.

**Thứ tự làm và đầu ra**

**M0**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M0.01 | Kiểm kê và đối chiếu 9 nguồn | R1 | Không | Đủ 9 hash, 6 trang PDF và 347 slide |
| M0.02 | Ghi ràng buộc mới và 5 vai trò | R1 | M0.01 | 5 người, 99 trang tối đa, không deadline, mẫu chờ bổ sung |
| M0.03 | Chuẩn bị đặc tả, ma trận và backlog | R3 | M0.02 | Yêu cầu có đầu ra và tiêu chí kiểm tra |
| M0.04 | Kiểm tra tính nhất quán bộ kế hoạch | R5 | M0.03 | JSON, link, task dependencies, tham số và hash nguồn hợp lệ |

**M1**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M1.01 | Tạo venv và smoke test dependencies | R5 | M0.04 | Import được thư viện; Streamlit smoke test; không phụ thuộc Python hệ thống |
| M1.02 | Đưa dữ liệu gốc vào dự án, kiểm provenance | R1 | M1.01 | URL, hash, quyền dùng và ngày nhận được ghi |
| M1.03 | Lập data dictionary và quality profile | R1 | M1.02 | 21 cột được kiểm tra, đếm missing/trùng/nhãn |
| M1.04 | Viết schema validator và normalization | R1 | M1.03 | Phân biệt trống/sai số/thiếu cột; quan hệ dịch vụ đúng |
| M1.05 | Tạo split và manifest | R3 | M1.04 | 60/20/20 stratify, seed 42, ID rời nhau |
| M1.06 | Ghi nhật ký làm sạch và kiểm ngoại lai | R1 | M1.05 | Mọi biến đổi có lý do và số dòng, không học từ test |
| M1.07 | Chuẩn bị notebook dữ liệu dùng module | R2 | M1.06 | Restart/run-all phần kiểm kê và split được |
| M1.08 | Ghi nhận đăng ký đề tài và nguồn với giảng viên | R1 | M0.02 | Không tự ghi đã đăng ký nếu chưa có thông tin |

**M2**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M2.01 | Tạo bảng nguồn cho 8 hình trên train | R2 | M1.07 | Có n, số positive, rate, đơn vị/partition |
| M2.02 | Sinh F01-F04 | R2 | M2.01 | Nhãn đầy đủ, đúng dữ liệu nguồn |
| M2.03 | Sinh F05-F08 | R2 | M2.01 | So sánh tỷ lệ, cỡ mẫu và tương quan rõ |
| M2.04 | Viết nhận định và nhóm kiểm chứng từng hình | R2 | M2.02, M2.03 | Quan sát định lượng, giới hạn; không kết luận nhân quả |
| M2.05 | Soạn bản nháp phần dữ liệu và EDA | R1 | M2.04 | Bảng/hình dẫn tới cùng dataset/split |

**M3**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M3.01 | Xây pipeline LR/RF import được | R3 | M1.06 | Fit đúng fold; numeric/categorical rõ; joblib tương thích |
| M3.02 | Chạy Dummy baseline | R3 | M3.01 | Không coi Dummy là mô hình học máy thứ hai |
| M3.03 | Chạy grid Logistic Regression | R3 | M3.02 | 8 cấu hình, 5 fold, lưu mean/std và warnings |
| M3.04 | Chạy grid Random Forest | R3 | M3.02 | 18 cấu hình, cùng folds, giới hạn worker |
| M3.05 | Kiểm hội tụ và tái lập nghiên cứu train | R3 | M3.03, M3.04 | Cảnh báo được xử lý/ghi nhận trước test |
| M3.06 | Chọn cấu hình/họ mô hình bằng quy tắc CV | R4 | M3.05 | Mean AP, tie-break đúng, chưa dùng test |
| M3.07 | Soạn phần phương pháp bằng cấu hình thật | R3 | M3.06, M2.05 | Đúng pipeline, split, CV, grid và metric đã chạy |

**M4**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M4.01 | Fit ứng viên trên train, lưu validation scores | R3 | M3.06 | classes_=1 đúng, scores gắn ID |
| M4.02 | Chọn threshold, ghi mục tiêu đạt/chưa đạt | R4 | M4.01 | Chỉ validation, precision floor và fallback đúng |
| M4.03 | Đóng băng selection record trước test | R4 | M4.02 | Có model/params/threshold, dataset/spec/split hashes |
| M4.04 | Chạy đánh giá test cuối của ứng viên cố định | R4 | M4.03 | Baseline, 0.5/selected threshold; không chọn lại bằng test |
| M4.05 | Tạo hình đánh giá và bảng so sánh | R4 | M4.04 | Tính lại từ prediction khớp, AP ghi đúng |
| M4.06 | Permutation importance và phân tích FP/FN | R4 | M4.05 | Nêu tập sử dụng, cỡ mẫu, quy tắc chọn ca |
| M4.07 | Lưu pipeline/metadata và kiểm save-load | R3 | M4.06 | Đúng pipeline đã đánh giá, allclose và hashes |
| M4.08 | Soạn kết quả và nhóm rà soát diễn giải | R4 | M4.07, M3.07 | Trả lời T1-T5, không thêm kết quả chưa đo |

**M5**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M5.01 | Khung app, loader artifacts và state | R5 | M4.07 | Thiếu/lệch run báo lỗi; không train trong UI |
| M5.02 | Trang tổng quan và EDA | R2 | M5.01, M2.04 | Nguồn, partition, cỡ mẫu rõ |
| M5.03 | Trang dự đoán một khách | R5 | M5.01 | 19 features, quan hệ dịch vụ, p/nhãn/ngưỡng đúng |
| M5.04 | Trang CSV và xuất kết quả | R5 | M5.03 | Giữ dòng/ID, lỗi rõ, không dùng Churn làm X |
| M5.05 | Trang đánh giá kết quả cố định | R4 | M5.01, M4.05 | Dữ liệu metrics cùng run, test không bị slider sửa |
| M5.06 | Trang khảo sát ngưỡng và giải thích | R4 | M5.05, M4.06 | Slider validation; không sửa official threshold |
| M5.07 | Kiểm thử form/CSV/module và trình duyệt | R5 | M5.02, M5.04, M5.06 | Parity, sai input, layout và tải file được kiểm |
| M5.08 | Chụp ảnh thật và viết chương ứng dụng | R5 | M5.07 | Ảnh đúng bản app đã kiểm, không dùng mockup thay |

**M6**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M6.01 | Ghép nội dung tám chương và nguồn tham khảo | R1 | M4.08, M5.08 | Đủ RQ và G1-G8/T1-T5, không lặp thừa |
| M6.02 | Bổ sung thông tin nhóm và đóng góp thực tế | R1 | M6.01 | Tên/MSSV do người dùng cung cấp, minh chứng thật |
| M6.03 | Rà soát nội dung, số liệu và khai báo AI | R2 | M6.02 | Một run, trích dẫn, đơn vị và nhận xét đúng |
| M6.04 | Đọc mẫu người dùng và áp dụng bố cục | R5 | M6.03 | Theo mẫu thật; không tự giả định cover/style |
| M6.05 | Xuất DOCX/PDF và kiểm mọi trang | R5 | M6.04 | Nội dung khớp, render không lỗi, tối đa 99 trang |
| M6.06 | Đối chiếu ma trận yêu cầu với báo cáo cuối | R4 | M6.05 | RQ01-RQ21 có bằng chứng hoặc trạng thái thực |

**M7**

| ID | Việc cần làm | Vai trò | Cần xong trước | Điều kiện hoàn thành |
|---|---|---|---|---|
| M7.01 | Làm slide từ kết quả đã chốt | R2 | M6.06 | Đọc được, kết quả và nguồn đúng |
| M7.02 | Kịch bản demo và dữ liệu dự phòng | R5 | M7.01 | Đi đủ luồng và lỗi, hoạt động local |
| M7.03 | Tài liệu giải thích và tập vấn đáp 5 người | R1 | M7.02 | Từng người tự chạy/giải thích/chỉnh sửa, không ghi hoàn thành giả |
| M7.04 | Khóa requirements và README thực thi | R5 | M7.02 | Các lệnh đúng đường dẫn tương đối và đã thử |
| M7.05 | Cài/chạy lại trong môi trường sạch | R5 | M7.04 | Notebook, train/evaluate, app và artifacts kiểm được |
| M7.06 | Kiểm tra chéo báo cáo-slide-app lần cuối | R4 | M7.03, M7.05 | Cùng model/run/threshold, trang PDF <100 |
| M7.07 | Đóng ZIP, hash manifest và kiểm giải nén | R5 | M7.06 | Đủ sản phẩm, không cache/venv/temp, README chạy được |

**Phần mở rộng chưa chọn**

| ID | Nội dung | Điều kiện |
|---|---|---|
| OPT.01 | Thêm Gradient Boosting trước test | Khai báo cùng protocol trước khi mở test |
| OPT.02 | Hiệu chỉnh xác suất trước test | Fit trong train/CV; không dùng test để calibration |
| OPT.03 | Khoảng tin cậy bootstrap theo kế hoạch chốt trước test | Phương pháp đã ghi trước, không lựa chọn lại theo test |
| OPT.04 | Giải thích cá nhân SHAP | Kiểm chứng đúng biến đổi/thang đo, không suy nhân quả |

Các mở rộng có ảnh hưởng mô hình/hiệu chỉnh phải được quyết định trước khi mở test. Nếu làm sau M4, phải tách thành nghiên cứu tiếp theo với thiết kế đánh giá phù hợp, không dùng lại test để gọi là xác nhận độc lập.

**Quy tắc cập nhật tiến độ**

- Mỗi việc ghi tệp thực tế, kết quả kiểm tra, lỗi còn lại và người/AI đã thực hiện; chỉ chuyển done khi tiêu chí đạt.
- Không chuyển done chỉ vì tạo tệp rỗng hoặc viết function chưa chạy.
- Công việc nhóm cung cấp/kiểm chứng được ghi bằng thông tin thật: đăng ký giảng viên, tên/MSSV, mẫu báo cáo, thực hành vấn đáp. Không tự đánh dấu thay nhóm.
- Thay đổi phạm vi/spec phải ghi trước/sau test. Lỗi triển khai sửa theo bằng chứng, không thay dữ liệu hoặc tiêu chí để tạo kết quả đẹp.
- Sau mỗi mốc, đối chiếu ma trận RQ và các câu hỏi đề tài; những thiếu sót liên quan phải xử lý trước bàn giao.

**Năm việc kỹ thuật đầu tiên sau chuẩn bị**

1. Tạo venv, cài/khóa tổ hợp dependency sau smoke test.
2. Nhận CSV chính thức, kiểm hash/nguồn và giữ nguyên raw.
3. Viết schema/data profile với kiểm thử trường hợp thiếu/sai kiểu.
4. Tạo split 60/20/20 và manifest ID, kiểm rời nhau.
5. Viết cleaning log và notebook để bắt đầu sinh tám hình EDA trên train.

Không cần người dùng xác nhận lại các lựa chọn triển khai thông thường đã nằm trong phạm vi. Chỉ trao đổi thêm khi thiếu thông tin thật hoặc có thay đổi làm ảnh hưởng đáng kể mục tiêu và kết quả.

