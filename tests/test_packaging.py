import xml.etree.ElementTree as ET

import pytest

from tools.package_project import check_test_reports


def report(path, names, **counts):
    suite = ET.Element("testsuite", tests=str(len(names)), failures="0", errors="0", skipped="0")
    suite.attrib.update({key: str(value) for key, value in counts.items()})
    for name in names:
        ET.SubElement(suite, "testcase", classname="tests.test_example", name=name)
    ET.ElementTree(suite).write(path)
    return path


def test_packaging_accepts_growing_matching_suites(tmp_path):
    names = [f"test_{i}" for i in range(70)]
    paths = [report(tmp_path / name, names) for name in ("main.xml", "clean.xml")]
    assert check_test_reports(paths) == [70, 70]


@pytest.mark.parametrize("counts", [{"failures": 1}, {"errors": 1}, {"skipped": 1}, {"tests": 0}, {"tests": 99}])
def test_packaging_rejects_incomplete_tests(tmp_path, counts):
    paths = [report(tmp_path / "main.xml", ["test_one"], **counts),
             report(tmp_path / "clean.xml", ["test_one"])]
    with pytest.raises(RuntimeError, match="not complete"):
        check_test_reports(paths)


def test_packaging_rejects_different_tests_with_same_count(tmp_path):
    paths = [report(tmp_path / "main.xml", ["test_one"]),
             report(tmp_path / "clean.xml", ["test_other"])]
    with pytest.raises(RuntimeError, match="do not match"):
        check_test_reports(paths)


def test_package_excludes_local_secrets(tmp_path, monkeypatch):
    from tools import package_project

    monkeypatch.setattr(package_project, "ROOT", tmp_path)
    (tmp_path / ".streamlit").mkdir()
    (tmp_path / ".chart-data-private").mkdir()
    (tmp_path / ".chart-data-private" / "temporary.xlsx").write_bytes(b"temporary")
    for name in ("app.py", ".env", ".env.local", ".env.example", ".streamlit/secrets.toml"):
        (tmp_path / name).write_text("fixture", encoding="utf-8")
    assert {p.name for p in package_project.files_to_ship()} == {"app.py", ".env.example"}
