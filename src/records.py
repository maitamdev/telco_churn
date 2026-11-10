"""Lưu bằng chứng, provenance và nhật ký sau từng bước."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import sys
from .config import ROOT

TZ = timezone(timedelta(hours=7))

def now():
    return datetime.now(TZ).isoformat(timespec="seconds")

def sha256(path):
    # Stream large datasets/models instead of allocating a complete second copy.
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False, default=str) + "\n"
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def environment():
    packages = {}
    for p in ["numpy", "pandas", "scikit-learn", "matplotlib", "seaborn", "joblib", "streamlit", "pytest", "nbformat", "nbclient"]:
        try:
            packages[p] = importlib.metadata.version(p)
        except importlib.metadata.PackageNotFoundError:
            packages[p] = None
    return {"recorded_at": now(), "python": platform.python_version(), "platform": platform.platform(),
            "executable": sys.executable, "packages": packages}

def log_step(step, title, actions, results, evidence, limitations=None):
    """Append-only: chạy lại tạo một sự kiện mới, không xóa lịch sử trước."""
    event = {"time": now(), "step": step, "title": title, "actions": actions,
             "results": results, "evidence": evidence, "limitations": limitations or [],
             "performed_by": "OpenAI Codex; nhóm sinh viên chưa ghi nhận tự kiểm chứng"}
    directory = ROOT / "logs"
    directory.mkdir(exist_ok=True)
    with (directory / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
    parts = [f"\n## {step} · {title}", f"\nThời điểm: {event['time']} (UTC+7).", "\nĐã thực hiện:"]
    parts += [f"- {s}" for s in actions]
    parts += ["\nKết quả:"] + [f"- {s}" for s in results]
    parts += ["\nTệp bằng chứng:"] + [f"- `{s}`" for s in evidence]
    if limitations:
        parts += ["\nGiới hạn / việc còn lại:"] + [f"- {s}" for s in limitations]
    parts += ["\nThực hiện với hỗ trợ OpenAI Codex; đóng góp và việc tự kiểm chứng của nhóm cần được ghi bổ sung.\n"]
    with (directory / "NHAT_KY_THUC_HIEN.md").open("a", encoding="utf-8") as f:
        f.write("\n".join(parts))
