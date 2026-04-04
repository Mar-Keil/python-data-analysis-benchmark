from pathlib import Path

import duckdb


def read_parquet(path: str | Path) -> duckdb.DuckDBPyRelation:
    return duckdb.read_parquet(str(path))


def write_parquet(dataset: duckdb.DuckDBPyRelation, path: str | Path) -> None:
    dataset.write_parquet(str(path), compression="zstd")


def materialize_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return duckdb.from_arrow(dataset.fetch_arrow_table())


def read_parquet_materialized(path: str | Path) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(read_parquet(path))


def filter_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.filter("aircraft_model = 'A319neo'")


def filter_dataset_materialized(
    dataset: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(filter_dataset(dataset))


def pivot_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.aggregate(
        "aircraft_model, sum(flight_distance) as sum_flight_distance"
    )


def pivot_dataset_materialized(
    dataset: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(pivot_dataset(dataset))


def group_count_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.aggregate(
        "aircraft_model, airline_code, count(flight_number) as count_aircraft"
    )


def group_count_dataset_materialized(
    dataset: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(group_count_dataset(dataset))


def join_dataset(
    dataset: duckdb.DuckDBPyRelation,
    other: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return dataset.set_alias("flights").join(
        other.set_alias("airlines"),
        condition="flights.airline_code = airlines.airline_code",
        how="inner",
    ).project(
        """
        flights.flight_number,
        flights.msn_number,
        flights.aircraft_model,
        flights.airline_code,
        flights.error_free,
        flights.departure_airport,
        flights.arrival_airport,
        flights.flight_distance,
        flights.departure_time,
        flights.arrival_time,
        airlines.airline_name,
        airlines.founding_year,
        airlines.airline_hub
        """
    )


def join_dataset_materialized(
    dataset: duckdb.DuckDBPyRelation,
    other: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(join_dataset(dataset, other))


def sort_dataset(dataset: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return dataset.order("flight_number")


def sort_dataset_materialized(
    dataset: duckdb.DuckDBPyRelation,
) -> duckdb.DuckDBPyRelation:
    return materialize_dataset(sort_dataset(dataset))
