from pathlib import Path

import duckdb


def read_parquet(path: str | Path) -> duckdb.DuckDBPyRelation:
    return duckdb.read_parquet(str(path))


def write_parquet(dataset: duckdb.DuckDBPyRelation, path: str | Path) -> None:
    dataset.write_parquet(str(path), compression="zstd")


def filter_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.filter("aircraft_model = 'A319neo'")


def pivot_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.aggregate(
        "aircraft_model, sum(flight_distance) as sum_flight_distance"
    )


def group_count_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.aggregate(
        "aircraft_model, airline_code, count(flight_number) as count_aircraft"
    )


def join_dataset(
    dataset: duckdb.DuckDBPyRelation,
    other: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return dataset.join(other, condition="airline_code = airline_code", how="inner")


def sort_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.order("flight_number")
