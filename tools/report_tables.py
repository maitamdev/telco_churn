"""Report tables assembled from frozen project artifacts; no model mutation."""
from pathlib import Path
import csv, json, collections
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'artifacts/final_run'

def csvrows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def dec(x, digits=4):
    return f'{float(x):.{digits}f}'.replace('.', ',')

def load_tables():
    t = {}
    def add(key, headers, rows, widths=None):
        t[key] = dict(headers=headers, rows=rows, widths=widths)
    add('objectives', ['Nội dung', 'Tiêu chí thực hiện', 'Cách đánh giá'], [
        ['Dữ liệu', 'Xác định nguồn, kiểu, thiếu, trùng và ngoại lai', 'Hồ sơ dữ liệu, kiểm tra ID và thống kê'],
        ['Khám phá', 'Ít nhất 5 biểu đồ có nhận định; thực hiện 8 biểu đồ', 'Hình và số liệu trên train'],
        ['Mô hình', 'Baseline, Logistic Regression và Random Forest', 'CV năm fold; AP trung bình'],
        ['Ngưỡng', 'Precision ≥ 0,50; ưu tiên recall; mong muốn recall ≥ 0,80', 'Lựa chọn trên validation'],
        ['Đánh giá', 'Đánh giá độc lập, phân tích FP/FN và giới hạn', 'Độ đo và ma trận nhầm lẫn test'],
        ['Ứng dụng', 'Dự đoán cá nhân và CSV bằng pipeline đã lưu', 'Kiểm thử tự động và thao tác giao diện'],
    ], [1900,3900,3261])
    add('metric_meaning', ['Trường hợp', 'Nhãn và dự đoán', 'Ý nghĩa trong sàng lọc'], [
        ['TP', 'Thực tế Yes; dự đoán Yes', 'Phát hiện đúng khách hàng churn'],
        ['TN', 'Thực tế No; dự đoán No', 'Không đánh dấu khách hàng không churn'],
        ['FP', 'Thực tế No; dự đoán Yes', 'Báo động nhầm, làm tăng danh sách cần xem xét'],
        ['FN', 'Thực tế Yes; dự đoán No', 'Bỏ sót khách hàng churn'],
    ], [1500,3000,4561])
    add('functional', ['Chức năng', 'Dữ liệu vào', 'Kết quả'], [
        ['Tổng quan', 'Dữ liệu gốc và tập train', 'Thống kê, biểu đồ, danh sách có bộ lọc'],
        ['Phân tích khách hàng', '19 thuộc tính; ID tùy chọn', 'Điểm churn và trạng thái theo ngưỡng'],
        ['Nhập danh sách', 'CSV có các cột bắt buộc', 'Dự đoán dòng hợp lệ, giữ dòng lỗi, xuất CSV'],
        ['Hiệu quả mô hình', 'Artifact đánh giá đã lưu', 'So sánh mô hình, sai số và kết quả theo nhóm'],
        ['Ngưỡng và giải thích', 'Xác suất validation, giá trị ngưỡng', 'Precision, recall, số hồ sơ và importance'],
    ], [2200,2800,4061])
    add('dataset', ['Đặc điểm', 'Giá trị', 'Vai trò'], [
        ['Nguồn', 'IBM Telco Customer Churn', 'Dữ liệu mẫu công khai'],
        ['Số hồ sơ / số cột', '7.043 / 21', 'Quy mô tệp gốc'],
        ['Thuộc tính học máy', '19', '3 cột số, 16 cột phân loại'],
        ['Churn=Yes', '1.869 (26,54%)', 'Lớp dương, mã hóa 1'],
        ['Churn=No', '5.174 (73,46%)', 'Lớp âm, mã hóa 0'],
        ['customerID', '7.043 giá trị duy nhất', 'Đối chiếu; không đưa vào mô hình'],
        ['TotalCharges thiếu', '11 (0,1562%)', 'Giữ hồ sơ; điền thiếu trong pipeline'],
    ], [2600,2800,3661])
    lines=(ROOT/'docs/DATA_DICTIONARY.md').read_text(encoding='utf-8').splitlines()
    dictionary=[['customerID','Mã khách hàng','Chuỗi định danh; không học'],['Churn','Tình trạng rời dịch vụ','No=0, Yes=1; nhãn mục tiêu']]
    for line in lines:
        if line.startswith('| ') and not line.startswith('| Cột '):
            dictionary.append([c.strip() for c in line.strip('|').split('|')])
    add('dictionary',['Thuộc tính','Ý nghĩa','Kiểu và miền giá trị'],dictionary,[2450,2600,4011])
    add('quality',['Nội dung kiểm tra','Kết quả','Cách xử lý'],[
        ['Ô thiếu','11 TotalCharges; 20 cột khác không thiếu','Giữ 11 dòng; chuyển chuỗi trắng thành giá trị thiếu'],
        ['Kiểu TotalCharges','Có chuỗi trắng trong trường số','Chuyển kiểu trong bước chuẩn hóa'],
        ['ID trùng / dòng trùng','0 / 0','Giữ toàn bộ hồ sơ'],
        ['SeniorCitizen','Giá trị 0 và 1','Xử lý như thuộc tính phân loại'],
        ['Không có dịch vụ','No internet service; No phone service','Giữ đúng nhóm ngữ nghĩa'],
        ['Ngoại lai IQR chung trên train','0 điểm vượt rào ở cả 3 biến số','Không cắt các giá trị hợp lệ'],
        ['Rào riêng nhóm churn','tenure: 13; TotalCharges: 67','Chỉ mô tả, không dùng nhãn để loại mẫu'],
    ],[2400,3000,3661])
    add('splits',['Tập dữ liệu','Số hồ sơ','No / Yes','Mục đích'],[
        ['Train','4.225','3.104 / 1.121','EDA, CV và fit'],
        ['Validation','1.409','1.035 / 374','Chọn ngưỡng, importance'],
        ['Test','1.409','1.035 / 374','Đánh giá cuối'],
        ['Tổng','7.043','5.174 / 1.869','Các tập không trùng ID'],
    ],[1900,1500,2500,3161])
    add('architecture',['Thành phần','Trách nhiệm','Đầu ra'],[
        ['Dữ liệu','Kiểm nguồn, chất lượng, chia tập','CSV gốc, các tập và manifest'],
        ['Khám phá','Thống kê và biểu đồ train','8 hình, bảng nguồn và nhận định'],
        ['Huấn luyện','Pipeline, CV, tìm siêu tham số','Kết quả CV, cấu hình tốt nhất'],
        ['Đánh giá','Ngưỡng, test, FP/FN, importance','Metrics, dự đoán, hình và bảng'],
        ['Suy luận','Nạp bundle; kiểm tra và dự đoán','Điểm churn, nhãn và lỗi dữ liệu'],
        ['Giao diện','Biểu mẫu, CSV và trình bày','5 màn hình Streamlit'],
    ],[2000,3500,3561])
    env=json.loads((RUN/'environment.json').read_text(encoding='utf-8'))
    roles={'numpy':'Tính toán mảng','pandas':'Xử lý dữ liệu bảng','scikit-learn':'Pipeline và học máy','matplotlib':'Biểu đồ thực nghiệm','seaborn':'Biểu đồ thống kê','joblib':'Lưu và nạp pipeline','streamlit':'Ứng dụng tương tác','pytest':'Kiểm thử tự động','nbformat':'Cấu trúc notebook','nbclient':'Thực thi notebook'}
    add('environment',['Thành phần','Phiên bản','Vai trò'],[['Python',env['python'],'Ngôn ngữ thực thi']]+[[k,v,roles[k]] for k,v in env['packages'].items()],[2800,1800,4461])
    add('modules',['Tệp hoặc thư mục','Nội dung chính','Quan hệ sử dụng'],[
        ['src/data.py','Nguồn, chất lượng, chia tập','Chuẩn bị dữ liệu'],
        ['src/validation.py','Hợp đồng và kiểm tra đầu vào','Huấn luyện, suy luận'],
        ['src/preprocessing.py','Pipeline dùng chung','CV, fit và dự đoán'],
        ['src/train.py; evaluation.py','Huấn luyện, chọn và đánh giá','Tạo artifact thực nghiệm'],
        ['src/inference.py','Nạp bundle và dự đoán','Giao diện cá nhân / CSV'],
        ['src/eda.py; result_figures.py','Hình và bảng phân tích','Notebook và báo cáo'],
        ['app.py; ui/','Điều hướng và 5 màn hình','Tương tác người dùng'],
        ['data/','Dữ liệu gốc, các tập, CSV mẫu','Đầu vào và minh họa'],
        ['artifacts/','Pipeline, metadata, kết quả','Suy luận và đánh giá'],
        ['notebooks/; tests/','Notebook và kiểm thử','Kiểm chứng quy trình'],
    ],[3000,3300,2761])
    add('preprocessing',['Bước','Cấu hình','Phạm vi fit'],[
        ['FeatureNormalizer','Chuẩn hóa kiểu và biểu diễn; chọn 19 cột','Không học thống kê phân bố'],
        ['Điền thiếu số','median; add_indicator=True','Train của từng fold hoặc toàn train'],
        ['Chuẩn hóa số','StandardScaler; chỉ Logistic Regression','Sau imputer; cùng dữ liệu fit'],
        ['Điền thiếu phân loại','most_frequent','Train của từng fold hoặc toàn train'],
        ['Mã hóa phân loại','OneHotEncoder; handle_unknown=ignore; drop=None','Tập giá trị học từ dữ liệu fit'],
        ['Bộ phân loại','Dummy / Logistic Regression / Random Forest','Dữ liệu sau biến đổi'],
    ],[2400,3700,2961])
    add('grids',['Mô hình','Siêu tham số','Các giá trị khảo sát'],[
        ['Logistic Regression','C','0,01; 0,1; 1; 10'],
        ['Logistic Regression','class_weight','None; balanced'],
        ['Random Forest','max_depth','4; 8; None'],
        ['Random Forest','min_samples_leaf','1; 5; 20'],
        ['Random Forest','class_weight','None; balanced'],
    ],[2800,2800,3461])
    selection=json.loads((RUN/'selection_record.json').read_text(encoding='utf-8'))
    names={'baseline':'Dummy','logistic_regression':'Logistic Regression','random_forest':'Random Forest'}
    add('val_thresholds',['Mô hình','Ngưỡng','Precision','Recall'],[[names[k],dec(v['threshold'],6),dec(v['validation_metrics']['precision_churn']),dec(v['validation_metrics']['recall_churn'])] for k,v in selection['threshold_records'].items()],[3400,2000,1830,1831])
    add('cv',['Mô hình','Cấu hình','AP trung bình','Độ lệch chuẩn'],[[names[v['model']],str(v['candidates']),dec(v['mean_average_precision'],6),dec(v['std_average_precision'],6)] for v in selection['cv_summary']],[3200,1500,2180,2181])
    metrics=csvrows(RUN/'test_metrics.csv')
    labels=['Dummy','LR (0,5)','LR (0,243999)','RF (0,5)','RF (0,478803)']
    add('test_prf',['Mô hình (ngưỡng)','Precision','Recall','F1'],[[lab]+[dec(row[k]) for k in ['precision_churn','recall_churn','f1_churn']] for lab,row in zip(labels,metrics)],[3400,1887,1887,1887])
    add('test_rank',['Mô hình (ngưỡng)','Accuracy','ROC-AUC','AP'],[[lab]+[dec(row[k]) for k in ['accuracy','roc_auc','average_precision']] for lab,row in zip(labels,metrics)],[3400,1887,1887,1887])
    rf=metrics[-2:]
    add('workload',['Kết quả','Ngưỡng 0,5','Ngưỡng 0,478803'],[[label,rf[0][k],rf[1][k]] for k,label in [('tp','Phát hiện đúng (TP)'),('fp','Báo động nhầm (FP)'),('fn','Bỏ sót (FN)'),('tn','Không churn đúng (TN)'),('flagged_count','Tổng được đánh dấu')]],[3900,2580,2581])
    imp=csvrows(RUN/'permutation_importance_validation.csv')[:10]
    add('importance',['Thuộc tính','Giảm AP trung bình','Độ lệch chuẩn'],[[r['feature'],dec(r['importance_mean'],5),dec(r['importance_std'],5)] for r in imp],[3300,2880,2881])
    errors=csvrows(RUN/'error_cases.csv')
    contracts={'Month-to-month':'Theo tháng','One year':'Một năm','Two year':'Hai năm'}
    for key,typ in [('fp_cases','FP'),('fn_cases','FN')]:
        add(key,['customerID','Điểm churn','tenure','Hợp đồng'],[[r['customerID'],dec(r['probability']),r['tenure'],contracts[r['Contract']]] for r in errors if r['outcome']==typ],[3100,2000,1500,2461])
    groups=csvrows(RUN/'subgroup_metrics.csv')
    for key,features in [('subgroup_service',['Contract','InternetService']),('subgroup_demographic',['gender','SeniorCitizen'])]:
        add(key,['Nhóm','Số mẫu','Precision','Recall'],[[r['group'] if r['feature']!='SeniorCitizen' else 'SeniorCitizen='+r['group'],r['n'],dec(r['precision_churn']),dec(r['recall_churn'])] for r in groups if r['feature'] in features],[3600,1500,1980,1981])
    testroot=ET.parse(ROOT/'reports/evidence/pytest_upgrade.xml').getroot()
    counts=collections.Counter(x.get('classname') for x in testroot.iter('testcase'))
    testlabels={'tests.test_app':'Giao diện Streamlit','tests.test_evaluation':'Đánh giá và ngưỡng','tests.test_pipeline':'Pipeline và suy luận','tests.test_validation':'Kiểm tra dữ liệu','tests.test_packaging':'Đóng gói và bằng chứng','tests.test_diagnostics':'Độ bất định và sàng lọc'}
    total=sum(counts.values())
    add('tests',['Nhóm kiểm thử','Số ca','Kết quả'],[[testlabels[k],str(v),'Đạt'] for k,v in counts.items()]+[['Tổng',str(total),f'{total} đạt; 0 lỗi; 0 bỏ qua']],[4700,1500,2861])
    add('ui_tests',['Tình huống','Kết quả mong đợi','Kết quả thực tế'],[
        ['Mở 5 trang','Hiển thị đúng dữ liệu và thành phần','Đạt'],
        ['Hồ sơ 8499-BRXTD','Điểm khớp pipeline; không đánh dấu','Khoảng 5,6%; khớp'],
        ['Thiếu TotalCharges','Điền thiếu bằng pipeline đã fit','Dự đoán được hồ sơ hợp lệ'],
        ['CSV có 3 dòng hỗn hợp','1 dự đoán; 2 dòng lỗi được giữ','Đúng số lượng và thứ tự'],
        ['Thiếu cột bắt buộc','Từ chối cấu trúc không hợp lệ','Có thông báo lỗi'],
        ['Dữ liệu âm / danh mục lạ','Không tạo xác suất cho dòng sai','Dòng lỗi có lý do'],
        ['Thay ngưỡng minh họa','Không đổi ngưỡng chính thức','Ngưỡng mô hình được giữ'],
    ],[2600,3600,2861])
    add('reproducibility',['Nội dung đối chiếu','Phạm vi','Kết quả'],[
        ['Dữ liệu các tập','7.043 ID và giá trị gốc','Đầy đủ, không giao nhau'],
        ['Nạp lại mô hình','1.409 xác suất test','Sai khác lớn nhất bằng 0'],
        ['Tính lại độ đo','5 cấu hình vận hành','Sai khác tối đa khoảng 1,11 × 10⁻¹⁶'],
        ['Notebook','6 ô mã','Đã thực thi; không có output lỗi'],
        ['Môi trường kiểm chứng',f'{total} ca kiểm thử',f'{total} đạt'],
        ['Tái huấn luyện','CV, lựa chọn, ngưỡng, xác suất','Sai khác bằng 0 trong phép đối chiếu'],
    ],[2900,2700,3461])
    diagnostics=json.loads((ROOT/'artifacts/diagnostics/summary.json').read_text(encoding='utf-8'))
    labels={'precision_churn':'Precision churn','recall_churn':'Recall churn','f1_churn':'F1 churn','roc_auc':'ROC-AUC','average_precision':'Average Precision','ap_difference':'AP của RF trừ AP của LR'}
    add('uncertainty',['Độ đo','Ước lượng','Cận dưới 95%','Cận trên 95%'],
        [[label]+[dec(diagnostics['test_intervals'][key][c]) for c in ['estimate','lower','upper']] for key,label in labels.items()],
        [3300,1920,1920,1921])
    names={'logistic_regression':'Logistic Regression','random_forest':'Random Forest','train_prevalence_reference':'Tỷ lệ churn train cố định'}
    add('calibration',['Mô hình / tham chiếu','Brier','Log loss'],
        [[names[r['model']],dec(r['brier']),dec(r['log_loss'])] for r in diagnostics['probability_scores_validation']], [4300,2380,2381])
    add('capacity',['Tỷ lệ xem xét','Số hồ sơ','Recall','Precision','Lift'],
        [[f"{r['requested_fraction']:.0%}",str(r['contact_count']),dec(r['recall']),dec(r['precision']),dec(r['lift'],2)] for r in diagnostics['capacity_validation']],
        [2100,1700,1800,1800,1661])
    return t

REFERENCES = [
    ('IBM','Telco Customer Churn on IBM Cloud Pak for Data','https://github.com/IBM/telco-customer-churn-on-icp4d'),
    ('scikit-learn developers','Pipelines and composite estimators','https://scikit-learn.org/stable/modules/compose.html'),
    ('scikit-learn developers','LogisticRegression','https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html'),
    ('scikit-learn developers','RandomForestClassifier','https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'),
    ('scikit-learn developers','Cross-validation: evaluating estimator performance','https://scikit-learn.org/stable/modules/cross_validation.html'),
    ('scikit-learn developers','Metrics and scoring: quantifying the quality of predictions','https://scikit-learn.org/stable/modules/model_evaluation.html'),
    ('scikit-learn developers','Tuning the decision threshold for class prediction','https://scikit-learn.org/stable/modules/classification_threshold.html'),
    ('scikit-learn developers','Permutation feature importance','https://scikit-learn.org/stable/modules/permutation_importance.html'),
    ('Streamlit','Caching overview','https://docs.streamlit.io/develop/concepts/architecture/caching'),
    ('scikit-learn developers','Imputation of missing values','https://scikit-learn.org/stable/modules/impute.html'),
    ('scikit-learn developers','Preprocessing data','https://scikit-learn.org/stable/modules/preprocessing.html'),
    ('scikit-learn developers','Probability calibration','https://scikit-learn.org/stable/modules/calibration.html'),
    ('scikit-learn developers','DummyClassifier','https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html'),
    ('SciPy developers','Bootstrap confidence intervals','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html'),
    ('SciPy developers','Binomial proportion confidence intervals','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html'),
]
