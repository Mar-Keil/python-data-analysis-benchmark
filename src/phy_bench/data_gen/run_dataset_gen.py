from concurrent.futures import ProcessPoolExecutor

from phy_bench.data_gen.config import BENCHMARK_DATASET_ROWS

from phy_bench.data_gen.airline_gen import create_airlines_dataset
from phy_bench.data_gen.flights_gen import create_flights_dataset


def main() -> None:
    print(f"Wrote airlines to {create_airlines_dataset()}")

    with ProcessPoolExecutor() as executor:
        for size, output_path in zip(
                BENCHMARK_DATASET_ROWS,
                executor.map(create_flights_dataset, BENCHMARK_DATASET_ROWS),
                strict=True,
        ):
            print(f"Wrote {size} flights to {output_path}")

if __name__ == "__main__":
    main()
