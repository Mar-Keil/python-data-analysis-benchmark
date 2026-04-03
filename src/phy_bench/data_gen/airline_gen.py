from pathlib import Path
from random import Random

import polars as pl

from phy_bench.data_gen.config import OUT_DIR, AIRLINE_NAMES, AIRPORT_CODES, SEED

def create_airlines_dataset() -> Path:
    target_path = OUT_DIR / "airlines.parquet"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    rnd = Random(SEED)

    airline_names = list(AIRLINE_NAMES)

    airline_code = list(range(1000, 1000 + len(airline_names)))

    founding_year = [rnd.randint(1919, 2026) for _ in airline_code]

    airline_hub = [rnd.choice(AIRPORT_CODES) for _ in airline_code]

    airlines_df = pl.DataFrame(
    {
            "airline_name": airline_names,
            "airline_code": airline_code,
            "founding_year": founding_year,
            "airline_hub": airline_hub,
        },
        schema={
            "airline_code": pl.Int32,
            "airline_name": pl.Utf8,
            "founding_year": pl.Int32,
            "airline_hub": pl.Utf8
        }
    )

    airlines_df.write_parquet(target_path, compression="zstd")

    return target_path