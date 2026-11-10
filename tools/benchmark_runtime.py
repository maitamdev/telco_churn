"""Measure the real CSV path without fitting or modifying the saved model."""
import argparse
import platform
import statistics
import time
from pathlib import Path

import pandas as pd

from src.config import ROOT, RUN_DIR, RAW_PATH, SPEC_PATH, SPLIT_DIR
from src.inference import load_bundle, predict_batch
from src.records import sha256, write_json, now
from src.validation import read_csv_bytes, validate_frame


def measure(operation, repeats):
    operation()  # Warm filesystem/import/model caches before timing.
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        samples.append(time.perf_counter() - start)
    return {"median_seconds": statistics.median(samples), "samples_seconds": samples}


def benchmark(rows=10000, repeats=5):
    sample = pd.read_csv(ROOT / "data/samples/valid_customers.csv", dtype=str,
                         keep_default_na=False)
    frame = pd.concat([sample] * ((rows + len(sample) - 1) // len(sample)),
                      ignore_index=True).iloc[:rows].copy()
    mixed = frame.copy()
    mixed.loc[::10, "tenure"] = "-1"
    payload = frame.to_csv(index=False).encode("utf-8-sig")
    pipeline, metadata = load_bundle()

    def fingerprint():
        paths = [*RUN_DIR.glob("*"), RAW_PATH, SPEC_PATH, *SPLIT_DIR.glob("*")]
        return tuple((str(p.relative_to(ROOT)), sha256(p))
                     for p in sorted(paths) if p.is_file())

    operations = {
        "validate_valid": lambda: validate_frame(frame),
        "validate_mixed": lambda: validate_frame(mixed),
        "parse_csv": lambda: read_csv_bytes(payload),
        "predict_batch": lambda: predict_batch(frame, pipeline, metadata),
        "csv_to_predictions": lambda: predict_batch(read_csv_bytes(payload), pipeline, metadata),
        "artifact_fingerprint": fingerprint,
    }
    timings = {}
    for name, operation in operations.items():
        timings[name] = measure(operation, repeats)
        print(f"{name}: {timings[name]['median_seconds']:.6f}s", flush=True)
    return {"measured_at": now(), "rows": rows, "repeats": repeats,
            "python": platform.python_version(), "platform": platform.platform(),
            "run_id": metadata["run_id"], "timings": timings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "reports/evidence/runtime_benchmark.json")
    args = parser.parse_args()
    if not 1 <= args.rows <= 10000 or args.repeats < 1:
        parser.error("rows must be 1..10000 and repeats must be positive")
    write_json(args.output, benchmark(args.rows, args.repeats))


if __name__ == "__main__":
    main()
