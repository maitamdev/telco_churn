"""Biểu đồ tương tác từ tập train và artifact đã khóa."""
import altair as alt
import pandas as pd
TEAL="#287b64"
MUTED="#b8cec1"
AMBER="#b7854d"

def style(chart):
    return chart.configure_view(stroke=None).configure_axis(
        labelFont="Segoe UI",titleFont="Segoe UI",labelFontSize=10,titleFontSize=10,
        labelColor="#7f8d84",titleColor="#829088",domain=False,ticks=False,
        gridColor="#edf1ee",titlePadding=12,labelPadding=7,
    ).configure_legend(labelFont="Segoe UI",titleFont="Segoe UI",labelFontSize=10,title=None)

def contract_rate(frame):
    groups=frame.assign(flag=frame.Churn.eq("Yes").astype(int)).groupby("Contract",observed=True).agg(rate=("flag","mean"),count=("flag","size")).reset_index()
    groups["contract"]=groups.Contract.map({"Month-to-month":"Theo tháng","One year":"Một năm","Two year":"Hai năm"})
    order=["Theo tháng","Một năm","Hai năm"]
    base=alt.Chart(groups).encode(y=alt.Y("contract:N",sort=order,title=None,axis=alt.Axis(labelLimit=110)),
        x=alt.X("rate:Q",scale=alt.Scale(domain=[0,.60]),title=None,axis=alt.Axis(format=".0%",tickCount=4)),
        tooltip=[alt.Tooltip("contract:N",title="Hợp đồng"),alt.Tooltip("rate:Q",format=".1%",title="Tỷ lệ churn"),alt.Tooltip("count:Q",title="Số khách")])
    bars=base.mark_bar(size=26,cornerRadiusEnd=3).encode(color=alt.condition(alt.datum.contract=="Theo tháng",alt.value(TEAL),alt.value(MUTED)))
    labels=base.mark_text(align="left",dx=9,fontSize=12,color="#526959").encode(text=alt.Text("rate:Q",format=".1%"))
    return style((bars+labels).properties(height=190))

def tenure_rate(frame):
    data=frame.assign(months=pd.to_numeric(frame.tenure),flag=frame.Churn.eq("Yes").astype(int))
    order=["0–12","13–24","25–36","37–48","49–60","61–72"]
    data["period"]=pd.cut(data.months,[-1,12,24,36,48,60,72],labels=order)
    grouped=data.groupby("period",observed=True).agg(rate=("flag","mean"),count=("flag","size")).reset_index()
    grouped["period"]=grouped.period.astype(str)
    chart=alt.Chart(grouped).mark_line(color=TEAL,strokeWidth=2.5,point=alt.OverlayMarkDef(size=42,filled=True,fill=TEAL)).encode(
        x=alt.X("period:N",sort=order,title="Thời gian sử dụng (tháng)",axis=alt.Axis(labelAngle=0)),
        y=alt.Y("rate:Q",title=None,scale=alt.Scale(domain=[0,.6]),axis=alt.Axis(format=".0%",tickCount=4)),
        tooltip=[alt.Tooltip("period:N",title="Tháng"),alt.Tooltip("rate:Q",format=".1%",title="Tỷ lệ churn"),alt.Tooltip("count:Q",title="Số khách")])
    return style(chart.properties(height=190))

def threshold_curve(sweep,official):
    data=sweep[["threshold","precision_churn","recall_churn"]].melt("threshold",var_name="metric",value_name="value")
    data["metric"]=data.metric.map({"precision_churn":"Precision","recall_churn":"Recall"})
    line=alt.Chart(data).mark_line(strokeWidth=2).encode(x=alt.X("threshold:Q",title="Ngưỡng dự đoán",scale=alt.Scale(domain=[0,1])),
        y=alt.Y("value:Q",title=None,axis=alt.Axis(format=".0%"),scale=alt.Scale(domain=[0,1])),
        color=alt.Color("metric:N",scale=alt.Scale(domain=["Precision","Recall"],range=[TEAL,AMBER]),legend=alt.Legend(orient="top")),
        tooltip=[alt.Tooltip("threshold:Q",format=".3f",title="Ngưỡng"),alt.Tooltip("metric:N",title="Chỉ số"),alt.Tooltip("value:Q",format=".1%",title="Giá trị")])
    rule=alt.Chart(pd.DataFrame({"threshold":[official]})).mark_rule(color="#9aa69f",strokeDash=[4,4]).encode(x="threshold:Q")
    return style((line+rule).properties(height=245))

def importance_chart(frame):
    data=frame.head(10).copy()
    chart=alt.Chart(data).mark_bar(color=TEAL,size=15,cornerRadiusEnd=2).encode(
        x=alt.X("importance_mean:Q",title="Mức giảm Average Precision",axis=alt.Axis(format=".2f")),
        y=alt.Y("feature:N",sort="-x",title=None),
        tooltip=[alt.Tooltip("feature:N",title="Đặc trưng"),alt.Tooltip("importance_mean:Q",format=".4f",title="Mean"),alt.Tooltip("importance_std:Q",format=".4f",title="Std")])
    return style(chart.properties(height=270))

