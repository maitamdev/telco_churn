"""Metrics và quy tắc chọn ngưỡng được chốt trước khi mở test."""
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix)
from .config import SPEC
from .diagnostics import binary_inputs

def metrics(y, probability, threshold=.5, predictions=None):
    y = np.asarray(y, dtype=int)
    p = np.asarray(probability, dtype=float)
    pred = (p >= threshold).astype(int) if predictions is None else np.asarray(predictions, dtype=int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    both = len(np.unique(y)) == 2
    return {
        "n": len(y), "threshold": float(threshold), "accuracy": float(accuracy_score(y, pred)),
        "precision_churn": float(precision_score(y, pred, zero_division=0)),
        "recall_churn": float(recall_score(y, pred, zero_division=0)),
        "f1_churn": float(f1_score(y, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, p)) if both else None,
        "average_precision": float(average_precision_score(y, p)) if both else None,
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "flagged_count": int(pred.sum()),
    }

def threshold_sweep(y, probability):
    y, p = binary_inputs(y, probability)
    thresholds = np.unique(np.concatenate(([0., 1.], p)))
    # Sort + suffix counts: O(n log n), không tạo ma trận n².
    order = np.argsort(p)
    sorted_p, sorted_y = p[order], y[order]
    suffix_tp = np.concatenate((np.cumsum(sorted_y[::-1])[::-1], [0]))
    idx = np.searchsorted(sorted_p, thresholds, side="left")
    flagged = len(y)-idx
    tp = suffix_tp[idx]
    precision = np.divide(tp, flagged, out=np.zeros_like(tp, dtype=float), where=flagged>0)
    recall = tp / y.sum() if y.sum() else np.zeros_like(tp, dtype=float)
    f1 = np.divide(2*precision*recall, precision+recall, out=np.zeros_like(precision), where=precision+recall>0)
    return pd.DataFrame({"threshold": thresholds, "precision_churn": precision, "recall_churn": recall,
                         "f1_churn": f1, "flagged_count": flagged, "tp": tp})

def choose_threshold(y, probability):
    sweep = threshold_sweep(y, probability)
    rule = SPEC["threshold"]
    feasible = sweep[(sweep.precision_churn >= rule["precision_floor"]) &
                     (sweep.flagged_count >= rule["minimum_flagged"])]
    if feasible.empty:
        chosen = metrics(y, probability, rule["fallback"]["threshold"])
        status = rule["fallback"]["status"]
    else:
        best = feasible.sort_values(["recall_churn", "precision_churn", "threshold"], ascending=False).iloc[0]
        chosen = metrics(y, probability, float(best.threshold))
        status = "precision_constraint_met"
    return {
        "threshold": chosen["threshold"], "status": status, "validation_metrics": chosen,
        "precision_floor": rule["precision_floor"], "aspirational_recall": rule["aspirational_recall"],
        "aspirational_recall_met": chosen["recall_churn"] >= rule["aspirational_recall"],
        "assumption": "precision>=0.50 và mong muốn recall>=0.80 là giả định nhóm; không phải thang điểm môn học.",
    }, sweep

