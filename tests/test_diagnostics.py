import shutil
from math import sqrt

import numpy as np
import pandas as pd
import pytest

from src.config import ROOT, RUN_DIR
from src.diagnostics import (binary_inputs, wilson_interval, frozen_model_intervals,
                             reliability_table, capacity_table, load_diagnostics)
from src.records import sha256


@pytest.mark.parametrize("y,p", [([.5], [.5]), ([2], [.2]), ([], []),
    ([0, 1], [.2]), ([[0]], [[.2]]), ([1], [float("nan")]), ([1], [1.1])])
def test_diagnostics_reject_invalid_inputs(y, p):
    with pytest.raises(ValueError):
        binary_inputs(y, p)


@pytest.mark.parametrize("successes,total", [(0, 9), (9, 9), (302, 374), (302, 595)])
def test_wilson_matches_reference_including_boundaries(successes, total):
    actual = wilson_interval(successes, total)
    # Independent closed-form Wilson reference, rather than reusing SciPy's API.
    z = 1.959963984540054
    fraction = successes / total
    denominator = 1 + z*z/total
    center = (fraction + z*z/(2*total)) / denominator
    radius = z*sqrt(fraction*(1-fraction)/total + z*z/(4*total*total)) / denominator
    assert actual["estimate"] == pytest.approx(fraction)
    assert actual["lower"] == pytest.approx(max(0., center-radius))
    assert actual["upper"] == pytest.approx(min(1., center+radius))
    assert 0 <= actual["lower"] <= actual["upper"] <= 1


def test_empty_denominator_is_undefined():
    result = wilson_interval(0, 0)
    assert result["estimate"] is None and result["lower"] is None


def test_reliability_bins_keep_zero_one_and_all_rows():
    y, p = [0, 1, 0, 1], [0, .1, .99, 1]
    table = reliability_table(y, p, bins=10)
    assert table.n.sum() == 4
    assert table.bin.tolist() == [0, 1, 9]
    assert table.iloc[-1].n == 2
    assert table.iloc[-1].observed_churn_rate == .5


def test_capacity_ties_use_id_not_outcome_and_is_order_independent():
    y = np.array([1, 0, 1, 0])
    p = np.full(4, .5)
    ids = np.array(["d", "a", "c", "b"])
    table = capacity_table(y, p, [.5, 1.], ids)
    assert table.iloc[0].captured_churn == 0  # IDs a,b, independent of labels.
    assert table.iloc[1].recall == 1 and table.iloc[1].lift == 1
    permutation = [2, 0, 3, 1]
    pd.testing.assert_frame_equal(table, capacity_table(y[permutation], p[permutation], [.5, 1.], ids[permutation]))


def test_capacity_no_positives_does_not_invent_lift():
    table = capacity_table([0, 0], [.2, .8], [.5])
    assert table.iloc[0].precision == 0
    assert pd.isna(table.iloc[0].recall) and pd.isna(table.iloc[0].lift)


def test_bootstrap_is_paired_reproducible_and_does_not_mutate():
    y = np.array([0, 1] * 10)
    p = np.linspace(.1, .9, 20)
    original = p.copy()
    first = frozen_model_intervals(y, p, .5, p, repeats=30, seed=4)
    second = frozen_model_intervals(y, p, .5, p, repeats=30, seed=4)
    assert first == second
    assert first["ap_difference"]["estimate"] == 0
    assert first["ap_difference"]["lower"] == first["ap_difference"]["upper"] == 0
    np.testing.assert_array_equal(p, original)


def test_diagnostic_evidence_matches_locked_run(bundle):
    before = sha256(RUN_DIR / "metadata.json")
    summary = load_diagnostics(bundle[1])
    assert summary["run_id"] == bundle[1]["run_id"]
    assert summary["bootstrap_repeats"] == 2000
    assert summary["test_intervals"]["precision_churn"]["estimate"] == pytest.approx(302 / 595)
    assert sha256(RUN_DIR / "metadata.json") == before


def test_diagnostics_reject_tampered_evidence(tmp_path, bundle):
    shutil.copytree(ROOT / "artifacts/diagnostics", tmp_path, dirs_exist_ok=True)
    with (tmp_path / "capacity_validation.csv").open("ab") as stream:
        stream.write(b"changed")
    with pytest.raises(ValueError, match="hash"):
        load_diagnostics(bundle[1], tmp_path)


def test_diagnostics_reject_different_run(bundle):
    with pytest.raises(ValueError, match="hiện tại"):
        load_diagnostics({**bundle[1], "run_id": "another_run"})
