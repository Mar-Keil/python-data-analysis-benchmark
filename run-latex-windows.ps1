param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$latexRoot = Join-Path $PSScriptRoot "latex"
$buildPath = Join-Path $latexRoot "build"
$pdfPath = Join-Path $buildPath "main.pdf"
$latexmkPath = "C:\Users\MK\AppData\Local\Programs\MiKTeX\miktex\bin\x64\latexmk.exe"

if ($Clean -and (Test-Path -LiteralPath $buildPath)) {
    Remove-Item -LiteralPath $buildPath -Recurse -Force
}

if (-not (Test-Path -LiteralPath $buildPath)) {
    New-Item -ItemType Directory -Path $buildPath | Out-Null
}

Push-Location $latexRoot

try {
    & $latexmkPath -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "PDF build finished without creating: $pdfPath"
}

Start-Process -FilePath $pdfPath
