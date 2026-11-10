**MA TRẬN YÊU CẦU VÀ BẰNG CHỨNG**

Nguồn chính: Huong_Dan_Do_An_CuoiKy.pdf ở thư mục cấp trên của dự án, 6 trang. Mã nguồn/hash của tài liệu được ghi trong planning/source_manifest.json. Các vị trí đầu ra dưới đây là mục tiêu cần tạo, không khẳng định đã tồn tại.

| Mã | Yêu cầu | Căn cứ | Công việc | Bằng chứng dự kiến |
|---|---|---|---|---|
| RQ01 | Nhóm, đăng ký nguồn và ≥3 câu hỏi | PDF tr.1 mục 2 | M0/M1, R1 | Đề cương; ghi nhận đăng ký theo giảng viên |
| RQ02 | Bài toán, y, tiêu chí thành công, baseline | PDF tr.1 bước 1 | M0/M3 | Chương 1, project_spec, bảng baseline |
| RQ03 | Nguồn, số dòng/cột, dtype, tỷ lệ thiếu | PDF tr.1 bước 2 | M1 | data_profile, nguồn/hash, data dictionary |
| RQ04 | Xử lý thiếu, kiểu, trùng, ngoại lai kèm lý do | PDF tr.1 bước 3 | M1 | cleaning_log, trước/sau, transformer |
| RQ05 | ≥5 hình EDA có nhãn và nhận định | PDF tr.1 bước 4 | M2 | F01-F08, bảng nguồn, nhận định |
| RQ06 | Pipeline/ColumnTransformer, fit train | PDF tr.1 bước 5; tr.2 mục 5 | M3 | preprocessing.py, kiểm tra fold và transform |
| RQ07 | Chia dữ liệu đúng | PDF tr.1 bước 6 | M1/M3 | split manifest, ID disjoint, tỷ lệ nhãn |
| RQ08 | ≥2 mô hình so với baseline | PDF tr.1 bước 6 | M3/M4 | Dummy + LR + RF, bảng CV/test |
| RQ09 | Độ đo phù hợp, có lý do nghiệp vụ | PDF tr.1 bước 7; tr.2 mục 5 | M0/M4 | AP, precision/recall/F1, FP/FN và lập luận |
| RQ10 | Confusion matrix | PDF tr.1 bước 7 | M4 | Bảng đếm TN/FP/FN/TP, hình tại các ngưỡng |
| RQ11 | Kiểm định chéo và tuning trong pipeline | PDF tr.1 bước 7 | M3 | cv_results, params, mean/std, seed |
| RQ12 | Phân tích lỗi và giới hạn | PDF tr.1 bước 8 | M4 | FP/FN cases, subgroup counts, hạn chế |
| RQ13 | Streamlit và model đã lưu | Yêu cầu người dùng; PDF bước 9 | M4/M5 | joblib/metadata, app chạy thật |
| RQ14 | Báo cáo đầy đủ | PDF tr.2 mục 4/7; người dùng | M6 | DOCX/PDF cùng nội dung, dưới 100 trang |
| RQ15 | Code đầu-cuối, requirements, README | PDF tr.2 mục 4 | M1-M7 | Script/notebook, phiên bản, chạy venv mới |
| RQ16 | Dữ liệu hoặc link | PDF tr.2 mục 4 | M1/M7 | raw hoặc hướng dẫn tải, nguồn kiểm chứng |
| RQ17 | Slide và trình bày/demo/vấn đáp | PDF tr.2 mục 4/8 | M7 | PPTX, script demo, checklist từng thành viên |
| RQ18 | Gói Git hoặc ZIP, môi trường sạch | PDF tr.2 mục 4 | M7 | ZIP + manifest, log cài/chạy |
| RQ19 | Seed và phiên bản | PDF tr.2 mục 5 | M1-M7 | spec, environment, metadata và khóa phiên bản |
| RQ20 | Khai báo AI, hiểu/sửa mã, đóng góp thật | PDF tr.2 mục 6 | Xuyên suốt | AI_USAGE, review nhóm, bảng đóng góp thật |
| RQ21 | Quyền sử dụng dữ liệu, nguồn và riêng tư | PDF tr.2 mục 6 | M1/M6 | Dataset card, trích dẫn, phạm vi dữ liệu mẫu |

**Tám câu hỏi chung cần trả lời**

| Câu | Nội dung | Nơi trả lời |
|---|---|---|
| G1 | Loại bài toán và nhãn | Chương 1, app giới thiệu |
| G2 | Tiêu chí thành công và baseline | Chương 1/4/5 |
| G3 | Nguồn, mẫu/đặc trưng và tỷ lệ thiếu | Chương 2 |
| G4 | Vấn đề làm sạch và cách xử lý | Chương 2, cleaning log |
| G5 | Phòng tránh leakage | Chương 4, schema/split/pipeline |
| G6 | Chọn metric và vì sao | Chương 4/5 |
| G7 | Vượt baseline ở đâu, sai ca nào | Chương 5/6 |
| G8 | Giới hạn và cải tiến | Chương 6/8 |

**Năm câu hỏi riêng đề tài 1**

| Câu | Nội dung | Bằng chứng |
|---|---|---|
| T1 | Mất cân bằng, accuracy so với precision/recall/F1 | F01 + Dummy + bảng metrics |
| T2 | Ưu tiên recall hay precision, vì sao | Mục tiêu giả định, threshold sweep, FP/FN |
| T3 | Hợp đồng/cước/dịch vụ có quan trọng không, kiểm chứng ra sao | EDA F02/F04/F05/F06 + permutation importance |
| T4 | Doanh nghiệp dùng dự đoán thế nào, đặt ngưỡng ra sao | Quy tắc validation, top-risk list, demo, giới hạn can thiệp |
| T5 | Đặc trưng chỉ xuất hiện sau khi đã churn | Kiểm tra nguồn/thời điểm của từng cột, blacklist và hạn chế snapshot |

**Theo dõi điểm**

PDF công bố Câu 1 = 4 điểm, Câu 2 = 4 điểm, Câu 3 = 2 điểm. Chưa có BM06 nên không tự chia nhỏ thành các điểm con hay bảo đảm điểm tối đa. RQ02-07/RQ15/RQ19 hỗ trợ Câu 1; RQ07-12 hỗ trợ Câu 2; RQ13/RQ17/RQ20 hỗ trợ Câu 3, có các phần giao nhau.

**Điều kiện người dùng cập nhật**

- USER01: 5 thành viên, tên/MSSV chưa có.
- USER02: toàn bộ báo cáo dưới 100 trang, áp dụng tối đa 99 trang.
- USER03: không lập deadline; mốc hoàn thành có điều kiện kiểm chứng.
- USER04: chờ mẫu báo cáo cho định dạng cuối, tiếp tục phần kỹ thuật trước.
- USER05: không tự publish/deploy/push; làm local.

Trước bàn giao, từng RQ phải được đánh dấu có bằng chứng thực tế hoặc nêu rõ còn thiếu; không dùng tài liệu kế hoạch làm bằng chứng thay kết quả chạy.
