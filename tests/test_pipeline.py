import shutil
import numpy as np
import pandas as pd
import pytest
from src.config import FEATURES, NUMERIC, RUN_DIR, RAW_PATH, SPLIT_DIR
from src.data import load_partition
from src.records import read_json,sha256
from src.validation import normalize_features
from src.preprocessing import churn_probability
from src.inference import load_bundle,predict_batch,ArtifactError

def test_splits_disjoint_and_complete():
    groups=[load_partition(n) for n in ["train","validation","test"]]
    ids=[set(d.customerID) for d in groups]
    assert [len(d) for d in groups]==[4225,1409,1409]
    assert not ids[0]&ids[1] and not ids[0]&ids[2] and not ids[1]&ids[2]
    assert len(set.union(*ids))==7043

def test_median_comes_from_train_only(bundle):
    pipeline,_=bundle
    expected=normalize_features(load_partition("train"))[NUMERIC].median().to_numpy()
    actual=pipeline["preprocess"].named_transformers_["numeric"]["imputer"].statistics_
    np.testing.assert_allclose(actual,expected,rtol=0,atol=1e-12)

def test_id_target_excluded(bundle,sample):
    pipeline,_=bundle
    before=churn_probability(pipeline,sample)
    sample["customerID"]="completely-different-id"
    sample["Churn"]="Yes"
    np.testing.assert_array_equal(before,churn_probability(pipeline,sample))
    assert pipeline["normalize"].n_features_in_==19

def test_holdout_transform_never_refits(bundle,sample):
    pipeline,_=bundle
    imputer=pipeline["preprocess"].named_transformers_["numeric"]["imputer"]
    old=imputer.statistics_.copy()
    modified=sample.copy()
    modified["TotalCharges"]="999999999"
    churn_probability(pipeline,modified)
    np.testing.assert_array_equal(imputer.statistics_,old)

def test_all_saved_test_probabilities_match_model(bundle):
    pipeline,meta=bundle
    df=load_partition("test")
    saved=pd.read_csv(RUN_DIR/"test_predictions.csv")
    actual=churn_probability(pipeline,df[FEATURES])
    np.testing.assert_allclose(actual,saved[meta["selected_model"]+"_probability"],rtol=0,atol=1e-12)

def test_selection_integrity_and_timing(bundle):
    _,meta=bundle
    selection=read_json(RUN_DIR/"selection_record.json")
    assert selection["test_opened"] is False
    assert selection["frozen_at"]<=meta["test_opened_at"]
    assert not selection["refit_train_plus_validation"]
    assert meta["selection_record_sha256"]==sha256(RUN_DIR/"selection_record.json")

def test_batch_preserves_bad_rows_and_order(bundle,sample):
    p,m=bundle
    sample.index=list(range(10,10+len(sample)))
    sample.loc[11,"tenure"]="-2"
    out,_=predict_batch(sample,p,m)
    assert len(out)==len(sample)
    assert out.customerID.tolist()==sample.customerID.tolist()
    assert out.prediction_status.tolist().count("invalid")==1
    assert np.isnan(out.loc[1,"estimated_churn_probability"])
    assert out.loc[1,"predicted_churn"]==""
    assert out.loc[0,"prediction_status"]=="ok"

def test_single_batch_parity(bundle,sample):
    p,m=bundle
    many,_=predict_batch(sample,p,m)
    one,_=predict_batch(sample.iloc[[0]],p,m)
    assert one.iloc[0].estimated_churn_probability==many.iloc[0].estimated_churn_probability

def test_all_invalid_never_calls_model(sample,bundle):
    class Forbidden:
        def predict_proba(self,x):
            raise AssertionError("Should never score invalid rows")
    sample["tenure"]="-1"
    result,_=predict_batch(sample,Forbidden(),bundle[1])
    assert result.estimated_churn_probability.isna().all()

def test_no_model_fallback_on_tamper(tmp_path):
    for file in RUN_DIR.iterdir():
        if file.is_file():
            shutil.copy2(file,tmp_path/file.name)
    with (tmp_path/"churn_pipeline.joblib").open("ab") as f:
        f.write(b"corruption")
    with pytest.raises(ArtifactError,match="hash"):
        load_bundle(tmp_path)

def test_missing_artifacts_fail_clearly(tmp_path):
    with pytest.raises(ArtifactError):
        load_bundle(tmp_path)

def test_output_column_collision_rejected(bundle,sample):
    sample["predicted_churn"]="previous"
    with pytest.raises(ValueError,match="trùng"):
        predict_batch(sample,*bundle)


def test_range_warnings_only_for_valid_nonmissing_values(bundle,sample):
    sample.loc[0,"tenure"]="999"
    sample.loc[0,"MonthlyCharges"]="999"
    sample.loc[0,"TotalCharges"]=""
    sample.loc[1,"tenure"]="999"
    sample.loc[1,"MonthlyCharges"]="-1"
    out,_=predict_batch(sample,*bundle)
    assert out.loc[0,"range_warnings"]=="Ngoài khoảng train: tenure, MonthlyCharges"
    assert out.loc[1,"prediction_status"]=="invalid"
    assert out.loc[1,"range_warnings"]==""
    assert np.isnan(out.loc[1,"estimated_churn_probability"])


@pytest.mark.parametrize("partition",["validation","test"])
def test_batch_predictions_match_every_saved_holdout_row(bundle,partition):
    frame=load_partition(partition)
    out,_=predict_batch(frame,*bundle)
    saved=pd.read_csv(RUN_DIR/f"{partition}_predictions.csv")
    np.testing.assert_array_equal(out.customerID,saved.customerID)
    assert out.prediction_status.eq("ok").all()
    np.testing.assert_allclose(out.estimated_churn_probability,
        saved[bundle[1]["selected_model"]+"_probability"],rtol=0,atol=1e-12)

