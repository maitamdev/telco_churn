**KẾ HOẠCH VIẾT BÁO CÁO VÀ QUẢN LÝ BẰNG CHỨNG**

Ràng buộc đã xác nhận: nhóm 5 người; toàn bộ báo cáo dưới 100 trang. Mẫu sẽ do người dùng gửi sau. Chưa tạo DOCX/PDF cuối hay viết sẵn kết luận thực nghiệm. Có thể chuẩn bị nội dung, hình/bảng và trích dẫn độc lập với style từ bây giờ.

**Phạm vi và ngân sách trang**

Mục tiêu ban đầu khoảng 45-65 trang toàn bộ, không phải số trang bắt buộc phải đạt. Giới hạn nghiệm thu tuyệt đối là 99 trang, tính cả bìa, mục lục, danh mục hình/bảng, tham khảo và phụ lục. Khi có mẫu, ưu tiên quy cách mẫu và đo lại bằng PDF đã render; không suy số trang từ lượng chữ.

| Phần | Khoảng trang dự kiến | Nội dung và nguồn |
|---|---:|---|
| Bìa, mục lục, danh mục, tóm tắt | 4-6 | Thông tin thật của 5 thành viên, GV/lớp; tóm tắt viết cuối |
| Chương 1. Bài toán và mục tiêu | 3-4 | Ngữ cảnh churn, người dùng, X/y, RQ, baseline, phạm vi |
| Chương 2. Dữ liệu và làm sạch | 5-6 | Nguồn, provenance, data dictionary, chất lượng và nhật ký |
| Chương 3. Khám phá dữ liệu | 5-7 | F01-F08 có nhận định, cỡ mẫu và giới hạn |
| Chương 4. Phương pháp | 6-8 | Pipeline, LR/RF, split, CV, grid, metrics và threshold |
| Chương 5. Kết quả và so sánh | 5-7 | CV, validation, test, lựa chọn mô hình, confusion/ROC/PR |
| Chương 6. Giải thích, lỗi và giới hạn | 4-5 | Importance, FP/FN, nhóm lỗi, phạm vi sử dụng |
| Chương 7. Ứng dụng Streamlit | 5-7 | Kiến trúc, chức năng, ảnh chạy thật, kiểm thử và cách chạy |
| Chương 8. Kết luận và phát triển | 2-3 | Trả lời câu hỏi ban đầu, đạt/chưa đạt, hướng tiếp theo |
| Phân công, khai báo AI, tham khảo | 2-3 | Minh chứng đóng góp thật, nhật ký AI và nguồn |
| Phụ lục chọn lọc | 4-6 | Schema đầy đủ, params, versions, lệnh chạy, bảng bổ sung |

Tổng khoảng 45-62 trang theo phân bổ trên, dành một ít linh hoạt theo mẫu. Không thêm lý thuyết không dùng, hình trùng hoặc toàn bộ source code chỉ để làm dày báo cáo.

**Dàn ý viết cụ thể**

Chương 1: (1.1) bối cảnh giữ chân khách; (1.2) phát biểu phân loại nhị phân; (1.3) đơn vị quan sát, X/y và positive class; (1.4) năm câu hỏi nghiên cứu; (1.5) baseline và mục tiêu kỹ thuật/nghiệp vụ giả định; (1.6) giới hạn snapshot và sản phẩm.

Chương 2: (2.1) nguồn và phiên bản; (2.2) cấu trúc 21 cột/19 features; (2.3) dtype/miền/thiếu/trùng; (2.4) TotalCharges và quyết định xử lý; (2.5) nhóm No internet service/No phone service; (2.6) kiểm tra thời điểm đặc trưng; (2.7) tách tập và hồ sơ dữ liệu sau xử lý. Không nói mọi cột snapshot chắc chắn đã tồn tại trước churn khi nguồn không chứng minh được.

Chương 3: (3.1) phân bố nhãn; (3.2) hợp đồng; (3.3) tenure/cước; (3.4) Internet/dịch vụ hỗ trợ; (3.5) thanh toán; (3.6) tương quan số; (3.7) tổng hợp các quan sát và giả thuyết cần kiểm chứng bằng mô hình. Đặt rõ EDA dùng train.

Chương 4: (4.1) tổng thể quy trình; (4.2) normalization/ColumnTransformer; (4.3) Dummy; (4.4) sigmoid, loss, regularization của Logistic Regression; (4.5) cây, bootstrap, chọn feature, độ sâu/lá của RF; (4.6) split/CV/grid; (4.7) confusion/precision/recall/F1/ROC/AP; (4.8) quy tắc threshold và fallback; (4.9) chống leakage/tái lập. Toán đủ để bảo vệ quyết định thực tế, không chép nguyên giáo trình.

Chương 5: (5.1) môi trường và run; (5.2) baseline; (5.3) CV mean/std và params; (5.4) ngưỡng validation; (5.5) kết quả test các ứng viên đã cố định; (5.6) confusion/ROC/PR; (5.7) đạt/chưa đạt mục tiêu và trade-off. Người thắng được chọn trước test; bảng test không làm cơ sở quay lại tuning.

Chương 6: (6.1) permutation importance; (6.2) diễn giải cẩn trọng; (6.3) ca FP/FN; (6.4) lỗi theo nhóm; (6.5) hạn chế calibration/dữ liệu/thời gian/cỡ mẫu; (6.6) giới hạn suy luận tác động chiến dịch.

Chương 7: (7.1) yêu cầu chức năng; (7.2) module và luồng dữ liệu; (7.3) năm trang; (7.4) form/CSV validation và xuất kết quả; (7.5) dùng đúng pipeline/metadata; (7.6) ảnh chạy thật; (7.7) kết quả kiểm thử và hướng dẫn chạy local.

Chương 8: trả lời từng câu hỏi ở 1.4 bằng bằng chứng đã có; nêu sản phẩm thực sự hoàn thành; phân biệt mục tiêu đạt và chưa đạt; đề xuất dữ liệu theo thời gian, hiệu chỉnh xác suất hoặc thử nghiệm can thiệp thực tế cho tương lai. Không thêm tuyên bố kết quả mới trong kết luận.

**Danh mục hình EDA và quy tắc viết nhận định**

| Mã | Hình | Bảng nguồn cần lưu | Nội dung phải đọc được |
|---|---|---|---|
| F01 | Count và tỷ lệ Churn | label_counts_train | N, số Yes/No, phần trăm và baseline |
| F02 | Churn rate theo Contract | contract_rates_train | Mẫu số từng nhóm, số churn, tỷ lệ |
| F03 | tenure theo nhãn | tenure_summary_train | Phân phối, trung vị/quantile, cỡ mẫu |
| F04 | MonthlyCharges theo nhãn | monthly_charges_summary_train | Đơn vị đã xác minh, trung vị/IQR |
| F05 | Churn rate theo InternetService | internet_rates_train | No/DSL/Fiber optic, cỡ nhóm |
| F06 | Churn theo TechSupport/OnlineSecurity | support_security_rates_train | Nhận diện không có Internet và không mua tiện ích |
| F07 | Churn theo PaymentMethod | payment_rates_train | Tỷ lệ, cỡ nhóm, yếu tố trộn cần thận trọng |
| F08 | Tương quan số hoặc scatter có mục đích | numeric_correlations_train | tenure/Monthly/Total, thiếu và tương quan |

Mỗi hình có caption, dataset partition, đơn vị, trục, legend cần thiết; xuất vector hoặc PNG rõ. Dưới hình có 2-4 câu: quan sát định lượng, ý nghĩa, giới hạn. Những khẳng định như hợp đồng tháng churn nhiều hơn phải chờ bảng thật; chưa điền trước để ép dữ liệu khớp câu chuyện.

Hình đánh giá riêng: sơ đồ pipeline/split, confusion ở threshold=0,5 và ngưỡng chọn, ROC, PR, đường precision/recall theo threshold validation, permutation importance, ảnh từng chức năng app. Hình đánh giá không thay số hình EDA bắt buộc.

**Danh mục bảng kết quả**

| Mã | Bảng | Đầu vào máy tính | Quy tắc |
|---|---|---|---|
| B01 | Data dictionary | schema và source description | Không dịch sai enum/đơn vị |
| B02 | Chất lượng và làm sạch | data_profile/cleaning_log | Nêu số trước/sau, phương pháp, lý do |
| B03 | Split | split_manifest | Counts và tỷ lệ mỗi tập |
| B04 | Search space và best params | spec/best_params | Ghi grid đã chạy thật |
| B05 | CV mean/std | cv_results | AP metric tuyển chọn, phân biệt mean/std với CI |
| B06 | Ngưỡng validation | threshold_sweep/selection_record | threshold, P/R/F1, flagged và mục tiêu |
| B07 | Test cuối | metrics/test_predictions | Cùng test, class=1, threshold rõ |
| B08 | Feature importance | permutation_importance | Mean/std và hạn chế collinearity |
| B09 | Ca sai | error_cases | ID, y, score, pred, FP/FN, thuộc tính |
| B10 | Lỗi theo nhóm | subgroup_errors | N và confusion counts, không chỉ tỷ lệ |
| B11 | Kiểm thử app | test results + browser checks | Kịch bản, expected/actual, pass/fail |
| B12 | Đóng góp | Nhật ký thực tế của nhóm | Không tự điền phần trăm hoặc người thực hiện |

**Quy tắc thống nhất số liệu**

Mỗi bảng/hình chỉ lấy từ một run được chọn, cùng dataset/split/spec/model hashes. Báo cáo hiển thị cùng ngưỡng với app. Lưu số đầy đủ trong JSON/CSV, chỉ làm tròn khi trình bày; cùng metric dùng một quy tắc làm tròn. Không gõ lại metrics bằng tay vào nhiều nơi. Nhận xét về tỷ lệ luôn có mẫu số/cỡ nhóm phù hợp.

Phần tóm tắt gồm mục tiêu, bộ dữ liệu, hai mô hình, protocol, kết quả thật và hạn chế trong một đoạn ngắn. Viết cuối để không hứa số liệu chưa tồn tại. Phần lý thuyết có tài liệu tham khảo chính thức; phần kết quả do nhóm tạo phải dẫn tới hình/bảng của nhóm.

**Áp mẫu khi người dùng gửi**

Đọc mẫu thật trước khi chọn font, lề, heading, numbering, cover, mục lục hay style bảng. Xác định các phần mẫu bắt buộc và giữ thông tin chưa biết dưới dạng chờ bổ sung trong bản nháp. Dùng style Word, caption và mục lục có thể cập nhật; không dùng dòng trống để ép layout.

Xuất DOCX và PDF từ cùng bản cuối, render kiểm tra mọi trang; sửa ảnh cắt, tràn bảng, chữ nhỏ, mục lục sai và trang trắng. Kiểm tra PDF dưới 100 trang. Nếu mẫu khiến vượt giới hạn, rút lặp, dời mã đầy đủ sang repo và giữ phụ lục chọn lọc; không ép chữ xuống mức khó đọc.

**Tài liệu tham khảo và liêm chính**

Nguồn chính gồm PDF/slide môn học, dataset IBM, tài liệu chính thức scikit-learn và Streamlit. Ghi phiên bản/ngày truy cập khi phù hợp; không trích dẫn repo sinh viên khác như kết quả của nhóm. Khai báo AI theo AI_USAGE.md và mô tả việc tự làm/điều chỉnh/kiểm chứng thực tế. Không điền tên nhóm, MSSV, GV hoặc thông tin đóng góp khi người dùng chưa cung cấp.
