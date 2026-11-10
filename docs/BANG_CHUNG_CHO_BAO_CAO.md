# Bằng chứng sử dụng trong báo cáo

Báo cáo: `reports/BAO_CAO_CUOI_KY_TELCO_CHURN.docx`, 64 trang, 6 chương theo mẫu người dùng gửi. Dàn ý hiện tại ở `reports/DAN_Y_BAO_CAO_CHI_TIET.md`; biên bản soát báo cáo ở `reports/evidence/report_qa.json`.

| Chương | Nội dung | Nguồn đối chiếu |
|---|---|---|
| 1. Tổng quan đề tài | Bài toán, nhãn, mục tiêu, câu hỏi và phạm vi | configs/project_spec.json; README.md; hướng dẫn cuối kỳ |
| 2. Cơ sở lý thuyết | Phân loại, pipeline, LR/RF/baseline, CV, độ đo và công nghệ | 13 tài liệu chính thức ở reports/evidence/report_references.json |
| 3. Phân tích và thiết kế hệ thống | Yêu cầu, nguồn, từ điển, làm sạch, chia tập, 8 hình EDA, kiến trúc | artifacts/preparation; artifacts/eda; data/splits; docs/DATA_DICTIONARY.md; reports/evidence/data_quality_audit.csv và outlier_audit_train.csv |
| 4. Xây dựng hệ thống | Môi trường, module, pipeline, tuning, chọn ngưỡng, ứng dụng | src/; ui/; requirements.txt; artifacts/final_run/selection_record.json; reports/evidence/report_overview.png, report_single.png và ui_v2_*.jpg |
| 5. Kiểm thử và đánh giá | CV/test, ngưỡng, confusion/ROC/PR, importance, FP/FN, nhóm, kiểm thử/tái lập | artifacts/final_run; reports/PHAN_TICH_KET_QUA.md; reports/evidence/pytest*.xml, full_reproduction.json, requirements_audit.json |
| 6. Kết luận và hướng phát triển | Kết quả đạt được, giới hạn, hướng cải tiến | Các số liệu ở Chương 3–5, giới hạn dữ liệu snapshot và phạm vi demo đã kiểm |

## Quy tắc đối chiếu

1. Số liệu lấy từ lần chạy đã khóa `telco_20261110T093056_0700`; không huấn luyện hoặc chỉnh ngưỡng theo test khi viết báo cáo.
2. Phân biệt toàn bộ dữ liệu, train, CV, validation và test.
3. AP không phải PR-AUC hình thang; độ lệch chuẩn CV không phải khoảng tin cậy.
4. RF được chọn bằng CV AP; ngưỡng được chọn trên validation.
5. Precision tối thiểu 0,50 và recall mong muốn 0,80 là tiêu chí thực nghiệm của nhóm.
6. Importance không chứng minh nhân quả; dữ liệu snapshot chưa kiểm chứng dự báo sớm.
7. Bảng Word được đối chiếu từng ô với `tools/report_tables.py` và nguồn artifact.
8. Thông tin cá nhân/giảng viên trong báo cáo để trống; đóng góp nhóm phải bổ sung theo việc thực sự đã làm.

## Đối chiếu khung điểm

| Cụm điểm | Bằng chứng trong báo cáo | Phần cần nhóm hoàn thành |
|---|---|---|
| 4 điểm dữ liệu, EDA và chuẩn bị | Nguồn, thiếu/trùng/ngoại lai, từ điển, 8 hình và pipeline | Hiểu và giải thích các quyết định |
| 4 điểm mô hình và đánh giá | Baseline + LR/RF, CV/tuning, test, lỗi, importance và giới hạn | Kiểm chứng và trình bày đúng kết quả |
| 2 điểm trình bày, demo, vấn đáp | 5 màn hình Streamlit, kịch bản và kiểm lỗi | Slide, luyện trình bày và trả lời của từng người |

Chưa có BM06 chi tiết. Có đủ bằng chứng không đồng nghĩa được bảo đảm điểm tối đa. Hồ sơ đóng góp nhóm và việc sử dụng công cụ hỗ trợ được lưu riêng ngoài báo cáo.
