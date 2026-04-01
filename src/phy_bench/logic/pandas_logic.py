from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas import DataFrame, Series


def read_parquet(path: str | Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def write_parquet(dataset: pd.DataFrame, path: str | Path) -> None:
    dataset.to_parquet(path, compression="zstd", index=False)


def filter_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    return dataset[dataset["aircraft_model"] == "A319neo"]


def pivot_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    return (
        dataset.groupby("aircraft_model", as_index=False, sort=False)["flight_distance"]
        .sum()
        .rename(columns={"flight_distance": "sum_flight_distance"})
    )


def group_count_dataset(dataset: pd.DataFrame) -> DataFrame:
    return (
        dataset.groupby(["aircraft_model", "airline_code"], as_index=False, sort=False)
        .size()
        .rename(columns={"size": "count_aircraft"})
    )


def join_dataset(dataset: pd.DataFrame, other: pd.DataFrame) -> pd.DataFrame:
    return dataset.merge(other, on="airline_code", how="inner")


def sort_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    return dataset.sort_values(by=["flight_number"], ascending=True)
