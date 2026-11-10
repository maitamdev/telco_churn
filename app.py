"""TELCO Customer Operations. Start: python -m streamlit run app.py."""
import streamlit as st
from src.config import ROOT,RUN_DIR,RAW_PATH,SPEC_PATH,SPLIT_DIR
from src.records import sha256
from src.inference import load_bundle,ArtifactError
from ui import overview,scoring,results
from ui.components import apply_theme,brand

st.set_page_config(page_title="TELCO · Customer Operations",page_icon=":material/analytics:",layout="wide",initial_sidebar_state="expanded")
apply_theme()
PAGES={"Tổng quan":"Tổng quan","Một khách hàng":"Phân tích khách hàng","Dự đoán CSV":"Nhập danh sách","Đánh giá":"Hiệu quả mô hình","Ngưỡng & giải thích":"Ngưỡng & giải thích"}

def bundle_fingerprint():
    paths=[*RUN_DIR.glob("*"),RAW_PATH,SPEC_PATH,*SPLIT_DIR.glob("*")]
    return tuple((str(p.relative_to(ROOT)),sha256(p)) for p in sorted(paths) if p.is_file())

@st.cache_resource(show_spinner="Đang tải…",max_entries=1)
def cached_bundle(fingerprint):
    return load_bundle()

with st.sidebar:
    brand()
    page=st.radio("Chức năng",list(PAGES),format_func=PAGES.get,key="navigation",label_visibility="collapsed")
try:
    pipeline,metadata=cached_bundle(bundle_fingerprint())
except (ArtifactError,OSError) as exc:
    st.error(str(exc))
    st.info("Kiểm tra bộ dữ liệu và mô hình theo hướng dẫn README.")
    st.stop()
if page=="Tổng quan":
    overview.render(metadata)
elif page=="Một khách hàng":
    scoring.single(pipeline,metadata)
elif page=="Dự đoán CSV":
    scoring.batch(pipeline,metadata)
elif page=="Đánh giá":
    results.evaluation(metadata)
else:
    results.threshold(metadata)

