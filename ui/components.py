"""Các thành phần trình bày dùng chung; không can thiệp mô hình."""
from html import escape
import streamlit as st
from src.config import ROOT

def apply_theme():
    st.html("<style>"+(ROOT/"ui/styles.css").read_text(encoding="utf-8")+"</style>")

def brand():
    st.html('<div class="brand"><div class="brand-mark"><i></i><i></i><i></i></div><div><div class="brand-name">TELCO</div><div class="brand-sub">Customer operations</div></div></div>')

def heading(title):
    st.title(title)

def panel(title,tag=None):
    badge=f'<span class="pill">{escape(tag)}</span>' if tag else ""
    st.html(f'<div class="panel-heading"><h3>{escape(title)}</h3>{badge}</div>')

def kpis(items):
    st.html('<div class="kpi-grid">'+''.join(f'<div class="kpi"><div class="kpi-label">{escape(label)}</div><div class="kpi-value">{escape(str(value))}</div></div>' for label,value in items)+'</div>')

def pill(label,kind=""):
    st.html(f'<span class="pill {escape(kind)}">{escape(label)}</span>')

def empty_result():
    st.html('<div class="empty-state"><div class="empty-mark">—</div><b>Chưa có kết quả</b></div>')

