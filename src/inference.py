"""Nạp artifact đáng tin cậy tại chỗ và suy luận dùng chung UI/tests."""
from pathlib import Path
import importlib.metadata
import joblib
import numpy as np
import pandas as pd
from .config import RUN_DIR, RAW_PATH, SPEC_PATH, SPLIT_DIR, EDA_DIR, FEATURES
from .records import read_json, sha256
from .preprocessing import churn_probability
from .validation import validate_frame

class ArtifactError(RuntimeError):
    pass

def load_bundle(directory=RUN_DIR):
    directory=Path(directory)
    try:
        manifest=read_json(directory/"artifact_manifest.json")
        required={"churn_pipeline.joblib","metadata.json","selection_record.json","test_metrics.json",
                  "test_predictions.csv","validation_predictions.csv","cv_summary.csv",
                  "permutation_importance_validation.csv","error_cases.csv","subgroup_metrics.csv"}
        if not required.issubset(manifest):
            raise ArtifactError("Manifest thiếu artifact bắt buộc.")
        for name,digest in manifest.items():
            if Path(name).name!=name or sha256(directory/name)!=digest:
                raise ArtifactError(f"Artifact sai hash hoặc tên: {name}")
        metadata=read_json(directory/"metadata.json")
        selection=read_json(directory/"selection_record.json")
        evaluation=read_json(directory/"test_metrics.json")
        if not metadata["run_id"]==selection["run_id"]==evaluation["run_id"]:
            raise ArtifactError("Các artifact không thuộc cùng một run.")
        if sha256(directory/"selection_record.json")!=metadata["selection_record_sha256"]:
            raise ArtifactError("Selection record đã bị thay đổi.")
        if sha256(directory/"churn_pipeline.joblib")!=metadata["pipeline_sha256"]:
            raise ArtifactError("Pipeline không khớp metadata.")
        for path,key in [(RAW_PATH,"dataset_sha256"),(SPEC_PATH,"spec_sha256"),(SPLIT_DIR/"split_manifest.json","split_manifest_sha256")]:
            if sha256(path)!=metadata[key]:
                raise ArtifactError(f"Dữ liệu/cấu hình không khớp run: {path.name}")
        for name,part in read_json(SPLIT_DIR/"split_manifest.json")["partitions"].items():
            if sha256(SPLIT_DIR/f"{name}.csv")!=part["file_sha256"]:
                raise ArtifactError("Nội dung split đã bị sửa: "+name)
        if importlib.metadata.version("scikit-learn")!=metadata["environment"]["packages"]["scikit-learn"]:
            raise ArtifactError("Phiên bản scikit-learn khác lúc huấn luyện. Cài requirements.txt.")
        # Chỉ joblib nội bộ có provenance. Không bao giờ nhận file model từ upload.
        pipeline=joblib.load(directory/"churn_pipeline.joblib")
        if list(pipeline.classes_)!=[0,1] or metadata["features"]!=FEATURES:
            raise ArtifactError("Lớp/schema pipeline không đúng.")
        return pipeline,metadata
    except ArtifactError:
        raise
    except (OSError,KeyError,ValueError,TypeError) as exc:
        raise ArtifactError("Thiếu hoặc hỏng artifact. Xem README và chạy đủ thí nghiệm.") from exc

def predict_batch(frame,pipeline,metadata):
    validated=validate_frame(frame)
    out=frame.reset_index(drop=True).copy()
    # Tránh ghi đè dữ liệu người dùng có cột cùng tên với kết quả.
    result_cols=["row_number","prediction_status","estimated_churn_probability","predicted_churn",
                 "threshold_used","validation_errors","range_warnings"]
    collisions=set(out.columns)&set(result_cols)
    if collisions:
        raise ValueError("Cột đầu vào trùng cột kết quả: "+", ".join(sorted(collisions)))
    out.insert(0,"row_number",np.arange(1,len(out)+1))
    mask=validated.valid_mask
    out["prediction_status"]=np.where(mask,"ok","invalid")
    out["estimated_churn_probability"]=np.nan
    out["predicted_churn"]=""
    out["threshold_used"]=float(metadata["selected_threshold"])
    out["validation_errors"]=["; ".join(e) for e in validated.errors]
    out["range_warnings"]=""
    if mask.any():
        p=churn_probability(pipeline,frame.loc[mask,FEATURES])
        if not np.isfinite(p).all() or ((p<0)|(p>1)).any():
            raise ArtifactError("Pipeline trả xác suất không hợp lệ.")
        out.loc[mask,"estimated_churn_probability"]=p
        out.loc[mask,"predicted_churn"]=np.where(p>=metadata["selected_threshold"],"Yes","No")
        reference=read_json(EDA_DIR/"numeric_reference.json")["features"]
        warnings=[[] for _ in range(len(out))]
        for c,limits in reference.items():
            values=validated.frame[c]
            outside=mask & values.notna() & ~values.between(limits["min"],limits["max"])
            for i in np.flatnonzero(outside):
                warnings[i].append(c)
        out["range_warnings"]=["Ngoài khoảng train: "+", ".join(cols) if cols else "" for cols in warnings]
    return out,validated.extra_columns

