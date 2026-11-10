**THIẾT KẾ MÃ NGUỒN VÀ DEMO STREAMLIT**

Đặc tả trước triển khai, chưa phải ứng dụng chạy được. Mọi đường dẫn ngoài docs/planning là đầu ra dự kiến sẽ được tạo ở các mốc sau.

**Luồng xử lý**

Luồng nghiên cứu: raw CSV -> kiểm kê và split -> EDA train -> CV/tuning pipeline -> ngưỡng validation -> selection record -> test cuối -> artifacts/hình/bảng.

Luồng sử dụng: form hoặc CSV -> schema validator dùng chung -> pipeline đã lưu -> xác suất -> threshold -> nhãn/bảng tải về. App không huấn luyện lại, không tự tìm mô hình tốt nhất và không sửa kết quả test.

**Phân chia trách nhiệm mã nguồn**

| Tệp dự kiến | Trách nhiệm | Không được làm |
|---|---|---|
| src/config.py | Đọc cấu hình chạy đã chốt; tên cột, seed, đường dẫn theo project root | Gắn đường dẫn tuyệt đối máy tác giả vào sản phẩm |
| src/data.py | Đọc raw, kiểm kê, tạo/lưu split và provenance | Tuning theo toàn bộ dữ liệu |
| src/validation.py | Schema, cú pháp số, category, quan hệ dịch vụ, lỗi từng dòng | Điền cột bị thiếu hẳn mà không báo |
| src/preprocessing.py | Transformer import được và pipeline LR/RF | Fit trước split hoặc trên test |
| src/train.py | Baseline, CV, grid, refit train, log | Tự mở test để chọn ứng viên |
| src/thresholds.py | Metric theo ngưỡng, lựa chọn theo policy validation | Gọi lại fit hay chọn ngưỡng từ nhãn test |
| src/evaluate.py | Final metrics, predictions, error cases | Đổi mô hình dựa vào bảng test |
| src/explain.py | Permutation và bảng giải thích | Khẳng định nhân quả |
| src/artifacts.py | Lưu/load, kiểm tra run/hash/schema/version | Nạp file joblib tùy ý do người dùng upload |
| src/predict.py | Hàm dự đoán chuẩn từ DataFrame raw hợp lệ | Định nghĩa preprocessing khác pipeline |
| src/plots.py | Sinh hình EDA và đánh giá từ bảng nguồn | Hard-code kết luận hoặc số đo |
| app.py và ui/ | Điều hướng, widget, bảng và thông báo | Tính số liệu báo cáo bằng logic riêng |
| notebooks/ | Giải thích cách chạy và diễn giải | Là nơi duy nhất chứa class cần joblib import |
| tests/ | Kiểm tra hành vi quan trọng, dữ liệu lỗi và parity | Chỉ kiểm tra hàm trả lại đúng giá trị hard-code của chính nó |

Đầu vào cấu hình thực thi có thể tách từ planning/project_spec.json khi M1 bắt đầu; giữ bản spec đã đóng băng theo run. Không để sửa một slider làm thay cấu hình thí nghiệm đã lưu.

**Trang 1: Tổng quan dữ liệu**

- Giới thiệu mục tiêu và ý nghĩa Churn; nguồn và phạm vi dữ liệu mẫu.
- Thống kê cấu trúc, tỷ lệ nhãn và chất lượng dữ liệu đã ghi nhận.
- EDA trên train với nhãn rõ: mẫu, đơn vị, filter đang áp dụng và cỡ nhóm.
- Bảng từ điển cột và mô tả giới hạn. Phân biệt tổng thể đã kiểm kê với tập train dùng vẽ.
- Khi chưa có artifacts, hiển thị hướng dẫn chạy chuẩn bị dữ liệu; không tạo số liệu mẫu giả làm dữ liệu thật.

**Trang 2: Dự đoán một khách hàng**

Form đủ 19 đặc trưng, chia thành thông tin khách, hợp đồng/thanh toán, điện thoại/Internet, dịch vụ bổ sung và cước. customerID là tùy chọn để đặt nhãn hồ sơ; không có trường nhập Churn.

- Form giữ nhãn tiếng Việt nhưng ánh xạ sang enum nguồn đúng; tooltip giải nghĩa tenure và SeniorCitizen.
- Không dùng mức cước/ngày/tháng không có đơn vị. Đơn vị tiền tệ chỉ đặt sau khi xác minh nguồn.
- Kiểm tra số hữu hạn, không âm, tenure nguyên; TotalCharges có thể chưa biết.
- Điều kiện dịch vụ tự hướng dẫn widget phù hợp; người dùng nhìn thấy trạng thái trước khi submit.
- Kết quả: xác suất ước lượng P(Yes), nhãn tại ngưỡng chính thức, threshold, model/run version; thông báo imputation nếu TotalCharges thiếu.
- Nếu ngoài miền số đã quan sát ở train, cảnh báo suy rộng; không giả vờ đó là dự đoán đã được kiểm chứng tốt.
- Có ví dụ chọn từ dữ liệu mẫu phù hợp; không gán sẵn kết quả mong muốn. Kết quả được giữ nhất quán qua rerun.
- Không gắn 3 mức thấp/vừa/cao tùy tiện. Phiên bản đầu hiển thị hai nhóm theo ngưỡng đã giải thích.

**Trang 3: Dự đoán CSV**

Hỗ trợ UTF-8/UTF-8-BOM, dấu phẩy, tối đa 10 MiB và 10.000 dòng trong bản demo. Cung cấp CSV mẫu theo đúng 19 cột và ID tùy chọn. Các giới hạn là quyết định sản phẩm, không phải yêu cầu giảng viên.

Quy trình: đọc header -> báo thiếu/trùng cột -> phân loại lỗi schema toàn tệp hoặc lỗi từng dòng -> preview dữ liệu và thông báo cột thừa -> dự đoán rõ ràng phần hợp lệ -> xuất kết quả.

- Thiếu một cột đặc trưng hoặc header trùng: dừng, chỉ rõ tên cột, cung cấp mẫu tải về.
- Có Churn: thông báo loại khỏi đặc trưng; không dùng để suy ra dự đoán và không tự công bố metric từ upload.
- Cột thừa: liệt kê được bỏ qua, tránh cảm giác mô hình sử dụng mọi thông tin.
- Dòng sai: giữ vị trí gốc, trạng thái INVALID và lý do. Người dùng biết tổng hợp lệ/không hợp lệ trước dự đoán, không âm thầm mất dòng.
- Nếu không có customerID, thêm row_id để đối chiếu, không giả tạo mã khách thật. Nếu ID trùng trong batch, cảnh báo nhưng bảo toàn từng dòng bằng row_id.
- Xuất toàn bộ dòng theo thứ tự gốc: row_id, customerID nếu có, status, error_message, churn_probability, predicted_label, threshold, model_version. Ô xác suất/nhãn để trống cho dòng lỗi.
- Không nhúng HTML từ dữ liệu vào giao diện. Nếu xuất text CSV có nguy cơ được phần mềm bảng tính coi là công thức, xử lý an toàn ở lớp xuất và mô tả; không thay dữ liệu dùng dự đoán.

**Trang 4: Đánh giá mô hình**

- Tách rõ CV train, validation và test cuối; không trộn các loại điểm trong một nhãn chung.
- Bảng baseline/LR/RF, selected model, tham số và ngưỡng đã lưu.
- Confusion matrix hiển thị actual/predicted và Churn=Yes là positive, cả số lượng và tỷ lệ khi hữu ích.
- ROC/PR với baseline phù hợp, AP đặt tên chính xác. Kết quả test ở ngưỡng chính thức cố định, không chỉnh theo slider khảo sát.
- Dữ liệu lấy từ artifacts cùng run; nếu hash/schema/run mismatch thì dừng và thông báo cần nạp bộ artifacts nhất quán.

**Trang 5: Ngưỡng và giải thích**

- Slider chỉ khảo sát trên validation predictions đã lưu; hiển thị precision, recall, F1, số cảnh báo và tình trạng thỏa precision floor.
- Có nút trở về threshold đã chốt. Slider không ghi đè metadata, không đổi ngưỡng chính thức của trang dự đoán.
- Hiển thị đường đánh đổi và confusion counts của validation khi đổi slider; phân biệt với kết quả test trang 4.
- Permutation importance toàn cục có cỡ mẫu và độ biến động; không diễn giải thành nguyên nhân cá nhân của một khách.
- Nếu thêm what-if, ghi rõ chỉ là dự đoán với hồ sơ thay đổi giả định, không phải tác động nhân quả của ưu đãi.

**Trạng thái ứng dụng và chất lượng giao diện**

Giao diện tiếng Việt, bố cục phục vụ phân tích, sidebar điều hướng và nội dung đọc được trên màn hình laptop. Không dùng trang quảng cáo hoặc chữ trang trí chiếm không gian. Có trạng thái đang tải, chưa có model, tệp sai, không có dòng hợp lệ, predict thành công và export thành công. Không để lỗi Python dài xuất hiện thay thông báo có cách xử lý.

st.form gom dữ liệu của một hồ sơ; st.cache_resource tải model; dữ liệu bảng/hình có thể dùng st.cache_data theo run_id/hash. Không dùng state từ lượt dự đoán cũ cho hồ sơ mới mà không ghi rõ. Sử dụng model dưới dạng chỉ đọc trong app.

**Metadata bắt buộc**

run_id, model_name, created_at, training_data_hash, split_manifest_hash, spec_hash, features theo thứ tự, dtypes/enums, class_mapping, positive_class_index, threshold chính thức, threshold_policy/status, best_params, training_versions, metrics_files, pipeline_sha256 và training reference ranges. Tải artifacts tin cậy do dự án tạo, không chấp nhận upload mô hình thực thi.

**Cấu trúc dự kiến sau triển khai**

```text
telco_churn/
  README.md
  docs/ và planning/          # bộ hồ sơ hiện có
  app.py
  src/                       # các module ở bảng trên
  ui/                        # năm trang và widget dùng chung
  notebooks/                 # dữ liệu/EDA; thí nghiệm
  data/raw/                  # CSV nguyên trạng
  data/splits/               # ID và manifest
  data/samples/              # mẫu demo, lỗi kiểm thử
  artifacts/<run_id>/        # metrics, predictions, model, metadata, hình
  reports/                   # báo cáo, slide, minh chứng
  tests/
  requirements.txt
  requirements-dev.txt
```

**Môi trường đã kiểm tra, chưa phải môi trường dự án**

Python hệ thống 3.14.3; numpy 2.4.3; pandas 3.0.6; sklearn 1.9.1; matplotlib 3.11.2; seaborn 0.13.2; joblib 1.6.0; pytest 8.4.2. Streamlit chưa cài. Tạo venv riêng, xác minh tổ hợp tương thích và khóa phiên bản sau smoke test; không dùng danh sách đang cài làm requirements dự án chưa kiểm chứng.

README thực thi sau này phải hướng dẫn venv, cài dependencies, lấy dữ liệu, huấn luyện/đánh giá và chạy app. Demo dùng model sẵn; huấn luyện không nằm trong đường chạy tương tác. Cài đặt theo [Streamlit chính thức](https://docs.streamlit.io/get-started/installation).
