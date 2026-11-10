$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw "Chua co .venv. Xem huong dan cai dat trong README.md."
}
& $projectPython -X utf8 -m streamlit run app.py --server.port 8501

