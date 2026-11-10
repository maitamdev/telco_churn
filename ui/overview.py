"""Bảng tổng quan phục vụ khám phá và mở hồ sơ khách hàng."""
import pandas as pd
import streamlit as st
from src.config import EDA_DIR,PREP_DIR,VI_VALUES
from src.records import read_json
from src.validation import safe_csv_bytes
from ui.components import heading,panel,kpis
from ui.charts import contract_rate,tenure_rate
from ui.data_views import train_customers,filter_customers,prefill_customer

def render(metadata):
    heading("Tổng quan khách hàng")
    profile=read_json(PREP_DIR/"data_profile.json")
    train=train_customers()
    count=profile["label_counts"]["Yes"]
    kpis([
        ("Tổng hồ sơ",f"{profile['rows']:,}".replace(",",".")),
        ("Khách đã rời bỏ",f"{count:,}".replace(",",".")),
        ("Hồ sơ train",f"{len(train):,}".replace(",",".")),
        ("Cước trung vị · train",f"{pd.to_numeric(train.MonthlyCharges).median():.2f}".replace(".",",")),
    ])
    left,right=st.columns([1.08,1],gap="medium")
    with left,st.container(border=True):
        panel("Rời bỏ theo hợp đồng",tag="TRAIN")
        st.altair_chart(contract_rate(train),width="stretch")
    with right,st.container(border=True):
        panel("Rời bỏ theo thâm niên",tag="TRAIN")
        st.altair_chart(tenure_rate(train),width="stretch")
    with st.container(border=True):
        panel("Hồ sơ khách hàng")
        a,b,c=st.columns([1.6,1,1])
        query=a.text_input("Tìm mã khách hàng",placeholder="Mã khách hàng",key="customer_search")
        contract=b.selectbox("Hợp đồng",["Tất cả","Month-to-month","One year","Two year"],format_func=lambda x:VI_VALUES.get(x,x),key="customer_contract")
        status=c.selectbox("Trạng thái thực tế",["Tất cả","Yes","No"],format_func=lambda x:{"Tất cả":"Tất cả","Yes":"Đã rời bỏ","No":"Đang sử dụng"}[x],key="customer_status")
        filtered=filter_customers(train,query,contract,status)
        preview=filtered.head(50)
        if preview.empty:
            st.info("Không có hồ sơ phù hợp.")
        else:
            table=preview[["customerID","Contract","tenure","MonthlyCharges","Churn"]].copy()
            table["Contract"]=table.Contract.map(VI_VALUES)
            table["tenure"]=pd.to_numeric(table.tenure)
            table["MonthlyCharges"]=pd.to_numeric(table.MonthlyCharges)
            table["Churn"]=table.Churn.map({"Yes":"Đã rời bỏ","No":"Đang sử dụng"})
            selection=st.dataframe(table,hide_index=True,width="stretch",height=248,
                column_config={"customerID":"Mã khách hàng","Contract":"Hợp đồng",
                    "tenure":st.column_config.NumberColumn("Thâm niên",format="%d tháng"),
                    "MonthlyCharges":st.column_config.NumberColumn("Cước tháng",format="%.2f"),
                    "Churn":"Trạng thái thực tế"},on_select="rerun",selection_mode="single-row",key="customer_table")
            selected=[i for i in selection.selection.rows if 0 <= i < len(preview)]
            action,download=st.columns([1.4,1])
            record=preview.iloc[selected[0]].to_dict() if selected else None
            action.button("Phân tích hồ sơ",type="primary",disabled=record is None,on_click=prefill_customer,args=(record,),icon=":material/arrow_forward:")
            download.download_button("Xuất danh sách đã lọc",safe_csv_bytes(filtered),"telco_filtered_train.csv","text/csv",icon=":material/download:")
        st.caption(f"{min(50,len(filtered))} / {len(filtered):,} hồ sơ")
    with st.expander("Biểu đồ khác"):
        names={"Phân bố nhãn":"01_class_balance","Loại hợp đồng":"02_Contract","Dịch vụ Internet":"03_InternetService","Phương thức thanh toán":"04_PaymentMethod","Thời gian sử dụng":"05_tenure","Cước tháng":"06_MonthlyCharges","Tổng cước":"07_TotalCharges","Tương quan":"08_correlation"}
        chosen=st.selectbox("Biểu đồ",list(names))
        st.image(str(EDA_DIR/(names[chosen]+".png")),width="stretch")

