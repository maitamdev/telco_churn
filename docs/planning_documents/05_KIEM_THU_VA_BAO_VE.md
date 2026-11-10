**KIỂM THỬ, BẢO VỆ VÀ ĐÓNG GÓI**

Đây là các kiểm tra sẽ thực hiện trong quá trình triển khai. Trạng thái chưa chạy cho ứng dụng/mô hình vì chưa có implementation. Bằng chứng phải là log/kết quả thực tế, không chỉ dấu tick.

**Các kiểm tra quan trọng**

| ID | Tình huống | Kỳ vọng | Mốc |
|---|---|---|---|
| QA01 | Tải đúng dữ liệu nguồn | Hash/shape/schema khớp, nguồn ghi rõ | M1 |
| QA02 | Chuỗi trống TotalCharges và chuỗi chữ lỗi | Trống thành NaN, chữ lỗi bị báo; không gộp hai loại | M1/M3 |
| QA03 | Miền category, số âm, inf, tenure lẻ | Báo dòng/cột, không tự sửa dữ liệu không rõ | M1/M5 |
| QA04 | Không có điện thoại/Internet nhưng dịch vụ con mâu thuẫn | Form/CSV xử lý nhất quán, người dùng biết | M5 |
| QA05 | Các ID qua train/validation/test | Không giao nhau; split reproducible; tỷ lệ lớp ghi lại | M1 |
| QA06 | Imputer/scaler/encoder | Tham số học từ train/fold; test statistics không tham gia fit | M3 |
| QA07 | GridSearchCV | Estimator là toàn pipeline, cùng CV/split cho LR/RF | M3 |
| QA08 | Baseline không cảnh báo ai | Recall/F1=0 theo quy ước, accuracy không được gọi là hiệu quả giữ chân | M3/M4 |
| QA09 | Chọn threshold với nhiều ứng viên hòa | Áp tie-break nhất quán; dùng p>=t và lớp 1 đúng | M4 |
| QA10 | Không có threshold đạt precision floor | Báo status chưa đạt, fallback=0,5; không giả precision=1 khi không cảnh báo | M4 |
| QA11 | Mở test | Đã có selection_record ghi lựa chọn trước test | M4 |
| QA12 | Recompute metrics từ prediction arrays | Khớp metrics.json và confusion counts, totals bằng số mẫu | M4 |
| QA13 | Save/load pipeline | Xác suất allclose rtol=1e-7, atol=1e-9 trong cùng môi trường | M4 |
| QA14 | Đổi thứ tự cột CSV | Dự đoán vẫn đúng bằng tên, không nhầm vị trí | M5 |
| QA15 | CSV thiếu/trùng header, rỗng, hỏng encoding | Báo lỗi dễ hiểu, có tệp mẫu | M5 |
| QA16 | CSV có cột Churn/ID/cột thừa | Không vào X; thông báo xử lý, không leakage | M5 |
| QA17 | Batch có dòng đúng/sai, ID trùng | Giữ thứ tự và row_id, xuất trạng thái/lỗi, không mất dòng âm thầm | M5 |
| QA18 | Cùng hồ sơ qua module/form/CSV | Cùng score/label/threshold/model version | M5 |
| QA19 | Slider validation | Chỉ đổi nhãn/metric validation, không fit, không sửa artifact chính thức | M5 |
| QA20 | Không có model hoặc artifact lệch run/hash | Dừng rõ lý do; không dùng mô hình dự phòng chưa công bố | M5 |
| QA21 | Thiếu nhãn thật trong upload | Không hiển thị accuracy/recall như đã đo | M5 |
| QA22 | AppTest các luồng hỗ trợ | Điều hướng, form, state, thông báo khớp expected | M5 |
| QA23 | Trình duyệt thật | Kiểm tra bố cục/điều khiển/upload/download và nhãn tiếng Việt | M5/M7 |
| QA24 | Máy/môi trường sạch | Cài requirements và chạy theo README; không dùng cache/path máy tác giả | M7 |
| QA25 | App local sau khi cài, không Internet | Model và ví dụ sẵn, dự đoán vẫn hoạt động | M7 |
| QA26 | Báo cáo/app/slide cùng run | Counts/metrics/model/threshold khớp | M6/M7 |
| QA27 | DOCX/PDF render | Không cắt hình/bảng; mục lục/đánh số đúng, toàn PDF <=99 trang | M6 |
| QA28 | Notebook restart/run-all | Không ô lệ thuộc state cũ; kết quả nguồn khớp | M7 |
| QA29 | Gói ZIP | Đủ file cần thiết, giải nén/running được, không .venv/cache/temp | M7 |
| QA30 | Vấn đáp và chỉnh sửa trực tiếp | 5 thành viên tự giải thích/chạy/sửa phần liên quan | M7 |

Test nhằm xác nhận hành vi có rủi ro sai kết quả hoặc trải nghiệm, không tạo test hình thức cho mỗi dòng code. AppTest chỉ kiểm logic được hỗ trợ; vẫn cần trình duyệt cho upload/download và layout thực. [Tài liệu AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).

**Kiểm tra chọn ngưỡng bằng dữ liệu tổng hợp nhỏ**

Tạo bộ y/probability có thể tính tay để kiểm ≥ ở đúng biên; tính precision/recall; ngưỡng không cảnh báo ai; nhiều ngưỡng cùng recall; không có ngưỡng đạt floor. Dữ liệu này chỉ dành cho unit test, không thay dataset thật hoặc được đưa vào bảng kết quả nghiên cứu.

**Tái lập và tiêu chí chấp nhận**

Sử dụng seed, dataset/split hash, đúng phiên bản. Trong cùng môi trường, pipeline tải lại phải khớp xác suất. Trên môi trường khác chỉ được hứa kết quả trong dung sai đã kiểm chứng; nếu thư viện/hệ điều hành đổi phải ghi ảnh hưởng. Cài môi trường thứ hai và chạy từ hướng dẫn để kiểm tra phụ thuộc ngầm.

Nghiệm thu gồm hai trạng thái riêng: (a) quy trình/phần mềm/hồ sơ có đầy đủ và đúng; (b) mục tiêu nghiệp vụ tự đặt có đạt không. Mô hình không đạt recall kỳ vọng vẫn có thể là một thí nghiệm đúng và phải được báo cáo trung thực; không sửa kết quả để qua checklist.

**Kịch bản demo dự kiến 5 phút, điều chỉnh khi biết thời lượng**

1. 30 giây: bài toán, nguồn dữ liệu, mô hình/ngưỡng đang sử dụng.
2. 60 giây: dự đoán một hồ sơ mẫu, đọc xác suất và nhãn, giải thích đây là ước lượng.
3. 60 giây: upload CSV mẫu, xem rows hợp lệ/lỗi và tải kết quả.
4. 60 giây: trang đánh giá, đọc một confusion matrix; giải thích FN/FP theo nghiệp vụ.
5. 45 giây: slider validation và đánh đổi precision/recall, trả về ngưỡng chính thức.
6. 45 giây: feature importance, giới hạn và kết luận.

Chọn hồ sơ mẫu từ dữ liệu và lưu xuất xứ, không gán sẵn kết quả. Có ảnh/video dự phòng từ app chạy thật, nhưng demo local là phương án chính. Không cần tài khoản hay API ngoài để chứng minh chức năng.

**Slide và tài liệu bảo vệ**

Đề xuất khoảng 12-15 slide tùy thời lượng: bài toán; dữ liệu; chất lượng; EDA; pipeline; split/CV; hai mô hình; threshold; kết quả; lỗi; ứng dụng; giới hạn/kết luận và đóng góp. Không sao chép toàn bộ bảng dài của báo cáo lên slide. Các slide kết quả cùng run với app.

Bộ tài liệu cần chuẩn bị: kịch bản nói theo phần; sơ đồ luồng dữ liệu; bảng thuật ngữ; câu hỏi vấn đáp; bài tập thay đổi một tham số/input và giải thích kết quả. Không học thuộc một con số thay cho hiểu cách tính.

**Câu hỏi vấn đáp theo vai trò**

| Vai trò | Câu hỏi phải tự giải thích được | Bài thực hành hiểu |
|---|---|---|
| R1 | Vì sao bỏ customerID? TotalCharges trống khác số 0 thế nào? Khi nào chia theo nhóm/thời gian? | Sửa một dòng đầu vào lỗi và giải thích validator |
| R2 | Churn rate khác count ra sao? Mẫu số là gì? Vì sao tương quan không chứng minh nguyên nhân? | Tạo lại một hình và viết nhận định có cỡ mẫu |
| R3 | LR là phân loại vì sao? Scaler/encoder fit ở đâu? RF regularize bằng gì? | Tìm một tham số pipeline và giải thích thay đổi trước khi chạy |
| R4 | Precision/recall/F1/AP khác nhau thế nào? Vì sao không tune trên test? | Tính confusion/precision/recall từ ví dụ nhỏ |
| R5 | App tải model nào? CSV thiếu cột xử lý ra sao? Vì sao không train khi rerun? | Dự đoán cùng hồ sơ qua form và CSV, đối chiếu |

Mọi người còn phải trả lời tám câu hỏi chung và năm câu đề tài 1 trong ma trận yêu cầu. Phân công vai trò không miễn hiểu toàn bộ quy trình.

**Gói bàn giao dự kiến**

- Báo cáo DOCX + PDF, slide PPTX, kịch bản demo/câu hỏi.
- Source code, notebook, requirements, README với lệnh thật đã thử.
- Raw data hoặc cách tải kiểm hash, split/source information và data dictionary.
- Pipeline/metadata, selected run metrics/predictions/figures và CSV mẫu.
- Bằng chứng kiểm thử, phân công thực tế, nhật ký AI.
- ZIP có manifest danh sách/hash. Loại .venv, cache, dữ liệu tạm, tệp khóa và thông tin không liên quan.

Chưa có yêu cầu xuất bản công khai, vì vậy gói nộp local/ZIP là phương án mặc định. Không tự tạo link demo bằng deploy.
