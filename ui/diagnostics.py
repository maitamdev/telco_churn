"""Evidence for uncertainty, probability reliability and validation capacity."""
import altair as alt
import pandas as pd
import streamlit as st

from src.config import ROOT, RUN_DIR
from src.diagnostics import load_diagnostics, capacity_table
from ui.components import panel

DIRECTORY = ROOT / "artifacts/diagnostics"
LABELS = {"precision_churn": "Precision churn", "recall_churn": "Recall churn",
          "accuracy": "Accuracy", "average_precision": "Average Precision",
          "roc_auc": "ROC-AUC", "f1_churn": "F1 churn", "ap_difference": "Chênh lệch AP: RF − LR"}
MODELS = {"random_forest": "Random Forest", "logistic_regression": "Logistic Regression",
          "train_prevalence_reference": "Xác suất cố định theo tỷ lệ churn train"}


def render(metadata):
    try:
        summary = load_diagnostics(metadata)
    except (OSError, ValueError, KeyError, TypeError):
        st.warning("Chưa thể xác minh đánh giá mở rộng. Kiểm tra bundle hoặc chạy tools.build_diagnostics.")
        return
    with st.container(border=True):
        panel("Độ tin cậy và khả năng sàng lọc")
        uncertainty, calibration, capacity = st.tabs(["Khoảng ước lượng", "Độ tin cậy xác suất", "Năng lực xử lý"])
        with uncertainty:
            rows = [{"Độ đo": LABELS[key], "Ước lượng": value["estimate"],
                     "Cận dưới 95%": value["lower"], "Cận trên 95%": value["upper"]}
                    for key, value in summary["test_intervals"].items()]
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
                column_config={c: st.column_config.NumberColumn(c, format="%.4f")
                               for c in ["Ước lượng", "Cận dưới 95%", "Cận trên 95%"]})
            delta = summary["test_intervals"]["ap_difference"]
            if delta["lower"] <= 0 <= delta["upper"]:
                st.info("Khoảng chênh lệch AP chứa 0: chưa đủ cơ sở khẳng định RF vượt LR một cách chắc chắn.")
            else:
                st.info("Khoảng chênh lệch AP trên test nghiêng về RF trong phép bootstrap ghép cặp này. Kết quả chỉ xét hai mô hình đã fit, không chứng minh RF luôn tốt hơn trên dữ liệu mới.")
            st.caption("Test, mô hình và ngưỡng cố định. Wilson cho tỷ lệ; bootstrap ghép cặp 2.000 lần cho AP, AUC, F1 và chênh lệch AP. Khoảng này không bao gồm biến động huấn luyện hoặc thay đổi dữ liệu tương lai.")
        with calibration:
            frame = pd.read_csv(DIRECTORY / "reliability_validation.csv")
            frame["Mô hình"] = frame.model.map(MODELS)
            points = alt.Chart(frame).mark_line(point=True).encode(
                x=alt.X("mean_probability:Q", title="Xác suất dự đoán trung bình", scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("observed_churn_rate:Q", title="Tỷ lệ churn quan sát", scale=alt.Scale(domain=[0, 1])),
                color=alt.Color("Mô hình:N", scale=alt.Scale(range=["#3976a8", "#176b57"])),
                tooltip=["Mô hình", "n", alt.Tooltip("mean_probability:Q", format=".3f"),
                         alt.Tooltip("observed_churn_rate:Q", format=".3f")])
            ideal = alt.Chart(pd.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(
                color="#888888", strokeDash=[5, 5]).encode(x="x:Q", y="y:Q")
            st.altair_chart((ideal + points).properties(height=300), width="stretch")
            scores = pd.DataFrame(summary["probability_scores_validation"])
            scores.model = scores.model.map(MODELS)
            st.dataframe(scores.rename(columns={"model": "Mô hình", "brier": "Brier", "log_loss": "Log loss"}),
                         hide_index=True, width="stretch")
            st.caption("Validation, 10 khoảng xác suất đều nhau. Brier và log loss càng thấp càng tốt, nhưng không đo riêng calibration. Đường chéo biểu thị hiệu chỉnh lý tưởng; xác suất hiện tại chưa được hiệu chỉnh.")
        with capacity:
            share = st.slider("Tỷ lệ hồ sơ có thể xem xét (%)", 10, 100, 20, 10, key="capacity_preview")
            validation = pd.read_csv(RUN_DIR / "validation_predictions.csv")
            result = capacity_table(validation.y_true, validation[metadata["selected_model"] + "_probability"],
                                    fractions=[share / 100], ids=validation.customerID).iloc[0]
            a, b, c = st.columns(3)
            a.metric("Hồ sơ ưu tiên", int(result.contact_count))
            b.metric("Tỷ lệ churn được bao phủ", f"{result.recall:.1%}")
            c.metric("Lift so với chọn ngẫu nhiên", f"{result.lift:.2f}×")
            st.caption("Khảo sát trên validation, xếp điểm giảm dần; phá hòa bằng customerID. Đây là số khách churn nằm trong danh sách, chưa phải khách được giữ chân. Thanh trượt không thay ngưỡng chính thức.")
