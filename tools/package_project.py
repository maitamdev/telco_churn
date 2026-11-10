"""Đóng gói bundle kỹ thuật, không kèm venv/cache; xác minh toàn bộ thành viên ZIP."""
from pathlib import Path
import hashlib
import os
import json
import zipfile
import xml.etree.ElementTree as ET
from src.config import ROOT,RUN_DIR
from src.records import sha256,read_json,write_json,now,log_step
from src.inference import load_bundle

EXCLUDE_DIRS={".venv",".venv_verify",".reproduction",".pytest_cache","__pycache__",".ipynb_checkpoints",".git","dist","tmp"}
MANIFEST=ROOT/"reports/evidence/package_manifest.json"

def files_to_ship():
    files=[]
    for base,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in EXCLUDE_DIRS]
        for name in names:
            path=Path(base)/name
            if path==MANIFEST or name.startswith("~$") or name.endswith((".pyc",".tmp")):
                continue
            if name==".env" or (name.startswith(".env.") and name!=".env.example"):
                continue
            if path==ROOT/".streamlit/secrets.toml":
                continue
            if path.parent.name=="logs" and name.startswith("server"):
                continue
            files.append(path)
    return sorted(files)

def build_zip(path):
    files=files_to_ship()
    entries={p.relative_to(ROOT).as_posix():sha256(p) for p in files}
    write_json(MANIFEST,{"created_at":now(),"root_folder":ROOT.name,"files":entries,
                        "note":"SHA-256 cho từng tệp; manifest không tự hash chính nó."})
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for item in files+[MANIFEST]:
            archive.write(item,ROOT.name+"/"+item.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(path,"r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError("ZIP CRC failed.")
        expected={ROOT.name+"/"+name for name in entries}|{ROOT.name+"/"+MANIFEST.relative_to(ROOT).as_posix()}
        if set(archive.namelist())!=expected:
            raise RuntimeError("ZIP inventory mismatch.")
        for name,digest in entries.items():
            if hashlib.sha256(archive.read(ROOT.name+"/"+name)).hexdigest()!=digest:
                raise RuntimeError("ZIP member hash mismatch: "+name)
    return len(files)+1

def check_test_reports(paths):
    """Require the same complete, passing test suite in both environments."""
    counts=[]
    identities=[]
    for path in paths:
        tree=ET.parse(path)
        suites=list(tree.getroot().iter("testsuite"))
        total=sum(int(x.attrib.get("tests",0)) for x in suites)
        failed=sum(int(x.attrib.get("failures",0))+int(x.attrib.get("errors",0)) for x in suites)
        skipped=sum(int(x.attrib.get("skipped",0)) for x in suites)
        cases=list(tree.getroot().iter("testcase"))
        ids={(case.get("classname"),case.get("name")) for case in cases}
        if not total or failed or skipped or total!=len(ids) or len(cases)!=total:
            raise RuntimeError("Tests not complete: "+str(path))
        if any(case.find(tag) is not None for case in cases for tag in ("failure","error","skipped")):
            raise RuntimeError("Tests not complete: "+str(path))
        counts.append(total)
        identities.append(ids)
    if len(identities)!=2 or identities[0]!=identities[1]:
        raise RuntimeError("Main and clean environment test suites do not match.")
    return counts


def check_evidence():
    load_bundle()
    directory=ROOT/"reports/evidence"
    names=(["pytest_optimized.xml","pytest_optimized_clean.xml"]
           if (directory/"pytest_optimized.xml").exists()
           else ["pytest.xml","pytest_clean_env.xml"])
    counts=check_test_reports([directory/name for name in names])
    if read_json(ROOT/"reports/evidence/full_reproduction.json")["status"]!="passed":
        raise RuntimeError("Full reproduction not passed.")
    if not read_json(ROOT/"reports/evidence/notebook_execution.json")["all_executed"]:
        raise RuntimeError("Notebook not executed.")
    if not list((ROOT/"reports/evidence").glob("ui_*.jpg")):
        raise RuntimeError("Missing browser evidence.")
    return counts

def package():
    test_count,clean_test_count=check_evidence()
    report_path=ROOT/"reports/BAOCAO-TTNT.docx"
    report_qa_path=ROOT/"reports/evidence/report_qa.json"
    report_qa=read_json(report_qa_path) if report_qa_path.exists() else {}
    report_ready=(report_path.exists() and report_qa.get("status")=="passed"
                  and report_qa.get("document_sha256")==sha256(report_path))
    report_summary=(f"Báo cáo DOCX {report_qa['pages']} trang đã viết và kiểm tra theo mẫu; thông tin cá nhân/giảng viên để trống theo yêu cầu."
                    if report_ready else "Báo cáo DOCX chưa có xác nhận kiểm tra cho phiên bản hiện tại.")
    dist=ROOT/"dist"
    dist.mkdir(exist_ok=True)
    path=dist/"DU_AN_TELCO_CHURN_KY_THUAT.zip"
    # Xác minh một gói thực trước khi ghi hoàn thành bước 18.
    build_zip(path)
    log_step("18","Tổng hợp và đóng gói kỹ thuật",
        ["Kiểm đủ bằng chứng tests, notebook, tái lập và trình duyệt","Tạo ZIP không kèm môi trường/cache; kiểm CRC và SHA-256 từng thành viên","Ghi trạng thái và việc còn lại, đóng gói lại để chứa nhật ký hoàn chỉnh"],
        ["18/18 bước kỹ thuật có bằng chứng","ZIP kỹ thuật đã kiểm tính toàn vẹn"],
        ["dist/DU_AN_TELCO_CHURN_KY_THUAT.zip","dist/DU_AN_TELCO_CHURN_KY_THUAT.sha256","dist/package_verification.json","reports/evidence/package_manifest.json","docs/BANG_CHUNG_CHO_BAO_CAO.md","docs/AI_USAGE.md"],
        [report_summary,"Chưa có slide; nhóm cần bổ sung thông tin và đóng góp thực, đọc lại báo cáo và chuẩn bị bảo vệ."])
    events=[json.loads(line) for line in (ROOT/"logs/events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    steps={e["step"]:{"title":e["title"],"status":"completed","recorded_at":e["time"],"evidence":e["evidence"]} for e in events}
    status={"updated_at":now(),"technical_steps_total":18,"technical_steps_completed":18,
            "steps":{k:steps[k] for k in sorted(steps)},
            "model_run_id":read_json(RUN_DIR/"metadata.json")["run_id"],
            "tests_passed":test_count,"clean_environment_tests_passed":clean_test_count,"full_reproduction":"passed",
            "interface_version":"2.0","report_written":report_ready,"slides_written":False,
            "report_template":"reports/templates/MAU_BAO_CAO_GOC.docx" if report_ready else "pending_user",
            "report_file":"reports/BAOCAO-TTNT.docx" if report_ready else None,
            "report_pages":report_qa.get("pages") if report_ready else None,
            "report_qa":"reports/evidence/report_qa.json" if report_ready else None,
            "student_review_and_contribution":"not_yet_recorded","deployed":False,
            "requirements_audit":"reports/KIEM_TRA_YEU_CAU_CUOI_KY.md" if (ROOT/"reports/KIEM_TRA_YEU_CAU_CUOI_KY.md").exists() else None,
            "report_outline":"reports/DAN_Y_BAO_CAO_CHI_TIET.md" if (ROOT/"reports/DAN_Y_BAO_CAO_CHI_TIET.md").exists() else None,
            "ready_for":"Nhóm đọc lại báo cáo 6 chương, bổ sung thông tin/đóng góp thực, chuẩn bị slide và bảo vệ." if report_ready else "Nhóm kiểm chứng/chỉnh sửa và chuẩn bị báo cáo theo mẫu."}
    if set(steps)!={f"{i:02}" for i in range(1,19)}:
        raise RuntimeError("Missing implementation step logs.")
    write_json(ROOT/"configs/execution_status.json",status)
    lines=["# Trạng thái hiện tại",f"\nCập nhật: {status['updated_at']}. 18/18 bước kỹ thuật hoàn thành và có bằng chứng.\n",
           "| Phần | Bước | Trạng thái |","|---|---|---|",
           "| Môi trường | 01–02 | Đã kiểm |","| Dữ liệu | 03–05 | Đã kiểm |",
           "| EDA | 06–07 | Đã kiểm |","| Mô hình và đánh giá | 08–12 | Đã kiểm |",
           "| Streamlit | 13–14 | Đã kiểm |","| Kiểm thử và bàn giao | 15–18 | Đã kiểm |",
           f"\n{test_count} tests đạt ở môi trường chính và {clean_test_count} tests đạt ở venv kiểm chứng. Bằng chứng tái huấn luyện ban đầu cho sai khác CV/metrics/xác suất = 0. Notebook thực thi đủ 6 ô mã.",
           "\nNhật ký chi tiết: logs/NHAT_KY_THUC_HIEN.md. Gói ZIP là bộ kỹ thuật, chưa phải bộ nộp cuối.",
           "\nĐối chiếu hướng dẫn và việc còn thiếu: reports/KIEM_TRA_YEU_CAU_CUOI_KY.md. 18/18 bước không đồng nghĩa hoàn tất báo cáo, slide hoặc yêu cầu đóng góp/bảo vệ.",
           "\n"+report_summary,
           "\nBáo cáo hiện tại: reports/BAOCAO-TTNT.docx. Sáu chương theo mẫu đã nhận; mục lục và danh mục hình/bảng tự động; tài liệu tham khảo ở cuối; không có phụ lục." if report_ready else "\nXem dàn ý tại reports/DAN_Y_BAO_CAO_CHI_TIET.md.",
           "\nCòn lại: thông tin nhóm/giảng viên; đóng góp tự thực hiện và việc đọc/kiểm chứng của 5 người; slide và luyện bảo vệ. Chưa deploy."]
    (ROOT/"docs/TIEN_DO_HIEN_TAI.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    count=build_zip(path)
    digest=sha256(path)
    (dist/"DU_AN_TELCO_CHURN_KY_THUAT.sha256").write_text(digest+"  "+path.name+"\n",encoding="ascii")
    write_json(dist/"package_verification.json",{"verified_at":now(),"status":"passed","archive":path.name,
              "files":count,"bytes":path.stat().st_size,"archive_sha256":digest,"crc_passed":True,
              "all_member_hashes_passed":True,"excluded":sorted(EXCLUDE_DIRS)})
    print(f"Verified technical ZIP: {count} files; {path.stat().st_size} bytes; SHA256={digest}",flush=True)

if __name__=="__main__":
    package()

