#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

DATASET_FILES=(
  "$ROOT_DIR/src/phy_bench/data_gen/out/airlines.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/20kFlights.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/80kFlights.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/320kFlights.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/1280kFlights.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/5120kFlights.parquet"
  "$ROOT_DIR/src/phy_bench/data_gen/out/20480kFlights.parquet"
)

pick_python() {
  local candidate

  for candidate in python3.14 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      local version_ok
      version_ok="$("$candidate" -c 'import sys; print("ok" if sys.version_info >= (3, 14) else "no")')"
      if [[ "$version_ok" == "ok" ]]; then
        printf '%s\n' "$candidate"
        return 0
      fi
    fi
  done

  return 1
}

ensure_datasets() {
  local file

  for file in "${DATASET_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
      echo "Generating benchmark datasets..."
      "$VENV_DIR/bin/python" -m phy_bench.data_gen.run_dataset_gen
      return 0
    fi
  done

  echo "Datasets already exist. Skipping generation."
}

main() {
  local system_python

  if ! system_python="$(pick_python)"; then
    echo "Python 3.14 or newer is required but was not found."
    echo "Install Python 3.14+, then rerun this script."
    exit 1
  fi

  echo "Using Python interpreter: $system_python"

  if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment in $VENV_DIR ..."
    "$system_python" -m venv "$VENV_DIR"
  else
    echo "Virtual environment already exists."
  fi

  echo "Installing project dependencies..."
  "$VENV_DIR/bin/python" -m pip install --upgrade pip
  "$VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR"

  ensure_datasets

  echo "Starting interactive benchmark selection..."
  "$VENV_DIR/bin/python" -m phy_bench.benchmark.run_benchmarks
}

if [[ "${1:-}" == "--inner" ]]; then
  main
  exit 0
fi

if command -v caffeinate >/dev/null 2>&1; then
  caffeinate bash -lc "$(printf 'cd %q && ./run-benchmark-macos.sh --inner' "$ROOT_DIR")"
  exit 0
fi

echo "caffeinate is not available. Continuing without sleep prevention."
main
