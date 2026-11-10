# Đánh giá và nâng cấp theo hướng dẫn 6 trang

Ngày 10/11/2026. Căn cứ: hướng dẫn cuối kỳ hiện có và xác nhận của người dùng; chưa có tiêu chí BM06 bổ sung. Đây là đánh giá mức độ có bằng chứng, không phải điểm chấm thay giảng viên.

## Dự án ban đầu đã tốt ở đâu?

Đã có một thí nghiệm có thể truy vết: dữ liệu/seed/hash cố định, 8 hình EDA trên train, Dummy + LR + RF, pipeline trong CV, validation chọn ngưỡng, test riêng, phân tích lỗi và demo Streamlit. Tối ưu CSV trước đó đã giảm thời gian 10.000 dòng từ khoảng 2,67 xuống 0,31 giây trên máy đo. Không cần đổi thuật toán chỉ để trông phức tạp hơn hoặc điều chỉnh theo kết quả test.

Các điểm còn yếu trước lượt này: chủ yếu trình bày ước lượng điểm, chưa định lượng bất định; chưa kiểm chất lượng xác suất, chưa nối kết quả xếp hạng với số hồ sơ đội chăm sóc có thể xem; chưa có PPTX hoàn chỉnh; hồ sơ luyện bảo vệ/đóng góp cần cụ thể hơn.

## Đối chiếu ba nhóm điểm

| Nhóm theo hướng dẫn | Bằng chứng hiện tại | Việc vẫn phụ thuộc nhóm |
|---|---|---|
| Dữ liệu, EDA, tiền xử lý, tái lập — 4 điểm | Nguồn và hash; kiểm thiếu/trùng/ngoại lai; 8 hình có nhận định; pipeline chống fit holdout; môi trường khóa phiên bản | Tự giải thích mỗi quyết định, chỉ được tới mã và bảng nguồn |
| Mô hình, đánh giá, giải thích, cải tiến — 4 điểm | Baseline + 2 thuật toán; 5-fold tuning; 5 điểm vận hành test; FP/FN; importance; bổ sung CI, xác suất, top-K | Tự tính độ đo; phân biệt validation/test; không suy diễn CI, tương quan hoặc hiệu quả giữ chân |
| Trình bày, demo, vấn đáp — 2 điểm | Báo cáo theo mẫu; 21 slide có notes; demo thật; kịch bản và 13 câu hỏi theo hướng dẫn | Điền thông tin, đóng góp thực, luyện trình bày/sửa mã và trả lời trực tiếp |

Mức bao phủ kỹ thuật không tự chuyển thành 10/10. Yêu cầu về đóng góp thật, công khai AI và năng lực bảo vệ chưa thể được phần mềm hoàn thành thay nhóm.

## Những nâng cấp đã thực hiện

1. Khoảng tin cậy Wilson cho precision/recall/accuracy; bootstrap hàng ghép cặp 2.000 lần, seed 42 cho AP/AUC/F1 và chênh AP RF–LR. Model và threshold được giữ cố định. Kết quả nằm trong `artifacts/diagnostics` với manifest kiểm hash nguồn.
2. Kiểm xác suất bằng reliability diagram, Brier và log-loss trên validation; thêm mốc xác suất hằng lấy prevalence train, phân biệt với Dummy most_frequent chính thức.
3. Bảng gain/lift theo năng lực 10–100%, chọn theo điểm giảm dần và ID phá hòa, không dùng nhãn để xếp hạng. Thêm điều khiển tương tác ở trang Hiệu quả mô hình.
4. Bắt lỗi nhãn không nhị phân/không đúng chiều trước khi ép kiểu trong threshold_sweep; bổ sung kiểm thử thống kê, bootstrap, tie, hash và giao diện.
5. Cập nhật báo cáo theo mẫu, bổ sung 3 phần đánh giá và công khai AI; tạo bộ 21 slide có bảng/biểu đồ gốc, nguồn trong notes; thêm hồ sơ luyện bảo vệ và bản đồ bằng chứng.

## Kết luận định lượng cần nói chính xác

| Kết quả | Cách diễn giải |
|---|---|
| Test recall 80,75%; Wilson 95%: 76,45–84,42% | Điểm quan sát đạt 80%, nhưng khoảng bao gồm mức thấp hơn; không bảo đảm đạt 80% ngoài mẫu |
| Test precision 50,76%; Wilson 95%: 46,75–54,76% | Chưa chứng minh precision của quần thể luôn ≥50% |
| AP test RF–LR = +0,01970; percentile 95%: +0,00161 đến +0,03661 | Khác biệt dương có điều kiện trên hai model đã fit; không bao gồm bất định tuning/train, không dùng để chọn lại model |
| Validation Brier: LR 0,13781; RF 0,16521 | LR tốt hơn ở điểm xác suất này; không kết luận RF hơn mọi mặt hoặc Brier chỉ đo calibration |
| Top 20% validation: 282 hồ sơ, 188 churn, recall 50,27%, lift 2,51 | Giúp ước lượng khối lượng xem xét; không có nghĩa giữ chân được 188 khách hoặc đã tối ưu lợi nhuận |

CI giả định dữ liệu IID và mô hình cố định; validation đã dùng chọn ngưỡng nên các chẩn đoán tại đây mang tính mô tả/thăm dò. Dữ liệu snapshot hư cấu không chứng minh khả năng dự báo trước thời hạn tương lai hoặc tác động kinh doanh.

## Bằng chứng và bước cuối

Kết quả kiểm thử ở `evidence/pytest_upgrade.xml` và `pytest_upgrade_clean.xml`; báo cáo ở `evidence/report_qa.json`; slide ở `evidence/slides_qa.json`; đối chiếu dữ liệu/model ở `evidence/requirements_audit.json`. QA tài liệu chỉ hợp lệ khi SHA-256 trùng file hiện tại. Các lần kiểm cũ được giữ để truy vết, không phải chứng nhận mã mới.

Nhóm thực hiện các bài thực hành và ghi đóng góp thật theo `docs/HO_SO_BAO_VE.md` và `docs/AI_USAGE.md`. Báo cáo/slide có khai báo phạm vi AI; không gán công việc do AI thực hiện cho sinh viên. Sau khi sửa tài liệu hoặc mã, chạy và kiểm lại đúng phần thay đổi trước nộp.
