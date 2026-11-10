"""Tải có hash, kiểm chất lượng và chia tập cố định. Chạy: python -m src.data."""
from urllib.request import urlopen, Request
import pandas as pd
from sklearn.model_selection import train_test_split
from .config import ROOT, SPEC, SPEC_PATH, RAW_PATH, SPLIT_DIR, PREP_DIR, SEED, FEATURES, CATEGORIES, NUMERIC, LABELS
from .records import sha256, write_json, log_step, now, environment
from .validation import validate_frame

def load_partition(name):
    if name not in {"train", "validation", "test"}:
        raise ValueError("Unknown partition")
    return pd.read_csv(SPLIT_DIR / f"{name}.csv", dtype=str, keep_default_na=False)

def prepare():
    PREP_DIR.mkdir(parents=True, exist_ok=True)
    if not RAW_PATH.exists():
        request = Request(SPEC["dataset"]["source_url"], headers={"User-Agent": "TelcoCourseProject/1.0"})
        with urlopen(request, timeout=60) as response:
            payload = response.read()
        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        RAW_PATH.write_bytes(payload)
    if sha256(RAW_PATH) != SPEC["dataset"]["expected_sha256"]:
        raise RuntimeError("Raw data hash khác cấu hình đã kiểm. Dừng để kiểm nguồn, không tự thay dữ liệu.")
    write_json(PREP_DIR / "provenance.json", {
        "download_verified_at": now(), "url": SPEC["dataset"]["source_url"], "sha256": sha256(RAW_PATH),
        "bytes": RAW_PATH.stat().st_size, "provider": "IBM public demonstration repository",
        "dataset_context": "Mẫu công ty viễn thông hư cấu, không phải dữ liệu khách hàng thực do nhóm thu thập.",
        "license_note": "Repo IBM có Apache-2.0 cho mã; không tự suy ra một giấy phép dữ liệu riêng. Giữ URL nguồn, file gốc và ghi công IBM.",
        "target_scope": "Churn Yes/No trong snapshot. Không xác lập dự báo trước 30/60/90 ngày."
    })
    log_step("03", "Nguồn dữ liệu", ["Tải/kiểm lại CSV IBM và hash SHA-256"], [f"{RAW_PATH.stat().st_size} bytes; hash trùng nguồn đã chốt"], ["data/raw/Telco-Customer-Churn.csv", "artifacts/preparation/provenance.json"])
    frame = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False)
    expected = {"customerID", "Churn", *FEATURES}
    if set(frame.columns) != expected or len(frame) != 7043:
        raise RuntimeError("Schema/kích thước nguồn khác dự kiến.")
    if frame["customerID"].duplicated().any() or frame.duplicated().any():
        raise RuntimeError("Trùng ID/dòng; cần quyết định xử lý trước chia tập.")
    if not set(frame.Churn) == {"No", "Yes"}:
        raise RuntimeError("Nhãn không hợp lệ.")
    result = validate_frame(frame)
    if not result.valid_mask.all():
        raise RuntimeError(f"Dữ liệu gốc có dòng không hợp lệ: {[(i,e) for i,e in enumerate(result.errors) if e][:5]}")
    blanks = {c: int(frame[c].str.strip().eq("").sum()) for c in frame}
    profile = {"rows": len(frame), "columns": len(frame.columns), "features": len(FEATURES),
               "unique_ids": int(frame.customerID.nunique()), "duplicate_rows": int(frame.duplicated().sum()),
               "label_counts": {str(k): int(v) for k,v in frame.Churn.value_counts().items()},
               "missing_blank": blanks, "totalcharges_blank_tenure": frame.loc[frame.TotalCharges.str.strip().eq(""), "tenure"].value_counts().to_dict(),
               "scope": "Toàn bộ dữ liệu: chỉ kiểm cấu trúc/chất lượng. EDA và quyết định mô hình dùng train."}
    write_json(PREP_DIR / "data_profile.json", profile)
    write_json(PREP_DIR / "cleaning_log.json", {
        "input_rows": len(frame), "output_rows": len(frame), "removed_rows": 0,
        "decisions": ["Giữ nguyên raw CSV; split giữ giá trị gốc.",
                      "TotalCharges có 11 khoảng trắng được chuyển NaN trong pipeline; median học trong từng fold/train.",
                      "Không gán 0 chỉ vì tenure=0; không xóa 11 khách mới.",
                      "ID dùng truy vết, không làm đặc trưng; Churn tách khỏi X.",
                      "SeniorCitizen là danh mục 0/1; No internet service/No phone service là giá trị có nghĩa.",
                      "Không loại outlier hoặc cân bằng lại trước chia tập; thử class_weight trong CV.",
                      "Không dùng biến churn reason/status/score hoặc thông tin tương lai."]})
    dictionary = ["# Từ điển dữ liệu", "", "Churn: No=0, Yes=1. customerID: mã truy vết, không vào mô hình.", "",
                  "| Cột | Ý nghĩa | Kiểu và miền hợp lệ |", "|---|---|---|"]
    for c in FEATURES:
        domain = ", ".join(CATEGORIES[c]) if c in CATEGORIES else ("số nguyên không âm" if c == "tenure" else "số hữu hạn không âm")
        if c == "TotalCharges":
            domain += "; được thiếu"
        dictionary.append(f"| {c} | {LABELS[c]} | {domain} |")
    dictionary += ["", "Đơn vị tiền giữ nguyên theo dữ liệu nguồn; không quy đổi sang VND. Dữ liệu dạng snapshot, không có timestamp để chia theo thời gian."]
    (ROOT / "docs/DATA_DICTIONARY.md").write_text("\n".join(dictionary), encoding="utf-8")
    log_step("04", "Kiểm chất lượng", ["Kiểm schema, ID, nhãn, số, danh mục, nhất quán dịch vụ", "Ghi từ điển và lý do làm sạch"], ["7.043 dòng × 21 cột; không trùng ID/dòng", "11 TotalCharges trống, đều tenure=0; giữ tất cả dòng"], ["artifacts/preparation/data_profile.json", "artifacts/preparation/cleaning_log.json", "docs/DATA_DICTIONARY.md"])
    trainval, test = train_test_split(frame, test_size=.2, random_state=SEED, stratify=frame.Churn)
    train, validation = train_test_split(trainval, test_size=.25, random_state=SEED, stratify=trainval.Churn)
    SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    partitions = {}
    for name, part in [("train", train), ("validation", validation), ("test", test)]:
        path = SPLIT_DIR / f"{name}.csv"
        if path.exists():
            existing = pd.read_csv(path, dtype=str, keep_default_na=False)
            if not existing.equals(part.reset_index(drop=True)):
                raise RuntimeError("Split tồn tại khác split mới; không ghi đè thí nghiệm.")
        else:
            part.to_csv(path, index=False)
        partitions[name] = {"rows": len(part), "label_counts": part.Churn.value_counts().to_dict(),
                            "ids": part.customerID.tolist(), "file_sha256": sha256(path)}
    assert not set(train.customerID) & set(validation.customerID)
    assert not set(train.customerID) & set(test.customerID)
    assert not set(validation.customerID) & set(test.customerID)
    write_json(SPLIT_DIR / "split_manifest.json", {
        "dataset_sha256": sha256(RAW_PATH), "seed": SEED, "strategy": SPEC["split"]["algorithm"], "partitions": partitions})
    # Mẫu demo chỉ lấy train, tránh đưa test vào thao tác chọn ngưỡng.
    sample = train.drop(columns="Churn").head(8).reset_index(drop=True)
    sample.to_csv(ROOT / "data/samples/valid_customers.csv", index=False)
    mixed = sample.head(3).copy()
    mixed.loc[1, "tenure"] = "-1"
    mixed.loc[2, "PaymentMethod"] = "UNKNOWN"
    mixed.to_csv(ROOT / "data/samples/mixed_valid_invalid.csv", index=False)
    sample.iloc[:0].to_csv(ROOT / "data/samples/template.csv", index=False)
    write_json(PREP_DIR / "environment.json", environment())
    log_step("05", "Cố định ba tập", ["Stratified 60/20/20, seed=42, lưu ID/hash", "Kiểm giao ID rỗng; tạo mẫu CSV từ train"], [f"{n}: {v['rows']} dòng" for n,v in partitions.items()], ["data/splits/split_manifest.json", "data/splits/train.csv", "data/splits/validation.csv", "data/splits/test.csv", "data/samples/"])
    print({n: p["rows"] for n,p in partitions.items()}, flush=True)

if __name__ == "__main__":
    prepare()

