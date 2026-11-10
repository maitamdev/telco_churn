"""Dữ liệu hiển thị và chuyển hồ sơ sang form; không fit lại mô hình."""
import pandas as pd
import streamlit as st
from src.config import CATEGORICAL
from src.data import load_partition

@st.cache_data
def train_customers():
    return load_partition("train")

def filter_customers(frame,query="",contract="Tất cả",status="Tất cả"):
    keep=pd.Series(True,index=frame.index)
    if query.strip():
        keep &= frame.customerID.str.contains(query.strip(),case=False,regex=False)
    if contract!="Tất cả":
        keep &= frame.Contract.eq(contract)
    if status!="Tất cả":
        keep &= frame.Churn.eq(status)
    return frame.loc[keep].copy()

def prefill_customer(row):
    """Callback runs before rerender, so navigation/widget state can be set safely."""
    for c in CATEGORICAL:
        st.session_state["single_"+c]=str(row[c])
    st.session_state["single_tenure"]=int(row["tenure"])
    st.session_state["single_monthly"]=float(row["MonthlyCharges"])
    raw=str(row["TotalCharges"]).strip()
    st.session_state["single_total"]=float(raw) if raw else 0.
    st.session_state["single_total_missing"]=not bool(raw)
    st.session_state["single_customer_id"]=str(row.get("customerID",""))
    st.session_state.pop("single_result",None)
    st.session_state["navigation"]="Một khách hàng"

