# python-data-analysis-benchmark

Benchmark suite for comparing `Polars`, `Pandas`, and `DuckDB` on typical data
analysis workloads. The project generates synthetic flight datasets, runs the same
operations against all three engines, and writes execution time and CPU metrics to
CSV files for later evaluation.

## Goal

This repository is designed to support reproducible performance comparisons between
popular Python data-processing tools. It focuses on workloads that are close to
common analytical tasks instead of microbenchmarks for isolated language features.

The benchmark currently compares:

- `Polars`
- `Pandas`
- `DuckDB`

For each engine, the project measures:

- average wall-clock time per invocation in `s/op`
- derived CPU usage in `cores`

## What the project does

The benchmark workflow has two major phases:

1. Generate synthetic benchmark datasets as Parquet files.
2. Run the selected engine benchmark interactively and store the results as CSV.

The helper scripts on macOS and Windows automate the full flow:

- create a local `.venv` if needed
- ensure a compatible Python version is used
- install the project in editable mode
- generate datasets if they are missing
- launch the interactive benchmark runner

## Requirements

- Python `3.14` or newer
- macOS or Windows for the provided convenience scripts

Project dependencies are defined in [pyproject.toml](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/pyproject.toml)
and currently include:

- `duckdb`
- `pandas`
- `polars`
- `psutil`
- `pyarrow`

## Quick Start

### macOS

```bash
chmod +x run-benchmark-macos.sh
./run-benchmark-macos.sh
```

The macOS script uses `caffeinate` when available so the machine does not go to
sleep during long-running benchmark executions.

### Windows

```powershell
.\run-benchmark-windows.ps1
```

The PowerShell script uses the Windows execution-state API to reduce the risk of
the machine going to sleep while benchmarks are running.

## Interactive benchmark selection

Both scripts start the same interactive prompt:

```text
What benchmark do you want to run?
- Polars
- Pandas
- DuckDB
- All
```

You can benchmark a single engine or run all engines in sequence.

## Running without the wrapper scripts

If you want to run the project manually, the package exposes two CLI entry points
through `pyproject.toml`:

- `generate-datasets`
- `benchmarks`

Example setup:

```bash
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
generate-datasets
benchmarks
```

You can also invoke the modules directly:

```bash
python -m phy_bench.data_gen.run_dataset_gen
python -m phy_bench.benchmark.run_benchmarks
```

## Generated datasets

The benchmark data is created under
[`src/phy_bench/data_gen/out`](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/src/phy_bench/data_gen/out).

Generated files include:

- `airlines.parquet`
- `20kFlights.parquet`
- `80kFlights.parquet`
- `320kFlights.parquet`
- `1280kFlights.parquet`
- `5120kFlights.parquet`
- `20480kFlights.parquet`

The flight datasets contain the following row counts:

- `20,000`
- `80,000`
- `320,000`
- `1,280,000`
- `5,120,000`
- `20,480,000`

The data is synthetic and generated from a fixed seed, which helps keep runs
reproducible across environments.

## Benchmarked operations

Each engine is evaluated on the same set of operations:

- `Read`: load flights and airlines Parquet files
- `Filter`: keep rows where `aircraft_model == "A319neo"`
- `Sort`: sort by `flight_number`
- `Pivot`: aggregate `flight_distance` by `aircraft_model`
- `GroupCount`: count flights by `aircraft_model` and `airline_code`
- `Join`: inner join flights with airlines on `airline_code`

For transformation operations, the benchmark measures two parts separately:

- operation logic itself
- writing the resulting dataset back to Parquet

This is why the result CSVs include method names such as:

- `Filter`
- `WriteFilter`
- `Sort`
- `WriteSort`
- `Pivot`
- `WritePivot`
- `GroupCount`
- `WriteGroupCount`
- `Join`
- `WriteJoin`

## Measurement model

The benchmark currently uses these defaults:

- `10` iterations per dataset size and operation
- repeated invocation loops to accumulate stable timing values
- wall-clock measurement via `perf_counter()`
- CPU-time measurement via `process_time()`

The derived CPU score is written as:

```text
cpu_cores = average_cpu_time / average_wall_time
```

This value represents how many CPU cores were effectively used on average during
the measured invocation.

## Output files

Benchmark results are written below
[`src/phy_bench/benchmark/out`](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/src/phy_bench/benchmark/out).

Each engine has its own output directory:

- `pandas_results`
- `polars_results`
- `duckdb_results`

Within these directories, the benchmark creates numbered CSV files such as
`1_results.csv`, `2_results.csv`, and so on. Each CSV starts with the columns:

```text
engine,benchmark_size,method,category,score,unit
```

Example categories:

- `Time`
- `CPU`

Example units:

- `s/op`
- `cores`

Intermediate Parquet outputs of benchmark operations are also written into
subdirectories such as `filter`, `sort`, `pivot`, `group_count`, and `join`.

## Project structure

```text
.
├── README.md
├── pyproject.toml
├── run-benchmark-macos.sh
├── run-benchmark-windows.ps1
├── run-latex.sh
├── latex/
├── out/
└── src/phy_bench/
    ├── benchmark/
    │   ├── default/
    │   ├── out/
    │   ├── run/
    │   └── run_benchmarks.py
    ├── data_gen/
    │   ├── config.py
    │   ├── out/
    │   └── run_dataset_gen.py
    └── logic/
        ├── duckdb_logic.py
        ├── pandas_logic.py
        └── polars_logic.py
```

### Important directories

- `src/phy_bench/data_gen`: synthetic dataset generation
- `src/phy_bench/logic`: engine-specific benchmark implementations
- `src/phy_bench/benchmark/run`: orchestration of benchmark execution
- `src/phy_bench/benchmark/default`: shared benchmark defaults and measurement logic
- `src/phy_bench/benchmark/out`: generated benchmark results
- `latex`: thesis-related material and documentation assets

## Notes and limitations

- The benchmark runner is interactive. There is currently no non-interactive CLI
  argument for engine selection.
- The project requires Python `3.14+`, which is stricter than many current Python
  data projects.
- Result directories for write benchmarks are cleared between iterations and reused
  so that each measured write run starts from a clean state.
- Dataset generation and benchmark execution can take a noticeable amount of time,
  especially for the larger input sizes.

## Related scripts

- [run-benchmark-macos.sh](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/run-benchmark-macos.sh):
  complete benchmark bootstrap for macOS
- [run-benchmark-windows.ps1](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/run-benchmark-windows.ps1):
  complete benchmark bootstrap for Windows
- [run-latex.sh](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/run-latex.sh):
  build helper for the LaTeX part of the repository

## Development

To inspect or extend the benchmark, the most relevant entry points are:

- [src/phy_bench/benchmark/run_benchmarks.py](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/src/phy_bench/benchmark/run_benchmarks.py)
- [src/phy_bench/data_gen/run_dataset_gen.py](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/src/phy_bench/data_gen/run_dataset_gen.py)
- [src/phy_bench/benchmark/run/engine_config.py](/Users/marcokeilwagen/PycharmProjects/python-data-analysis-benchmark/src/phy_bench/benchmark/run/engine_config.py)

If you add a new engine, you will typically need to:

- implement the engine-specific logic in `src/phy_bench/logic`
- register the engine in `ENGINE_CONFIGS`
- define how read, write, and operation functions are mapped

## Current status

The repository is packaged as an installable Python project and is currently best
understood as a focused benchmark prototype for comparative evaluation of Python
data-analysis engines.
