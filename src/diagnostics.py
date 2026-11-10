"""Diagnostics for frozen predictions; never fit or select a production model."""
from numbers import Integral

import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.metrics import average_precision_score, roc_auc_score


def binary_inputs(y, probability):
    labels = np.asarray(y)
    scores = np.asarray(probability, dtype=float)
    if (labels.ndim != 1 or scores.ndim != 1 or labels.size == 0
            or labels.shape != scores.shape or not np.isin(labels, [0, 1]).all()
            or not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any()):
        raise ValueError("Cần nhãn nhị phân và xác suất hữu hạn cùng số dòng.")
    return labels.astype(int), scores


def wilson_interval(successes, total, confidence=.95):
    if not 0 < confidence < 1:
        raise ValueError("Confidence phải nằm trong (0, 1).")
    if (not isinstance(successes, Integral) or not isinstance(total, Integral)
            or total < 0 or not 0 <= successes <= total):
        raise ValueError("Số thành công và tổng phải là số nguyên hợp lệ.")
    if total == 0:
        return {"estimate": None, "lower": None, "upper": None, "n": 0,
                "method": "wilson", "confidence": confidence}
    interval = binomtest(int(successes), int(total)).proportion_ci(confidence, method="wilson")
    return {"estimate": successes / total, "lower": float(interval.low),
            "upper": float(interval.high), "n": int(total),
            "method": "wilson", "confidence": confidence}


def frozen_model_intervals(y, probability, threshold, comparator=None, *, repeats=2000, seed=42):
    """Paired IID row bootstrap; conditions on fitted models and fixed thresholds.

    Percentile intervals describe finite holdout sampling uncertainty, excluding
    training/tuning, deployment shift and intervention effects. They are not
    simultaneous intervals or a model-promotion procedure.
    """
    y, probability = binary_inputs(y, probability)
    if np.unique(y).size != 2:
        raise ValueError("Bootstrap AP/ROC-AUC cần đủ hai lớp.")
    if not isinstance(repeats, Integral) or repeats < 2 or not 0 <= threshold <= 1:
        raise ValueError("Cần ít nhất hai lần bootstrap và ngưỡng trong [0, 1].")
    if comparator is not None:
        _, comparator = binary_inputs(y, comparator)
    predicted = probability >= threshold
    tp = int((predicted & (y == 1)).sum())
    fp = int((predicted & (y == 0)).sum())
    fn = int((~predicted & (y == 1)).sum())
    result = {
        "precision_churn": wilson_interval(tp, tp + fp),
        "recall_churn": wilson_interval(tp, tp + fn),
        "accuracy": wilson_interval(int((predicted == y).sum()), len(y)),
    }
    estimates = {"average_precision": float(average_precision_score(y, probability)),
                 "roc_auc": float(roc_auc_score(y, probability)),
                 "f1_churn": 2 * tp / (2 * tp + fp + fn)}
    if comparator is not None:
        estimates["ap_difference"] = estimates["average_precision"] - float(average_precision_score(y, comparator))
    draws = {name: [] for name in estimates}
    rng = np.random.default_rng(seed)
    skipped = 0
    for _ in range(repeats):
        indices = rng.integers(0, len(y), len(y))
        labels, scores, predictions = y[indices], probability[indices], predicted[indices]
        if np.unique(labels).size != 2:
            skipped += 1
            continue
        ap = float(average_precision_score(labels, scores))
        draws["average_precision"].append(ap)
        draws["roc_auc"].append(float(roc_auc_score(labels, scores)))
        hits = int((predictions & (labels == 1)).sum())
        draws["f1_churn"].append(2 * hits / (int(predictions.sum()) + int(labels.sum())))
        if comparator is not None:
            draws["ap_difference"].append(ap - float(average_precision_score(labels, comparator[indices])))
    if len(draws["average_precision"]) < 2:
        raise ValueError("Không đủ mẫu bootstrap có hai lớp để tính khoảng.")
    for name, values in draws.items():
        lower, upper = np.quantile(values, [.025, .975])
        result[name] = {"estimate": estimates[name], "lower": float(lower), "upper": float(upper),
                        "method": "paired_iid_percentile_bootstrap", "confidence": .95,
                        "resamples_used": len(values), "resamples_skipped": skipped, "seed": seed}
    return result


def reliability_table(y, probability, bins=10):
    """Fixed-width probability bins; p=1 belongs to the final bin."""
    y, p = binary_inputs(y, probability)
    if not isinstance(bins, Integral) or bins < 2:
        raise ValueError("Cần ít nhất hai khoảng xác suất.")
    indices = np.minimum((p * bins).astype(int), bins - 1)
    rows = []
    for i in range(bins):
        selected = indices == i
        n = int(selected.sum())
        if n:
            interval = wilson_interval(int(y[selected].sum()), n)
            rows.append({"bin": i, "left": i / bins, "right": (i + 1) / bins,
                         "n": n, "mean_probability": float(p[selected].mean()),
                         "observed_churn_rate": interval["estimate"],
                         "lower": interval["lower"], "upper": interval["upper"]})
    return pd.DataFrame(rows)


def load_diagnostics(metadata, directory=None):
    """Verify derived evidence and its frozen prediction sources before display."""
    from pathlib import Path
    from .config import ROOT, RUN_DIR
    from .records import read_json, sha256

    directory = Path(directory) if directory is not None else ROOT / "artifacts/diagnostics"
    manifest = read_json(directory / "manifest.json")
    required = {"summary.json", "confidence_intervals_test.csv", "reliability_validation.csv",
                "probability_scores_validation.csv", "capacity_validation.csv"}
    if not required.issubset(manifest):
        raise ValueError("Thiếu bằng chứng đánh giá mở rộng.")
    for name, digest in manifest.items():
        if Path(name).name != name or sha256(directory / name) != digest:
            raise ValueError("Bằng chứng đánh giá mở rộng không khớp hash.")
    summary = read_json(directory / "summary.json")
    if summary["run_id"] != metadata["run_id"] or summary["selected_threshold"] != metadata["selected_threshold"]:
        raise ValueError("Bằng chứng đánh giá mở rộng không thuộc mô hình hiện tại.")
    expected_sources = {"metadata.json", "selection_record.json", "test_predictions.csv", "validation_predictions.csv"}
    if set(summary["sources"]) != expected_sources:
        raise ValueError("Nguồn đánh giá mở rộng không đầy đủ.")
    for name, digest in summary["sources"].items():
        if sha256(RUN_DIR / name) != digest:
            raise ValueError("Dữ liệu nguồn của đánh giá mở rộng đã thay đổi.")
    return summary


def capacity_table(y, probability, fractions=(.1, .2, .3, .4, .5, 1.), ids=None):
    """Top-k ranking diagnostics. Ties use ID/order, never outcome labels."""
    y, p = binary_inputs(y, probability)
    identifiers = np.arange(len(y)) if ids is None else np.asarray(ids)
    if identifiers.ndim != 1 or len(identifiers) != len(y):
        raise ValueError("Danh sách ID không khớp dữ liệu.")
    fractions = np.asarray(fractions, dtype=float)
    if fractions.ndim != 1 or not len(fractions) or not np.isfinite(fractions).all() or ((fractions <= 0) | (fractions > 1)).any():
        raise ValueError("Tỷ lệ năng lực xử lý phải trong (0, 1].")
    order = np.lexsort((identifiers, -p))
    positives = int(y.sum())
    base_rate = positives / len(y)
    cumulative = np.cumsum(y[order])
    rows = []
    for fraction in fractions:
        count = int(np.ceil(len(y) * fraction))
        captured = int(cumulative[count - 1])
        precision = captured / count
        rows.append({"requested_fraction": float(fraction), "contact_count": count,
                     "actual_fraction": count / len(y), "captured_churn": captured,
                     "precision": precision, "recall": captured / positives if positives else None,
                     "lift": precision / base_rate if positives else None,
                     "cutoff_probability": float(p[order[count - 1]])})
    return pd.DataFrame(rows)
