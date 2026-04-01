from __future__ import annotations

from phy_bench.logic import pandas_logic


def main() -> None:
    print(
        "Pandas benchmark runner is configured.",
        f"Available module: {pandas_logic.__name__}",
    )


if __name__ == "__main__":
    main()
