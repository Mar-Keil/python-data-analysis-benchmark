from __future__ import annotations

from pathlib import Path

import polars as pl


def read_parquet(path: str | Path) -> pl.DataFrame:
    return pl.read_parquet(path)


def write_parquet(dataset: pl.DataFrame, path: str | Path) -> None:
    dataset.write_parquet(path)


def filter_dataset(dataset: pl.DataFrame) -> pl.DataFrame:
    return dataset.filter(pl.col("aircraft_model") == "A319neo")


def pivot_dataset(dataset: pl.DataFrame) -> pl.DataFrame:
    return dataset.group_by("aircraft_model").agg(
        pl.col("flight_distance").sum().alias("sum_flight_distance")
    )


def group_count_dataset(dataset: pl.DataFrame) -> pl.DataFrame:
    return dataset.group_by("aircraft_model", "airline_code").agg(
        pl.col("flight_number").count().alias("count_aircraft")
    )


def join_dataset(dataset: pl.DataFrame, other: pl.DataFrame) -> pl.DataFrame:
    return dataset.join(other, on="airline_code", how="inner")


def sort_dataset(dataset: pl.DataFrame) -> pl.DataFrame:
    return dataset.sort("flight_number")