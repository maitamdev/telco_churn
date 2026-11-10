"""EDA chỉ dùng train; lưu cả hình, bảng nguồn và nhận xét định lượng."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from .config import ROOT, EDA_DIR, NUMERIC
from .data import load_partition
from .validation import normalize_features
from .records import log_step, write_json

sns.set_theme(style="whitegrid", palette=["#2563eb", "#ea580c"], font="DejaVu Sans")
plt.rcParams.update({"figure.dpi": 120, "savefig.dpi": 180, "axes.titleweight": "bold"})

def save(fig, name):
    fig.savefig(EDA_DIR / f"{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)

def run():
    EDA_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_partition("train")
    x = normalize_features(raw)
    x["Churn"] = raw.Churn
    x["churn_flag"] = raw.Churn.eq("Yes").astype(int)
    notes = []
    counts = x.Churn.value_counts().reindex(["No","Yes"])
    counts.rename("count").to_csv(EDA_DIR/"01_class_balance.csv")
    fig, ax = plt.subplots(figsize=(8,4))
    bars = ax.bar(["Không rời bỏ", "Rời bỏ"], counts, color=["#2563eb","#ea580c"])
    ax.bar_label(bars, labels=[f"{v:,} ({v/len(x):.1%})" for v in counts], padding=5)
    ax.set(title="01 · Phân bố nhãn — chỉ tập train", ylabel="Số khách hàng", ylim=(0,counts.max()*1.18))
    save(fig,"01_class_balance")
    notes.append(f"Tập train có {len(x):,} khách; churn {counts['Yes']:,} ({counts['Yes']/len(x):.2%}). Accuracy cần so với tỷ lệ lớp đa số {counts['No']/len(x):.2%}.")

    for index, col in [(2,"Contract"),(3,"InternetService"),(4,"PaymentMethod")]:
        group = x.groupby(col, observed=True).agg(n=("churn_flag","size"),churn=("churn_flag","sum"),rate=("churn_flag","mean")).sort_values("rate",ascending=False)
        group.to_csv(EDA_DIR/f"{index:02d}_{col}.csv")
        fig, ax = plt.subplots(figsize=(9,4.8))
        bars=ax.barh(group.index,group.rate*100,color="#2563eb")
        ax.bar_label(bars,labels=[f"{r:.1%} · n={n}" for r,n in zip(group.rate,group.n)],padding=5,fontsize=9)
        ax.invert_yaxis()
        ax.set(title=f"{index:02d} · Tỷ lệ churn theo {col} — train",xlabel="Tỷ lệ churn (%)",xlim=(0,max(65,group.rate.max()*135)))
        save(fig,f"{index:02d}_{col}")
        first,last=group.iloc[0],group.iloc[-1]
        notes.append(f"{col}: nhóm {group.index[0]} có tỷ lệ churn {first.rate:.2%} (n={int(first.n)}), so với {last.rate:.2%} (n={int(last.n)}) ở {group.index[-1]}. Đây là tương quan, không chứng minh nguyên nhân.")

    summary=x.groupby("Churn",observed=True)[NUMERIC].agg(["count","mean","median","std","min","max"])
    summary.to_csv(EDA_DIR/"numeric_summary.csv")
    for index,col,bins in [(5,"tenure",np.arange(0,79,6)),(6,"MonthlyCharges",np.arange(0,141,10))]:
        fig,ax=plt.subplots(figsize=(8,4.7))
        sns.histplot(data=x,x=col,hue="Churn",bins=bins,stat="density",common_norm=False,element="step",alpha=.22,ax=ax)
        ax.set(title=f"{index:02d} · Phân bố {col} theo nhãn — train",ylabel="Mật độ trong từng lớp",xlabel="Số tháng" if col=="tenure" else "Cước tháng (đơn vị gốc)")
        save(fig,f"{index:02d}_{col}")
        for label in ["No","Yes"]:
            hist,edges=np.histogram(x.loc[x.Churn.eq(label),col].dropna(),bins=bins)
            pd.DataFrame({"left":edges[:-1],"right":edges[1:],"count":hist}).to_csv(EDA_DIR/f"{index:02d}_{col}_{label}.csv",index=False)
        med=x.groupby("Churn")[col].median()
        notes.append(f"Median {col}: churn={med['Yes']:.2f}, không churn={med['No']:.2f}. Các phân bố vẫn chồng lấp; không thể quyết định từ một biến.")

    fig,ax=plt.subplots(figsize=(7,4.8))
    sns.boxplot(data=x,x="Churn",y="TotalCharges",hue="Churn",legend=False,ax=ax,showfliers=True)
    ax.set(title="07 · Tổng cước theo nhãn — train",xlabel="Churn",ylabel="Tổng cước (đơn vị gốc)")
    save(fig,"07_TotalCharges")
    med_total=x.groupby("Churn")["TotalCharges"].median()
    notes.append(f"Median TotalCharges: churn={med_total['Yes']:.2f}, không churn={med_total['No']:.2f} (đơn vị gốc). Tổng cước còn liên quan thời gian sử dụng, không suy ra tổng cước thấp gây churn. Các điểm ngoài râu hộp chưa đủ bằng chứng là dữ liệu sai nên được giữ lại. Train có {int(x.TotalCharges.isna().sum())} TotalCharges thiếu; hình bỏ qua ô thiếu để mô tả, mô hình điền median trong fold/train và không xóa khách.")

    corr=x[NUMERIC+["churn_flag"]].corr()
    corr.to_csv(EDA_DIR/"08_correlation.csv")
    fig,ax=plt.subplots(figsize=(7,5))
    sns.heatmap(corr,annot=True,fmt=".2f",vmin=-1,vmax=1,cmap="coolwarm",square=True,ax=ax)
    ax.set(title="08 · Tương quan Pearson — train")
    save(fig,"08_correlation")
    notes.append(f"tenure–TotalCharges có tương quan Pearson {corr.loc['tenure','TotalCharges']:.3f}; biến liên quan có thể chia sẻ độ quan trọng. Pearson không mô tả đầy đủ quan hệ phi tuyến.")
    (EDA_DIR/"NHAN_XET_EDA.md").write_text("# Nhận xét EDA từ số liệu thật\n\nPhạm vi: train; không dùng validation/test để chọn đặc trưng.\n\n"+"\n\n".join(f"{i+1}. {n}" for i,n in enumerate(notes))+"\n\nKhông suy diễn quan hệ nhân quả từ dữ liệu quan sát. Không thực hiện cắt outlier hoặc xóa đặc trưng theo biểu đồ.\n",encoding="utf-8")
    stats={c:{"min":float(x[c].min()),"max":float(x[c].max()),"median":float(x[c].median())} for c in NUMERIC}
    write_json(EDA_DIR/"numeric_reference.json",{"partition":"train","features":stats})
    log_step("06","Tám biểu đồ EDA",["Tạo 8 biểu đồ có nhãn/trục, chỉ trên train","Lưu CSV số liệu nguồn"],["8 PNG; bảng nhóm, phân phối và thống kê số"],["artifacts/eda/"])
    print("EDA complete: 8 figures and source tables.",flush=True)

if __name__ == "__main__":
    run()

