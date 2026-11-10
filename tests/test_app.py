import pytest
from streamlit.testing.v1 import AppTest
from src.config import ROOT,RUN_DIR
from src.records import sha256

def open_page(name):
    app=AppTest.from_file(str(ROOT/"app.py"),default_timeout=30).run()
    app.radio(key="navigation").set_value(name).run()
    assert not app.exception
    return app

@pytest.mark.parametrize("name",["Tổng quan","Một khách hàng","Dự đoán CSV","Đánh giá","Ngưỡng & giải thích"])
def test_all_five_pages_render(name):
    app=open_page(name)
    assert not app.error
    assert app.title

def test_single_form_scores_real_model():
    app=open_page("Một khách hàng")
    next(b for b in app.button if b.label=="Dự đoán khách hàng").click().run()
    assert not app.exception and not app.error
    assert any(m.label=="Xác suất churn ước lượng" for m in app.metric)

def test_form_handles_no_services_and_missing_total():
    app=open_page("Một khách hàng")
    app.selectbox(key="single_PhoneService").set_value("No").run()
    app.selectbox(key="single_InternetService").set_value("No").run()
    app.checkbox[0].check().run()
    next(b for b in app.button if b.label=="Dự đoán khách hàng").click().run()
    assert not app.exception and not app.error

@pytest.mark.parametrize("source,expected", [("Mẫu hợp lệ",["8","8","0"]),("Mẫu có lỗi",["3","1","2"])])
def test_csv_samples_show_correct_counts(source,expected):
    app=open_page("Dự đoán CSV")
    next(r for r in app.radio if r.label=="Nguồn dữ liệu").set_value(source).run()
    next(b for b in app.button if b.label=="Dự đoán CSV").click().run()
    assert not app.exception and not app.error
    assert [m.value for m in app.metric]==expected

def test_playground_cannot_change_official_threshold():
    before=sha256(RUN_DIR/"metadata.json")
    app=open_page("Ngưỡng & giải thích")
    app.slider[0].set_value(.9).run()
    assert not app.exception
    assert sha256(RUN_DIR/"metadata.json")==before
    app.radio(key="navigation").set_value("Một khách hàng").run()
    next(b for b in app.button if b.label=="Dự đoán khách hàng").click().run()
    assert next(m for m in app.metric if m.label=="Ngưỡng chính thức").value=="0.4788"


def test_changing_form_hides_outdated_prediction():
    app=open_page("Một khách hàng")
    next(b for b in app.button if b.label=="Dự đoán khách hàng").click().run()
    assert any(m.label=="Xác suất churn ước lượng" for m in app.metric)
    app.number_input(key="single_tenure").set_value(60).run()
    assert not app.exception and not app.error
    assert not any(m.label=="Xác suất churn ước lượng" for m in app.metric)
    next(b for b in app.button if b.label=="Dự đoán khách hàng").click().run()
    assert any(m.label=="Xác suất churn ước lượng" for m in app.metric)


def test_changing_csv_hides_outdated_prediction():
    app=open_page("Dự đoán CSV")
    source=next(r for r in app.radio if r.label=="Nguồn dữ liệu")
    source.set_value("Mẫu hợp lệ").run()
    next(b for b in app.button if b.label=="Dự đoán CSV").click().run()
    assert [m.value for m in app.metric]==["8","8","0"]
    next(r for r in app.radio if r.label=="Nguồn dữ liệu").set_value("Mẫu có lỗi").run()
    assert not app.exception and not app.metric


def test_model_or_threshold_change_invalidates_result_signature(bundle):
    from ui.scoring import request_signature

    metadata=bundle[1]
    original=request_signature(b"same customer",metadata)
    assert original!=request_signature(b"same customer",{**metadata,"selected_threshold":.9})
    assert original!=request_signature(b"same customer",{**metadata,"pipeline_sha256":"new model"})


def test_capacity_preview_changes_workload_without_changing_model():
    before=sha256(RUN_DIR/"metadata.json")
    app=open_page("Đánh giá")
    initial=next(m for m in app.metric if m.label=="Hồ sơ ưu tiên").value
    app.slider(key="capacity_preview").set_value(50).run()
    assert not app.exception and not app.error
    updated=next(m for m in app.metric if m.label=="Hồ sơ ưu tiên").value
    assert int(updated)>int(initial)
    assert sha256(RUN_DIR/"metadata.json")==before

