"""Create additional descriptive evidence without changing the locked experiment."""
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss

from src.config import ROOT, RUN_DIR, SEED
from src.diagnostics import frozen_model_intervals, reliability_table, capacity_table
from src.inference import load_bundle
from src.records import read_json, write_json, sha256, now

OUTPUT = ROOT / "artifacts/diagnostics"


def build(repeats=2000):
    _, metadata = load_bundle()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = {name: sha256(RUN_DIR / name) for name in
               ("metadata.json", "selection_record.json", "test_predictions.csv", "validation_predictions.csv")}
    validation = pd.read_csv(RUN_DIR / "validation_predictions.csv")
    test = pd.read_csv(RUN_DIR / "test_predictions.csv")
    name = metadata["selected_model"]
    intervals = frozen_model_intervals(test.y_true, test[name + "_probability"],
        metadata["selected_threshold"], test.logistic_regression_probability, repeats=repeats, seed=SEED)
    rows = [{"metric": metric, **result} for metric, result in intervals.items()]
    pd.DataFrame(rows).to_csv(OUTPUT / "confidence_intervals_test.csv", index=False)
    reliability = []
    probability_scores = []
    # A probability reference must use train prevalence, not a holdout fit.
    train = pd.read_csv(ROOT / "data/splits/train.csv", usecols=["Churn"])
    train_prevalence = float(train.Churn.eq("Yes").mean())
    for model in ("logistic_regression", "random_forest"):
        scores = validation[model + "_probability"]
        reliability.append(reliability_table(validation.y_true, scores).assign(model=model))
        probability_scores.append({"model": model, "brier": float(brier_score_loss(validation.y_true, scores)),
                                   "log_loss": float(log_loss(validation.y_true, scores))})
    constant = np.full(len(validation), train_prevalence)
    probability_scores.append({"model": "train_prevalence_reference",
        "brier": float(brier_score_loss(validation.y_true, constant)),
        "log_loss": float(log_loss(validation.y_true, constant))})
    reliability = pd.concat(reliability, ignore_index=True)
    reliability.to_csv(OUTPUT / "reliability_validation.csv", index=False)
    pd.DataFrame(probability_scores).to_csv(OUTPUT / "probability_scores_validation.csv", index=False)
    capacity = capacity_table(validation.y_true, validation[name + "_probability"], ids=validation.customerID)
    capacity.to_csv(OUTPUT / "capacity_validation.csv", index=False)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(8, 5.2), constrained_layout=True)
    for model, color, label in [("logistic_regression", "#3976a8", "Logistic Regression"),
                                ("random_forest", "#176b57", "Random Forest")]:
        part = reliability[reliability.model.eq(model)]
        ax.plot(part.mean_probability, part.observed_churn_rate, "o-", color=color, label=label)
    ax.plot([0, 1], [0, 1], "--", color="#777777", label="Hiệu chỉnh lý tưởng")
    ax.set(xlabel="Xác suất dự đoán trung bình", ylabel="Tỷ lệ churn quan sát",
           title="Độ tin cậy xác suất trên validation", xlim=(0, 1), ylim=(0, 1))
    ax.legend(loc="upper left")
    fig.savefig(OUTPUT / "reliability_validation.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.8), constrained_layout=True)
    ax.plot([0, *capacity.actual_fraction], [0, *capacity.recall], "o-", color="#176b57", label="Ưu tiên theo RF")
    ax.plot([0, 1], [0, 1], "--", color="#777777", label="Chọn ngẫu nhiên (kỳ vọng)")
    ax.set(xlabel="Tỷ lệ hồ sơ được xem xét", ylabel="Tỷ lệ churn nằm trong danh sách",
           title="Khả năng ưu tiên hồ sơ trên validation", xlim=(0, 1), ylim=(0, 1))
    ax.legend(loc="lower right")
    fig.savefig(OUTPUT / "capacity_validation.png", dpi=180)
    plt.close(fig)
    summary = {"created_at": now(), "run_id": metadata["run_id"], "sources": sources,
        "selected_model": name, "selected_threshold": metadata["selected_threshold"],
        "bootstrap_repeats": repeats, "seed": SEED, "test_intervals": intervals,
        "probability_scores_validation": probability_scores, "capacity_validation": capacity.to_dict("records"),
        "method": "Wilson for binomial proportions; paired IID percentile bootstrap for AP, AUC, F1 and RF-minus-LR AP.",
        "scope": "Descriptive diagnostics of frozen predictions. No refit, threshold tuning or model promotion.",
        "limitations": ["Intervals condition on the fitted model; they exclude training/model-selection uncertainty and dataset shift.",
                        "IID row resampling is an assumption, not a verified property of future customer streams.",
                        "Validation ranking/calibration diagnostics are exploratory because validation was used for threshold selection.",
                        "Ranking lift measures captured observed churn, not customers retained or causal business uplift.",
                        "Brier/log-loss combine calibration and discrimination; they are not pure calibration measures.",
                        "The train-prevalence probability reference is distinct from the official most-frequent Dummy baseline."]}
    assert all(sha256(RUN_DIR / path) == digest for path, digest in sources.items())
    write_json(OUTPUT / "summary.json", summary)
    write_json(OUTPUT / "manifest.json", {p.name: sha256(p) for p in sorted(OUTPUT.iterdir())
                                         if p.is_file() and p.name != "manifest.json"})
    print("Diagnostics created; locked experiment unchanged.")
    print(pd.DataFrame(rows)[["metric", "estimate", "lower", "upper"]].to_string(index=False))
    print(capacity.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=2000)
    build(parser.parse_args().repeats)
