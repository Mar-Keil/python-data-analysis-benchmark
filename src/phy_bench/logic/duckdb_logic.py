from pathlib import Path

import duckdb


def read_parquet(path: Path) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(duckdb.read_parquet(str(path)))


def write_parquet(dataset: duckdb.DuckDBPyRelation, path: Path) -> None:
    dataset.write_parquet(str(path), compression="zstd")


def materialize_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return duckdb.from_arrow(dataset.fetch_arrow_table())


def filter_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(dataset.filter("aircraft_model = 'A319neo'"))


def pivot_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(
        dataset.aggregate("aircraft_model, sum(flight_distance) as sum_flight_distance")
    )


def group_count_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(
        dataset.aggregate(
            "aircraft_model, airline_code, count(flight_number) as count_aircraft"
        )
    )


def join_dataset(
    dataset: duckdb.DuckDBPyRelation,
    other: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(dataset.join(other, condition="airline_code", how="inner"))


def sort_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(dataset.order("flight_number"))
