# python-data-analysis-benchmark
Compares the Python packages Polars, Pandas, and DuckDB about their execution time and the CPU usage.

## Run the benchmark

macOS:

```bash
chmod +x run-benchmark-macos.sh
./run-benchmark-macos.sh
```

Windows:

```powershell
.\run-benchmark-windows.ps1
```

Both scripts:
- create `.venv` if needed
- install the project and dependencies
- generate benchmark datasets if they are missing
- start the existing interactive benchmark selection

Supported Python versions:
- Python 3.14 or newer
