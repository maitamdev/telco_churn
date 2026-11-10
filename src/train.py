"""Thí nghiệm có khóa lựa chọn trước test. Chạy duy nhất: python -m src.train."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import time
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_validate
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from sklearn.inspection import permutation_importance
from sklearn.exceptions import ConvergenceWarning
from .config import ROOT, SPEC, SPEC_PATH, RAW_PATH, SPLIT_DIR, RUN_DIR, FEATURES, SEED
from .records import now, sha256, write_json, environment, log_step
from .data import load_partition
from .preprocessing import build_pipeline, churn_probability
from .evaluation import metrics, choose_threshold

def refit_index(results):
    return int(pd.DataFrame({"mean":results["mean_test_average_precision"],
                             "std":results["std_test_average_precision"]})
               .sort_values(["mean","std"],ascending=[False,True],kind="stable").index[0])

def train():
    if (RUN_DIR/"selection_record.json").exists():
        raise RuntimeError("Run đã khóa lựa chọn/test. Không ghi đè. Xem README để tái lập trong bản sao sạch.")
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    started=time.perf_counter()
    run_id="telco_"+now().replace(":","").replace("-","").replace("+","_")
    train_df, val_df = load_partition("train"), load_partition("validation")
    x, y = train_df[FEATURES], train_df.Churn.eq("Yes").astype(int)
    xv, yv = val_df[FEATURES], val_df.Churn.eq("Yes").astype(int)
    cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=SEED)
    scoring={"average_precision":"average_precision","roc_auc":"roc_auc","accuracy":"accuracy",
             "precision":make_scorer(precision_score,zero_division=0),
             "recall":make_scorer(recall_score,zero_division=0),
             "f1":make_scorer(f1_score,zero_division=0)}
    pipelines={}
    cv_summary=[]
    base=build_pipeline("baseline")
    base_cv=cross_validate(base,x,y,cv=cv,scoring=scoring,n_jobs=1,error_score="raise")
    pd.DataFrame({k:v for k,v in base_cv.items()}).to_csv(RUN_DIR/"baseline_cv.csv",index=False)
    base.fit(x,y)
    pipelines["baseline"]=base
    row={"model":"baseline","candidates":1,"best_params":{}}
    for metric in scoring:
        row[f"mean_{metric}"]=float(np.mean(base_cv["test_"+metric]))
        row[f"std_{metric}"]=float(np.std(base_cv["test_"+metric]))
    cv_summary.append(row)
    log_step("08","Pipeline và baseline",["Normalizer -> ColumnTransformer -> estimator","Imputer/scaler/encoder fit trong từng fold; Dummy most_frequent giữ dự đoán gốc"],[f"Baseline CV AP={row['mean_average_precision']:.6f}"],["src/preprocessing.py","artifacts/final_run/baseline_cv.csv"])
    print("Baseline complete.",flush=True)
    for name, spec in SPEC["experiments"]["models"].items():
        print("CV starting: "+name,flush=True)
        grid={"model__"+k:v for k,v in spec["grid"].items()}
        model=build_pipeline(name)
        search=GridSearchCV(model,grid,scoring=scoring,refit=refit_index,cv=cv,n_jobs=4,
                            return_train_score=True,error_score="raise",verbose=1)
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            search.fit(x,y)
        warning_messages=[str(w.message) for w in captured]
        # Child processes may not forward warnings; n_iter is checked on final LR as well.
        converged = not any(isinstance(w.message,ConvergenceWarning) for w in captured)
        if name=="logistic_regression" and (not converged or search.best_estimator_["model"].n_iter_.max()>=2000):
            model.set_params(model__max_iter=10000)
            search.fit(x,y)
            warning_messages.append("Retried LR max_iter=10000 before test.")
            if search.best_estimator_["model"].n_iter_.max()>=10000:
                raise RuntimeError("LR chưa hội tụ; dừng trước test.")
        pd.DataFrame(search.cv_results_).to_csv(RUN_DIR/f"{name}_cv_results.csv",index=False)
        pipelines[name]=search.best_estimator_
        idx=search.best_index_
        row={"model":name,"candidates":len(search.cv_results_["params"]),"best_params":search.best_params_}
        for metric in scoring:
            row[f"mean_{metric}"]=float(search.cv_results_["mean_test_"+metric][idx])
            row[f"std_{metric}"]=float(search.cv_results_["std_test_"+metric][idx])
        cv_summary.append(row)
        write_json(RUN_DIR/f"{name}_search_notes.json",{"warnings":warning_messages,"best_index":int(idx),
                    "refit": "highest mean AP, lowest std AP; stable first exact tie"})
        print(f"CV complete: {name}; AP={row['mean_average_precision']:.6f}",flush=True)
    write_json(RUN_DIR/"cv_summary.json",cv_summary)
    pd.DataFrame(cv_summary).drop(columns="best_params").to_csv(RUN_DIR/"cv_summary.csv",index=False)
    log_step("09","Tuning hai mô hình",["5-fold stratified CV trên train; 8 cấu hình LR + 18 RF","Chọn bằng mean AP, dùng std AP phá hòa; lưu mọi cấu hình và train/CV score"],[f"{r['model']}: AP={r['mean_average_precision']:.6f} ± {r['std_average_precision']:.6f}" for r in cv_summary],["artifacts/final_run/cv_summary.json","artifacts/final_run/logistic_regression_cv_results.csv","artifacts/final_run/random_forest_cv_results.csv"],["Độ lệch chuẩn giữa fold không phải khoảng tin cậy."])
    candidates=[r for r in cv_summary if r["model"]!="baseline"]
    winner=sorted(candidates,key=lambda r:(-r["mean_average_precision"],r["std_average_precision"],0 if r["model"]=="logistic_regression" else 1))[0]
    name=winner["model"]
    chosen=pipelines[name]
    val_predictions=pd.DataFrame({"customerID":val_df.customerID,"y_true":yv})
    threshold_records={}
    for key, pipeline in pipelines.items():
        proba=churn_probability(pipeline,xv)
        val_predictions[key+"_probability"]=proba
        if key!="baseline":
            rec,sweep=choose_threshold(yv,proba)
            threshold_records[key]=rec
            sweep.to_csv(RUN_DIR/f"{key}_threshold_sweep.csv",index=False)
    val_predictions.to_csv(RUN_DIR/"validation_predictions.csv",index=False)
    selection={
        "run_id":run_id,"frozen_at":now(),"dataset_sha256":sha256(RAW_PATH),
        "split_manifest_sha256":sha256(SPLIT_DIR/"split_manifest.json"),"spec_sha256":sha256(SPEC_PATH),
        "selected_model":name,"best_params":winner["best_params"],
        "selection_rule":"Train CV mean AP desc; std AP asc; LR on exact tie. No test-based promotion.",
        "selected_threshold":threshold_records[name]["threshold"],"threshold_records":threshold_records,
        "cv_summary":cv_summary,"test_opened":False,"refit_train_plus_validation":False,
    }
    write_json(RUN_DIR/"selection_record.json",selection)
    selection_hash=sha256(RUN_DIR/"selection_record.json")
    log_step("10","Khóa mô hình và ngưỡng trước test",["Chọn mô hình theo train CV","Chọn ngưỡng trên validation; lưu selection_record trước khi đọc test"],[f"Mô hình: {name}",f"Ngưỡng: {selection['selected_threshold']:.10f}",str(threshold_records[name])],["artifacts/final_run/selection_record.json","artifacts/final_run/validation_predictions.csv"])
    print("Selection frozen. Opening test once for fixed evaluation.",flush=True)

    test_opened_at=now()
    test_df=load_partition("test")
    xt, yt=test_df[FEATURES],test_df.Churn.eq("Yes").astype(int)
    test_predictions=pd.DataFrame({"customerID":test_df.customerID,"y_true":yt})
    all_metrics=[]
    for key,pipeline in pipelines.items():
        probability=churn_probability(pipeline,xt)
        test_predictions[key+"_probability"]=probability
        if key=="baseline":
            pred=pipeline.predict(xt)
            test_predictions[key+"_native"]=pred
            all_metrics.append({"model":key,"operating_point":"native_most_frequent",**metrics(yt,probability,predictions=pred)})
        else:
            for label,threshold in [("default_0.5",.5),("validation_selected",threshold_records[key]["threshold"])]:
                test_predictions[key+"_"+label]=(probability>=threshold).astype(int)
                all_metrics.append({"model":key,"operating_point":label,**metrics(yt,probability,threshold)})
    test_predictions.to_csv(RUN_DIR/"test_predictions.csv",index=False)
    pd.DataFrame(all_metrics).to_csv(RUN_DIR/"test_metrics.csv",index=False)
    write_json(RUN_DIR/"test_metrics.json",{"run_id":run_id,"test_opened_at":test_opened_at,
               "selection_record_sha256":selection_hash,"partition":"test","metrics":all_metrics})
    print("Computing validation permutation importance...",flush=True)
    importance=permutation_importance(chosen,xv,yv,scoring="average_precision",n_repeats=20,random_state=SEED,n_jobs=2)
    imp=pd.DataFrame({"feature":FEATURES,"importance_mean":importance.importances_mean,"importance_std":importance.importances_std}).sort_values("importance_mean",ascending=False)
    imp.to_csv(RUN_DIR/"permutation_importance_validation.csv",index=False)
    pd.DataFrame(importance.importances,index=FEATURES).to_csv(RUN_DIR/"permutation_repeats_validation.csv")
    probability=test_predictions[name+"_probability"].to_numpy()
    pred=(probability>=selection["selected_threshold"]).astype(int)
    cases=test_df.copy()
    cases["y_true"]=yt
    cases["probability"]=probability
    cases["prediction"]=pred
    cases["outcome"]=np.select([(yt==0)&(pred==0),(yt==0)&(pred==1),(yt==1)&(pred==0),(yt==1)&(pred==1)],["TN","FP","FN","TP"],default="unknown")
    cases["distance_from_threshold"]=np.abs(probability-selection["selected_threshold"])
    # Max 10, gồm lỗi tự tin nhất và sát ngưỡng; không chọn bằng tay.
    selected_cases=[]
    for outcome in ["FP","FN"]:
        group=cases[cases.outcome.eq(outcome)]
        take=pd.concat([group.nlargest(3,"distance_from_threshold"),group.nsmallest(2,"distance_from_threshold")]).drop_duplicates("customerID")
        selected_cases.append(take)
    pd.concat(selected_cases).to_csv(RUN_DIR/"error_cases.csv",index=False)
    subgroup=[]
    for feature in ["Contract","InternetService","gender","SeniorCitizen"]:
        for value,part in cases.groupby(feature,observed=True):
            subgroup.append({"feature":feature,"group":value,**metrics(part.y_true,part.probability,selection["selected_threshold"])})
    pd.DataFrame(subgroup).to_csv(RUN_DIR/"subgroup_metrics.csv",index=False)
    log_step("11","Đánh giá cố định và phân tích lỗi",["Đánh giá test tại 0.5 và ngưỡng đã khóa","Permutation importance trên validation, 20 lần; xuất FP/FN và thống kê nhóm"],[str(r) for r in all_metrics if r["model"] in ["baseline",name]],["artifacts/final_run/test_metrics.json","artifacts/final_run/test_predictions.csv","artifacts/final_run/permutation_importance_validation.csv","artifacts/final_run/error_cases.csv","artifacts/final_run/subgroup_metrics.csv"],["Test dùng mô tả kết quả, không đổi mô hình/ngưỡng sau khi xem.","Importance không chứng minh nhân quả; các biến tương quan có thể chia sẻ thông tin."])
    joblib.dump(chosen,RUN_DIR/"churn_pipeline.joblib",compress=3)
    loaded=joblib.load(RUN_DIR/"churn_pipeline.joblib")
    max_difference=float(np.max(np.abs(churn_probability(loaded,xv)-churn_probability(chosen,xv))))
    if max_difference>1e-12:
        raise RuntimeError("Save/load parity failed.")
    env=environment()
    write_json(RUN_DIR/"environment.json",env)
    metadata={**selection,"test_opened":True,"test_opened_at":test_opened_at,
              "pipeline_sha256":sha256(RUN_DIR/"churn_pipeline.joblib"),
              "selection_record_sha256":selection_hash,"features":FEATURES,
              "classes":[int(c) for c in chosen.classes_],"probability_class":1,
              "probability_calibrated":False,"trained_rows":len(x),
              "save_load_max_abs_difference":max_difference,
              "elapsed_seconds":round(time.perf_counter()-started,2),"environment":env}
    write_json(RUN_DIR/"metadata.json",metadata)
    write_json(RUN_DIR/"artifact_manifest.json",{p.name:sha256(p) for p in sorted(RUN_DIR.iterdir()) if p.is_file() and p.name!="artifact_manifest.json"})
    log_step("12","Đóng gói pipeline",["Lưu toàn bộ pipeline và metadata/hash/environment","Load lại và so toàn bộ xác suất validation"],[f"Sai khác lớn nhất={max_difference}",f"Thời gian thí nghiệm={metadata['elapsed_seconds']} giây"],["artifacts/final_run/churn_pipeline.joblib","artifacts/final_run/metadata.json","artifacts/final_run/artifact_manifest.json"])
    print(f"Completed {run_id}; winner={name}; threshold={selection['selected_threshold']:.8f}",flush=True)

if __name__=="__main__":
    train()

