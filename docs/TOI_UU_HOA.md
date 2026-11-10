# Tối ưu thời gian chạy và độ tin cậy

Ngày thực hiện: 10/11/2026. Phạm vi: xử lý đầu vào, suy luận hàng loạt, trạng thái giao diện và quy trình kiểm chứng/đóng gói. Model đã huấn luyện, split, cấu hình thí nghiệm, lựa chọn ngưỡng và các số liệu đánh giá được giữ nguyên.

## Kết quả đo

Máy Windows 11, Python 3.14.3; 10.000 dòng tạo bằng cách lặp mẫu 8 khách hàng hợp lệ. Mỗi tác vụ warm-up một lần, sau đó lấy trung vị ba lần chạy. Mẫu có lỗi đặt tenure=-1 ở 10% số dòng. Đây là benchmark tổng hợp trong bộ nhớ trên một máy, không đo tải nhiều người dùng hoặc thời gian truyền tệp qua mạng.

| Tác vụ | Trước (giây) | Sau (giây) | Nhanh hơn |
|---|---:|---:|---:|
| Kiểm tra 10.000 dòng hợp lệ | 0,808 | 0,112 | 7,2 lần |
| Kiểm tra dữ liệu có lỗi | 0,836 | 0,125 | 6,7 lần |
| Đọc CSV và kiểm cấu trúc | 0,825 | 0,057 | 14,4 lần |
| Dự đoán batch, gồm kiểm tra dữ liệu | 1,883 | 0,339 | 5,6 lần |
| Toàn bộ CSV → dự đoán | 2,671 | 0,308 | 8,7 lần |

Nguồn: [trước](../reports/evidence/runtime_before.json), [sau](../reports/evidence/runtime_after.json). Phép đo đọc CSV sau thay đổi chỉ kiểm cấu trúc; kiểm lỗi từng ô nằm trong predict_batch. So sánh toàn bộ CSV → dự đoán bao gồm đủ cả hai bước ở cả hai phiên bản. Các tác vụ được đo độc lập nên tổng trung vị từng phần có thể khác trung vị toàn tuyến.

Đo lại, không huấn luyện hoặc thay artifact:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m tools.benchmark_runtime --rows 10000 --repeats 5
```

## Thay đổi

- `src/validation.py`: dùng NumPy/pandas kiểm theo cột, chỉ tạo thông báo cho dòng lỗi; giữ thứ tự lỗi và vị trí dòng. Parser đọc từng bản ghi và dừng ngay khi vượt giới hạn. Không lặp lại kiểm lỗi từng ô ở bước đọc CSV. UTF-8/BOM, dấu nháy, dòng trống, cột trùng/thiếu và giới hạn 10 MiB/10.000 dòng vẫn được kiểm tra.
- `src/inference.py`: tạo cảnh báo ngoài khoảng train theo cột, không duyệt từng ô bằng `.at`; giữ nguyên pipeline và cách xác định churn.
- `src/records.py`: hash theo luồng đọc để tránh nạp toàn bộ mỗi tệp vào một buffer. Fingerprint vẫn kiểm đầy đủ nội dung mỗi lượt rerun: đo khoảng 14 ms nên không đổi sang cache chỉ dựa vào timestamp.
- `ui/scoring.py`: gắn kết quả với chữ ký của đầu vào, model và ngưỡng. Thay đổi thông tin làm hết hiệu lực kết quả cũ. `app.py` giữ tối đa một bundle trong cache tài nguyên.
- CSV tải xuống bảo vệ cả tiêu đề do người dùng cung cấp khỏi bị diễn giải thành công thức; không chuyển các số âm thật thành chuỗi.
- `tools/package_project.py`: lấy số test thực tế từ JUnit XML; yêu cầu cùng danh sách ca kiểm thử ở hai môi trường và không có failed/error/skipped. Bỏ secrets khỏi ZIP. Đồng bộ tên báo cáo hiện có `BAOCAO-TTNT.docx`; hash vẫn khớp bằng chứng kiểm báo cáo cũ.
- `.gitattributes` giữ nguyên byte của JSON/CSV/joblib để Git không làm hỏng hash artifact khi clone trên Windows. `pytest.ini` giới hạn việc tìm test trong `tests/`. GitHub Actions chạy bộ kiểm thử trên Windows/Python 3.14; các action được khóa bằng commit SHA.

## Kiểm chứng

**76/76 kiểm thử đạt ở cả hai môi trường** (`.venv` và `.venv_verify`, mỗi môi trường khoảng 9 giây). Các bài kiểm thử đối chiếu xác suất toàn bộ 1.409 dòng validation và 1.409 dòng test với kết quả đã lưu, sai số cho phép 1e-12; phép đối chiếu thực tế cho sai khác lớn nhất bằng **0** ở cả hai tập. Bao gồm kiểm hash model, phân hoạch dữ liệu, median chỉ fit trên train, dòng lỗi không được chấm điểm, tính đồng nhất dự đoán đơn/batch và cả năm trang Streamlit bằng AppTest.

Bằng chứng mới: [môi trường chính](../reports/evidence/pytest_optimized.xml) và [môi trường kiểm chứng](../reports/evidence/pytest_optimized_clean.xml). Các báo cáo `pytest.xml`, `pytest_clean_env.xml` và `full_reproduction.json` là bằng chứng của lần triển khai ban đầu, không được trình bày như lần tái huấn luyện mới.

Máy chủ Streamlit thực tế đã trả HTTP 200 ở trang gốc và `ok` tại endpoint health trên localhost; xem [kết quả smoke test](../reports/evidence/server_optimized.json). Tiến trình kiểm tra được dừng sau khi xác nhận.

Workflow [Python checks](../.github/workflows/tests.yml) chỉ kiểm thử; không triển khai ứng dụng.
