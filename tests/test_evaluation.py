import numpy as np
import pytest
from src.evaluation import threshold_sweep,choose_threshold,metrics
from src.train import refit_index

def test_sweep_matches_bruteforce_including_boundary():
    y=np.array([0,1,1,0,1,0])
    p=np.array([0,.5,.5,1,1,.2])
    sweep=threshold_sweep(y,p)
    for row in sweep.itertuples():
        m=metrics(y,p,row.threshold)
        for field in ["precision_churn","recall_churn","f1_churn","flagged_count","tp"]:
            assert getattr(row,field)==pytest.approx(m[field])

def test_threshold_meets_declared_rule():
    y=[0,0,1,1,1,0]; p=[.1,.2,.3,.4,.8,.9]
    chosen,sweep=choose_threshold(y,p)
    feasible=sweep[(sweep.precision_churn>=.5)&(sweep.flagged_count>=1)]
    best=feasible.sort_values(["recall_churn","precision_churn","threshold"],ascending=False).iloc[0]
    assert chosen["threshold"]==best.threshold

def test_no_positive_falls_back_honestly():
    chosen,_=choose_threshold([0,0],[.2,.3])
    assert chosen["threshold"]==.5
    assert chosen["status"]=="precision_constraint_not_met_research_demo_only"
    assert not chosen["aspirational_recall_met"]

def test_baseline_native_prediction_is_preserved():
    m=metrics([0,1],[.8,.8],predictions=[0,0])
    assert m["flagged_count"]==0 and m["recall_churn"]==0

def test_cv_tie_break_uses_std():
    assert refit_index({"mean_test_average_precision":[.7,.7,.6],"std_test_average_precision":[.02,.01,0]})==1

@pytest.mark.parametrize("proba",[[float("nan")],[1.1],[-.1]])
def test_bad_probabilities_rejected(proba):
    with pytest.raises(ValueError):
        threshold_sweep([1],proba)

