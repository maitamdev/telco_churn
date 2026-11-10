param(
    [string]$DocumentPath = (Join-Path $PSScriptRoot "../reports/BAOCAO-TTNT.docx"),
    [string]$PdfPath = (Join-Path $PSScriptRoot "../tmp/report_upgrade/BAO_CAO_QA.pdf")
)
$ErrorActionPreference = "Stop"
$documentFullPath = (Resolve-Path -LiteralPath $DocumentPath).Path
$pdfFullPath = [IO.Path]::GetFullPath($PdfPath)
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($pdfFullPath)) | Out-Null
$wordApp = $null
$wordDocument = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordDocument = $wordApp.Documents.Open($documentFullPath, $false, $false)
    $wordDocument.Fields.Update() | Out-Null
    foreach ($toc in $wordDocument.TablesOfContents) { $toc.Update() }
    foreach ($tof in $wordDocument.TablesOfFigures) { $tof.Update() }
    $wordDocument.Repaginate()
    $wordDocument.Fields.Update() | Out-Null
    foreach ($toc in $wordDocument.TablesOfContents) { $toc.UpdatePageNumbers() }
    foreach ($tof in $wordDocument.TablesOfFigures) { $tof.UpdatePageNumbers() }
    $wordDocument.Save()
    $wordDocument.ExportAsFixedFormat($pdfFullPath, 17)
    Write-Output "Exported PDF: $pdfFullPath"
    Write-Output "Pages: $($wordDocument.ComputeStatistics(2))"
} finally {
    if ($null -ne $wordDocument) { $wordDocument.Close($false) }
    if ($null -ne $wordApp) { $wordApp.Quit() }
    if ($null -ne $wordDocument) { [Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordDocument) | Out-Null }
    if ($null -ne $wordApp) { [Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp) | Out-Null }
}
