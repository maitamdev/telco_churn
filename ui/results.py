"""Màn hình đánh giá và ngưỡng: đọc artifact cố định, không chọn lại mô hình."""
import pandas as pd
import streamlit as st
from src.config import RUN_DIR
from src.records import read_json
from src.evaluation import metrics
from ui.components import heading,panel
from ui.charts import threshold_curve,importance_chart
from ui.diagnostics import render as render_diagnostics

MODEL_LABELS={"baseline":"Dummy · lớp đa số","logistic_regression":"Logistic Regression","random_forest":"Random Forest"}

def confusion(m):
    st.html(f'<div class="confusion"><div></div><small>Dự đoán không churn</small><small>Dự đoán churn</small><small>Thực tế không churn</small><div class="correct"><b>{m["tn"]}</b><span>Đúng âm · TN</span></div><div class="mistake"><b>{m["fp"]}</b><span>Báo động nhầm · FP</span></div><small>Thực tế churn</small><div class="mistake"><b>{m["fn"]}</b><span>Bỏ sót · FN</span></div><div class="correct"><b>{m["tp"]}</b><span>Phát hiện đúng · TP</span></div></div>')

def evaluation(metadata):
    heading("Hiệu quả mô hình")
    rows=read_json(RUN_DIR/"test_metrics.json")["metrics"]
    selected=next(r for r in rows if r["model"]==metadata["selected_model"] and r["operating_point"]=="validation_selected")
    cols=st.columns(4)
    for col,key,label in zip(cols,["precision_churn","recall_churn","f1_churn","roc_auc"],["Precision · churn","Recall · churn","F1 · churn","ROC-AUC"]):
        col.metric(label,f"{selected[key]:.3f}")
    with st.container(border=True):
        panel("So sánh mô hình",tag="TEST · 1.409 hồ sơ")
        table=pd.DataFrame(rows)
        table["Mô hình"]=table.model.map(MODEL_LABELS)
        table["Ngưỡng"]=table.threshold
        table["Thiết lập"]=table.operating_point.map({"native_most_frequent":"Lớp đa số","default_0.5":"Mặc định","validation_selected":"Đã chọn trên validation"})
        for old,new in [("accuracy","Accuracy"),("precision_churn","Precision"),("recall_churn","Recall"),("f1_churn","F1"),("roc_auc","ROC-AUC"),("average_precision","AP")]:
            table[new]=table[old]
        labels=["Accuracy","Precision","Recall","F1","ROC-AUC","AP"]
        st.dataframe(table[["Mô hình","Thiết lập","Ngưỡng",*labels]],hide_index=True,width="stretch",
            column_config={c:st.column_config.NumberColumn(c,format="%.3f") for c in ["Ngưỡng",*labels]})
    left,right=st.columns([1.2,1],gap="medium")
    with left,st.container(border=True):
        panel("Kết quả phân loại",tag=MODEL_LABELS[metadata["selected_model"]])
        confusion(selected)
    with right,st.container(border=True):
        panel("Tổng hợp")
        st.html(f'<div class="insight"><strong>{selected["tp"]}</strong><p>Phát hiện đúng</p></div><div class="insight"><strong>{selected["fp"]}</strong><p>Báo động nhầm</p></div><div class="insight"><strong>{selected["fn"]}</strong><p>Bỏ sót</p></div>')
    with st.container(border=True):
        panel("Chi tiết")
        curves,errors,cv,groups=st.tabs(["ROC & Precision–Recall","Ca dự đoán sai","Cross-validation","Theo nhóm khách"])
        with curves:
            st.image(str(RUN_DIR/"evaluation_curves.png"),width="stretch")
        with errors:
            st.dataframe(pd.read_csv(RUN_DIR/"error_cases.csv"),hide_index=True,width="stretch")
        with cv:
            st.dataframe(pd.read_csv(RUN_DIR/"cv_summary.csv"),hide_index=True,width="stretch")
        with groups:
            st.dataframe(pd.read_csv(RUN_DIR/"subgroup_metrics.csv"),hide_index=True,width="stretch")
    render_diagnostics(metadata)

def threshold(metadata):
    heading("Ngưỡng & giải thích")
    name=metadata["selected_model"]
    val=pd.read_csv(RUN_DIR/"validation_predictions.csv")
    controls,chart=st.columns([1,1.8],gap="medium")
    with controls,st.container(border=True):
        panel("Thử ngưỡng dự đoán")
        st.slider("Ngưỡng minh họa · validation",0.,1.,value=round(metadata["selected_threshold"],3),step=.001,format="%.3f",key="threshold_preview")
        chosen=st.session_state["threshold_preview"]
        m=metrics(val.y_true,val[name+"_probability"],chosen)
        st.caption(f"Ngưỡng đang dùng: {metadata['selected_threshold']:.4f}")
    with chart,st.container(border=True):
        panel("Precision & recall",tag="VALIDATION")
        st.altair_chart(threshold_curve(pd.read_csv(RUN_DIR/(name+"_threshold_sweep.csv")),metadata["selected_threshold"]),width="stretch")
    cols=st.columns(4)
    for col,key,label in zip(cols,["precision_churn","recall_churn","flagged_count","fn"],["Precision","Recall","Khách được đánh dấu","Churn bị bỏ sót"]):
        col.metric(label,f"{m[key]:.1%}" if key in ["precision_churn","recall_churn"] else m[key])
    importance,rules=st.columns([1.4,1],gap="medium")
    with importance,st.container(border=True):
        panel("Độ quan trọng đặc trưng",tag="VALIDATION")
        st.altair_chart(importance_chart(pd.read_csv(RUN_DIR/"permutation_importance_validation.csv")),width="stretch")
    with rules,st.container(border=True):
        panel("Tiêu chí chọn ngưỡng")
        official=metadata["threshold_records"][name]
        st.html('<div class="note-row"><strong>Precision tối thiểu · 50%</strong></div><div class="note-row"><strong>Recall mục tiêu · 80%</strong></div>')
        if official["status"]!="precision_constraint_met":
            st.warning("Chưa đạt ràng buộc precision; dùng ngưỡng fallback 0,5.")
    with st.expander("Ma trận nhầm lẫn tại ngưỡng minh họa"):
        confusion(m)

