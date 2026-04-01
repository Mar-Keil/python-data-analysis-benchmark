from __future__ import annotations

from phy_bench.logic import polars_logic


def main() -> None:
    print(
        "Polars benchmark runner is configured.",
        f"Available module: {polars_logic.__name__}",
    )


if __name__ == "__main__":
    main()
