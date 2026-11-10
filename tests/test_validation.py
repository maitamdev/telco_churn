import numpy as np
import pandas as pd
import pytest
from src.config import FEATURES, SPEC, ROOT
from src.validation import InputError,validate_frame,read_csv_bytes,safe_csv_bytes

def test_source_sample_is_valid(sample):
    assert validate_frame(sample).valid_mask.all()

@pytest.mark.parametrize("column,value",[
    ("tenure","-1"),("tenure","2.5"),("tenure",""),("MonthlyCharges","inf"),
    ("MonthlyCharges","nan"),("MonthlyCharges","bad"),("TotalCharges","NaN"),
    ("TotalCharges","-5"),("gender","Unknown"),("Contract",""),
    ("SeniorCitizen",2),("PaymentMethod",None),
])
def test_invalid_cells_rejected(sample,column,value):
    sample[column]=sample[column].astype(object)
    sample.loc[0,column]=value
    r=validate_frame(sample)
    assert not r.valid_mask[0]
    assert r.valid_mask[1:].all()
    assert any(column in error for error in r.errors[0])

def test_totalcharges_blank_allowed(sample):
    sample.loc[0,"TotalCharges"]="   "
    r=validate_frame(sample)
    assert r.valid_mask.all()
    assert np.isnan(r.frame.loc[0,"TotalCharges"])

def test_normalize_whitespace_and_senior(sample):
    sample.loc[0,"gender"]=" "+sample.loc[0,"gender"]+" "
    sample["SeniorCitizen"]=sample["SeniorCitizen"].astype(object)
    sample.loc[0,"SeniorCitizen"]=0.0
    assert validate_frame(sample).valid_mask.all()

def test_missing_header_rejected_even_nullable(sample):
    with pytest.raises(InputError,match="TotalCharges"):
        validate_frame(sample.drop(columns="TotalCharges"))

def test_inconsistent_services(sample):
    sample.loc[0,"PhoneService"]="No"
    sample.loc[0,"MultipleLines"]="Yes"
    sample.loc[1,"InternetService"]="No"
    sample.loc[1,"OnlineSecurity"]="Yes"
    r=validate_frame(sample)
    assert not r.valid_mask[0] and not r.valid_mask[1]

def test_csv_duplicate_header(sample):
    payload=sample.to_csv(index=False).replace("customerID,","gender,",1).encode()
    with pytest.raises(InputError,match="trùng"):
        read_csv_bytes(payload)

def test_csv_unicode_error():
    with pytest.raises(InputError,match="UTF-8"):
        read_csv_bytes(b"\xff\xff")

def test_blank_csv_line_preserved(sample):
    payload=sample.to_csv(index=False).encode()+b"\n"
    parsed=read_csv_bytes(payload)
    assert len(parsed)==len(sample)+1
    assert not validate_frame(parsed).valid_mask[-1]

def test_csv_column_count_rejected(sample):
    payload=sample.to_csv(index=False).encode()+b"too,few,columns\n"
    with pytest.raises(InputError,match="số ô"):
        read_csv_bytes(payload)

def test_size_and_rows_limit(sample,monkeypatch):
    monkeypatch.setitem(SPEC["application"],"csv_max_bytes",10)
    with pytest.raises(InputError,match="10 MiB"):
        read_csv_bytes(b"x"*11)
    monkeypatch.setitem(SPEC["application"],"csv_max_rows",1)
    with pytest.raises(InputError,match="10.000"):
        validate_frame(sample)

def test_formula_export_escaped():
    out=safe_csv_bytes(pd.DataFrame({"id":["=1+1","+cmd","@x","-ABC","plain"]})).decode("utf-8-sig")
    assert "'=1+1" in out and "'+cmd" in out and "'@x" in out and "'-ABC" in out

def test_empty_table_rejected(sample):
    with pytest.raises(InputError,match="không có dòng"):
        validate_frame(sample.iloc[:0])


def test_errors_preserve_position_order_and_multiple_failures(sample):
    sample = sample.astype(object)
    sample.index = [17] * len(sample)
    sample.iloc[0, sample.columns.get_loc("tenure")] = "2.5"
    sample.iloc[0, sample.columns.get_loc("MonthlyCharges")] = "-1"
    sample.iloc[0, sample.columns.get_loc("TotalCharges")] = "inf"
    sample.iloc[0, sample.columns.get_loc("gender")] = None
    sample.iloc[0, sample.columns.get_loc("PhoneService")] = "No"
    sample.iloc[0, sample.columns.get_loc("MultipleLines")] = "Yes"
    result = validate_frame(sample)
    assert result.errors[0] == [
        "tenure: cần số tháng nguyên", "MonthlyCharges: không được âm",
        "TotalCharges: cần số hữu hạn hợp lệ", "gender: giá trị ngoài danh mục",
        "PhoneService và MultipleLines không nhất quán",
    ]
    assert result.valid_mask[1:].all()
    assert sample.index.tolist() == [17] * len(sample)


@pytest.mark.parametrize("internet,addon", [("No", "Yes"), ("DSL", "No internet service")])
def test_all_internet_dependencies_checked(sample, internet, addon):
    from src.config import INTERNET_ADDONS

    sample.loc[0, "InternetService"] = internet
    sample.loc[0, INTERNET_ADDONS] = addon
    result = validate_frame(sample)
    assert result.errors[0] == [f"InternetService và {c} không nhất quán" for c in INTERNET_ADDONS]


def test_invalid_service_does_not_create_spurious_dependency_errors(sample):
    sample.loc[0, "InternetService"] = "Unknown"
    sample.loc[0, "PhoneService"] = "Unknown"
    result = validate_frame(sample)
    assert result.errors[0] == ["PhoneService: giá trị ngoài danh mục", "InternetService: giá trị ngoài danh mục"]


def test_csv_bom_quoted_commas_and_embedded_newlines(sample):
    sample.loc[0, "customerID"] = 'KH, "quoted"\r\nsecond line'
    parsed = read_csv_bytes(sample.to_csv(index=False).encode("utf-8-sig"))
    pd.testing.assert_frame_equal(parsed, sample)


def test_csv_limit_stops_before_parsing_excess_payload(sample, monkeypatch):
    monkeypatch.setitem(SPEC["application"], "csv_max_rows", 1)
    payload = sample.iloc[:2].to_csv(index=False).encode() + b'"unterminated'
    with pytest.raises(InputError, match="10.000"):
        read_csv_bytes(payload)


def test_csv_missing_required_column_with_extra_header(sample):
    payload = sample.rename(columns={"TotalCharges": "UnusedColumn"}).to_csv(index=False).encode()
    with pytest.raises(InputError, match="TotalCharges"):
        read_csv_bytes(payload)


def test_formula_export_escapes_headers_and_preserves_numeric_values():
    from io import BytesIO

    frame = pd.DataFrame({"=HYPERLINK()": [" \t=1+1"], "amount": [-12.5]})
    exported = pd.read_csv(BytesIO(safe_csv_bytes(frame)))
    assert exported.columns[0] == "'=HYPERLINK()"
    assert exported.iloc[0, 0] == "' \t=1+1"
    assert exported.amount.iloc[0] == -12.5
    assert frame.columns[0] == "=HYPERLINK()"

