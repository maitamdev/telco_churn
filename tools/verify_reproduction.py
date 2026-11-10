"""Tái lập đầy đủ trong bản sao riêng; không ghi đè run chính hoặc chọn lại bằng test."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import numpy as np
import pandas as pd
from src.config import ROOT,RUN_DIR
from src.records import read_json,write_json,now,environment

def run():
    parent=ROOT/".reproduction"
    parent.mkdir(exist_ok=True)
    target=Path(tempfile.mkdtemp(prefix="fixed_spec_",dir=parent))
    for name in ["src","configs"]:
        shutil.copytree(ROOT/name,target/name,ignore=shutil.ignore_patterns("__pycache__"))
    for name in ["raw","splits"]:
        shutil.copytree(ROOT/"data"/name,target/"data"/name)
    (target/"logs").mkdir()
    with (ROOT/"logs/reproduction_training.log").open("w",encoding="utf-8") as log:
        result=subprocess.run([sys.executable,"-X","utf8","-u","-m","src.train"],cwd=target,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError("Reproduction training failed; see logs/reproduction_training.log")
    original=read_json(RUN_DIR/"metadata.json")
    replica=read_json(target/"artifacts/final_run/metadata.json")
    assert original["selected_model"]==replica["selected_model"]
    assert original["best_params"]==replica["best_params"]
    assert abs(original["selected_threshold"]-replica["selected_threshold"])<1e-12
    differences={}
    for filename in ["validation_predictions.csv","test_predictions.csv","test_metrics.csv","cv_summary.csv"]:
        left=pd.read_csv(RUN_DIR/filename)
        right=pd.read_csv(target/"artifacts/final_run"/filename)
        assert list(left.columns)==list(right.columns) and left.shape==right.shape
        numeric=left.select_dtypes(include="number").columns
        differences[filename]=float(np.max(np.abs(left[numeric].to_numpy()-right[numeric].to_numpy())))
        np.testing.assert_allclose(left[numeric],right[numeric],rtol=0,atol=1e-12)
        for col in left.columns.difference(numeric):
            assert left[col].equals(right[col])
    write_json(ROOT/"reports/evidence/full_reproduction.json",{
        "time":now(),"status":"passed","purpose":"Tái lập cấu hình cố định; không tối ưu lại theo test.",
        "replica_directory":str(target.relative_to(ROOT)),"original_run_id":original["run_id"],"replica_run_id":replica["run_id"],
        "selected_model_identical":True,"best_params_identical":True,"threshold_identical":True,
        "max_absolute_difference":differences,"environment":environment()})
    print("Full fixed-spec reproduction PASSED. Max differences:",differences,flush=True)

if __name__=="__main__":
    run()

