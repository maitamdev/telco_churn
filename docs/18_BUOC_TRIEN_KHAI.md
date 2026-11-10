**SÁU PHẦN, MƯỜI TÁM BƯỚC TRƯỚC KHI VIẾT BÁO CÁO CUỐI**

Đây là lộ trình thực thi gộp từ backlog nghiên cứu trước đó. Nhật ký từng bước ở logs/NHAT_KY_THUC_HIEN.md và events.jsonl. Chỉ đánh dấu hoàn thành khi đã có bằng chứng.

| Phần | Bước | Công việc | Bằng chứng |
|---|---|---|---|
| 1. Môi trường | 01 | Tạo thư mục riêng, sao lưu kế hoạch | Cấu trúc và bản snapshot |
| | 02 | Venv, cài thư viện, ghi phiên bản | Environment và requirements |
| 2. Dữ liệu | 03 | Tải dữ liệu gốc và kiểm hash | Raw CSV, provenance |
| | 04 | Kiểm schema, chất lượng và quyết định làm sạch | Profile, dictionary, cleaning log |
| | 05 | Chia train/validation/test cố định | Split manifest và ID |
| 3. EDA | 06 | Tạo tám hình và bảng nguồn từ train | Hình/bảng EDA |
| | 07 | Viết nhận định định lượng và kiểm hình | Observations và kiểm tra hình |
| 4. Mô hình | 08 | Pipeline và baseline | Mã, baseline CV |
| | 09 | CV/tuning LR và RF | CV results, best params |
| | 10 | Chọn mô hình/ngưỡng trên train/validation | Selection record trước test |
| | 11 | Đánh giá test, giải thích và phân tích lỗi | Metrics, predictions, importance, error cases |
| | 12 | Lưu/load pipeline và metadata | Model bundle, parity check |
| 5. Streamlit | 13 | Tổng quan và dự đoán một khách | App dùng pipeline thật |
| | 14 | CSV, đánh giá, ngưỡng và giải thích | Năm trang, mẫu dữ liệu |
| 6. Kiểm chứng | 15 | Unit/integration/AppTest | Test log |
| | 16 | Kiểm trên trình duyệt thật | Ảnh và nhật ký UI |
| | 17 | Môi trường sạch, notebook, hướng dẫn chạy | Reproduction log và README |
| | 18 | Tổng hợp bằng chứng, gói mã và ghi việc còn lại | Manifest, gói ZIP, ghi chú cho báo cáo |

Sau bước 18, mới hoàn thiện báo cáo theo mẫu người dùng gửi. Kết quả mô hình không được bảo đảm hoàn hảo: luôn báo mục tiêu đạt/chưa đạt và giới hạn thật. Không tự deploy/push. Nhóm 5 người phải tham gia chỉnh sửa/kiểm chứng và hiểu bài theo hướng dẫn môn học.
