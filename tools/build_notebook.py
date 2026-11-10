"""Tạo và thực thi notebook bằng đúng Python đang chạy script."""
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from src.config import ROOT
from src.records import write_json,now,environment

def build():
    nb=nbformat.v4.new_notebook()
    md=nbformat.v4.new_markdown_cell
    code=nbformat.v4.new_code_cell
    nb.cells=[
        md("# Đề tài 01 · Telco Customer Churn\n\nNotebook bằng chứng thực nghiệm, không phải báo cáo nộp cuối. Tất cả đầu ra được thực thi từ dữ liệu/artifact thật. Không tuning lại theo test. Có hỗ trợ OpenAI Codex; nhóm cần đọc, sửa và tự kiểm chứng."),
        md("## 1. Bài toán và nguồn\n\nPhân loại Churn: Yes=1, No=0. Dữ liệu mẫu IBM của công ty hư cấu. Câu hỏi: mức mất cân bằng; các yếu tố liên quan; mức cải thiện so với baseline; đánh đổi precision/recall. Nguồn và hash ở preparation/provenance.json. Snapshot không chứng minh dự báo trước một khoảng thời gian."),
        code("from pathlib import Path\nimport sys\nroot=Path.cwd()\nif root.name=='notebooks': root=root.parent\nsys.path.insert(0,str(root))\nimport pandas as pd\nfrom IPython.display import display,Image,Markdown\nfrom src.config import ROOT,PREP_DIR,EDA_DIR,RUN_DIR,FEATURES,NUMERIC\nfrom src.records import read_json\nfrom src.data import load_partition\nfrom src.inference import load_bundle\nprint('Python:',sys.executable)\nprofile=read_json(PREP_DIR/'data_profile.json')\ndisplay(pd.DataFrame({'Giá trị':[profile['rows'],profile['columns'],profile['unique_ids'],profile['missing_blank']['TotalCharges']]},index=['Dòng','Cột','ID duy nhất','TotalCharges thiếu']))"),
        md("## 2. Chia tập và tiền xử lý\n\n4.225 train / 1.409 validation / 1.409 test, stratify seed 42. Normalizer không học thống kê → ColumnTransformer → model. Median/scaler/one-hot fit bên trong từng fold. Giữ các danh mục không dùng dịch vụ; ID và target không làm đặc trưng."),
        code("train=load_partition('train')\nprint('Train:',train.shape)\ndisplay(train.head())\npipeline,metadata=load_bundle()\ndisplay(pipeline)\nprint('Median chỉ học từ train:',pipeline['preprocess'].named_transformers_['numeric']['imputer'].statistics_)"),
        md("## 3. EDA chỉ trên train\n\nTám hình có CSV nguồn; không dùng biểu đồ test để quyết định mô hình."),
        code("for image in sorted(EDA_DIR.glob('*.png')):\n    display(Image(filename=str(image),width=750))\ndisplay(Markdown((EDA_DIR/'NHAN_XET_EDA.md').read_text(encoding='utf-8')))"),
        md("## 4. CV và khóa lựa chọn\n\nDummy most_frequent; LR: 8 cấu hình; RF: 18 cấu hình × 5 folds. Chọn theo AP trung bình; std phá hòa. Tối đa recall với precision≥0,50 trên validation. Recall≥0,80 là mục tiêu nhóm. Selection record được ghi trước đọc test."),
        code("display(pd.read_csv(RUN_DIR/'cv_summary.csv'))\nselection=read_json(RUN_DIR/'selection_record.json')\nprint('Chọn:',selection['selected_model'])\nprint('Ngưỡng:',selection['selected_threshold'])\nprint('Khóa trước test:',selection['frozen_at'],'; mở test:',metadata['test_opened_at'])\ndisplay(pd.DataFrame([metadata['threshold_records'][metadata['selected_model']]['validation_metrics']]))"),
        md("## 5. Đánh giá và giải thích\n\nCác số test dưới đây chỉ dùng mô tả kết quả. AP khác PR-AUC hình thang. Permutation importance dùng validation; không suy ra nhân quả."),
        code("display(pd.read_csv(RUN_DIR/'test_metrics.csv'))\nfor name in ['evaluation_confusion','evaluation_curves','evaluation_threshold','evaluation_importance']:\n    display(Image(filename=str(RUN_DIR/(name+'.png')),width=850))\ndisplay(pd.read_csv(RUN_DIR/'error_cases.csv'))"),
        md("## 6. Giới hạn và nội dung để bảo vệ\n\nXác suất chưa calibration; chưa có chi phí nghiệp vụ; dữ liệu mẫu không chứng minh tính khái quát ngoài mẫu. Nhóm cần giải thích leakage, split, pipeline, CV, class_weight, threshold, FP/FN, importance và AI usage."),
        code("display(Markdown((ROOT/'reports/PHAN_TICH_KET_QUA.md').read_text(encoding='utf-8')))"),
    ]
    nb.metadata={"kernelspec":{"display_name":"Python 3 (Telco environment)","language":"python","name":"python3"},"language_info":{"name":"python","version":sys.version.split()[0]}}
    path=ROOT/"notebooks/01_telco_churn.ipynb"
    nbformat.write(nb,path)
    manager=KernelManager(kernel_name="python3")
    manager.kernel_spec.argv=[sys.executable,"-m","ipykernel_launcher","-f","{connection_file}"]
    client=NotebookClient(nb,km=manager,timeout=180,resources={"metadata":{"path":str(ROOT)}})
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    nbformat.write(nb,path)
    code_cells=[cell for cell in nb.cells if cell.cell_type=="code"]
    if any(cell.execution_count is None for cell in code_cells):
        raise RuntimeError("Notebook chưa chạy hết.")
    write_json(ROOT/"reports/evidence/notebook_execution.json",{"time":now(),"python":sys.executable,"code_cells":len(code_cells),"all_executed":True,"environment":environment()})
    print("Notebook executed: "+str(len(code_cells))+" code cells.",flush=True)

if __name__=="__main__":
    build()

