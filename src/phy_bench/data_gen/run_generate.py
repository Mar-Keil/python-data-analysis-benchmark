from pathlib import Path

from random import Random

from phy_bench.data_gen.config import SEED

from phy_bench.data_gen.airline_gen import create_airlines_dataset


def print_output_path(path: Path) -> None:
    print(f"Wrote empty flights dataset to {path}")


def main() -> None:
    rnd = Random(SEED)

    create_airlines_dataset(rnd)

if __name__ == "__main__":
    main()
