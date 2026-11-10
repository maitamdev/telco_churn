"""Hình đánh giá và phân tích kết quả; không thay đổi mô hình/ngưỡng."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, precision_recall_curve
from .config import RUN_DIR, ROOT
from .records import read_json, write_json, sha256
sns.set_theme(style="whitegrid",font="DejaVu Sans")

def run():
    meta=read_json(RUN_DIR/"metadata.json")
    name=meta["selected_model"]
    threshold=meta["selected_threshold"]
    test=pd.read_csv(RUN_DIR/"test_predictions.csv")
    val=pd.read_csv(RUN_DIR/"validation_predictions.csv")
    rows=read_json(RUN_DIR/"test_metrics.json")["metrics"]
    selected=next(r for r in rows if r["model"]==name and r["operating_point"]=="validation_selected")
    def save(fig,name):
        fig.savefig(RUN_DIR/(name+".png"),dpi=180,bbox_inches="tight",facecolor="white")
        plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,point in zip(axes,["default_0.5","validation_selected"]):
        m=next(r for r in rows if r["model"]==name and r["operating_point"]==point)
        sns.heatmap([[m["tn"],m["fp"]],[m["fn"],m["tp"]]],annot=True,fmt="d",cmap="Blues",cbar=False,
                    xticklabels=["Không churn","Churn"],yticklabels=["Không churn","Churn"],ax=ax)
        ax.set(title=f"Ngưỡng {m['threshold']:.4f} · test",xlabel="Dự đoán",ylabel="Thực tế")
    fig.suptitle(f"Ma trận nhầm lẫn · {name}",fontweight="bold")
    save(fig,"evaluation_confusion")

    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    colors={"baseline":"#64748b","logistic_regression":"#2563eb","random_forest":"#ea580c"}
    for key in colors:
        p=test[key+"_probability"]
        fpr,tpr,_=roc_curve(test.y_true,p)
        precision,recall,_=precision_recall_curve(test.y_true,p)
        metric=next(r for r in rows if r["model"]==key)
        axes[0].plot(fpr,tpr,label=f"{key} · AUC={metric['roc_auc']:.3f}",color=colors[key])
        axes[1].plot(recall,precision,label=f"{key} · AP={metric['average_precision']:.3f}",color=colors[key])
    axes[0].plot([0,1],[0,1],"--",color="#cbd5e1")
    axes[0].set(title="ROC — test",xlabel="Tỷ lệ dương giả (FPR)",ylabel="Tỷ lệ dương thật (TPR)")
    axes[1].set(title="Precision–Recall — test",xlabel="Recall",ylabel="Precision")
    for ax in axes:
        ax.legend(fontsize=8)
        ax.set(xlim=(0,1),ylim=(0,1.03))
    save(fig,"evaluation_curves")

    imp=pd.read_csv(RUN_DIR/"permutation_importance_validation.csv").head(12).sort_values("importance_mean")
    fig,ax=plt.subplots(figsize=(8,5.5))
    ax.barh(imp.feature,imp.importance_mean,xerr=imp.importance_std,color="#2563eb",capsize=3)
    ax.axvline(0,color="#94a3b8",linewidth=1)
    ax.set(title="Permutation importance — validation, 20 lần",xlabel="Mức giảm Average Precision (mean ± std)")
    save(fig,"evaluation_importance")

    sweep=pd.read_csv(RUN_DIR/(name+"_threshold_sweep.csv"))
    fig,ax=plt.subplots(figsize=(8,4.5))
    for col,label,color in [("precision_churn","Precision","#2563eb"),("recall_churn","Recall","#ea580c"),("f1_churn","F1","#059669")]:
        ax.plot(sweep.threshold,sweep[col],label=label,color=color)
    ax.axvline(threshold,linestyle="--",color="#475569",label=f"Đã chọn {threshold:.4f}")
    ax.axhline(.5,linestyle=":",color="#94a3b8")
    ax.set(title="Đánh đổi theo ngưỡng — chỉ validation",xlabel="Ngưỡng",ylabel="Giá trị",xlim=(0,1),ylim=(0,1.04))
    ax.legend()
    save(fig,"evaluation_threshold")
    error=pd.read_csv(RUN_DIR/"error_cases.csv")
    top=imp.sort_values("importance_mean",ascending=False).head(3)
    v=meta["threshold_records"][name]
    text=[
        "# Phân tích kết quả thực nghiệm",
        f"Run: {meta['run_id']}. Mô hình được chọn bằng train CV: **{name}**; test không tham gia lựa chọn.",
        f"Ngưỡng **{threshold:.10f}** chọn trên validation với precision≥0,50, tối đa recall. Đây là giả định nghiệp vụ, chưa có chi phí giữ chân thực.",
        f"Validation: precision={v['validation_metrics']['precision_churn']:.2%}, recall={v['validation_metrics']['recall_churn']:.2%}; mục tiêu recall≥80%: {'đạt' if v['aspirational_recall_met'] else 'chưa đạt'}.",
        f"Test n={selected['n']}: AP={selected['average_precision']:.4f}; ROC-AUC={selected['roc_auc']:.4f}; accuracy={selected['accuracy']:.2%}; precision={selected['precision_churn']:.2%}; recall={selected['recall_churn']:.2%}; F1={selected['f1_churn']:.4f}.",
        f"Test: TP={selected['tp']}, FP={selected['fp']}, FN={selected['fn']}, TN={selected['tn']}. Đánh dấu {selected['flagged_count']} khách để xem xét; không tự động kết luận phải giữ chân.",
        f"FP: {selected['fp']} khách không churn vẫn bị đánh dấu; có thể làm tăng chi phí liên hệ. FN: {selected['fn']} khách churn bị bỏ sót; có thể mất cơ hội hỗ trợ. Chưa có dữ liệu can thiệp để suy ra ROI hay hiệu quả giữ chân.",
        "Ba biến có mean permutation importance lớn nhất trên validation: "+", ".join(f"{r.feature} ({r.importance_mean:.4f} ± {r.importance_std:.4f})" for r in top.itertuples())+". Đo mức phụ thuộc của mô hình, không phải nguyên nhân churn. Std là độ dao động qua 20 lần hoán vị.",
        "Ví dụ lỗi được lấy tự động: mỗi loại FP/FN gồm 3 lỗi xa ngưỡng nhất và 2 gần ngưỡng nhất, loại trùng; không tuyển chọn thủ công để làm đẹp kết quả.",
    ]
    for r in error.itertuples():
        text.append(f"- {r.customerID}: {r.outcome}, xác suất ước lượng={r.probability:.4f}, nhãn={r.Churn}, tenure={r.tenure}, Contract={r.Contract}, InternetService={r.InternetService}. Mẫu này minh họa sai số, không đủ để kết luận nguyên nhân cá nhân.")
    text += [
        "## Giới hạn và hướng phát triển",
        "- Dữ liệu mẫu công ty hư cấu; chưa xác minh khả năng áp dụng cho doanh nghiệp Việt Nam.",
        "- Snapshot không có timestamp, không chứng minh dự báo trước một khoảng thời gian cụ thể; ngẫu nhiên stratified không thay thế validation theo thời gian.",
        "- Xác suất chưa hiệu chỉnh calibration. Ngưỡng có thể lệch khi tỷ lệ churn/chi phí thay đổi; cần validation mới.",
        "- Có nhóm nhân khẩu học; bảng subgroup có cỡ mẫu nhưng chưa chứng minh công bằng hoặc tác động thực tế.",
        "- Chênh lệch CV giữa hai mô hình chỉ là ước lượng trên một split/seed; chưa kiểm định khác biệt thống kê.",
        "- Sau khi xem test, không sửa để tối ưu trên test này. Nếu thay thiết kế, cần thí nghiệm mới và tập đánh giá mới phù hợp.",
        "- Đề xuất hỗ trợ nhóm hợp đồng tháng/tenure thấp chỉ là giả thuyết để kiểm tra bằng thử nghiệm can thiệp có kiểm soát.",
    ]
    (ROOT/"reports/PHAN_TICH_KET_QUA.md").write_text("\n\n".join(text)+"\n",encoding="utf-8")
    write_json(RUN_DIR/"artifact_manifest.json",{p.name:sha256(p) for p in sorted(RUN_DIR.iterdir()) if p.is_file() and p.name!="artifact_manifest.json"})
    print("Evaluation figures and interpretation complete.",flush=True)

if __name__=="__main__":
    run()

