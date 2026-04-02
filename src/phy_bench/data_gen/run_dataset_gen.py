from pathlib import Path

from random import Random

from phy_bench.data_gen.config import SEED, BENCHMARK_DATASET_ROWS

from phy_bench.data_gen.airline_gen import create_airlines_dataset
from phy_bench.data_gen.flights_gen import create_flights_dataset


def print_output_path(path: Path) -> None:
    print(f"Wrote dataset to {path}")


def main() -> None:
    rnd = Random(SEED)

    print_output_path(create_airlines_dataset(rnd))

    for size in BENCHMARK_DATASET_ROWS:
        print_output_path(create_flights_dataset(size, rnd))

if __name__ == "__main__":
    main()
