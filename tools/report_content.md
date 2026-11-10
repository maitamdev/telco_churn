# TỔNG QUAN ĐỀ TÀI
## Đặt vấn đề
Trong hoạt động cung cấp dịch vụ viễn thông, thông tin khách hàng không chỉ phục vụ quản lý hợp đồng và thanh toán mà còn có thể được khai thác để hỗ trợ công tác chăm sóc khách hàng. Khi số lượng hồ sơ tăng lên, việc xem xét từng khách hàng bằng phương pháp thủ công gặp nhiều khó khăn. Các thuộc tính như thời gian sử dụng, loại hợp đồng, hình thức thanh toán và dịch vụ đăng ký tạo thành nhiều tổ hợp khác nhau, khiến việc xây dựng một quy tắc đơn giản cho tất cả trường hợp trở nên thiếu linh hoạt.

Khách hàng rời dịch vụ, thường được gọi là churn, là đối tượng cần được quan tâm trong bài toán này. Hệ thống dự đoán churn sử dụng những hồ sơ đã có nhãn để học mối liên hệ giữa các thuộc tính và tình trạng rời dịch vụ. Từ đó, hệ thống tính điểm cho hồ sơ cần phân tích, giúp người sử dụng xác định những trường hợp nên xem xét trước. Kết quả của mô hình hỗ trợ sàng lọc, còn hoạt động liên hệ, xác minh nguyên nhân và lựa chọn biện pháp chăm sóc vẫn thuộc trách nhiệm của nhân viên.

Đề tài sử dụng bộ dữ liệu Telco Customer Churn được công bố trong kho mã của IBM [1]. Dữ liệu có 7.043 hồ sơ, gồm các thông tin về khách hàng, dịch vụ, hợp đồng, cước và nhãn Churn. Đây là bộ dữ liệu mẫu của một doanh nghiệp viễn thông hư cấu, phù hợp để xây dựng và đánh giá một quy trình học máy có giám sát. Kết quả thực nghiệm trên bộ dữ liệu này không được xem là số liệu kinh doanh của một doanh nghiệp viễn thông tại Việt Nam.

Một khó khăn đáng chú ý là sự mất cân bằng giữa hai lớp. Số khách hàng có Churn=Yes chiếm 26,54%, trong khi phần còn lại thuộc lớp No. Nếu hệ thống luôn dự đoán khách hàng không rời dịch vụ thì vẫn có thể đạt accuracy tương đối cao, nhưng không phát hiện được trường hợp churn nào. Vì vậy, đề tài cần xây dựng mô hình đối chứng, lựa chọn độ đo phù hợp và phân tích sai số thay vì chỉ báo cáo một tỷ lệ dự đoán đúng chung.

Từ yêu cầu đó, đề tài “Dự đoán khách hàng rời dịch vụ viễn thông bằng học máy” được thực hiện theo một quy trình thống nhất từ kiểm tra dữ liệu, khám phá, tiền xử lý, huấn luyện, lựa chọn mô hình đến xây dựng ứng dụng Streamlit. Hai mô hình Logistic Regression và Random Forest được so sánh với mô hình đối chứng DummyClassifier. Ứng dụng sử dụng trực tiếp pipeline đã lưu để dự đoán hồ sơ cá nhân và danh sách khách hàng, đồng thời cung cấp các màn hình phục vụ giải thích kết quả thực nghiệm.

## Mục tiêu đề tài
### Mục tiêu tổng quát
Mục tiêu tổng quát của đề tài là xây dựng một hệ thống thử nghiệm có khả năng phân loại tình trạng churn từ dữ liệu khách hàng dạng bảng, đánh giá được chất lượng mô hình trên dữ liệu độc lập và cung cấp giao diện sử dụng trực quan. Sản phẩm phải thể hiện được mối liên hệ giữa bài toán nghiệp vụ, dữ liệu đầu vào, thuật toán học máy và cách sử dụng kết quả trong một quy trình chăm sóc khách hàng.

### Mục tiêu cụ thể
Về dữ liệu, đề tài xác định rõ nguồn, quy mô, ý nghĩa thuộc tính, tình trạng thiếu, trùng lặp và các giá trị cần kiểm tra. Các nhận định khám phá được rút ra từ tập huấn luyện, kèm biểu đồ và số liệu tương ứng. Những bước học thống kê như điền giá trị thiếu, chuẩn hóa và mã hóa được đặt trong pipeline để tránh sử dụng thông tin của tập đánh giá trong quá trình huấn luyện.

Về mô hình, đề tài xây dựng một baseline và hai thuật toán phân loại, thực hiện kiểm định chéo phân tầng năm phần, tìm kiếm siêu tham số và so sánh theo Average Precision. Ngưỡng phân loại được lựa chọn trên tập validation với mục tiêu ưu tiên recall trong điều kiện precision không thấp hơn 50%. Mức recall 80% được dùng làm mục tiêu mong muốn của nhóm trong thực nghiệm, không phải một cam kết chất lượng khi triển khai thực tế.

Về ứng dụng, đề tài xây dựng năm màn hình gồm tổng quan, phân tích khách hàng, nhập danh sách, hiệu quả mô hình và khảo sát ngưỡng. Dữ liệu đầu vào được kiểm tra trước khi dự đoán; kết quả thể hiện điểm churn, trạng thái phân loại và khả năng xuất danh sách. Đồng thời, dự án lưu dữ liệu, cấu hình, phiên bản thư viện và kết quả kiểm thử nhằm hỗ trợ chạy lại và đối chiếu.

@table objectives|Mục tiêu và tiêu chí đánh giá của đề tài

### Câu hỏi nghiên cứu
Đề tài tập trung trả lời năm câu hỏi. Thứ nhất, mức độ mất cân bằng của dữ liệu ảnh hưởng thế nào đến cách đánh giá mô hình? Thứ hai, loại hợp đồng, thời gian sử dụng, dịch vụ Internet và cước có liên hệ như thế nào với churn trên tập huấn luyện? Thứ ba, Logistic Regression và Random Forest cải thiện ra sao so với baseline? Thứ tư, việc thay đổi ngưỡng tạo ra sự đánh đổi nào giữa phát hiện khách hàng churn và báo động nhầm? Thứ năm, các trường hợp dự đoán sai và độ quan trọng của thuộc tính cho thấy những giới hạn nào của hệ thống?

## Đối tượng và phạm vi đề tài
### Đối tượng nghiên cứu
Đối tượng nghiên cứu là bài toán phân loại nhị phân trên dữ liệu Telco Customer Churn. Một quan sát tương ứng với một hồ sơ khách hàng. Nhãn mục tiêu được mã hóa Churn=Yes thành 1 và Churn=No thành 0. Từ 21 cột ban đầu, customerID chỉ được giữ để truy vết và Churn được tách làm nhãn; 19 thuộc tính còn lại được đưa vào mô hình.

Người sử dụng giả định của ứng dụng là nhân viên hoặc người quản lý công tác chăm sóc khách hàng. Người sử dụng cần tra cứu một hồ sơ, kiểm tra danh sách nhiều hồ sơ và hiểu chất lượng của bộ phân loại trước khi sử dụng kết quả. Trong phạm vi đồ án, ứng dụng chạy tại máy tính cá nhân và sử dụng dữ liệu mẫu, chưa kết nối với hệ thống quản lý khách hàng của doanh nghiệp.

### Phạm vi thực hiện
Đề tài thực hiện quy trình xử lý dữ liệu dạng bảng, phân tích khám phá, xây dựng mô hình, lựa chọn ngưỡng, đánh giá và tích hợp dự đoán vào Streamlit. Thực nghiệm tập trung so sánh Logistic Regression và Random Forest, giữ khả năng truy vết dữ liệu sau biến đổi về thuộc tính gốc.

Dữ liệu được cung cấp dưới dạng một ảnh chụp trạng thái, không có lịch sử thời điểm ghi nhận từng thuộc tính trước sự kiện churn. Vì vậy, bài toán trong báo cáo là phân loại theo nhãn của bộ dữ liệu hiện có. Đề tài chưa xác nhận khả năng dự báo trước 30, 60 hay 90 ngày, chưa đo lường tác động của một chiến dịch giữ chân khách hàng và chưa tính toán lợi nhuận thực tế từ kết quả dự đoán.

## Phương pháp thực hiện
Quy trình thực hiện bắt đầu bằng việc kiểm tra tệp gốc, ghi nhận nguồn dữ liệu và làm rõ ý nghĩa từng trường. Sau đó, dữ liệu được chia phân tầng thành train, validation và test với tỷ lệ xấp xỉ 60/20/20, sử dụng seed 42. Tập train phục vụ khám phá và kiểm định chéo; validation phục vụ lựa chọn ngưỡng và phân tích độ quan trọng thuộc tính; test chỉ phục vụ đánh giá sau khi lựa chọn mô hình đã được cố định.

Các phương pháp được đánh giá trong cùng điều kiện dữ liệu. Pipeline của mỗi mô hình gồm chuẩn hóa biểu diễn đầu vào, xử lý riêng các cột số và phân loại, sau đó áp dụng bộ phân loại. Tìm kiếm siêu tham số được tiến hành bên trong kiểm định chéo để những thống kê tiền xử lý được học lại trong từng fold. Sau khi chọn mô hình theo AP trung bình, ngưỡng được xác định bằng các xác suất trên validation và lưu cùng mô hình.

Phần triển khai ứng dụng sử dụng lại pipeline đã huấn luyện, không xây dựng một quy trình mã hóa khác ở giao diện. Kiểm thử được thực hiện ở các lớp dữ liệu, tiền xử lý, đánh giá, suy luận và giao diện. Báo cáo sử dụng số liệu từ lần chạy đã lưu cùng các hình phân tích và bằng chứng kiểm thử của dự án.

## Cấu trúc báo cáo
Báo cáo gồm sáu chương: tổng quan đề tài; cơ sở lý thuyết; phân tích và thiết kế hệ thống; xây dựng mô hình và ứng dụng; kết quả thực nghiệm; kết luận và hướng phát triển. Các chương lần lượt làm rõ bài toán, phương pháp, quá trình triển khai và kết quả kiểm chứng. Danh mục tài liệu tham khảo được đặt ở cuối báo cáo.

# CƠ SỞ LÝ THUYẾT
## Bài toán phân loại khách hàng rời dịch vụ
Học có giám sát sử dụng dữ liệu gồm đầu vào và nhãn đã biết để xây dựng hàm dự đoán. Trong đề tài, đầu vào x là tập thuộc tính của một khách hàng và nhãn y nhận giá trị 0 hoặc 1. Mô hình trả về điểm cho lớp churn, ký hiệu p(x). Để tạo ra quyết định phân loại, điểm này được so sánh với một ngưỡng t. Quy tắc phân loại của hệ thống là dự đoán churn khi p(x) lớn hơn hoặc bằng t.

@equation ŷ = 1 nếu p(x) ≥ t; ŷ = 0 nếu p(x) < t

Mô hình dự đoán và ngưỡng quyết định giải quyết hai vấn đề khác nhau. Mô hình học cách xếp hạng các hồ sơ theo điểm; ngưỡng xác định tập hồ sơ được đánh dấu. Ngưỡng mặc định 0,5 có thể không phù hợp với mọi mục tiêu sử dụng. Việc điều chỉnh ngưỡng cần dựa trên dữ liệu riêng và tiêu chí đã xác định, tránh lựa chọn lại ngưỡng trên chính tập kiểm thử cuối [7].

Trong đề tài, điểm dự đoán được dùng để hỗ trợ sàng lọc. Một điểm 0,60 không đồng nghĩa khách hàng chắc chắn có 60% khả năng rời dịch vụ trong một tháng tới. Cách diễn giải xác suất cần xét đến hiệu chỉnh, phân bố dữ liệu và thời hạn dự báo. Mô hình hiện tại chưa thực hiện hiệu chỉnh xác suất; do đó, báo cáo đánh giá điểm theo khả năng phân loại và xếp hạng, không khẳng định đó là xác suất đã được hiệu chỉnh [12].

## Tiền xử lý dữ liệu dạng bảng
### Xử lý giá trị thiếu và chuẩn hóa
Với thuộc tính số, một ô trống cần được phân biệt với giá trị 0. SimpleImputer có thể điền thiếu theo trung vị và bổ sung chỉ báo thiếu [10]; StandardScaler biến đổi thuộc tính theo trung bình và độ lệch chuẩn học từ dữ liệu huấn luyện [11]. Trong đề tài, TotalCharges được chuyển sang dạng số, các ô trống được biểu diễn bằng giá trị thiếu trước khi đưa vào pipeline.

Việc điền thiếu có ý nghĩa khác với sửa dữ liệu gốc. Một giá trị được điền bằng trung vị chỉ là cách cung cấp đầu vào cho thuật toán, không phải bằng chứng khách hàng thực sự có mức tổng cước đó. Dự án vẫn giữ bản dữ liệu ban đầu và ghi nhận ô thiếu để có thể kiểm tra lại. Nhánh số của Logistic Regression được chuẩn hóa; Random Forest sử dụng nhánh số đã điền thiếu mà không cần bước StandardScaler.

### Mã hóa thuộc tính phân loại
One-hot encoding biểu diễn mỗi giá trị phân loại bằng một cột nhị phân. Cách biểu diễn này tránh gán một thứ tự số học không có căn cứ cho các nhóm như hình thức thanh toán hoặc loại dịch vụ. OneHotEncoder học tập giá trị từ dữ liệu fit và có tùy chọn xử lý giá trị chưa gặp khi biến đổi dữ liệu mới [11].

Trong dữ liệu Telco, SeniorCitizen có giá trị 0 hoặc 1 nhưng mang ý nghĩa nhóm, nên được xử lý như thuộc tính phân loại. Các giá trị No internet service và No phone service mô tả tình trạng dịch vụ, không phải ô thiếu. Việc giữ đúng ý nghĩa này giúp tránh gộp những trường hợp không đăng ký dịch vụ với các trường hợp chưa biết thông tin.

### Pipeline và phòng tránh rò rỉ dữ liệu
Pipeline ghép các bước biến đổi và mô hình thành một đối tượng thống nhất. ColumnTransformer cho phép áp dụng các bước khác nhau cho từng nhóm cột. Khi pipeline được đưa vào kiểm định chéo, các bộ biến đổi được fit trên phần huấn luyện của từng fold; phần đánh giá chỉ đi qua transform và predict. Cách tổ chức này giảm nguy cơ rò rỉ do học trung vị, thang đo hoặc tập giá trị phân loại từ dữ liệu đánh giá [2].

Đối với đề tài, việc tách nhãn và mã định danh được thực hiện rõ ràng trước khi xây dựng X. Ngoài rò rỉ do thao tác tính toán, còn có rủi ro thời gian: một thuộc tính có thể chỉ được biết sau sự kiện cần dự đoán. Pipeline giải quyết sự phân tách dữ liệu trong tính toán nhưng không tự xác nhận thời điểm thu thập từng trường. Hai vấn đề này được xem xét riêng trong thiết kế và đánh giá.

## Các mô hình phân loại
### Mô hình đối chứng DummyClassifier
Mô hình đối chứng tạo ra một mức tham chiếu đơn giản để xác định liệu các thuật toán có khai thác được thông tin hữu ích hay không. DummyClassifier với chiến lược most_frequent luôn chọn lớp xuất hiện nhiều nhất trong tập huấn luyện [13]. Trong đề tài, lớp này là No. Vì vậy, baseline có thể có accuracy cao do phân bố nhãn nhưng không phát hiện được khách hàng churn.

Baseline không được tính là một trong hai thuật toán học máy cần so sánh. Vai trò của nó là làm rõ hạn chế của accuracy và tạo điểm xuất phát cho các độ đo đánh giá. Cả Logistic Regression và Random Forest đều phải được đối chiếu với mức tham chiếu này trên cùng tập dữ liệu.

### Logistic Regression
Logistic Regression mô hình hóa log-odds của lớp dương bằng một tổ hợp tuyến tính các thuộc tính. Hàm sigmoid chuyển giá trị tuyến tính thành điểm trong khoảng từ 0 đến 1. Regularization hạn chế độ lớn hệ số; tham số C biểu diễn mức nghịch đảo của cường độ regularization trong triển khai scikit-learn [3].

@equation z = β₀ + β₁x₁ + … + βₘxₘ; p(x) = 1 / (1 + exp(−z))

Trong đề tài, Logistic Regression được chọn vì phù hợp làm mô hình so sánh cho dữ liệu dạng bảng đã mã hóa. Các cột số được chuẩn hóa trước khi fit; cấu hình sử dụng regularization L2 và bộ giải lbfgs. Tham số C được khảo sát trên bốn giá trị để kiểm tra mức độ ràng buộc hệ số phù hợp. Giới hạn của phương pháp trong thiết kế hiện tại là quan hệ giữa các thuộc tính và log-odds vẫn có dạng tuyến tính, trong khi tương tác giữa hợp đồng, thời gian sử dụng và dịch vụ có thể phức tạp hơn.

### Random Forest
Random Forest kết hợp nhiều cây quyết định được học từ các mẫu dữ liệu và tập thuộc tính có yếu tố ngẫu nhiên. Kết quả được tổng hợp từ các cây nhằm giảm sự phụ thuộc vào một cây đơn lẻ. Trong scikit-learn, điểm phân loại của rừng được tính bằng trung bình xác suất lớp từ các cây thành phần. Các tham số như max_depth, min_samples_leaf và class_weight điều khiển độ phức tạp và cách xử lý mất cân bằng [4].

Đề tài sử dụng 300 cây và khảo sát số mẫu tối thiểu tại lá. Việc tăng min_samples_leaf làm cho một lá phải đại diện cho nhiều hồ sơ hơn, qua đó hạn chế những quyết định dựa trên một nhóm quá nhỏ. Random Forest được kỳ vọng biểu diễn được các mối quan hệ phi tuyến mà Logistic Regression chưa mô tả đầy đủ; kỳ vọng này được kiểm tra bằng kết quả thực nghiệm thay vì mặc định coi mô hình phức tạp hơn là tốt hơn.

## Kiểm định chéo và lựa chọn siêu tham số
Kiểm định chéo chia tập huấn luyện thành nhiều phần và luân phiên sử dụng một phần để đánh giá. StratifiedKFold duy trì tỷ lệ các lớp gần với tỷ lệ chung trong từng fold, phù hợp với dữ liệu có mất cân bằng. Giá trị trung bình qua các fold cho biết chất lượng trong quy trình đánh giá đã chọn; độ lệch chuẩn mô tả sự thay đổi giữa các fold [5].

Trong đồ án, năm fold được sử dụng với shuffle và seed 42. Mỗi cấu hình được đánh giá bằng AP; mô hình có AP trung bình cao hơn được ưu tiên. Nếu bằng nhau, độ lệch chuẩn thấp hơn được xét tiếp, sau đó ưu tiên Logistic Regression khi vẫn trùng hoàn toàn. Quy tắc được xác định trước khi đánh giá test để tránh thay đổi tiêu chí theo kết quả mong muốn.

## Các độ đo đánh giá
### Ma trận nhầm lẫn
Ma trận nhầm lẫn phân chia kết quả thành bốn trường hợp. TP là khách hàng thực sự churn và được dự đoán churn; TN là khách hàng không churn và được dự đoán không churn; FP là khách hàng không churn nhưng bị đánh dấu; FN là khách hàng churn nhưng bị bỏ sót. Với quy ước lớp dương là Churn=Yes, bốn đại lượng này là cơ sở để tính precision, recall và F1.

@table metric_meaning|Ý nghĩa các kết quả phân loại trong bài toán churn

### Accuracy, precision, recall và F1
Accuracy phản ánh tỷ lệ dự đoán đúng trên toàn bộ mẫu. Precision cho biết tỷ lệ khách hàng thực sự churn trong danh sách được đánh dấu. Recall cho biết tỷ lệ khách hàng churn được phát hiện. F1 là trung bình điều hòa của precision và recall. Các độ đo này phụ thuộc ngưỡng phân loại; chúng cần được đọc cùng ma trận nhầm lẫn và phân bố lớp [6].

@equation Accuracy = (TP + TN) / N; Precision = TP / (TP + FP)
@equation R = TP / (TP + FN); F1 = 2PR / (P + R)

Trong các công thức trên, N là tổng số hồ sơ, P là precision và R là recall.

Trong ứng dụng chăm sóc khách hàng, FN là hồ sơ churn bị bỏ sót, còn FP làm tăng số hồ sơ cần xem xét. Đề tài ưu tiên recall và đặt ràng buộc precision để kiểm soát quy mô danh sách cảnh báo.

### ROC-AUC và Average Precision
ROC-AUC đo khả năng phân biệt hai lớp trên các ngưỡng, trong khi đường precision–recall tập trung vào lớp dương. Average Precision tổng hợp precision theo mức tăng recall và được dùng làm tiêu chí chính để lựa chọn mô hình trong đề tài [6]. AP không phải phép lấy diện tích hình thang trực tiếp dưới mọi đường PR; báo cáo sử dụng kết quả average_precision_score nhất quán giữa huấn luyện và đánh giá.

ROC-AUC và AP không đổi khi chỉ thay ngưỡng mà giữ nguyên điểm dự đoán, trong khi precision, recall và số hồ sơ được đánh dấu có thể thay đổi. Vì vậy, Chương 5 phân biệt chất lượng xếp hạng với chất lượng tại một ngưỡng cụ thể.

## Độ quan trọng thuộc tính
Permutation importance đánh giá mức giảm chất lượng khi tráo ngẫu nhiên một thuộc tính trong dữ liệu đánh giá. Nếu mô hình phụ thuộc vào thông tin của thuộc tính đó, việc tráo giá trị thường làm điểm đánh giá giảm. Phép tính có thể lặp lại nhiều lần để mô tả mức dao động. Các thuộc tính tương quan có thể chia sẻ thông tin, nên kết quả cần được diễn giải cùng cấu trúc dữ liệu [8].

Đề tài tính mức giảm AP trên validation với 20 lần tráo cho mỗi thuộc tính gốc. Kết quả cho biết mô hình đang sử dụng thông tin nào để dự đoán trên tập dữ liệu này. Đây là phân tích tổng thể của mô hình, không phải lời giải thích riêng cho từng khách hàng và không chứng minh một thuộc tính gây ra churn.

## Công nghệ xây dựng ứng dụng
Streamlit cung cấp biểu mẫu, bảng, biểu đồ và thành phần tải tệp cho ứng dụng Python. st.cache_resource lưu đối tượng mô hình để dùng lại, còn st.cache_data lưu kết quả dữ liệu [9].

Hệ thống dùng Streamlit cho giao diện, pandas để xử lý bảng, scikit-learn cho pipeline và joblib để lưu mô hình. Notebook, kiểm thử và giao diện dùng chung pipeline; khi nhập hồ sơ mới, ứng dụng kiểm tra đầu vào rồi gọi suy luận.

# PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
## Phân tích yêu cầu hệ thống
### Yêu cầu chức năng
Hệ thống được thiết kế theo quy trình từ xem tổng quan đến phân tích hồ sơ và kiểm tra hiệu quả dự đoán. Màn hình tổng quan giúp người sử dụng nhận biết quy mô dữ liệu, tỷ lệ churn và các nhóm khách hàng đáng chú ý. Từ danh sách khách hàng, người sử dụng có thể chọn một hồ sơ để chuyển sang biểu mẫu phân tích, nhờ đó giảm thao tác nhập lại và giữ được tính nhất quán giữa dữ liệu tham khảo với dữ liệu đưa vào mô hình.

Chức năng phân tích cá nhân tiếp nhận 19 thuộc tính, kiểm tra miền giá trị và trả về điểm churn cùng trạng thái theo ngưỡng chính thức. Chức năng xử lý danh sách thực hiện cùng quy trình đối với một tệp CSV. Những dòng sai được giữ lại với nội dung lỗi để người sử dụng sửa dữ liệu; chúng không được gán xác suất hoặc âm thầm loại khỏi kết quả. Hai màn hình còn lại phục vụ theo dõi chất lượng mô hình và khảo sát tác động của ngưỡng.

@table functional|Các yêu cầu chức năng của hệ thống

### Yêu cầu phi chức năng
Đối với tính đúng đắn, ứng dụng phải sử dụng cùng thứ tự cột, quy tắc chuẩn hóa và pipeline như lúc huấn luyện. Điểm dự đoán trên giao diện cần khớp với điểm khi nạp trực tiếp mô hình đã lưu. Đối với tính dễ sử dụng, các trường dữ liệu được chia thành nhóm thông tin khách hàng, dịch vụ và thanh toán; thông báo lỗi gắn với dữ liệu cần sửa. Màu sắc và cách trình bày được giữ nhất quán giữa các trang.

Đối với khả năng tái lập, dự án lưu phiên bản thư viện, seed, cấu hình mô hình, danh sách ID của các tập và kết quả thực nghiệm. Người kiểm tra có thể đối chiếu tệp dữ liệu, nạp mô hình và chạy lại các phép đánh giá. Trong phạm vi demo, hệ thống xử lý tệp tối đa 10 MiB và 10.000 dòng, chạy trên máy cá nhân và không có chức năng đăng nhập, phân quyền hoặc đồng bộ dữ liệu với CRM.

## Nguồn dữ liệu và cấu trúc thuộc tính
### Nguồn và quy mô
Bộ dữ liệu được lấy từ tệp Telco-Customer-Churn.csv trong kho IBM telco-customer-churn-on-icp4d [1]. Bản dữ liệu sử dụng trong dự án gồm 7.043 dòng và 21 cột. Có 1.869 hồ sơ thuộc lớp Yes và 5.174 hồ sơ thuộc lớp No. Mỗi customerID xuất hiện một lần; kiểm tra không phát hiện dòng trùng hoàn toàn hoặc mã khách hàng trùng lặp.

Dự án lưu bản CSV gốc và mã băm SHA-256 để nhận biết đúng phiên bản dữ liệu. Từ điển thuộc tính được sử dụng xuyên suốt quá trình tiền xử lý và xây dựng giao diện. Việc có mã định danh phục vụ đối chiếu và chọn hồ sơ, nhưng mã này không mang ý nghĩa đo lường khách hàng nên được loại khỏi tập thuộc tính học máy.

@table dataset|Tổng quan bộ dữ liệu sử dụng
@table dictionary|Từ điển dữ liệu Telco Customer Churn

### Kiểu dữ liệu và giá trị thiếu
Ba thuộc tính số của mô hình là tenure, MonthlyCharges và TotalCharges. Trong tệp gốc, TotalCharges chứa 11 ô là chuỗi trắng, khiến kiểu đọc ban đầu không hoàn toàn phản ánh ý nghĩa số của trường. Sau khi loại khoảng trắng và chuyển kiểu, các ô này được nhận diện là thiếu, tương đương khoảng 0,1562% toàn bộ dữ liệu. Hai mươi cột còn lại không có ô thiếu theo phép kiểm tra ô rỗng và chuỗi trắng.

Cả 11 hồ sơ thiếu TotalCharges đều có tenure bằng 0. Kết quả này phù hợp với tình huống khách hàng mới bắt đầu sử dụng, nhưng dữ liệu không cung cấp đủ bằng chứng để tự động khẳng định tổng cước thật của họ bằng 0. Vì vậy, đề tài giữ các hồ sơ, chuyển ô trống thành giá trị thiếu và để bộ điền thiếu học trung vị từ phần dữ liệu huấn luyện phù hợp. Tập train có 7 ô TotalCharges thiếu; số còn lại thuộc các tập giữ riêng.

@table quality|Kết quả kiểm tra chất lượng và cách xử lý dữ liệu

## Thiết kế quy trình chuẩn bị dữ liệu
### Làm sạch và kiểm tra ngoại lai
Các phép biến đổi không học thống kê gồm chuẩn hóa biểu diễn chuỗi, chuyển kiểu số và thống nhất dạng giá trị phân loại. Những phép tính có sử dụng phân bố như trung vị, trung bình, độ lệch chuẩn và tập giá trị one-hot chỉ được học trong pipeline. Việc tách hai nhóm thao tác này giúp quá trình làm sạch không trở thành một bước học ngầm từ toàn bộ dữ liệu trước khi chia tập.

Đề tài kiểm tra ngoại lai trên train bằng rào 1,5 lần khoảng tứ phân vị. Khi xét từng biến trên toàn bộ train, tenure, MonthlyCharges và TotalCharges không có giá trị vượt rào chung. Khi quan sát riêng nhóm Churn=Yes để giải thích biểu đồ, tenure có 13 điểm và TotalCharges có 67 điểm vượt rào của nhóm. Hai số này có thể trùng khách hàng và không được cộng thành số hồ sơ riêng biệt.

Các giá trị vẫn nằm trong miền dữ liệu hợp lệ và chưa có bằng chứng là lỗi nhập liệu, nên đề tài không cắt bỏ. Đặc biệt, rào tính riêng theo nhãn chỉ phục vụ mô tả; không dùng nhãn churn để quyết định xóa một khách hàng trước khi huấn luyện. Cách xử lý này giữ được những trường hợp hiếm nhưng có thể hợp lệ, đồng thời tránh làm dữ liệu trở nên thuận lợi một cách nhân tạo cho mô hình.

### Chia tập dữ liệu
Dữ liệu được chia phân tầng theo Churn với seed 42. Tập train có 4.225 hồ sơ, validation có 1.409 hồ sơ và test có 1.409 hồ sơ. Số lượng khác nhau một vài hồ sơ so với tỷ lệ toán học là do cần dùng số nguyên khi chia dữ liệu. Danh sách customerID của từng tập được lưu để xác nhận các tập không giao nhau và có thể ghép lại đầy đủ dữ liệu gốc.

@table splits|Phân bố dữ liệu sau khi chia tập

Train được dùng để xây dựng nhận định khám phá, kiểm định chéo và fit mô hình. Validation được dùng để chọn ngưỡng vận hành và tính permutation importance sau khi đã lựa chọn cấu hình theo CV. Test được giữ riêng cho lần đánh giá cuối. Quy trình này không gộp train với validation để fit lại trước khi sử dụng ngưỡng, vì việc fit lại sẽ làm thay đổi phân bố điểm so với mô hình đã dùng để lựa chọn ngưỡng đó.

### Phòng tránh sử dụng thông tin không phù hợp
customerID và Churn không đi vào X. Trong 19 đầu vào không có các cột như nguyên nhân churn, churn score hoặc trạng thái được tạo từ kết quả dự đoán. Dữ liệu validation và test không tham gia học imputer, scaler hay encoder. Các bước kiểm tra ID và thống kê fit được dùng để xác nhận sự phân tách trong quy trình tính toán.

Tuy nhiên, dữ liệu snapshot không chứa thời điểm đo riêng cho tenure, TotalCharges và trạng thái dịch vụ. Nếu xây dựng hệ thống dự báo sớm cho doanh nghiệp, cần xác nhận các giá trị này đã tồn tại tại thời điểm ra quyết định. Giới hạn thời gian này không thể được loại bỏ chỉ bằng chia tập ngẫu nhiên hoặc bằng cách đặt các bước xử lý vào pipeline.

## Phân tích khám phá dữ liệu
### Phân bố nhãn churn
Phân tích khám phá sử dụng 4.225 hồ sơ của tập train. Trong đó, 1.121 hồ sơ có nhãn churn và 3.104 hồ sơ không churn, tương ứng 26,53% và 73,47%. Sự chênh lệch cho thấy lớp dương ít hơn rõ rệt nhưng vẫn có đủ quan sát để tiến hành so sánh các nhóm và kiểm định chéo phân tầng.

@figure artifacts/eda/01_class_balance.png|Phân bố nhãn Churn trên tập train

Nếu chỉ nhìn tỷ lệ dự đoán đúng chung, một mô hình chọn lớp No cho mọi hồ sơ sẽ tạo ra kết quả dễ gây hiểu nhầm. Vì vậy, các phân tích tiếp theo chú ý đến tỷ lệ churn trong từng nhóm và các độ đo dành cho lớp dương. Khi tính tỷ lệ theo nhóm, mẫu số là số khách hàng của chính nhóm đó, không phải tổng số khách hàng churn trong train.

### Churn theo loại hợp đồng
Nhóm hợp đồng theo tháng có 2.326 khách hàng với tỷ lệ churn khoảng 43,08%. Nhóm hợp đồng một năm có 865 khách hàng, tỷ lệ khoảng 10,80%; nhóm hai năm có 1.034 khách hàng, tỷ lệ khoảng 2,51%. Chênh lệch này làm cho Contract trở thành một thuộc tính đáng chú ý trong bước mô hình hóa.

@figure artifacts/eda/02_Contract.png|Tỷ lệ churn theo loại hợp đồng trên train

Kết quả mô tả cho thấy churn xuất hiện nhiều hơn ở nhóm hợp đồng ngắn trong dữ liệu. Tuy nhiên, không thể từ đó khẳng định chuyển mọi khách hàng sang hợp đồng dài sẽ làm churn giảm đúng bằng chênh lệch quan sát. Loại hợp đồng có thể liên hệ với thời gian sử dụng, cách lựa chọn dịch vụ và đặc điểm của khách hàng. Đề tài sử dụng thuộc tính này để dự đoán và tiếp tục kiểm tra mức phụ thuộc của mô hình ở bước đánh giá.

### Churn theo dịch vụ Internet
Nhóm Fiber optic gồm 1.843 khách hàng và có tỷ lệ churn khoảng 42,32%, cao hơn nhóm DSL gồm 1.474 khách hàng với tỷ lệ khoảng 18,70%. Nhóm không sử dụng Internet gồm 908 khách hàng, có tỷ lệ churn khoảng 7,27%. Sự khác biệt cho thấy loại dịch vụ Internet chứa thông tin phân biệt đáng kể trên train.

@figure artifacts/eda/03_InternetService.png|Tỷ lệ churn theo dịch vụ Internet trên train

Dữ liệu không có chỉ tiêu đo chất lượng đường truyền, sự cố hoặc mức hài lòng. Do đó, tỷ lệ cao ở nhóm Fiber optic không đủ để kết luận công nghệ cáp quang gây churn. Trong mô hình, thuộc tính này được xem cùng hợp đồng, cước và thời gian sử dụng. Việc kiểm tra hiệu quả theo từng loại Internet ở Chương 5 giúp đánh giá mô hình có hoạt động đồng đều giữa các nhóm hay không.

### Churn theo phương thức thanh toán
Nhóm thanh toán bằng Electronic check có 1.410 hồ sơ và tỷ lệ churn khoảng 45,60%. Các nhóm Mailed check, Bank transfer (automatic) và Credit card (automatic) lần lượt có tỷ lệ khoảng 19,50%, 16,20% và 15,07%. Trong đó, nhóm thanh toán séc điện tử vừa có quy mô lớn vừa có tỷ lệ churn cao hơn các nhóm còn lại.

@figure artifacts/eda/04_PaymentMethod.png|Tỷ lệ churn theo phương thức thanh toán trên train

PaymentMethod phản ánh cách khách hàng tương tác với hoạt động thanh toán và có thể liên hệ với các thuộc tính khác. Kết quả này cung cấp một hướng kiểm tra cho mô hình, nhưng chưa chứng minh thay đổi phương thức thanh toán sẽ trực tiếp giữ chân được khách hàng. Khi đề xuất ứng dụng, nhóm chỉ sử dụng quan hệ quan sát được để sàng lọc và không chuyển thành một quy tắc can thiệp mang tính nhân quả.

### Thời gian sử dụng và churn
Trung vị tenure của nhóm churn là 10 tháng, trong khi nhóm không churn là 37 tháng. Biểu đồ cho thấy khách hàng churn tập trung nhiều hơn ở thời gian sử dụng ngắn, còn nhóm không churn trải rộng đến các mức thời gian dài. Đây là một dấu hiệu quan trọng để kiểm tra cùng loại hợp đồng.

@figure artifacts/eda/05_tenure.png|Phân bố thời gian sử dụng theo Churn trên train

Dù vậy, hai phân bố vẫn chồng lấp và vẫn có khách hàng sử dụng lâu thuộc lớp churn. Vì vậy, một quy tắc chỉ đánh dấu khách hàng mới sẽ bỏ sót các trường hợp không điển hình. Hệ thống sử dụng tenure như một thuộc tính trong mô hình đa biến; kết quả phân loại không được suy ra chỉ từ trung vị của hai nhóm.

### Cước hàng tháng và tổng cước
Trung vị MonthlyCharges của nhóm churn là 79,75, cao hơn mức 64,38 của nhóm không churn. Các giá trị được giữ theo đơn vị trong dữ liệu gốc, không quy đổi hoặc ghi thành đồng Việt Nam. Phân bố chồng lấp cho thấy cước hàng tháng cung cấp thông tin hữu ích nhưng không tạo được một ranh giới tuyệt đối giữa hai lớp.

@figure artifacts/eda/06_MonthlyCharges.png|Phân bố cước hàng tháng theo Churn trên train

Với TotalCharges, trung vị của nhóm churn là 679,30 và của nhóm không churn là 1.677,85. Kết quả tổng cước thấp hơn ở nhóm churn cần được đọc cùng tenure ngắn hơn; không thể kết luận một cách độc lập rằng khách hàng có tổng cước thấp sẽ rời dịch vụ. Khi tính các thống kê mô tả, các ô thiếu không được coi là số 0.

@figure artifacts/eda/07_TotalCharges.png|Phân bố tổng cước theo Churn trên train

Hai biểu đồ cước giúp làm rõ sự khác biệt giữa chi phí hàng tháng và phần tích lũy trong thời gian sử dụng. MonthlyCharges có thể cao trong khi TotalCharges vẫn thấp nếu khách hàng mới sử dụng dịch vụ. Đây là một lý do để giữ cả ba thuộc tính số trong quá trình so sánh mô hình và kiểm tra khả năng biểu diễn tương tác của Random Forest.

### Tương quan giữa các thuộc tính số
Trên train, tương quan giữa tenure và TotalCharges xấp xỉ 0,834; giữa MonthlyCharges và TotalCharges xấp xỉ 0,65; giữa tenure và MonthlyCharges xấp xỉ 0,26. Khi mã hóa Churn thành 0/1, hệ số với tenure khoảng −0,35, với MonthlyCharges khoảng 0,20 và với TotalCharges khoảng −0,20.

@figure artifacts/eda/08_correlation.png|Ma trận tương quan các biến số trên train

Hệ số lớn giữa tenure và TotalCharges phù hợp với tính tích lũy của tổng cước. Quan hệ này cũng ảnh hưởng đến cách đọc permutation importance: hai thuộc tính có thể chia sẻ thông tin, nên mức giảm điểm khi tráo một cột không phản ánh toàn bộ vai trò của nhóm thuộc tính liên quan. Tương quan tuyến tính không bao quát mọi dạng quan hệ và không được dùng làm bằng chứng nhân quả.

## Thiết kế kiến trúc hệ thống
Hệ thống được chia thành ba phần trách nhiệm. Phần chuẩn bị và huấn luyện đọc dữ liệu, tạo các tập, chạy CV, lựa chọn mô hình và sinh artifact. Phần suy luận nạp pipeline cùng metadata, kiểm tra đầu vào và tính điểm churn. Phần giao diện gọi lớp suy luận và hiển thị các kết quả đã được tính sẵn. Dữ liệu đánh giá không được dùng như một nguồn huấn luyện ngầm khi người sử dụng mở màn hình.

@table architecture|Các thành phần trong kiến trúc hệ thống

Pipeline đã lưu và metadata là cầu nối giữa phần thực nghiệm với phần ứng dụng. Metadata xác định mô hình được chọn, ngưỡng chính thức và thông tin lần chạy. Khi ứng dụng khởi động, bộ nạp kiểm tra bundle trước khi cung cấp đối tượng suy luận. Cách tổ chức này hạn chế tình huống giao diện sử dụng nhầm một mô hình với ngưỡng của lần chạy khác.

## Thiết kế luồng xử lý và giao diện
### Luồng phân tích một khách hàng
Người sử dụng nhập hoặc chọn hồ sơ, sau đó kiểm tra các nhóm thông tin. Các giá trị dịch vụ phụ thuộc được ràng buộc theo PhoneService và InternetService để tránh tổ hợp mâu thuẫn. Khi người sử dụng yêu cầu phân tích, ứng dụng kiểm tra dữ liệu, chọn đúng 19 thuộc tính, gọi predict_proba của pipeline và lấy cột tương ứng lớp 1. Kết quả được so với ngưỡng chính thức để tạo trạng thái hiển thị.

### Luồng xử lý danh sách
Ứng dụng đọc tệp CSV, kiểm tra dung lượng, số dòng, các cột bắt buộc và từng hồ sơ. Các dòng hợp lệ được dự đoán theo lô; dòng lỗi được giữ lại cùng lý do. Danh sách kết quả có thể tải xuống để tiếp tục kiểm tra. Churn không phải cột đầu vào bắt buộc khi dùng chức năng này, vì nhãn thực tế thường chưa có trong dữ liệu cần dự đoán.

### Luồng xem hiệu quả và khảo sát ngưỡng
Màn hình hiệu quả mô hình đọc kết quả test đã lưu, gồm các độ đo, ma trận nhầm lẫn, đường ROC/PR, trường hợp sai và thống kê nhóm. Màn hình ngưỡng chỉ sử dụng validation để cho thấy tác động của việc thay đổi mức đánh dấu. Thao tác kéo thanh trượt không ghi đè ngưỡng chính thức và không thay đổi mô hình đang phục vụ dự đoán.

Giao diện được tổ chức theo các tác vụ thực tế, sử dụng nền sáng, màu nhấn xanh đậm, bảng và biểu đồ có nhãn rõ ràng. Thông tin kỹ thuật như tên thuật toán hoặc tập đánh giá được đặt ở màn hình phục vụ đánh giá; biểu mẫu khách hàng tập trung vào dữ liệu cần nhập và kết quả sử dụng. Cách bố trí giúp người dùng thực hiện tác vụ chính trước, sau đó mở phần phân tích khi cần tìm hiểu sâu hơn.

# XÂY DỰNG HỆ THỐNG
## Môi trường phát triển và tổ chức mã nguồn
### Môi trường thực nghiệm
Dự án được thực hiện trên Windows với Python 3.14.3 và một môi trường ảo riêng. Các phiên bản thư viện được khóa trong requirements.txt nhằm giảm khác biệt khi cài đặt lại. Toàn bộ quy trình mô hình sử dụng CPU; ứng dụng không yêu cầu GPU hoặc khóa truy cập một dịch vụ dự đoán bên ngoài.

@table environment|Các thành phần chính của môi trường thực nghiệm

Trong lần kiểm chứng môi trường sạch, dự án được cài phụ thuộc, chạy bộ kiểm thử và tái thực hiện quy trình mô hình. Kết quả này chứng minh khả năng tái lập trong môi trường đã kiểm tra, không có nghĩa hệ thống đã được xác nhận trên mọi hệ điều hành hoặc mọi phiên bản Python. Khi chuyển máy, việc giữ đúng phiên bản scikit-learn đặc biệt cần thiết vì pipeline được lưu dưới dạng đối tượng thư viện.

### Tổ chức mã nguồn
Mã nguồn được chia theo trách nhiệm để quy trình huấn luyện và giao diện có thể dùng chung các thành phần cốt lõi. Các thư mục dữ liệu, artifact và bằng chứng đánh giá được lưu riêng, giúp phân biệt dữ liệu gốc với kết quả đã biến đổi. Notebook trình bày quá trình khảo sát và kết quả, còn các module chịu trách nhiệm thực thi quy trình đầy đủ.

@table modules|Tổ chức các thành phần mã nguồn và dữ liệu

## Xây dựng pipeline tiền xử lý
Lớp FeatureNormalizer kiểm tra các cột bắt buộc và chuẩn hóa biểu diễn đầu vào. Hàm transform gọi cùng quy tắc normalize_features được sử dụng trong các phép kiểm tra dữ liệu. Bước này không học trung vị hoặc phân bố từ dữ liệu. Việc khai báo 19 thuộc tính đầu vào giúp kiểm soát trường hợp CSV bổ sung cột không liên quan và tránh đưa nhầm nhãn vào mô hình.

ColumnTransformer chia các cột thành hai nhánh. Nhánh số sử dụng SimpleImputer với strategy=median và add_indicator=True. Nhánh phân loại điền thiếu theo giá trị xuất hiện nhiều nhất trước khi one-hot encoding. Logistic Regression có thêm StandardScaler sau bước điền thiếu của nhánh số. Cả hai nhánh được ghép lại và chuyển sang bộ phân loại.

@table preprocessing|Cấu hình các bước tiền xử lý

OneHotEncoder được đặt handle_unknown=ignore để bộ biến đổi không hỏng khi gặp giá trị ngoài các nhóm đã học. Tuy nhiên, đây không phải lý do để chấp nhận mọi dữ liệu nhập tại giao diện. Lớp kiểm tra đầu vào của ứng dụng vẫn từ chối các giá trị phân loại ngoài từ điển dữ liệu. Hai cơ chế có vai trò khác nhau: encoder bảo đảm tính ổn định của pipeline, còn validation bảo đảm hồ sơ người dùng phù hợp hợp đồng đầu vào của demo.

Việc điền thiếu cho biến phân loại được giữ trong pipeline như một bước phòng vệ, dù dữ liệu huấn luyện hiện tại không có ô phân loại thiếu. Với dữ liệu người dùng, các trường bắt buộc vẫn phải có giá trị hợp lệ. Riêng TotalCharges được cho phép thiếu giá trị, nhưng tên cột vẫn bắt buộc xuất hiện trong CSV để hệ thống nhận biết đúng cấu trúc.

## Huấn luyện và lựa chọn mô hình
### Thiết lập tìm kiếm siêu tham số
Logistic Regression được khảo sát với C thuộc tập {0,01; 0,1; 1; 10} và class_weight thuộc {None; balanced}, tạo thành 8 cấu hình. Random Forest giữ 300 cây, max_features=sqrt và khảo sát ba mức max_depth, ba mức min_samples_leaf cùng hai lựa chọn class_weight, tạo thành 18 cấu hình. Mỗi cấu hình được đánh giá trên năm fold phân tầng của train.

@table grids|Không gian tìm kiếm siêu tham số

Hai mô hình học máy tạo ra tổng cộng 130 lượt fit trong CV, chưa tính baseline và các lượt fit lại cấu hình tốt nhất. Pipeline được truyền trực tiếp vào quá trình tìm kiếm, vì vậy ở mỗi fold, các bộ điền thiếu và mã hóa chỉ học từ phần huấn luyện của fold đó. Kết quả của mọi cấu hình được lưu để có thể đối chiếu quá trình chọn lựa.

### Cấu hình được chọn
Logistic Regression đạt AP trung bình tốt nhất trong lưới của nó khi C=10 và class_weight=None. Random Forest đạt kết quả tốt nhất khi max_depth=None, min_samples_leaf=20 và class_weight=balanced. AP trung bình của Random Forest cao hơn Logistic Regression trong CV nên được chọn theo quy tắc đã xác định. Độ lệch chuẩn và mức chênh lệch cụ thể được trình bày ở Chương 5.

max_depth=None không có nghĩa cây tăng trưởng không chịu bất kỳ hạn chế nào. Trong cấu hình được chọn, min_samples_leaf=20 vẫn yêu cầu mỗi lá có số mẫu tối thiểu, ảnh hưởng trực tiếp đến độ chi tiết của các nhánh. class_weight=balanced điều chỉnh trọng số lớp khi học; đây không phải phép sinh thêm khách hàng hoặc thay đổi số lượng dòng trong dữ liệu.

### Lựa chọn ngưỡng trên validation
Sau khi fit cấu hình tốt nhất trên toàn bộ train, hệ thống tính xác suất churn cho validation và khảo sát các ngưỡng ứng viên. Các ngưỡng có precision thấp hơn 0,50 bị loại khỏi tập lựa chọn. Trong các ngưỡng còn lại, hệ thống ưu tiên recall cao nhất, sau đó xét precision và ngưỡng cao hơn khi cần phá hòa. Không sử dụng nhãn test trong bước này.

Ngưỡng của Random Forest được chọn là 0,4788031716353531. Tại ngưỡng đó, validation có TP=301, FP=300, FN=73 và TN=735; precision đạt 0,5008, recall đạt 0,8048. Ngưỡng so sánh của Logistic Regression là 0,24399930610278062, với precision 0,5000 và recall 0,8048 trên validation. Các giá trị này được lưu cùng bản ghi lựa chọn.

@table val_thresholds|Kết quả lựa chọn ngưỡng trên validation

### Lưu mô hình và cố định lựa chọn
Lần chạy được sử dụng trong báo cáo có mã telco_20261110T093056_0700. Bản ghi lựa chọn được cố định lúc 09:31:41 ngày 10/11/2026, trước bước đánh giá test. Pipeline của Random Forest được lưu bằng joblib, đi kèm metadata, cấu hình tốt nhất, ngưỡng và manifest kiểm tra tính toàn vẹn. Quy trình không fit lại trên train cộng validation sau khi chọn ngưỡng.

Ứng dụng nạp mô hình từ bundle của dự án và xác nhận các tệp cần thiết trước khi dự đoán. Các thuộc tính kết quả như tên mô hình và ngưỡng được lấy từ metadata, giúp màn hình đánh giá và màn hình dự đoán sử dụng cùng cấu hình. Người dùng CSV chỉ cung cấp dữ liệu khách hàng, không tải lên một mô hình khác để thực thi.

## Xây dựng ứng dụng Streamlit
### Màn hình tổng quan
Màn hình tổng quan hiển thị tổng số hồ sơ, số khách hàng đã rời bỏ, số hồ sơ train và cước trung vị trên train. Biểu đồ theo hợp đồng và nhóm thâm niên hỗ trợ quan sát nhanh các nhóm dữ liệu. Bảng khách hàng phía dưới cho phép tìm mã, lọc hợp đồng, lọc nhãn thực tế và xuất danh sách đã lọc.

@figure reports/evidence/report_overview.png|Màn hình tổng quan khách hàng

Các số tổng 7.043 và 1.869 mô tả toàn bộ dữ liệu gốc, trong khi biểu đồ khám phá và danh sách hồ sơ tham khảo sử dụng train. Sự phân biệt này cần được giữ khi đọc giao diện để không nhầm một tỷ lệ của train với tỷ lệ toàn bộ dữ liệu. Bảng hiển thị trước tối đa 50 hồ sơ; chức năng xuất danh sách sử dụng toàn bộ kết quả thỏa bộ lọc.

### Màn hình phân tích khách hàng
Biểu mẫu được chia thành ba thẻ Hồ sơ, Dịch vụ và Thanh toán. Các trường số được kiểm tra miền giá trị; các lựa chọn dịch vụ có quan hệ phụ thuộc được phối hợp để tránh hồ sơ không nhất quán. Người dùng có thể để TotalCharges chưa có giá trị và để pipeline xử lý theo cách đã được huấn luyện.

@figure reports/evidence/report_single.png|Màn hình phân tích một khách hàng

Kết quả chỉ được cập nhật khi bấm Dự đoán khách hàng. Màn hình trình bày mã hồ sơ của lần phân tích gần nhất, điểm churn, ngưỡng chính thức và trạng thái cần xem xét. Ví dụ hồ sơ DEMO-001 trong hình nhận điểm hiển thị 60,0%, cao hơn ngưỡng 0,4788 nên được đánh dấu. Đây là kết quả của một hồ sơ minh họa, không được dùng để tính chất lượng mô hình.

### Màn hình nhập danh sách
Chức năng nhập danh sách tiếp nhận CSV sử dụng dấu phẩy, mã hóa UTF-8 hoặc UTF-8 có BOM. Tệp phải có đủ 19 cột thuộc tính; customerID có thể có hoặc không. Ứng dụng kiểm tra cột thiếu, cột kết quả trùng tên, kiểu số, miền giá trị, danh mục và quan hệ dịch vụ trước khi chạy dự đoán. Cột bổ sung được giữ trong dữ liệu kết quả nhưng không được đưa vào mô hình.

@figure reports/evidence/audit_csv.jpg|Màn hình xử lý danh sách khách hàng từ CSV

Trong tệp mixed_valid_invalid.csv dùng kiểm thử, một dòng hợp lệ được dự đoán và hai dòng lỗi được giữ lại với trạng thái không hợp lệ. Xác suất của các dòng lỗi được để trống. Cách xử lý này giúp người dùng biết số lượng hồ sơ thực sự đã phân tích và tránh coi dòng lỗi là một khách hàng được dự đoán không churn. Danh sách sau xử lý có thể tải về để sửa hoặc tiếp tục xem xét.

### Màn hình hiệu quả mô hình
Màn hình hiệu quả mô hình trình bày các độ đo trên test, bảng so sánh các cấu hình vận hành và ma trận nhầm lẫn. Các thẻ nội dung cung cấp đường ROC/PR, trường hợp sai, kết quả CV và kết quả theo nhóm. Các bảng đều đọc từ artifact của lần chạy đã cố định, không được tính lại bằng dữ liệu người dùng tải lên.

@figure reports/evidence/audit_evaluation.jpg|Màn hình đánh giá hiệu quả mô hình

Màn hình này giải quyết nhu cầu hiểu mô hình hoạt động tốt ở đâu và còn bỏ sót những trường hợp nào. Người sử dụng có thể đối chiếu recall với số FN, precision với số FP, đồng thời nhìn thấy sự khác biệt giữa Logistic Regression, Random Forest và baseline. Việc đưa kết quả đối chứng vào cùng ứng dụng giúp tránh đánh giá hệ thống chỉ dựa trên một hồ sơ dự đoán đúng.

### Màn hình ngưỡng và giải thích
Màn hình ngưỡng sử dụng xác suất validation để tính lại precision, recall và số khách hàng được đánh dấu theo vị trí thanh trượt. Biểu đồ thể hiện sự thay đổi của các đại lượng khi ngưỡng thay đổi. Phần độ quan trọng thuộc tính sử dụng kết quả permutation importance đã tính trên validation.

@figure reports/evidence/audit_threshold.jpg|Màn hình khảo sát ngưỡng phân loại

Thanh trượt có giá trị hiển thị mặc định làm tròn là 0,479, khác với ngưỡng chính thức đầy đủ 0,4788031716353531. Tại 0,479, màn hình có thể hiển thị 600 hồ sơ được đánh dấu và 74 trường hợp bỏ sót, trong khi ngưỡng chính thức cho 601 hồ sơ và 73 trường hợp bỏ sót trên validation. Khác biệt một hồ sơ xuất phát từ làm tròn ngưỡng, không phải thay đổi dữ liệu hoặc thay đổi mô hình. Dự đoán cá nhân và CSV vẫn sử dụng giá trị chính thức lưu trong metadata.

## Cấu hình và vận hành demo
Ứng dụng được chạy tại thư mục dự án bằng trình thông dịch trong môi trường ảo và lệnh streamlit run app.py. File CHAY_DEMO.ps1 cung cấp cách mở demo trên Windows. Sau khi cài đặt các phụ thuộc, mô hình và dữ liệu đã nằm trong dự án nên thao tác dự đoán không cần gọi một dịch vụ học máy bên ngoài.

Khi chuẩn bị demo, người thực hiện kiểm tra bundle, mở màn hình tổng quan, chọn một hồ sơ để phân tích, sau đó nhập tệp CSV có cả dòng hợp lệ và lỗi. Cuối cùng, màn hình đánh giá và ngưỡng được dùng để giải thích sự đánh đổi giữa phát hiện churn và báo động nhầm. Kịch bản này bao quát cả tình huống thành công, dữ liệu lỗi và giới hạn của mô hình.

Trong quá trình sử dụng, thay đổi nội dung biểu mẫu không làm thay đổi mô hình đã lưu. Muốn thực hiện một thiết kế thực nghiệm mới cần tạo lần chạy riêng, giữ dữ liệu đánh giá phù hợp và không ghi đè kết quả hiện tại chỉ để làm đẹp các chỉ số test. Cách quản lý này giúp nội dung demo, báo cáo và artifact giữ cùng một nguồn số liệu.

## Phạm vi hỗ trợ của công cụ AI
OpenAI Codex hỗ trợ xây dựng một phần đáng kể mã nguồn, kiểm thử, nội dung phân tích và tài liệu của dự án. Phạm vi hỗ trợ bao gồm rà soát đầu vào, tổ chức pipeline, tạo công cụ kiểm chứng, tối ưu xử lý CSV, bổ sung đánh giá độ bất định và chuẩn bị nội dung trình bày. Các kết quả định lượng trong báo cáo lấy từ dữ liệu và artifact thực thi, không thay bằng con số do công cụ tự suy đoán.

Nhật ký sử dụng AI được lưu trong docs/AI_USAGE.md; hồ sơ đóng góp riêng của từng thành viên phải ghi công việc thực sự tự đọc, chạy, sửa và kiểm chứng. Sự hỗ trợ của công cụ không thay thế trách nhiệm giải thích thuật toán, sửa mã trực tiếp và bảo vệ các quyết định của nhóm. Việc đánh giá tính đúng đắn phải dựa vào dữ liệu, kiểm thử, nguồn tài liệu và lập luận của người thực hiện.

# KIỂM THỬ VÀ ĐÁNH GIÁ
## Mục tiêu và phạm vi đánh giá
Đánh giá của đề tài gồm hai nhóm. Nhóm thứ nhất kiểm tra chất lượng học máy: mô hình có cải thiện so với baseline hay không, mức đánh đổi giữa các loại sai số và khả năng khái quát trên test. Nhóm thứ hai kiểm tra tính đúng đắn của hệ thống: dữ liệu có được xử lý nhất quán, mô hình đã lưu có cho cùng kết quả, CSV lỗi có được phát hiện và các màn hình có thực hiện đúng luồng chức năng hay không.

Kết quả mô hình được báo cáo trên tập test gồm 1.409 khách hàng, trong đó có 374 trường hợp churn và 1.035 trường hợp không churn. Mô hình và ngưỡng đã được lựa chọn trước khi đánh giá tập này. Các số thập phân trong bảng được làm tròn để trình bày; các phép tính đối chiếu sử dụng giá trị đầy đủ trong tệp kết quả.

## Kết quả kiểm định chéo
AP trung bình qua năm fold của baseline là 0,265325. Logistic Regression đạt 0,667818 với độ lệch chuẩn 0,024414; Random Forest đạt 0,672568 với độ lệch chuẩn 0,013939. Hai mô hình đều cao hơn rõ rệt so với mức đối chứng, cho thấy các thuộc tính đang cung cấp thông tin hữu ích để xếp hạng lớp churn trong quy trình CV.

@table cv|Kết quả kiểm định chéo trên tập train

Random Forest cao hơn Logistic Regression khoảng 0,004750 AP, nên được chọn theo tiêu chí đã xác định. Tuy nhiên, đây là một chênh lệch nhỏ so với mức dao động giữa các fold. Đề tài chưa thực hiện kiểm định thống kê hoặc đánh giá trên nhiều lần chia độc lập để khẳng định Random Forest vượt trội một cách tổng quát. Độ lệch chuẩn trong bảng mô tả các fold của lần chạy này, không phải khoảng tin cậy của chất lượng ngoài thực tế.

Việc lựa chọn Random Forest cũng không hàm ý mô hình này tốt nhất theo mọi độ đo. Logistic Regression có thể cho precision hoặc accuracy cao hơn tại ngưỡng mặc định. Tiêu chí lựa chọn của dự án là AP trong CV, sau đó lựa chọn ngưỡng nhằm phục vụ mục tiêu recall có ràng buộc precision. Cách đọc kết quả cần giữ đúng thứ tự và mục tiêu này.

## Kết quả đánh giá trên test
### So sánh các mô hình và ngưỡng
Để phân biệt tác động của thuật toán và tác động của ngưỡng, báo cáo trình bày năm cấu hình vận hành: baseline gốc, Logistic Regression tại 0,5, Logistic Regression tại ngưỡng chọn từ validation, Random Forest tại 0,5 và Random Forest tại ngưỡng chính thức. Hai ngưỡng bổ sung không được lựa chọn bằng cách tối ưu trên test.

@table test_prf|Precision, recall và F1 của các cấu hình trên test
@table test_rank|Accuracy, ROC-AUC và AP của các cấu hình trên test

Baseline đạt accuracy 0,7346 nhưng precision, recall và F1 cho lớp churn đều bằng 0 vì không đánh dấu khách hàng nào. Kết quả này xác nhận accuracy đơn độc không đủ phản ánh khả năng phát hiện churn. Logistic Regression tại ngưỡng 0,5 có accuracy 0,7984 và precision 0,6389, nhưng recall chỉ đạt 0,5535; tức là còn bỏ sót gần một nửa khách hàng churn trong test.

Khi sử dụng ngưỡng 0,243999 được chọn từ validation, recall của Logistic Regression tăng lên 0,8182, trong khi precision giảm xuống 0,4976. Ràng buộc precision 0,50 được đáp ứng ở validation không tự bảo đảm được đáp ứng trên test. Đây là một ví dụ cụ thể về sự biến động khi áp dụng cùng quy tắc cho dữ liệu độc lập.

Random Forest tại ngưỡng chính thức đạt precision 0,5076, recall 0,8075, F1 0,6233, ROC-AUC 0,8435 và AP 0,6482. So với baseline, mô hình có khả năng phát hiện phần lớn lớp churn thay vì chỉ chọn lớp đa số. So với Random Forest tại 0,5, ngưỡng chính thức tăng recall nhưng giảm precision, F1 và accuracy. Kết quả phù hợp mục tiêu ưu tiên recall của thiết kế, nhưng không phải phương án tối ưu F1 trên test.

### Ma trận nhầm lẫn và khối lượng sàng lọc
Tại ngưỡng chính thức, Random Forest xác định đúng 302 khách hàng churn, bỏ sót 72 khách hàng churn, đánh dấu nhầm 293 khách hàng không churn và xác định đúng 742 khách hàng không churn. Tổng số khách hàng được đánh dấu là 595, tương đương khoảng 42,23% tập test. Như vậy, để phát hiện 302 trường hợp churn trong dữ liệu, danh sách xem xét còn chứa 293 trường hợp báo động nhầm.

@figure artifacts/final_run/evaluation_confusion.png|Ma trận nhầm lẫn của Random Forest trên test
@table workload|Khối lượng sàng lọc của Random Forest theo hai ngưỡng

So với ngưỡng 0,5, hạ ngưỡng xuống mức chính thức giúp phát hiện thêm 4 trường hợp churn, đồng thời làm tăng 20 báo động nhầm. Số hồ sơ cần xem xét tăng từ 571 lên 595. Đây là sự đánh đổi quan sát được trên test của ngưỡng đã chọn từ validation, không phải một lý do để tiếp tục điều chỉnh ngưỡng theo test.

Nếu doanh nghiệp có năng lực liên hệ hạn chế, precision và số khách hàng cần xử lý sẽ trở nên quan trọng hơn. Ngược lại, nếu mục tiêu là giảm bỏ sót trong bước sàng lọc ban đầu, recall có thể được ưu tiên. Dữ liệu hiện tại không có chi phí liên hệ, tỷ lệ khách hàng phản hồi hoặc hiệu quả của biện pháp can thiệp, nên đề tài chưa kết luận ngưỡng này tối ưu lợi nhuận.

### Đường ROC và precision–recall
Đường ROC và PR được xây dựng từ xác suất dự đoán trên test. Random Forest đạt ROC-AUC 0,8435 và AP 0,6482; Logistic Regression đạt ROC-AUC 0,8425 và AP 0,6285. Mức ROC-AUC gần nhau cho thấy khác biệt về khả năng xếp hạng tổng thể không lớn theo độ đo này, trong khi AP thể hiện chênh lệch rõ hơn khi tập trung vào lớp churn.

@figure artifacts/final_run/evaluation_curves.png|Đường ROC và precision–recall trên test

Hai dòng kết quả của cùng một thuật toán ở các ngưỡng khác nhau có cùng ROC-AUC và AP vì sử dụng cùng điểm dự đoán. Việc thay ngưỡng chỉ chọn một vị trí quyết định trên tập điểm đó. Nhận định về hiệu quả ứng dụng do vậy cần kết hợp các đường đánh giá với precision, recall và khối lượng sàng lọc tại ngưỡng được sử dụng.

## Đánh giá lựa chọn ngưỡng
Trên validation, ngưỡng chính thức của Random Forest đạt precision 0,5008 và recall 0,8048, đáp ứng ràng buộc và mục tiêu mong muốn của lần thực nghiệm. Đường khảo sát cho thấy việc giảm ngưỡng mở rộng tập được đánh dấu, thường làm recall tăng và khiến precision phải đánh đổi. Các đoạn thay đổi dạng bậc xuất phát từ số lượng hữu hạn các hồ sơ và điểm dự đoán trong validation.

@figure artifacts/final_run/evaluation_threshold.png|Precision và recall theo ngưỡng trên validation

Chọn ngưỡng trên validation giúp tách quyết định vận hành khỏi phép đánh giá test, nhưng validation vẫn là một mẫu hữu hạn. Khi phân bố khách hàng hoặc tỷ lệ churn thay đổi, cùng ngưỡng có thể tạo ra precision và khối lượng công việc khác. Vì vậy, kết quả hiện tại chứng minh quy trình lựa chọn và đánh giá có thể thực hiện nhất quán; nó chưa thay thế việc xác nhận bằng dữ liệu mới của đơn vị sử dụng.

## Phân tích độ quan trọng thuộc tính
Permutation importance được tính trên validation bằng mức giảm AP khi tráo từng cột gốc, lặp lại 20 lần với seed 42. Contract có mức giảm AP trung bình khoảng 0,07770, InternetService khoảng 0,05414 và tenure khoảng 0,03660. Đây là ba thuộc tính có mức giảm lớn nhất trong lần phân tích.

@figure artifacts/final_run/evaluation_importance.png|Độ quan trọng thuộc tính trên validation
@table importance|Mười thuộc tính có mức giảm AP trung bình cao nhất

Kết quả phù hợp với các khác biệt đã quan sát ở EDA về hợp đồng, loại Internet và thời gian sử dụng. TotalCharges đứng tiếp theo với mức giảm AP khoảng 0,01940; OnlineSecurity có mức giảm khoảng 0,01390. Sự phù hợp giữa EDA và importance làm rõ mô hình có khai thác những khác biệt của dữ liệu, nhưng không cho phép coi các yếu tố đó là nguyên nhân trực tiếp của churn.

Đối với các thuộc tính có mức giảm nhỏ và độ lệch chuẩn tương đối lớn, thứ hạng không nên được diễn giải quá cứng nhắc. MonthlyCharges có thể chia sẻ thông tin với TotalCharges và các dịch vụ; khi chỉ tráo một biến, mô hình vẫn còn các biến liên quan để sử dụng. Biểu đồ cũng không giải thích tại sao một khách hàng cụ thể có điểm 60%, vì phép tính đo chất lượng trên toàn validation chứ không phân rã dự đoán từng cá nhân.

## Phân tích các trường hợp dự đoán sai
### Các trường hợp báo động nhầm
Đề tài xem xét năm FP tiêu biểu, gồm ba trường hợp có điểm cao và hai trường hợp gần ngưỡng. Những trường hợp này được chọn để đọc sâu các dạng sai số, không phải mẫu ngẫu nhiên đại diện cho toàn bộ 293 FP. Các hồ sơ vẫn giữ mã định danh của dữ liệu mẫu nhằm đối chiếu lại các thuộc tính khi cần.

@table fp_cases|Một số trường hợp FP trên test

Khách hàng 2545-EBUPK có tenure 2 tháng, hợp đồng theo tháng, sử dụng Fiber optic và nhận điểm khoảng 0,9333 dù nhãn thực tế là No. Hai khách hàng 8739-XNIKG và 8161-QYMTT cũng có thời gian sử dụng ngắn, hợp đồng theo tháng và Internet cáp quang. Các thuộc tính này gần với những nhóm có tỷ lệ churn cao trong train, nhưng việc thuộc một nhóm có tỷ lệ cao không đồng nghĩa từng khách hàng trong nhóm đều churn.

Hai trường hợp 5804-HYIEZ và 1194-SPVSP có điểm lần lượt khoảng 0,4801 và 0,4815, chỉ cao hơn ngưỡng chính thức một khoảng nhỏ. Những hồ sơ gần ranh giới dễ đổi nhãn nếu ngưỡng thay đổi. Vì vậy, việc trình bày cả điểm và trạng thái giúp người sử dụng tránh coi hai nhãn hai phía ngưỡng là những mức độ chắc chắn hoàn toàn khác nhau.

### Các trường hợp bỏ sót
Năm FN tiêu biểu cũng được chọn theo hai nhóm xa và gần ngưỡng. Khách hàng 8580-QVLOC có tenure 72 tháng, hợp đồng hai năm, dùng DSL nhưng có nhãn churn. Điểm dự đoán chỉ khoảng 0,0467. Hồ sơ 3400-ESFUW sử dụng 55 tháng, hợp đồng hai năm và cũng bị bỏ sót với điểm khoảng 0,0784.

@table fn_cases|Một số trường hợp FN trên test

Những trường hợp này cho thấy mô hình có thể bỏ qua khách hàng churn thuộc nhóm vốn có tỷ lệ thấp trong train. Dữ liệu chưa có thông tin về trải nghiệm dịch vụ, khiếu nại, thay đổi nhu cầu hoặc sự kiện gần thời điểm rời bỏ để giúp phân biệt các trường hợp ngoại lệ. Không thể xác nhận nguyên nhân thực tế của từng khách hàng chỉ bằng những thuộc tính hiện có.

Hai hồ sơ 4695-VADHF và 6646-QVXLR có điểm khoảng 0,4758 và 0,4757, gần phía dưới ngưỡng. Hạ ngưỡng có thể phát hiện thêm các trường hợp này nhưng đồng thời làm tăng FP ở các hồ sơ khác. Trong khi đó, những FN có điểm rất thấp sẽ không được giải quyết bằng một thay đổi ngưỡng nhỏ; chúng gợi ra nhu cầu bổ sung dữ liệu và đánh giá mô hình trên các nhóm ít churn.

## Đánh giá theo nhóm khách hàng
### Hợp đồng và loại dịch vụ Internet
Kết quả phân nhóm được tính trên test bằng cùng ngưỡng chính thức. Nhóm hợp đồng theo tháng có 773 hồ sơ và recall khoảng 0,9088. Nhóm hợp đồng một năm có 300 hồ sơ nhưng recall chỉ 0,0833; nhóm hai năm có 336 hồ sơ và không phát hiện được trường hợp churn nào trong 9 trường hợp thực tế của nhóm. Như vậy, recall chung 0,8075 không phản ánh chất lượng đồng đều giữa các loại hợp đồng.

@table subgroup_service|Kết quả test theo hợp đồng và dịch vụ Internet

Đối với Internet, recall của nhóm Fiber optic khoảng 0,8889, DSL khoảng 0,6907 và nhóm không sử dụng Internet khoảng 0,4400. Các kết quả này bổ sung góc nhìn quan trọng cho ma trận nhầm lẫn chung: mô hình phát hiện tốt hơn ở các nhóm churn phổ biến nhưng còn bỏ sót đáng kể ở nhóm có ít trường hợp dương. Việc cải tiến cần được đánh giá theo nhóm và trên dữ liệu mới, tránh chọn một ngưỡng riêng cho từng nhóm chỉ nhằm sửa kết quả test hiện tại.

### Giới tính và nhóm tuổi
Trên test, nhóm Female có 687 hồ sơ, precision khoảng 0,5315 và recall 0,7876; nhóm Male có 722 hồ sơ, precision khoảng 0,4854 và recall 0,8287. Nhóm SeniorCitizen=1 có 222 hồ sơ và recall khoảng 0,8980, trong khi nhóm SeniorCitizen=0 có 1.187 hồ sơ và recall khoảng 0,7754.

@table subgroup_demographic|Kết quả test theo giới tính và nhóm tuổi

Các chênh lệch được trình bày nhằm kiểm tra thêm hành vi mô hình, chưa đủ để kết luận công bằng hoặc bất công giữa các nhóm. Quy mô mẫu, tỷ lệ churn, phân bố hợp đồng và sai số ước lượng đều có thể ảnh hưởng đến các độ đo. Dữ liệu cần được mở rộng và xác định tiêu chí đánh giá phù hợp trước khi đưa ra kết luận về công bằng khi triển khai.

## Độ bất định của kết quả đánh giá
Các độ đo trên test là ước lượng từ 1.409 hồ sơ hữu hạn, vì vậy cần trình bày khoảng ước lượng cùng giá trị điểm. Precision và recall sử dụng khoảng Wilson 95% theo mô hình tỷ lệ nhị thức [15]. AP, ROC-AUC, F1 và chênh lệch AP giữa RF với LR sử dụng 2.000 mẫu bootstrap theo hàng có hoàn lại, seed 42, lấy phân vị 2,5% và 97,5% [14]. Hai mô hình dùng cùng chỉ số lấy mẫu ở mỗi lần lặp để giữ tính ghép cặp trên cùng khách hàng.

@table uncertainty|Khoảng ước lượng 95% trên test của các mô hình đã cố định

Tại ngưỡng chính thức, recall của RF bằng 0,8075, với khoảng Wilson từ 0,7645 đến 0,8442. Precision bằng 0,5076, với khoảng từ 0,4675 đến 0,5476. Như vậy, precision quan sát vượt 50% không đồng nghĩa đã chứng minh precision quần thể luôn vượt mức đó. Mục tiêu 80% recall cũng là mục tiêu vận hành trên một mẫu, không phải cam kết cho mọi nhóm khách hàng hoặc giai đoạn mới.

Chênh lệch AP trên test của RF trừ LR bằng 0,0197; khoảng bootstrap ghép cặp từ 0,0016 đến 0,0366 nằm phía dương trong phép tính này. Kết quả mô tả lợi thế của RF đối với hai mô hình đã fit và mẫu test hiện có. Nó không thay thế tiêu chí chọn mô hình bằng CV trên train, không được dùng để chọn lại siêu tham số và không bao gồm sai số do thử nhiều cấu hình. Độ lệch chuẩn giữa năm fold CV ở phần trước là một đại lượng khác với các khoảng này.

Bootstrap giả định các hàng có thể được xem là những quan sát độc lập cùng phân bố. Dữ liệu hiện tại không cho phép kiểm chứng giả định đó đối với khách hàng tương lai hoặc các cụm hộ gia đình. Khoảng phân vị là xấp xỉ có điều kiện trên mô hình đã huấn luyện, không phản ánh bất định của toàn bộ quá trình huấn luyện, lựa chọn mô hình, thay đổi thị trường hoặc hiệu quả can thiệp. Các khoảng được đọc riêng từng độ đo, không phải một tập khoảng đồng thời đã hiệu chỉnh cho so sánh nhiều lần.

## Độ tin cậy của xác suất dự đoán
Khả năng xếp hạng tốt và khả năng ước lượng xác suất đúng là hai thuộc tính khác nhau. Đường độ tin cậy chia xác suất validation thành 10 khoảng đều nhau, rồi so xác suất dự đoán trung bình với tỷ lệ churn thực tế trong từng khoảng. Điểm gần đường chéo thể hiện sự phù hợp giữa hai đại lượng; khoảng ít mẫu có độ bất định lớn hơn. Tệp dữ liệu đi kèm lưu số mẫu và khoảng Wilson của từng khoảng để hỗ trợ kiểm tra [12].

@figure artifacts/diagnostics/reliability_validation.png|Độ tin cậy của xác suất trên validation
@table calibration|Brier và log loss trên validation

Logistic Regression có Brier 0,1378 và log loss 0,4281, thấp hơn RF tương ứng 0,1652 và 0,4942; cả hai tốt hơn mốc xác suất train cố định. Điều này cho thấy ưu thế AP của RF không đồng nghĩa RF tốt nhất về chất lượng xác suất. Quyết định chọn RF vẫn theo tiêu chí CV AP đã chốt, trong khi sự khác biệt này được ghi nhận như một giới hạn cần cân nhắc nếu mục đích sử dụng chuyển sang dự báo xác suất gắn với chi phí.

Brier là trung bình bình phương sai số giữa xác suất và nhãn nhị phân; log loss phạt mạnh dự đoán tự tin nhưng sai. Cả hai càng thấp càng tốt, nhưng cùng phản ánh hiệu chỉnh, khả năng phân biệt và đặc điểm nhãn nên không được diễn giải như thước đo riêng của calibration [12]. Mốc tham chiếu xác suất cố định lấy tỷ lệ churn trên train; đây là phép tham chiếu bổ sung cho chất lượng xác suất, khác với Dummy most_frequent chính thức luôn dự đoán No.

Phân tích này là chẩn đoán mô tả trên validation đã tham gia chọn ngưỡng. Dự án không fit bộ hiệu chỉnh trên test và không đổi xác suất của mô hình demo. Nếu cần hiệu chỉnh ở lần nghiên cứu tiếp theo, dữ liệu dùng để fit bộ hiệu chỉnh phải độc lập với dữ liệu đánh giá cuối, hoặc quy trình hiệu chỉnh phải nằm trong thiết kế kiểm định chéo phù hợp. Các điểm churn hiện có vẫn được gọi là xác suất ước lượng chưa hiệu chỉnh.

## Khả năng ưu tiên hồ sơ theo năng lực xử lý
Trong một chiến dịch có số nhân viên hữu hạn, câu hỏi vận hành có thể là cần xem xét bao nhiêu hồ sơ để bao phủ một phần khách hàng churn. Phép khảo sát sắp xác suất RF trên validation theo thứ tự giảm dần, lấy số hồ sơ bằng phần nguyên làm tròn lên của tỷ lệ năng lực nhân với 1.409. Nếu điểm bằng nhau, thứ tự customerID phá hòa; nhãn không tham gia xếp hạng.

@figure artifacts/diagnostics/capacity_validation.png|Khả năng bao phủ churn theo tỷ lệ hồ sơ được xem xét trên validation
@table capacity|Đánh đổi giữa năng lực xử lý và khả năng bao phủ churn

Khi xem xét 20% hồ sơ, danh sách gồm 282 khách và chứa 188 trong 374 trường hợp churn của validation. Recall đạt 50,27%, precision đạt 66,67% và lift so với chọn ngẫu nhiên bằng khoảng 2,51. Khi năng lực tăng đến 40%, danh sách gồm 564 khách, chứa 292 trường hợp churn, tương ứng recall 78,07%. Những con số này giúp giải thích đánh đổi giữa độ phủ và khối lượng công việc thay vì chỉ đưa ra một ngưỡng thiếu bối cảnh.

Lift được tính bằng precision trong danh sách chia cho tỷ lệ churn toàn validation. Đại lượng này đo mức tập trung khách churn quan sát trong danh sách, không phải mức tăng giữ chân hay lợi nhuận. Để đánh giá tác động kinh doanh cần dữ liệu can thiệp có nhóm đối chứng, chi phí liên hệ, giá trị giữ chân và phản hồi thực tế. Thanh trượt năng lực trong ứng dụng chỉ minh họa trên validation, không thay ngưỡng chính thức đã khóa.

## Kiểm thử chức năng và tính tái lập
### Bộ kiểm thử tự động
Bộ kiểm thử hiện tại đều đạt trong lần kiểm tra trên mã dự án hiện hành; số ca theo từng nhóm lấy trực tiếp từ JUnit XML và trình bày ở bảng dưới. Nội dung bao quát dữ liệu, phân hoạch, tiền xử lý, lựa chọn ngưỡng, suy luận, CSV, các luồng Streamlit, đóng gói, khoảng ước lượng và phân tích năng lực xử lý. Không có ca lỗi hoặc bị bỏ qua trong lần kiểm chứng được trình bày.

@table tests|Kết quả bộ kiểm thử tự động theo nhóm

Việc kiểm thử tập trung vào những sai lệch có thể làm kết quả học máy không còn đáng tin cậy. Ví dụ, kiểm tra tập ID giúp phát hiện khách hàng xuất hiện ở cả train và test; kiểm tra bước điền thiếu giúp xác nhận thống kê fit không lấy từ holdout; kiểm tra dự đoán CSV bảo đảm dòng lỗi không nhận điểm giả. Các kiểm tra này bổ sung cho việc quan sát giao diện bằng mắt.

### Kiểm thử giao diện và tình huống dữ liệu
Giao diện được kiểm tra qua các luồng xem tổng quan, chọn hồ sơ, dự đoán cá nhân, nhập danh sách có lỗi, đọc kết quả đánh giá và kéo ngưỡng. Hồ sơ tham khảo 8499-BRXTD nhận điểm khoảng 0,0555, hiển thị làm tròn thành 5,6% và không được đánh dấu. Điểm từ pipeline nạp trực tiếp khớp với kết quả của luồng giao diện đã kiểm tra.

@table ui_tests|Các tình huống kiểm tra chức năng ứng dụng

Tệp CSV có dòng thiếu cột bắt buộc được từ chối ở mức cấu trúc. Với tệp có cấu trúc đúng nhưng một số dòng không hợp lệ, ứng dụng giữ toàn bộ dòng để phản hồi lỗi và chỉ dự đoán phần hợp lệ. Cách xử lý đã được kiểm tra với dữ liệu âm, danh mục lạ và quan hệ dịch vụ không nhất quán. Không có phép tính accuracy tự động trên nhãn tùy ý do người dùng tải lên.

### Kiểm chứng số liệu và môi trường sạch
Khi nạp lại pipeline đã lưu và tính xác suất cho toàn bộ test, sai khác lớn nhất so với tệp dự đoán đã lưu bằng 0. Năm dòng kết quả đánh giá được tính lại từ nhãn và dự đoán, với sai khác số thực lớn nhất khoảng 1,11 × 10⁻¹⁶. Sai khác này thuộc mức biểu diễn số thực của máy, không phải thay đổi kết quả phân loại.

Ba tập được ghép lại theo customerID, đủ 7.043 hồ sơ và không trùng ID giữa các tập. Notebook có sáu ô mã đã được thực thi và không có output lỗi. Bộ kiểm thử mới được chạy ở môi trường chính và môi trường kiểm chứng độc lập với cùng phiên bản thư viện. Bằng chứng tái huấn luyện của lần triển khai ban đầu cho cùng kết quả CV, tham số lựa chọn, ngưỡng và xác suất; lần nâng cấp đánh giá hiện tại không huấn luyện hoặc chọn lại mô hình.

@table reproducibility|Kết quả kiểm chứng tính nhất quán và tái lập

Những bằng chứng trên xác nhận khả năng chạy lại và sự nhất quán giữa mã, mô hình, bảng số liệu và demo trong môi trường đã kiểm. Chúng không thay thế đánh giá trên một doanh nghiệp mới hoặc một giai đoạn thời gian mới. Dự án chưa thực hiện đo tải nhiều người dùng đồng thời, kiểm thử vận hành dài hạn hoặc triển khai công khai.

## Đánh giá tổng hợp
Đề tài đáp ứng mục tiêu xây dựng một quy trình phân loại có đối chứng và một ứng dụng sử dụng mô hình thật. Các kết quả được liên kết từ dữ liệu gốc đến phân hoạch, CV, lựa chọn ngưỡng, đánh giá test và giao diện. Random Forest ở ngưỡng chính thức phát hiện 302 trên 374 trường hợp churn của test, trong khi baseline không phát hiện trường hợp nào.

Giới hạn nổi bật là số báo động nhầm còn lớn và chất lượng khác biệt giữa các nhóm hợp đồng. Ngưỡng hiện tại phù hợp với giả định sàng lọc ưu tiên recall đã đặt ra, chưa chứng minh tối ưu chi phí. Kết quả theo nhóm và các FN có điểm thấp cho thấy việc cải tiến cần thêm dữ liệu liên quan thời điểm và trải nghiệm khách hàng, đồng thời phải duy trì một tập đánh giá độc lập.

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
## Kết luận
Đề tài đã xây dựng hệ thống thử nghiệm dự đoán khách hàng rời dịch vụ viễn thông trên bộ dữ liệu Telco Customer Churn. Quy trình được thực hiện từ kiểm tra và khám phá dữ liệu đến tiền xử lý, kiểm định chéo, lựa chọn mô hình, lựa chọn ngưỡng và đánh giá trên test. Ứng dụng Streamlit cung cấp năm màn hình phục vụ xem dữ liệu, phân tích cá nhân, xử lý CSV và đọc kết quả mô hình.

Kết quả cho thấy việc đánh giá bài toán churn cần vượt ra ngoài accuracy. Baseline luôn chọn lớp No đạt accuracy 73,46% trên test nhưng recall bằng 0. Random Forest được chọn bằng AP trong CV và sử dụng ngưỡng 0,478803 từ validation; trên test, mô hình đạt recall 80,75%, precision 50,76%, F1 0,6233 và AP 0,6482. Mô hình hỗ trợ phát hiện phần lớn trường hợp churn trong bộ dữ liệu, đồng thời vẫn tạo ra 293 báo động nhầm và bỏ sót 72 trường hợp.

## Kết quả đạt được
Về dữ liệu, đề tài kiểm tra đủ 7.043 hồ sơ, xác định 11 giá trị TotalCharges thiếu, không phát hiện ID hoặc dòng trùng và giữ lại các quan sát có giá trị hợp lệ. Tám biểu đồ trên train làm rõ sự khác biệt theo hợp đồng, Internet, thanh toán, thời gian sử dụng và cước. Các nhận định khám phá được kết hợp với phân tích tương quan và độ quan trọng thuộc tính để giải thích cách mô hình khai thác thông tin.

Về phương pháp, đề tài xây dựng pipeline dùng chung, so sánh hai mô hình với baseline, khảo sát 26 cấu hình học máy bằng CV năm fold và tách việc lựa chọn ngưỡng khỏi đánh giá test. Kết quả có đầy đủ độ đo, ma trận nhầm lẫn, ROC/PR, phân tích FP/FN và đánh giá theo nhóm. Cấu hình cùng ngưỡng được lưu để sử dụng thống nhất ở ứng dụng.

Về triển khai, ứng dụng có khả năng dự đoán một hồ sơ và danh sách, kiểm tra đầu vào, giữ dòng lỗi để phản hồi và xuất kết quả. Bộ 99 kiểm thử cùng các phép đối chiếu mô hình, số liệu và môi trường sạch cung cấp bằng chứng cho tính đúng đắn của luồng xử lý. Người sử dụng có thể kiểm tra được kết quả bằng dữ liệu và artifact đi kèm dự án.

## Giới hạn phạm vi của đề tài
Bộ dữ liệu là dữ liệu mẫu của một doanh nghiệp hư cấu và chưa được xác nhận đại diện cho khách hàng của một nhà mạng cụ thể. Các quan hệ được phát hiện chỉ phản ánh bộ dữ liệu và cách chia tập hiện tại. Không thể từ kết quả này suy ra tỷ lệ giữ chân hoặc doanh thu tăng thêm khi triển khai tại doanh nghiệp.

Dữ liệu không có lịch sử thời điểm đầy đủ nên đề tài chưa xác nhận một kỳ dự báo sớm. Xác suất Random Forest chưa được hiệu chỉnh; các giá trị hiển thị không được xem là xác suất chính xác cho một thời hạn tương lai đã xác định. Khoảng Wilson và bootstrap mới bổ sung mô tả bất định của mẫu holdout có điều kiện trên mô hình cố định. Kiểm định chéo vẫn dùng một cấu hình chia, chưa lượng hóa biến động của toàn bộ quá trình huấn luyện qua nhiều lần chia hoặc qua các giai đoạn thời gian.

Mô hình còn yếu ở nhóm khách hàng có hợp đồng dài. Đặc biệt, trên test, cả 9 trường hợp churn của nhóm hợp đồng hai năm đều bị bỏ sót tại ngưỡng chính thức. Phân tích importance là phân tích tổng thể, chưa có phương pháp giải thích cục bộ cho từng dự đoán. Ngoài ra, hệ thống hiện chạy local, chưa có quản lý tài khoản, kết nối CRM, lịch huấn luyện lại hoặc giám sát mô hình trong vận hành.

## Hướng phát triển
### Bổ sung dữ liệu và xác định thời điểm dự báo
Hướng ưu tiên là thu thập dữ liệu có thời điểm quan sát rõ ràng và định nghĩa một cửa sổ dự báo cụ thể. Mỗi hồ sơ cần được xây dựng từ thông tin có trước thời điểm ra quyết định, trong khi nhãn được xác định ở giai đoạn sau. Khi có lịch sử, cách chia train và test theo thời gian sẽ phù hợp hơn để đánh giá khả năng sử dụng cho các khách hàng ở giai đoạn tương lai.

Các nhóm thông tin có thể khảo sát thêm gồm sự cố dịch vụ, lịch sử khiếu nại, mức sử dụng, thay đổi gói cước và phản hồi chăm sóc. Việc bổ sung phải đi kèm kiểm tra thời điểm phát sinh, chất lượng và quyền sử dụng dữ liệu. Mục tiêu là cải thiện khả năng phân biệt các trường hợp churn ít điển hình, không chỉ tăng số lượng thuộc tính.

### Cải tiến đánh giá và lựa chọn mô hình
Đề tài có thể mở rộng sang đánh giá nhiều lần chia, ước lượng độ bất định và so sánh thêm thuật toán phù hợp dữ liệu bảng. Mọi cấu hình mới cần được lựa chọn trên phần dữ liệu huấn luyện và validation, đồng thời đánh giá trên một tập độc lập chưa tham gia tối ưu. Mô hình chỉ nên thay thế phiên bản hiện tại khi có bằng chứng cải thiện theo tiêu chí đã xác định trước.

Hiệu chỉnh xác suất là một hướng cần thiết nếu điểm sẽ được sử dụng trong quyết định gắn với chi phí. Sau khi có chi phí liên hệ, tổn thất do bỏ sót và dữ liệu hiệu quả can thiệp, ngưỡng có thể được lựa chọn theo giá trị kỳ vọng hoặc năng lực xử lý. Cách đánh giá cũng cần theo dõi riêng các nhóm hợp đồng để tránh che khuất chất lượng thấp của nhóm nhỏ bằng độ đo chung.

### Hoàn thiện khả năng sử dụng
Ở mức ứng dụng, có thể bổ sung phân quyền, quản lý lịch sử phân tích, kết nối hệ thống khách hàng và quy trình ghi nhận kết quả liên hệ. Khi triển khai, cần lưu phiên bản mô hình gắn với mỗi dự đoán để đối chiếu và kiểm soát thay đổi. Các chức năng vận hành như giám sát phân bố đầu vào, kiểm tra chất lượng theo thời gian và cơ chế quay lại phiên bản trước cũng cần được thiết kế.

Việc đánh giá tác động của hệ thống nên dựa trên kết quả thực hiện một quy trình chăm sóc có đối chứng, thay vì chỉ dựa trên điểm phân loại. Khi có dữ liệu phản hồi, doanh nghiệp mới có thể kiểm tra liệu danh sách ưu tiên có giúp sử dụng nguồn lực hiệu quả và giảm churn hay không. Đây là bước tiếp theo để chuyển từ một demo học máy có kiểm chứng sang một công cụ hỗ trợ hoạt động thực tế.

# DANH MỤC TÀI LIỆU THAM KHẢO
@references
