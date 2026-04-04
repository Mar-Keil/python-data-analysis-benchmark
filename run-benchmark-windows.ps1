$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $repoRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

$datasetFiles = @(
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\airlines.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\20kFlights.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\80kFlights.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\320kFlights.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\1280kFlights.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\5120kFlights.parquet"),
    (Join-Path $repoRoot "src\phy_bench\data_gen\out\20480kFlights.parquet")
)

function Get-SystemPython {
    $candidates = @(
        @{ Label = "py -3.14"; Command = "py"; Arguments = @("-3.14") },
        @{ Label = "py -3"; Command = "py"; Arguments = @("-3") },
        @{ Label = "python"; Command = "python"; Arguments = @() }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) {
            continue
        }

        $versionOutput = & $candidate.Command @($candidate.Arguments + @("-c", "import sys; print('ok' if sys.version_info >= (3, 14) else 'no')"))
        if ($LASTEXITCODE -eq 0 -and $versionOutput -eq "ok") {
            return $candidate
        }
    }

    return $null
}

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        $PythonSpec,

        [Parameter(Mandatory = $true)]
        [string[]] $Arguments
    )

    & $PythonSpec.Command @($PythonSpec.Arguments + $Arguments)
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: $($PythonSpec.Label)"
    }
}

function Ensure-Datasets {
    $missingDataset = $datasetFiles | Where-Object { -not (Test-Path $_) } | Select-Object -First 1

    if ($missingDataset) {
        Write-Host "Generating benchmark datasets..."
        & $venvPython -m phy_bench.data_gen.run_dataset_gen
        if ($LASTEXITCODE -ne 0) {
            throw "Dataset generation failed."
        }
        return
    }

    Write-Host "Datasets already exist. Skipping generation."
}

Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class SleepGuard {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = 0x80000000
$ES_SYSTEM_REQUIRED = 0x00000001
$ES_AWAYMODE_REQUIRED = 0x00000040

$systemPython = Get-SystemPython
if (-not $systemPython) {
    throw "Python 3.14 or newer is required but was not found. Install Python 3.14+ and rerun the script."
}

Write-Host "Using Python interpreter: $($systemPython.Label)"

try {
    [void][SleepGuard]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED)

    if (-not (Test-Path $venvPython)) {
        Write-Host "Creating virtual environment in $venvPath ..."
        Invoke-Python -PythonSpec $systemPython -Arguments @("-m", "venv", $venvPath)
    }
    else {
        Write-Host "Virtual environment already exists."
    }

    Write-Host "Installing project dependencies..."
    & $venvPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "pip upgrade failed."
    }

    & $venvPython -m pip install -e $repoRoot
    if ($LASTEXITCODE -ne 0) {
        throw "Dependency installation failed."
    }

    Ensure-Datasets

    Write-Host "Starting interactive benchmark selection..."
    & $venvPython -m phy_bench.benchmark.run_benchmarks
    if ($LASTEXITCODE -ne 0) {
        throw "Benchmark execution failed."
    }
}
finally {
    [void][SleepGuard]::SetThreadExecutionState($ES_CONTINUOUS)
}
