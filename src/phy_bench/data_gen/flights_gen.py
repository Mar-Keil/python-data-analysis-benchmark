from pathlib import Path

import numpy as np
import polars as pl

from phy_bench.data_gen.config import OUT_DIR
from phy_bench.data_gen.config import SEED
from phy_bench.data_gen.config import AIRCRAFT_MODELS
from phy_bench.data_gen.config import AIRLINE_NAMES
from phy_bench.data_gen.config import AIRPORT_CODES
from phy_bench.data_gen.config import AIRPORT_COORDINATES
from phy_bench.data_gen.config import AVERAGE_FLIGHT_SPEED_KMH

EARTH_RADIUS_KM = 6371.0088
AIRPORT_INDEX = {code: idx for idx, code in enumerate(AIRPORT_CODES)}
AIRPORT_COORDINATE_ARRAY = np.array(
    [AIRPORT_COORDINATES[code] for code in AIRPORT_CODES],
    dtype=np.float64,
)


def create_flights_dataset(dataset_rows: int) -> Path:

    rng = np.random.default_rng(SEED)

    target_path = OUT_DIR / f"{dataset_rows // 1000}kFlights.parquet"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    flight_number = rng.permutation(
        np.arange(10_000_000, 10_000_000 + dataset_rows, dtype=np.int32)
    )

    msn_pool_size = dataset_rows // 10
    msn_pool = np.arange(100_000, 100_000 + msn_pool_size, dtype=np.int32)
    msn_indices = rng.integers(0, msn_pool_size, size=dataset_rows, dtype=np.int32)
    msn_number = msn_pool[msn_indices]

    airline_code_pool = np.arange(1000, 1000 + len(AIRLINE_NAMES), dtype=np.int32)
    msn_airline_code = rng.choice(
        airline_code_pool,
        size=msn_pool_size,
        replace=True,
    )
    airline_code = msn_airline_code[msn_indices]

    aircraft_model_pool = np.array(AIRCRAFT_MODELS, dtype=str)
    msn_aircraft_model = rng.choice(
        aircraft_model_pool,
        size=msn_pool_size,
        replace=True,
    )
    aircraft_model = msn_aircraft_model[msn_indices]

    error_free = rng.random(dataset_rows) < 0.99

    airport_code_pool = np.array(AIRPORT_CODES, dtype=str)
    departure_airport = rng.choice(
        airport_code_pool,
        size=dataset_rows,
        replace=True,
    )
    arrival_airport = rng.choice(
        airport_code_pool,
        size=dataset_rows,
        replace=True,
    )

    flight_distance = calculate_distances(departure_airport, arrival_airport)

    base_time = np.datetime64("2020-01-01T00:00:00")
    departure_days = rng.integers(0, 365 * 6 + 1, size=dataset_rows, dtype=np.int32)
    departure_hours = rng.integers(0, 24, size=dataset_rows, dtype=np.int32)
    departure_minutes = rng.integers(0, 60, size=dataset_rows, dtype=np.int32)
    departure_offset_minutes = np.asarray(
        departure_days * 24 * 60
        + departure_hours * 60
        + departure_minutes,
        dtype=np.int32,
    )
    departure_time = (
        base_time + departure_offset_minutes.astype("timedelta64[m]")
    ).astype("datetime64[ms]")

    flight_duration_minutes = np.rint(
        flight_distance / AVERAGE_FLIGHT_SPEED_KMH * 60
    ).astype(np.int32)

    arrival_time = (
        departure_time + flight_duration_minutes.astype("timedelta64[m]")
    ).astype("datetime64[ms]")

    departure_time_formatted = (
        pl.Series("departure_time", departure_time, dtype=pl.Datetime("ms"))
        .dt.strftime("%H:%M %d.%m.%Y")
    )

    arrival_time_formatted = (
        pl.Series("arrival_time", arrival_time, dtype=pl.Datetime("ms"))
        .dt.strftime("%H:%M %d.%m.%Y")
    )

    flights_df = pl.DataFrame(
        {
            "flight_number": "FL" + pl.Series("flight_number", flight_number).cast(pl.Utf8),
            "msn_number": "MSN" +  pl.Series("msn_number", msn_number).cast(pl.Utf8),
            "aircraft_model": aircraft_model,
            "airline_code": airline_code,
            "error_free": error_free,
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "flight_distance": flight_distance,
            "departure_time": departure_time_formatted,
            "arrival_time": arrival_time_formatted,
        },
        schema={
            "flight_number": pl.Utf8,
            "msn_number": pl.Utf8,
            "aircraft_model": pl.Utf8,
            "airline_code": pl.Int32,
            "error_free": pl.Boolean,
            "departure_airport": pl.Utf8,
            "arrival_airport": pl.Utf8,
            "flight_distance": pl.Int32,
            "departure_time": pl.Utf8,
            "arrival_time": pl.Utf8,
        }
    )

    flights_df.write_parquet(target_path, compression="zstd")

    return target_path


def calculate_distances(
    departure_airport: np.ndarray,
    arrival_airport: np.ndarray,
) -> np.ndarray:
    departure_indices = np.fromiter(
        (AIRPORT_INDEX[code] for code in departure_airport),
        dtype=np.int32,
        count=departure_airport.size,
    )
    arrival_indices = np.fromiter(
        (AIRPORT_INDEX[code] for code in arrival_airport),
        dtype=np.int32,
        count=arrival_airport.size,
    )

    departure_coords = AIRPORT_COORDINATE_ARRAY[departure_indices]
    arrival_coords = AIRPORT_COORDINATE_ARRAY[arrival_indices]

    departure_lat_rad = np.radians(departure_coords[:, 0])
    departure_lon_rad = np.radians(departure_coords[:, 1])
    arrival_lat_rad = np.radians(arrival_coords[:, 0])
    arrival_lon_rad = np.radians(arrival_coords[:, 1])

    delta_lat = arrival_lat_rad - departure_lat_rad
    delta_lon = arrival_lon_rad - departure_lon_rad

    haversine = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(departure_lat_rad) * np.cos(arrival_lat_rad) * np.sin(delta_lon / 2) ** 2
    )

    return np.rint(2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(haversine))).astype(np.int32)
