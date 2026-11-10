// Run with the bundled Artifact Tool runtime; see docs/HO_SO_BAO_VE.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const ROOT = process.env.TELCO_PROJECT_ROOT;
const SKILL = process.env.TELCO_PRESENTATION_SKILL;
const PYTHON = process.env.TELCO_ARTIFACT_PYTHON;
if (!ROOT || !SKILL || !PYTHON) throw new Error('Missing TELCO_PROJECT_ROOT, TELCO_PRESENTATION_SKILL or TELCO_ARTIFACT_PYTHON');
const BUILD = path.join(ROOT, 'tmp/slides_upgrade');
const FINAL = path.join(ROOT, 'reports/BAO_VE_TELCO_CHURN.pptx');
const { applyPresentationChartFont, finalizePresentation } = await import(pathToFileURL(path.join(SKILL, 'container_tools/artifact_tool_utils.mjs')));
const json = async p => JSON.parse(await fs.readFile(path.join(ROOT, p), 'utf8'));
const metadata = await json('artifacts/final_run/metadata.json');
const diagnostic = await json('artifacts/diagnostics/summary.json');
const evaluation = await json('artifacts/final_run/test_metrics.json');
const cv = await json('artifacts/final_run/cv_summary.json');
const FONT = 'Arial', INK = '#172E28', GREEN = '#176B57', MUTED = '#52665F', PAPER = '#F7F8F5';
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const tableOwners = [], chartOwners = [];
const manifest = [];
const pct = n => (n * 100).toFixed(1).replace('.', ',') + '%';
const num = n => n.toFixed(3).replace('.', ',');
const sources = 'Dữ liệu và mã: https://github.com/maitamdev/telco_churn\nNguồn IBM: https://github.com/IBM/telco-customer-churn-on-icp4d';

function text(slide, value, x, y, w, h, size=28, options={}) {
  const shape = slide.shapes.add({ geometry: 'textbox', position: { left:x, top:y, width:w, height:h },
    fill:'none', line:{fill:'none',width:0} });
  shape.text = value;
  shape.text.style = {typeface:FONT,fontSize:size,color:options.color || INK,bold:options.bold || false};
  return shape;
}
function slide(title, notes='') {
  const s = deck.slides.add(); s.background.fill=PAPER;
  const index=deck.slides.items.length;
  text(s,title,64,42,1152,105,44,{bold:true});
  text(s,String(index).padStart(2,'0'),1160,670,55,28,18,{color:MUTED});
  s.speakerNotes.text=notes+'\n\n'+sources;
  manifest.push({slide:index,title,notes});
  return s;
}
function note(s, value) { text(s,value,68,600,1110,60,21,{color:MUTED}); }
function points(s, values, x=70,y=175,w=1120,step=100) {
  values.forEach((v,i)=>text(s,v,x,y+i*step,w,step-12,30));
}
function table(s, values, widths, top=170, rowHeight=66, size=25) {
  const rows=values.length, columns=values[0].length;
  const t=s.tables.add({rows,columns,left:68,top,width:1140,height:rows*rowHeight,values,columnWidths:widths});
  for(let r=0;r<rows;r++) for(let c=0;c<columns;c++) {
    const cell=t.getCell(r,c);
    cell.fill=r===0?GREEN:(r%2===0?'#EDF1EA':'#FFFFFF');
    cell.text.style={typeface:FONT,fontSize:size,color:r===0?'#FFFFFF':INK,bold:r===0};
  }
  t.borders.assign({fill:'#CAD4CD',width:1,style:'solid'});
  t.cells.block({row:0,column:0,rowCount:rows,columnCount:columns}).assign({margins:{left:12,right:10,top:9,bottom:9}});
  tableOwners.push(deck.slides.items.length);
  return t;
}
function chart(s, type, config) {
  // Round plotted literals to ten decimals so Excel can retain their precision.
  // Full precision remains in the source CSV/JSON artifacts.
  config.series=config.series.map(series=>({...series,
    values:series.values?.map(value=>value===null?null:Number(value.toFixed(10))),
    ...(series.xValues?{xValues:series.xValues.map(value=>Number(value.toFixed(10)))}:{})}));
  const c=s.charts.add(type,{position:{left:70,top:160,width:1120,height:420},chartFill:PAPER,
    hasLegend:false,plotAreaFill:PAPER,...config});
  applyPresentationChartFont(c,{fontFamily:FONT});
  chartOwners.push(deck.slides.items.length);
  return c;
}
const axis={textStyle:{fontSize:21,fill:INK},line:{fill:'#CAD4CD',width:1}};
const rf=evaluation.metrics.find(x=>x.model==='random_forest'&&x.operating_point==='validation_selected');

{
 const s=deck.slides.add();s.background.fill=GREEN;
 text(s,'TELCO\nCUSTOMER CHURN',70,140,1110,205,78,{bold:true,color:'#FFFFFF'});
 text(s,'Dự đoán và sàng lọc khách hàng rời dịch vụ',75,398,1100,84,36,{color:'#FFFFFF'});
 text(s,'Đồ án học phần 04224',75,585,900,40,24,{color:'#E0EBE5'});
 s.speakerNotes.text='Bài toán phân loại trên dữ liệu snapshot IBM. Mục tiêu hỗ trợ xem xét khách hàng có điểm churn cao. Chưa chứng minh dự báo trước một thời hạn tương lai. Giới thiệu tên và vai trò thực tế của các thành viên khi trình bày.\n'+sources;
 manifest.push({slide:1,title:'Telco Customer Churn'});
}
{
 const s=slide('Bài toán và tiêu chí thành công','Nhãn Churn Yes=1. Giải thích vì sao khách hàng bị đánh dấu chỉ là đối tượng cần xem xét. Precision tối thiểu 50% và recall mong muốn 80% là giả định nghiên cứu, không phải ngưỡng do giảng viên hoặc doanh nghiệp xác nhận. Nguồn: configs/project_spec.json.');
 points(s,['Phân loại Churn Yes/No từ 19 thuộc tính khách hàng.','AP trên CV chọn mô hình có khả năng xếp hạng tốt.','Ngưỡng validation ưu tiên recall, với precision tối thiểu 50%.','Test độc lập đánh giá lựa chọn đã cố định.'],70,170,1120,95);
 note(s,'Ứng dụng hỗ trợ sàng lọc. Hiệu quả giữ chân thực tế cần thí nghiệm can thiệp.');
}
{
 const s=slide('Dữ liệu và quyết định làm sạch','Nguồn: data/raw, artifacts/preparation, reports/evidence/data_quality_audit.csv. Không giả định TotalCharges trống nghĩa là 0. Median và missing indicator được fit trong từng fold/train. Ngoại lai hợp lệ được giữ, không cắt theo nhãn.');
 table(s,[['Đặc điểm','Số liệu','Xử lý'],['Hồ sơ / cột','7.043 / 21','19 đầu vào, loại ID và nhãn'],['Churn','1.869 (26,54%)','Stratify khi chia dữ liệu'],['TotalCharges trống','11 (0,156%)','NaN, median trong pipeline'],['ID / dòng trùng','0 / 0','Kiểm tra trước chia tập']],[345,280,515],170,74);
 note(s,'IBM mô tả một công ty viễn thông hư cấu. Nguồn và hash được lưu trong dự án.');
}
{
 const raw=await fs.readFile(path.join(ROOT,'artifacts/eda/02_Contract.csv'),'utf8');
 const records=raw.trim().split(/\r?\n/).slice(1).map(x=>x.split(','));
 const s=slide('Hợp đồng ngắn đi cùng tỷ lệ churn cao','EDA chỉ dùng train. Đây là mối liên hệ quan sát, không phải bằng chứng đổi hợp đồng sẽ gây giảm churn. Nguồn: artifacts/eda/02_Contract.csv.');
 chart(s,'bar',{categories:records.map(r=>({'Month-to-month':'Theo tháng','One year':'Một năm','Two year':'Hai năm'}[r[0]])),
   series:[{name:'Tỷ lệ churn train',values:records.map(r=>Number(r[3])),fill:GREEN}],barOptions:{direction:'column',gapWidth:80},
   yAxis:{...axis,min:0,max:.5,numberFormatCode:'0%',majorGridlines:{fill:'#DCE3DC',width:1}},xAxis:axis,
   dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.0%',textStyle:{fontSize:22,fill:INK}}});
 note(s,'Đọc cùng tenure và các dịch vụ. Không dùng nhãn để loại bỏ các ngoại lai.');
}
{
 const s=slide('Phân hoạch và phòng tránh rò rỉ','Nguồn: data/splits/split_manifest.json và src/preprocessing.py. Trình bày thứ tự: chia trước; fit imputer/scaler/encoder trong CV pipeline; chọn trên train/validation; khóa rồi mở test. Rò rỉ thời gian chưa được loại trừ vì không có lịch sử từng thuộc tính.');
 table(s,[['Tập','Số khách','Vai trò'],['Train','4.225','EDA, CV 5 fold, fit pipeline'],['Validation','1.409','Chọn ngưỡng, phân tích bổ sung'],['Test','1.409','Đánh giá mô hình và ngưỡng đã khóa']],[290,240,610],180,80);
 note(s,'Stratify, seed 42. Không refit train + validation sau khi chọn ngưỡng.');
}
{
 const s=slide('Baseline và hai thuật toán','Nguồn: src/preprocessing.py, configs/project_spec.json. LR dùng sigmoid của tổng tuyến tính, tối ưu log loss có điều chuẩn. RF tổng hợp nhiều cây học từ bootstrap, dùng ngẫu nhiên một tập thuộc tính tại nút. Không cần deep learning để đáp ứng đề tài.');
 table(s,[['Mô hình','Nguyên lý','Cấu hình tìm kiếm'],['Dummy','Luôn dự đoán lớp đa số','Baseline độc lập'],['Logistic Regression','Sigmoid của tổ hợp tuyến tính','8 cấu hình C / class_weight'],['Random Forest','Tổng hợp xác suất từ nhiều cây','18 cấu hình depth / leaf / weight']],[300,470,370],170,80,24);
 note(s,'LR chuẩn hóa biến số. RF không cần scaler. Cả hai dùng cùng hợp đồng đầu vào.');
}
{
 const s=slide('RF có AP CV cao nhất trong thí nghiệm','Nguồn: artifacts/final_run/cv_summary.json. Chênh RF-LR chỉ 0,00475 AP. Độ lệch chuẩn fold không phải khoảng tin cậy, không khẳng định RF luôn tốt hơn. Cấu hình RF: 300 cây, max_depth=None, min_samples_leaf=20, class_weight=balanced.');
 chart(s,'bar',{categories:['Dummy','Logistic Regression','Random Forest'],
  series:[{name:'AP trung bình CV',values:cv.map(r=>r.mean_average_precision),fill:GREEN}],
  barOptions:{direction:'column',gapWidth:80},xAxis:axis,yAxis:{...axis,min:0,max:.8,majorGridlines:{fill:'#DCE3DC',width:1}},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.000',textStyle:{fontSize:23,fill:INK}}});
 note(s,'LR: 0,6678 ± 0,0244. RF: 0,6726 ± 0,0139. Dấu ± là độ lệch chuẩn giữa fold.');
}
{
 const v=metadata.threshold_records.random_forest.validation_metrics;
 const s=slide('Chọn ngưỡng trên validation','Nguồn: selection_record.json và metadata.json. Chọn recall lớn nhất khi precision>=0,50 và có hồ sơ được đánh dấu. Phá hòa bằng precision, rồi ngưỡng cao hơn. Không chọn ngưỡng dựa vào test.');
 text(s,metadata.selected_threshold.toFixed(6).replace('.',','),75,175,1050,100,76,{bold:true,color:GREEN});
 table(s,[['Precision validation','Recall validation','Hồ sơ được đánh dấu'],[pct(v.precision_churn),pct(v.recall_churn),String(v.flagged_count)]],[380,380,380],315,80,29);
 note(s,'Mục tiêu recall 80% là mong muốn của nhóm. Dữ liệu mới có thể cho precision và recall khác.');
}
{
 const labels=['Dummy','LR, t=0,5','LR, t đã chọn','RF, t=0,5','RF, t đã chọn'];
 const s=slide('So sánh trên test ở các ngưỡng cố định','Nguồn: artifacts/final_run/test_metrics.json. Giải thích precision cao của LR mặc định nhưng recall thấp hơn RF ở ngưỡng chính thức. AP không đổi khi chỉ thay ngưỡng. Dữ liệu test không được dùng để chọn lại mô hình.');
 table(s,[['Mô hình','Precision','Recall','F1','AP'],...evaluation.metrics.map((r,i)=>[labels[i],num(r.precision_churn),num(r.recall_churn),num(r.f1_churn),num(r.average_precision)])],[340,200,200,200,200],165,62,24);
 note(s,'Dummy có accuracy 73,46% nhưng recall churn bằng 0. Accuracy đơn độc dễ gây hiểu nhầm.');
}
{
 const s=slide('RF phát hiện 302 trong 374 khách churn','Nguồn: artifacts/final_run/test_metrics.json. Đọc cả 4 ô. 595 hồ sơ được đánh dấu gồm 302 TP và 293 FP. Không nói 302 khách được giữ chân vì chưa có can thiệp.');
 table(s,[['Thực tế / dự đoán','Không churn','Churn'],['Không churn','TN = 742','FP = 293'],['Churn','FN = 72','TP = 302']],[460,340,340],185,96,30);
 note(s,'Ngưỡng chính thức 0,478803. Recall 80,75%, precision 50,76%, F1 62,33%.');
}
{
 const s=slide('Sai số cần đọc theo từng nhóm khách hàng','Nguồn: artifacts/final_run/error_cases.csv, subgroup_metrics.csv. Dự án lưu FP/FN tự tin và sát ngưỡng theo quy tắc, không chọn thủ công ví dụ đẹp. Nhóm hợp đồng hai năm có 9 churn và đều bị bỏ sót; mẫu nhỏ nên không suy rộng kết luận.');
 points(s,['293 báo động nhầm tạo thêm khối lượng xem xét.','72 khách churn bị bỏ sót ở ngưỡng chính thức.','Nhóm hợp đồng hai năm: bỏ sót cả 9 trường hợp churn.','Contract, InternetService, tenure đứng đầu permutation importance.'],70,170,1120,95);
 note(s,'Importance giải thích sự phụ thuộc của mô hình, không chứng minh quan hệ nhân quả.');
}
{
 const names={precision_churn:'Precision',recall_churn:'Recall',average_precision:'AP',ap_difference:'AP của RF trừ LR'};
 const s=slide('Khoảng ước lượng làm rõ mức chắc chắn','Nguồn: artifacts/diagnostics/summary.json. Wilson cho precision/recall. Bootstrap IID ghép cặp 2.000 lần, seed 42, khoảng phân vị 95% cho AP và delta. Khoảng delta dương trong phép đo này nhưng điều kiện trên hai mô hình đã fit; không bao gồm tuning uncertainty, shift hoặc kiểm định đồng thời. Tài liệu: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html');
 table(s,[['Độ đo','Ước lượng','Khoảng 95%'],...Object.entries(names).map(([k,v])=>{const q=diagnostic.test_intervals[k];return[v,num(q.estimate),num(q.lower)+' đến '+num(q.upper)]})],[440,280,420],165,72,25);
 note(s,'Precision quan sát >50% không chứng minh precision trên quần thể luôn đạt 50%.');
}
{
 const s=slide('Chất lượng xác suất khác khả năng xếp hạng','Nguồn: artifacts/diagnostics/probability_scores_validation.csv. LR Brier/log loss thấp hơn RF trên validation, dù RF được chọn bằng CV AP. Brier và log loss không đo riêng calibration. Không hiệu chỉnh hoặc đổi model sau khi xem test. Tài liệu: https://scikit-learn.org/stable/modules/calibration.html');
 table(s,[['Mô hình / tham chiếu','Brier','Log loss'],...diagnostic.probability_scores_validation.map(r=>[
  {logistic_regression:'Logistic Regression',random_forest:'Random Forest',train_prevalence_reference:'Tỷ lệ churn train cố định'}[r.model],num(r.brier),num(r.log_loss)])],[640,250,250],190,80,26);
 note(s,'Validation. Giá trị thấp hơn tốt hơn. Điểm RF hiện tại vẫn là xác suất ước lượng chưa hiệu chỉnh.');
}
{
 const r=diagnostic.capacity_validation;
 const s=slide('20% hồ sơ bao phủ 50,27% churn validation','Nguồn: artifacts/diagnostics/capacity_validation.csv. Top 282 trong 1.409 hồ sơ gồm 188/374 churn, precision 66,67%, lift 2,51. Tie break bằng customerID. Đây là chẩn đoán trên validation, không phải chứng minh giữ chân khách hàng.');
 chart(s,'scatter',{scatterOptions:{style:'lineWithMarkers'},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:20}},
  series:[{name:'Xếp theo điểm RF',xValues:[0,...r.map(x=>x.actual_fraction)],values:[0,...r.map(x=>x.recall)],line:{fill:GREEN,width:3},marker:{symbol:'circle',size:6}},
          {name:'Ngẫu nhiên (kỳ vọng)',xValues:[0,1],values:[0,1],line:{fill:'#8B9690',width:2}}],
  xAxis:{...axis,min:0,max:1,numberFormatCode:'0%',title:'Tỷ lệ hồ sơ được xem xét'},
  yAxis:{...axis,min:0,max:1,numberFormatCode:'0%',title:'Tỷ lệ churn trong danh sách'}});
 note(s,'Lift đo mức tập trung churn quan sát. Chưa có bằng chứng về tác động giữ chân hoặc lợi nhuận.');
}
{
 const s=slide('Demo xử lý cả dữ liệu hợp lệ và dữ liệu lỗi','Mở app local. Chọn mẫu có lỗi: 3 dòng, 1 dự đoán và 2 dòng cần sửa. Tải kết quả. Sau đó đổi dữ liệu để chứng minh kết quả cũ biến mất. Nguồn ảnh: reports/evidence/ui_v2_csv.jpg, phần CSV giữ cùng quy tắc. Các trang hiện tại được kiểm bằng AppTest.');
 s.images.add({blob:await fs.readFile(path.join(ROOT,'reports/evidence/ui_v2_csv.jpg')),contentType:'image/jpeg',alt:'Demo CSV giữ dòng lỗi và trả dự đoán cho dòng hợp lệ',fit:'contain',position:{left:65,top:148,width:840,height:420}});
 text(s,'1 dòng hợp lệ\n2 dòng cần sửa\n\nKhông tạo điểm giả\ncho dòng sai',935,200,285,290,29);
 note(s,'Chạy offline sau khi cài thư viện. Cùng pipeline cho dự đoán cá nhân và CSV.');
}
{
 const s=slide('Bằng chứng kiểm thử và tái lập','Nguồn: reports/evidence/pytest_upgrade.xml, pytest_upgrade_clean.xml, full_reproduction.json, runtime_before.json, runtime_after.json. Phân biệt lần tái huấn luyện ban đầu và lần nâng cấp chẩn đoán hiện tại. 8,7 lần là phép đo cục bộ với mẫu lặp, không phải cam kết nhiều người dùng.');
 points(s,['99 kiểm thử đạt trong hai môi trường Python.','2.818 xác suất validation/test khớp kết quả đã lưu.','CSV 10.000 dòng: khoảng 2,67 giây xuống 0,31 giây.','GitHub Actions kiểm tra tự động khi push và pull request.'],70,170,1120,95);
 note(s,'Hash liên kết dữ liệu, mô hình, lựa chọn ngưỡng và các bằng chứng đánh giá.');
}
{
 const s=slide('Giới hạn và hướng phát triển','Không hứa dự báo trước 30/60/90 ngày. Thử nghiệm tiếp theo cần dữ liệu có mốc thời gian, holdout mới, chi phí và bằng chứng can thiệp. Không chọn thêm thuật toán theo test hiện tại. Nguồn: báo cáo Chương 6, summary.json limitations.');
 points(s,['Snapshot chưa chứng minh dự báo trước một kỳ tương lai.','Chưa hiệu chỉnh xác suất và chưa có dữ liệu can thiệp.','Nhóm hợp đồng dài cần phân tích thêm bằng dữ liệu mới.','Lần nghiên cứu tiếp theo cần thiết kế đánh giá độc lập mới.'],70,170,1120,95);
}
{
 const s=slide('Kết luận','Tóm tắt kết quả có bằng chứng. Các thành viên giải thích phần tự thực hiện và trình bày đầy đủ phạm vi hỗ trợ AI. Không quy số tests hoặc độ chính xác thành điểm môn học.');
 text(s,'Quy trình có đối chứng\nvà demo chạy bằng mô hình thật',72,175,1120,150,52,{bold:true,color:GREEN});
 text(s,'302/374 churn được phát hiện trên test tại ngưỡng đã khóa.',75,370,1110,70,33);
 text(s,'Đánh đổi: 293 báo động nhầm và bất định trên dữ liệu mới.',75,470,1110,70,31);
 note(s,'OpenAI Codex hỗ trợ đáng kể mã và phân tích. Đóng góp tự thực hiện của nhóm cần được ghi nhận trung thực.');
}
{
 const s=slide('Câu hỏi bảo vệ về phương pháp','Dành cho hỏi đáp. Thành viên phải tự diễn giải, chạy và sửa mã. Ví dụ thao tác: đổi dữ liệu hợp đồng trong form, quan sát đầu vào không khớp dịch vụ bị báo lỗi; giải thích tại sao threshold UI không ghi metadata.');
 table(s,[['Câu hỏi','Điểm cần giải thích'],['Tại sao không dùng accuracy?','Dummy accuracy cao nhưng recall bằng 0'],['AP khác ROC-AUC thế nào?','AP tóm tắt precision theo recall, nhạy tỷ lệ lớp'],['Đổi ngưỡng có đổi AP?','Không, AP đánh giá xếp hạng xác suất'],['Tại sao không fit imputer toàn bộ?','Thống kê holdout sẽ rò vào huấn luyện']],[520,620],165,74,25);
}
{
 const s=slide('Truy vết bằng chứng trong mã nguồn','Dành cho hỏi đáp và sửa mã trực tiếp. Mở từng module, không chỉ đọc lời giải thích trên slide. Hướng dẫn thành viên làm bài thực hành trong docs/HO_SO_BAO_VE.md và ghi kết quả thật.');
 table(s,[['Nội dung','Vị trí'],['Schema, dữ liệu lỗi','src/validation.py'],['Tiền xử lý, mô hình','src/preprocessing.py, src/train.py'],['Ngưỡng, đánh giá','src/evaluation.py'],['Khoảng ước lượng, top-k','src/diagnostics.py'],['Đóng gói, kiểm chứng','tests/, tools/package_project.py']],[520,620],160,63,24);
}
{
 const s=slide('Nguồn và ghi nhận hỗ trợ','Tài liệu chính: IBM Telco repository; scikit-learn pipeline, model_evaluation, calibration; SciPy bootstrap và Wilson. Nguồn từng số liệu nằm trong speaker notes từng slide. GitHub: https://github.com/maitamdev/telco_churn. OpenAI Codex hỗ trợ tạo một phần đáng kể mã, kiểm thử, báo cáo và slide. Nhóm cần ghi đóng góp tự thực hiện và đáp ứng yêu cầu liêm chính của học phần.');
 points(s,['IBM Telco Customer Churn: dữ liệu và bối cảnh.','scikit-learn: pipeline, đánh giá, ngưỡng và calibration.','SciPy: bootstrap và khoảng Wilson.','Repository dự án: mã, dữ liệu, artifact và kiểm thử.'],70,165,1120,90);
 note(s,'Nguồn chi tiết trong ghi chú của từng slide và tài liệu tham khảo của báo cáo.');
}

await fs.mkdir(BUILD,{recursive:true});
await fs.writeFile(path.join(BUILD,'slide_manifest.json'),JSON.stringify(manifest,null,2));
for(let i=0;i<deck.slides.items.length;i++) {
 const png=await deck.export({slide:deck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(BUILD,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidatePath=path.join(BUILD,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const finalized=await finalizePresentation({workspaceDir:ROOT,candidatePath,finalPath:FINAL,
 pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',
  ...tableOwners.flatMap(number=>['--require-native-table-slide',String(number)])],
 explicitTotalSlideCount:21,requiredNativeTableOwnerSlides:tableOwners,requiredNativeChartOwnerSlides:chartOwners,
 materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
 receiptPath:path.join(BUILD,'validation.json')});
console.log(JSON.stringify(finalized));
