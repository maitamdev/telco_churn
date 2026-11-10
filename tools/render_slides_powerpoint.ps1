param(
    [string]$Source = "reports/BAO_VE_TELCO_CHURN.pptx",
    [string]$OutputDirectory = "tmp/slides_upgrade/native"
)
$ErrorActionPreference = "Stop"
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$null = New-Item -ItemType Directory -Force -Path $OutputDirectory
$outputPath = (Resolve-Path -LiteralPath $OutputDirectory).Path
$powerpoint = New-Object -ComObject PowerPoint.Application
$priorCount = $powerpoint.Presentations.Count
$presentation = $null
try {
    $presentation = $powerpoint.Presentations.Open($sourcePath, -1, 0, 0)
    $evidence = @()
    foreach ($slide in $presentation.Slides) {
        $slide.Export((Join-Path $outputPath ("slide-{0:00}.png" -f $slide.SlideIndex)), "PNG", 1280, 720)
        $tables = 0
        $charts = 0
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTable -eq -1) { $tables++ }
            if ($shape.HasChart -eq -1) { $charts++ }
        }
        $evidence += @{slide=$slide.SlideIndex; tables=$tables; charts=$charts}
    }
    $evidence | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputPath "native_inventory.json") -Encoding utf8
    Write-Output "PowerPoint opened and rendered $($presentation.Slides.Count) slides."
} finally {
    if ($null -ne $presentation) { $presentation.Close() }
    if ($priorCount -eq 0) { $powerpoint.Quit() }
}
