"""Nhập hồ sơ và danh sách CSV; giao diện dùng pipeline đã khóa."""
import hashlib
import json
import pandas as pd
import streamlit as st
from src.config import ROOT,CATEGORIES,LABELS,VI_VALUES,INTERNET_ADDONS
from src.validation import InputError,read_csv_bytes,safe_csv_bytes
from src.inference import predict_batch,ArtifactError
from ui.components import heading,panel,pill,empty_result


def request_signature(payload,metadata):
    """Bind displayed results to both the input and the model operating point."""
    model=json.dumps({key:metadata[key] for key in
                      ("run_id","pipeline_sha256","selected_threshold")},sort_keys=True).encode()
    return hashlib.sha256(model+b"\0"+payload).hexdigest()

def category(c,options=None,disabled=False):
    return st.selectbox(LABELS[c],options or CATEGORIES[c],format_func=lambda x:VI_VALUES.get(x,x),key="single_"+c,disabled=disabled)

def single(pipeline,metadata):
    heading("Phân tích khách hàng")
    form,result_panel=st.columns([2,1],gap="medium")
    with form,st.container(border=True):
        panel("Thông tin khách hàng")
        identity,services,billing=st.tabs(["Hồ sơ","Dịch vụ","Thanh toán"])
        with identity:
            customer_id=st.text_input("Mã khách hàng (tùy chọn)",value="DEMO-001",key="single_customer_id")
            values={}
            a,b=st.columns(2)
            with a:
                for c in ["gender","Partner"]:
                    values[c]=category(c)
                values["tenure"]=st.number_input(LABELS["tenure"],min_value=0,value=12,step=1,key="single_tenure")
            with b:
                for c in ["SeniorCitizen","Dependents"]:
                    values[c]=category(c)
        with services:
            a,b=st.columns(2)
            with a:
                values["PhoneService"]=category("PhoneService")
            with b:
                values["InternetService"]=category("InternetService")
            phone,internet=values["PhoneService"],values["InternetService"]
            a,b=st.columns(2)
            with a:
                values["MultipleLines"]=category("MultipleLines",["No phone service"] if phone=="No" else ["No","Yes"],disabled=phone=="No")
                for c in INTERNET_ADDONS[:3]:
                    values[c]=category(c,["No internet service"] if internet=="No" else ["No","Yes"],disabled=internet=="No")
            with b:
                for c in INTERNET_ADDONS[3:]:
                    values[c]=category(c,["No internet service"] if internet=="No" else ["No","Yes"],disabled=internet=="No")
        with billing:
            a,b=st.columns(2)
            with a:
                for c in ["Contract","PaymentMethod"]:
                    values[c]=category(c)
            with b:
                values["PaperlessBilling"]=category("PaperlessBilling")
                values["MonthlyCharges"]=st.number_input(LABELS["MonthlyCharges"],min_value=0.,value=70.,step=5.,format="%.2f",key="single_monthly")
            missing=st.checkbox("Chưa có tổng cước",key="single_total_missing")
            total=st.number_input(LABELS["TotalCharges"],min_value=0.,value=840.,step=50.,format="%.2f",disabled=missing,key="single_total")
            values["TotalCharges"]="" if missing else total
        st.divider()
        submitted=st.button("Dự đoán khách hàng",type="primary",width="stretch",icon=":material/analytics:")
    record={"customerID":customer_id,**values}
    signature=request_signature(json.dumps(record,sort_keys=True).encode(),metadata)
    if st.session_state.get("single_signature")!=signature:
        st.session_state.pop("single_result",None)
    if submitted:
        frame=pd.DataFrame([record])
        try:
            result,_=predict_batch(frame,pipeline,metadata)
            st.session_state["single_result"]=result.iloc[0].to_dict()
            st.session_state["single_signature"]=signature
        except (InputError,ArtifactError,ValueError) as exc:
            st.session_state.pop("single_result",None)
            st.error(str(exc))
    with result_panel,st.container(border=True):
        panel("Kết quả gần nhất")
        r=st.session_state.get("single_result")
        if r is None:
            empty_result()
        elif r["prediction_status"]!="ok":
            st.error(r["validation_errors"])
        else:
            flagged=r["predicted_churn"]=="Yes"
            pill("Cần xem xét" if flagged else "Chưa đánh dấu","warn" if flagged else "good")
            st.caption("Hồ sơ: "+str(r.get("customerID") or "Chưa đặt mã"))
            st.metric("Xác suất churn ước lượng",f"{r['estimated_churn_probability']:.1%}")
            st.progress(float(r["estimated_churn_probability"]))
            st.metric("Ngưỡng chính thức",f"{r['threshold_used']:.4f}")
            if r["range_warnings"]:
                st.warning(r["range_warnings"])

def batch(pipeline,metadata):
    heading("Nhập danh sách khách hàng")
    upload_panel,guide=st.columns([1.65,1],gap="medium")
    with upload_panel,st.container(border=True):
        panel("Danh sách khách hàng")
        source=st.radio("Nguồn dữ liệu",["Tải CSV của bạn","Mẫu hợp lệ","Mẫu có lỗi"],horizontal=True,label_visibility="collapsed")
        if source=="Tải CSV của bạn":
            upload=st.file_uploader("Tải danh sách CSV",type=["csv"],max_upload_size=10)
            payload=upload.getvalue() if upload else None
        else:
            filename="valid_customers.csv" if source=="Mẫu hợp lệ" else "mixed_valid_invalid.csv"
            payload=(ROOT/"data/samples"/filename).read_bytes()
        signature=request_signature(payload,metadata) if payload else None
        if st.session_state.get("batch_signature")!=signature:
            st.session_state.pop("batch_result",None)
        requested=st.button("Dự đoán CSV",type="primary",disabled=payload is None,icon=":material/analytics:")
    with guide,st.container(border=True):
        panel("Tệp mẫu")
        st.caption("CSV UTF-8 · Tối đa 10.000 dòng")
        st.download_button("Tải mẫu cột CSV",(ROOT/"data/samples/template.csv").read_bytes(),"telco_template.csv","text/csv",icon=":material/download:")
        st.download_button("Tải 8 khách mẫu hợp lệ",(ROOT/"data/samples/valid_customers.csv").read_bytes(),"telco_sample.csv","text/csv",icon=":material/download:")
    if requested:
        try:
            frame=read_csv_bytes(payload)
            result,extra=predict_batch(frame,pipeline,metadata)
            st.session_state["batch_result"]=result
            st.session_state["batch_extra"]=extra
            st.session_state["batch_signature"]=signature
        except (InputError,ArtifactError,ValueError) as exc:
            st.session_state.pop("batch_result",None)
            st.error(str(exc))
    if "batch_result" in st.session_state:
        result=st.session_state["batch_result"]
        valid=result.prediction_status.eq("ok")
        a,b,c=st.columns(3)
        a.metric("Tổng dòng",len(result))
        b.metric("Đã dự đoán",int(valid.sum()))
        c.metric("Dòng cần sửa",int((~valid).sum()))
        with st.container(border=True):
            panel("Kết quả")
            if (~valid).any():
                st.warning("Có dòng cần sửa. Xem cột Chi tiết lỗi trong bảng kết quả.")
            extra=[x for x in st.session_state.get("batch_extra",[]) if x!="customerID"]
            if extra:
                st.caption("Bỏ qua cột: "+", ".join(extra))
            view=pd.DataFrame({"Dòng":result.row_number,"Mã khách":result.customerID if "customerID" in result else "",
                "Kiểm tra":result.prediction_status.map({"ok":"Hợp lệ","invalid":"Cần sửa"}),
                "Rủi ro (%)":result.estimated_churn_probability*100,
                "Đề xuất":result.predicted_churn.map({"Yes":"Xem xét","No":"Chưa đánh dấu","":""}),
                "Chi tiết lỗi":result.validation_errors,"Lưu ý":result.range_warnings})
            st.dataframe(view,hide_index=True,width="stretch",
                column_config={"Rủi ro (%)":st.column_config.ProgressColumn("Rủi ro (%)",min_value=0,max_value=100,format="%.1f%%")})
            st.download_button("Tải toàn bộ kết quả",safe_csv_bytes(result),"telco_predictions.csv","text/csv",icon=":material/download:")
            with st.expander("Dữ liệu đầy đủ"):
                st.dataframe(result,hide_index=True,width="stretch")

