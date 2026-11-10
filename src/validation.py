"""Hợp đồng đầu vào dùng chung cho dữ liệu gốc, form và CSV."""
from dataclasses import dataclass
from io import StringIO
import csv
import numpy as np
import pandas as pd
from .config import FEATURES, NUMERIC, CATEGORIES, INTERNET_ADDONS, SPEC

class InputError(ValueError):
    pass

@dataclass
class ValidationResult:
    frame: pd.DataFrame
    errors: list
    extra_columns: list

    @property
    def valid_mask(self):
        return np.array([not e for e in self.errors], dtype=bool)

def normalize_features(frame):
    """Không học thống kê. Chỉ chuẩn hóa kiểu/whitespace; imputation nằm trong pipeline."""
    out = frame.loc[:, FEATURES].copy()
    for c in FEATURES:
        if c in NUMERIC:
            s = out[c].astype("string").str.strip().replace("", pd.NA)
            out[c] = pd.to_numeric(s, errors="coerce").astype(float)
        else:
            s = out[c].astype("string").str.strip()
            if c == "SeniorCitizen":
                s = s.replace({"0.0": "0", "1.0": "1"})
            out[c] = s.replace("", pd.NA).astype(object).where(s.notna(), np.nan)
    return out

def validate_structure(frame):
    """Check the table contract without normalizing or validating every cell."""
    if not isinstance(frame, pd.DataFrame):
        raise InputError("Đầu vào phải là bảng dữ liệu.")
    if not frame.columns.is_unique:
        raise InputError("Tên cột bị trùng.")
    missing = [c for c in FEATURES if c not in frame.columns]
    if missing:
        raise InputError("Thiếu cột bắt buộc: " + ", ".join(missing))
    if len(frame) == 0:
        raise InputError("Bảng dữ liệu không có dòng nào.")
    if len(frame) > SPEC["application"]["csv_max_rows"]:
        raise InputError("Tối đa 10.000 dòng mỗi lần.")


def validate_frame(frame):
    validate_structure(frame)
    out = normalize_features(frame).reset_index(drop=True)
    errors = [[] for _ in range(len(out))]

    def add_errors(mask, message):
        # Build text only for failing rows; pandas/NumPy handle column checks.
        for i in np.flatnonzero(np.asarray(mask, dtype=bool)):
            errors[i].append(message)

    for c in NUMERIC:
        raw = frame[c].astype("string").str.strip().reset_index(drop=True)
        blank = (raw.isna() | raw.eq("").fillna(False)).to_numpy(dtype=bool)
        values = out[c].to_numpy(dtype=float)
        finite = np.isfinite(values)
        if c != "TotalCharges":
            add_errors(blank, f"{c}: không được để trống")
        add_errors(~blank & ~finite, f"{c}: cần số hữu hạn hợp lệ")
        add_errors(~blank & finite & (values < 0), f"{c}: không được âm")
        if c == "tenure":
            add_errors(~blank & finite & (values >= 0) & (values != np.floor(values)),
                       "tenure: cần số tháng nguyên")
    for c, allowed in CATEGORIES.items():
        add_errors(~out[c].isin(allowed), f"{c}: giá trị ngoài danh mục")
    phone, lines = out["PhoneService"], out["MultipleLines"]
    add_errors(phone.isin(CATEGORIES["PhoneService"]) & lines.isin(CATEGORIES["MultipleLines"])
               & (phone.eq("No") != lines.eq("No phone service")),
               "PhoneService và MultipleLines không nhất quán")
    internet = out["InternetService"]
    internet_valid = internet.isin(CATEGORIES["InternetService"])
    for c in INTERNET_ADDONS:
        add_errors(internet_valid & out[c].isin(CATEGORIES[c])
                   & (internet.eq("No") != out[c].eq("No internet service")),
                   f"InternetService và {c} không nhất quán")
    return ValidationResult(out, errors, [c for c in frame.columns if c not in FEATURES])

def read_csv_bytes(payload):
    if len(payload) > SPEC["application"]["csv_max_bytes"]:
        raise InputError("Tệp vượt quá giới hạn 10 MiB.")
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError("CSV cần mã hóa UTF-8 hoặc UTF-8 BOM.") from exc
    data = []
    try:
        rows = csv.reader(StringIO(text, newline=""), delimiter=",", strict=True)
        first = next(rows, None)
        if first is None:
            raise InputError("Tệp trống.")
        header = [c.strip() for c in first]
        if any(not c for c in header) or len(set(header)) != len(header):
            raise InputError("Tên cột trống hoặc bị trùng.")
        if len(header) < len(FEATURES):
            raise InputError("CSV cần phân tách bằng dấu phẩy và đủ 19 cột đặc trưng.")
        for n, row in enumerate(rows, start=2):
            if len(data) >= SPEC["application"]["csv_max_rows"]:
                raise InputError("Tối đa 10.000 dòng mỗi lần.")
            if not row or all(not x.strip() for x in row):
                row = [""] * len(header)  # giữ dòng trống để trả lỗi theo đúng thứ tự
            if len(row) != len(header):
                raise InputError(f"Bản ghi CSV thứ {n}: số ô khác số cột tiêu đề.")
            data.append(row)
    except csv.Error as exc:
        raise InputError("CSV sai cấu trúc dấu phẩy/dấu nháy.") from exc
    frame = pd.DataFrame(data, columns=header)
    # Cell errors are returned by predict_batch, not thrown away during parsing.
    validate_structure(frame)
    return frame

def safe_csv_bytes(frame):
    """Ngăn ô chuỗi được phần mềm bảng tính diễn giải như công thức."""
    def escape_formula(value):
        return "'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value

    out = frame.copy()
    for c in out.columns:
        out[c] = out[c].map(escape_formula)
    out.columns = [escape_formula(c) for c in out.columns]
    return out.to_csv(index=False).encode("utf-8-sig")

