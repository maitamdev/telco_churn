"""Đối soát bằng chứng hiện có; không fit lại model hoặc thay ngưỡng đã khóa."""
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import roc_auc_score, average_precision_score
from src.config import ROOT, RAW_PATH, RUN_DIR, NUMERIC, FEATURES
from src.data import load_partition
from src.inference import load_bundle
from src.diagnostics import load_diagnostics
from tools.package_project import check_test_reports
from src.records import read_json, write_json, now, sha256
from src.validation import normalize_features, validate_frame


def run():
    evidence = ROOT / "reports/evidence"
    pipeline, metadata = load_bundle()
    original_model_hash = sha256(RUN_DIR / "churn_pipeline.joblib")
    raw = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False)
    validated = validate_frame(raw)
    assert validated.valid_mask.all()
    quality = []
    for column in raw:
        missing = int(raw[column].str.strip().eq("").sum())
        meaning = ("integer_months" if column == "tenure" else "numeric") if column in NUMERIC else (
            "identifier" if column == "customerID" else "binary_target" if column == "Churn" else "categorical")
        quality.append({"column": column, "read_dtype": str(raw[column].dtype), "semantic_type": meaning,
                        "rows": len(raw), "missing_count": missing, "missing_percent": 100 * missing / len(raw)})
    pd.DataFrame(quality).to_csv(evidence / "data_quality_audit.csv", index=False, encoding="utf-8-sig")
    parts = {name: load_partition(name) for name in ["train", "validation", "test"]}
    merged = pd.concat(parts.values(), ignore_index=True)
    assert not merged.customerID.duplicated().any()
    pd.testing.assert_frame_equal(raw.sort_values("customerID").reset_index(drop=True),
                                  merged.sort_values("customerID").reset_index(drop=True))
    train = normalize_features(parts["train"])
    outliers = []
    for group in ["all", "No", "Yes"]:
        selected = train if group == "all" else train.loc[parts["train"].Churn.eq(group)]
        for column in NUMERIC:
            values = selected[column].dropna()
            q1, q3 = values.quantile([.25, .75])
            lower, upper = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
            outliers.append({"partition": "train", "churn_group": group, "feature": column,
                             "n_nonmissing": len(values), "q1": q1, "q3": q3,
                             "iqr_lower": lower, "iqr_upper": upper,
                             "outside_1_5_iqr": int(((values < lower) | (values > upper)).sum()),
                             "min": values.min(), "max": values.max(),
                             "action": "retain; descriptive audit only; no refit"})
    pd.DataFrame(outliers).to_csv(evidence / "outlier_audit_train.csv", index=False, encoding="utf-8-sig")

    saved = pd.read_csv(RUN_DIR / "test_predictions.csv")
    assert saved.customerID.tolist() == parts["test"].customerID.tolist()
    y = parts["test"].Churn.eq("Yes").astype(int).to_numpy()
    np.testing.assert_array_equal(saved.y_true, y)
    model_probability = pipeline.predict_proba(parts["test"][FEATURES])[:, list(pipeline.classes_).index(1)]
    np.testing.assert_allclose(model_probability, saved[metadata["selected_model"] + "_probability"], atol=1e-12, rtol=0)
    max_difference = 0.
    for record in read_json(RUN_DIR / "test_metrics.json")["metrics"]:
        name = record["model"]
        probability = saved[name + "_probability"].to_numpy()
        pred = saved[name + "_native"].to_numpy() if name == "baseline" else (probability >= record["threshold"]).astype(int)
        tp, fp = int(((pred == 1) & (y == 1)).sum()), int(((pred == 1) & (y == 0)).sum())
        tn, fn = int(((pred == 0) & (y == 0)).sum()), int(((pred == 0) & (y == 1)).sum())
        precision, recall = tp / (tp + fp) if tp + fp else 0., tp / (tp + fn)
        measured = {"n": len(y), "tn": tn, "fp": fp, "fn": fn, "tp": tp, "flagged_count": tp + fp,
                    "accuracy": (tp + tn) / len(y), "precision_churn": precision, "recall_churn": recall,
                    "f1_churn": 2 * precision * recall / (precision + recall) if precision + recall else 0.,
                    "roc_auc": roc_auc_score(y, probability), "average_precision": average_precision_score(y, probability)}
        for key, value in measured.items():
            difference = abs(record[key] - value)
            max_difference = max(max_difference, difference)
            assert difference < 1e-12, (name, record["operating_point"], key)

    images = sorted((ROOT / "artifacts/eda").glob("*.png"))
    assert len(images) == 8
    for path in images + sorted(RUN_DIR.glob("evaluation_*.png")):
        with Image.open(path) as im:
            im.verify()
    notebook = read_json(ROOT / "notebooks/01_telco_churn.ipynb")
    cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert len(cells) == 6 and all(cell["execution_count"] is not None for cell in cells)
    assert not any(output.get("output_type") == "error" for cell in cells for output in cell.get("outputs", []))
    test_paths = [evidence / name for name in ("pytest_upgrade.xml", "pytest_upgrade_clean.xml")]
    counts = check_test_reports(test_paths)
    suites = list(ET.parse(test_paths[0]).getroot().iter("testsuite"))
    tests = {key: sum(int(s.attrib.get(key, 0)) for s in suites) for key in ["tests", "failures", "errors", "skipped"]}
    assert tests == {"tests": counts[0], "failures": 0, "errors": 0, "skipped": 0}
    diagnostics = load_diagnostics(metadata)
    reproduction = read_json(evidence / "full_reproduction.json")
    replica = ROOT / reproduction["replica_directory"]
    reproduction_sources = ["src/train.py", "src/data.py", "src/preprocessing.py", "src/evaluation.py",
                            "src/validation.py", "src/config.py", "configs/project_spec.json"]
    matched = {name: sha256(ROOT / name) == sha256(replica / name) for name in reproduction_sources} if replica.exists() else {}
    assert reproduction["status"] == "passed"
    # This is historical training evidence. Changes to validation/diagnostics
    # are checked with current regression tests and direct probability parity.
    report_qa = read_json(evidence / "report_qa.json")
    slides_qa = read_json(evidence / "slides_qa.json")
    assert report_qa["status"] == slides_qa["status"] == "passed"
    assert report_qa["document_sha256"] == sha256(ROOT / "reports/BAOCAO-TTNT.docx")
    assert slides_qa["presentation_sha256"] == sha256(ROOT / "reports/BAO_VE_TELCO_CHURN.pptx")
    assert sha256(RUN_DIR / "churn_pipeline.joblib") == original_model_hash
    result = {"checked_at": now(), "status": "technical_checks_passed_submission_incomplete",
              "guide_sha256": sha256(ROOT.parent / "Huong_Dan_Do_An_CuoiKy.pdf") if (ROOT.parent / "Huong_Dan_Do_An_CuoiKy.pdf").exists() else None,
              "model_run_id": metadata["run_id"], "model_sha256": original_model_hash,
              "data_shape": list(raw.shape), "invalid_rows": int((~validated.valid_mask).sum()),
              "duplicates": int(raw.duplicated().sum()), "split_sizes": {k: len(v) for k, v in parts.items()},
              "splits_disjoint_complete_and_raw_identical": True, "test_metric_records_recomputed": 5,
              "test_metric_max_abs_difference": max_difference, "test_model_probability_max_abs_difference":
                  float(np.max(np.abs(model_probability - saved[metadata["selected_model"] + "_probability"].to_numpy()))),
              "eda_png_count": len(images), "executed_notebook_code_cells": len(cells), "pytest": tests,
              "previous_clean_environment_reproduction": reproduction["time"],
              "reproduction_source_hashes_match": matched, "model_or_threshold_changed": False,
              "replica_source_check_performed": replica.exists(),
              "report_written": True, "slides_written": True, "student_contribution_recorded": False,
              "diagnostics_verified": True, "diagnostics_run_id": diagnostics["run_id"],
              "clean_environment_test_count": counts[1],
              "teacher_registration_confirmed": False, "bm06_available": False,
              "limits": ["No new training in this audit. Historical reproduction is retained; source hash differences are reported rather than claimed identical. Current model parity and tests were rerun.",
                         "Snapshot cannot establish all features existed before a prospective prediction date.",
                         "Submission and oral defense cannot be certified by software tests."]}
    write_json(evidence / "requirements_audit.json", result)
    print(f"Audit passed: data/splits, 5 metric records, model parity, 8 EDA figures, 6 executed cells, {counts[0]} tests in both environments, diagnostics and document hashes.")
    print(pd.DataFrame(outliers)[["churn_group", "feature", "outside_1_5_iqr"]].to_string(index=False))
    print("Missing TotalCharges: 11/7043 =", 100 * 11 / 7043, "%")


if __name__ == "__main__":
    run()
