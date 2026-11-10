"""Đường dẫn tương đối dự án và schema từ cấu hình đã chốt."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "configs/project_spec.json"
SPEC = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
RAW_PATH = ROOT / "data/raw/Telco-Customer-Churn.csv"
SPLIT_DIR = ROOT / "data/splits"
PREP_DIR = ROOT / "artifacts/preparation"
EDA_DIR = ROOT / "artifacts/eda"
RUN_DIR = ROOT / "artifacts/final_run"
SEED = SPEC["split"]["random_state"]
NUMERIC = SPEC["dataset"]["numeric_features"]
CATEGORICAL = SPEC["dataset"]["categorical_features"]
FEATURES = NUMERIC + CATEGORICAL
INTERNET_ADDONS = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
CATEGORIES = {
    "gender": ["Female", "Male"], "SeniorCitizen": ["0", "1"],
    "Partner": ["No", "Yes"], "Dependents": ["No", "Yes"],
    "PhoneService": ["No", "Yes"], "MultipleLines": ["No", "Yes", "No phone service"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    **{c: ["No", "Yes", "No internet service"] for c in INTERNET_ADDONS},
    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": ["No", "Yes"],
    "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
}
LABELS = {
    "gender": "Giới tính", "SeniorCitizen": "Thuộc nhóm cao tuổi", "Partner": "Có bạn đời",
    "Dependents": "Có người phụ thuộc", "tenure": "Thời gian sử dụng (tháng)",
    "PhoneService": "Dịch vụ điện thoại", "MultipleLines": "Nhiều đường dây",
    "InternetService": "Loại Internet", "OnlineSecurity": "Bảo mật trực tuyến",
    "OnlineBackup": "Sao lưu trực tuyến", "DeviceProtection": "Bảo vệ thiết bị",
    "TechSupport": "Hỗ trợ kỹ thuật", "StreamingTV": "Truyền hình trực tuyến",
    "StreamingMovies": "Phim trực tuyến", "Contract": "Loại hợp đồng",
    "PaperlessBilling": "Hóa đơn điện tử", "PaymentMethod": "Phương thức thanh toán",
    "MonthlyCharges": "Cước tháng (đơn vị gốc)", "TotalCharges": "Tổng cước (đơn vị gốc)",
}
VI_VALUES = {"No": "Không", "Yes": "Có", "Female": "Nữ", "Male": "Nam", "0": "Không", "1": "Có",
             "Month-to-month": "Theo tháng", "One year": "Một năm", "Two year": "Hai năm",
             "No internet service": "Không sử dụng Internet", "No phone service": "Không sử dụng điện thoại",
             "Fiber optic": "Cáp quang", "DSL": "DSL", "Electronic check": "Séc điện tử",
             "Mailed check": "Séc gửi qua bưu điện", "Bank transfer (automatic)": "Chuyển khoản tự động",
             "Credit card (automatic)": "Thẻ tín dụng tự động"}
