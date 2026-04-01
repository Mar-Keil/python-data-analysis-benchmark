from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BASE_DIR.parents[1]
BENCHMARKING_DIR = BASE_DIR / "benchmark"

DATA_GEN_OUT_DIR = BASE_DIR / "data_gen" / "out"
BENCHMARK_OUT_DIR = BENCHMARKING_DIR / "out"
PANDAS_OUT_DIR = BENCHMARK_OUT_DIR / "pandas_results"
POLARS_OUT_DIR = BENCHMARK_OUT_DIR / "polars_results"
DUCKDB_OUT_DIR = BENCHMARK_OUT_DIR / "duckdb_results"

BENCHMARK_ITERATIONS = 10
BENCHMARK_DURATION_SECONDS = 10

AIRLINES_INPUT_PATH = DATA_GEN_OUT_DIR / "airlines.parquet"

PARAM = (
    DATA_GEN_OUT_DIR / "20kFlights.parquet",
    DATA_GEN_OUT_DIR / "80kFlights.parquet",
    DATA_GEN_OUT_DIR / "320kFlights.parquet",
    DATA_GEN_OUT_DIR / "1280kFlights.parquet",
    DATA_GEN_OUT_DIR / "5120kFlights.parquet",
    DATA_GEN_OUT_DIR / "20480kFlights.parquet",
)
