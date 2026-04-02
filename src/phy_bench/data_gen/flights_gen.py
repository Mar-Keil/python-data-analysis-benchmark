from pathlib import Path
from random import Random
from datetime import datetime, timedelta

import polars as pl
from geopy.distance import geodesic

from phy_bench.data_gen.config import OUT_DIR
from phy_bench.data_gen.config import AIRCRAFT_MODELS
from phy_bench.data_gen.config import AIRLINE_NAMES
from phy_bench.data_gen.config import AIRPORT_CODES
from phy_bench.data_gen.config import AIRPORT_COORDINATES
from phy_bench.data_gen.config import AVERAGE_FLIGHT_SPEED_KMH


def create_flights_dataset(dataset_rows: int, rnd: Random) -> Path:
    target_path = OUT_DIR / f"{dataset_rows // 1000}kFlights.parquet"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    flight_numbers = [f"FL{number}" for number in range(10_000_000, 10_000_000 + dataset_rows)]
    rnd.shuffle(flight_numbers)

    msn_pool = [f"MSN{100_000 + i}" for i in range(dataset_rows // 10)]
    airline_code_pool = list(range(1000, 1000 + len(AIRLINE_NAMES)))

    msn_to_model = {
        msn_value: rnd.choice(AIRCRAFT_MODELS)
        for msn_value in msn_pool
    }

    msn_to_airline = {
        msn_value: rnd.choice(airline_code_pool)
        for msn_value in msn_pool
    }

    msn = [rnd.choice(msn_pool) for _ in range(dataset_rows)]

    aircraft_model = [msn_to_model[msn_value] for msn_value in msn]

    airline_code = [msn_to_airline[msn_value] for msn_value in msn]

    error_free = [rnd.random() < 0.9 for _ in range(dataset_rows)]

    departure_airport = [rnd.choice(AIRPORT_CODES) for _ in range(dataset_rows)]

    arrival_airport = [rnd.choice(AIRPORT_CODES) for _ in range(dataset_rows)]

    flight_distance = [
        int(round(geodesic(AIRPORT_COORDINATES[departure_code], AIRPORT_COORDINATES[arrival_code]).kilometers))
        for departure_code, arrival_code in zip(departure_airport, arrival_airport)
    ]

    departure_time = [
        datetime(2020, 1, 1)
        + timedelta(
            days=rnd.randint(0, 365 * 6),
            hours=rnd.randint(0, 23),
            minutes=rnd.randint(0, 59),
        )
        for _ in range(dataset_rows)
    ]

    arrival_time = [
        departure_value + timedelta(hours=distance_km / AVERAGE_FLIGHT_SPEED_KMH)
        for departure_value, distance_km in zip(departure_time, flight_distance)
    ]

    flights_df = pl.DataFrame(
        {
            "flight_number": flight_numbers,
            "msn": msn,
            "aircraft_model": aircraft_model,
            "airline_code": airline_code,
            "error_free": error_free,
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "flight_distance": flight_distance,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        },
        schema={
            "flight_number": pl.Utf8,
            "msn": pl.Utf8,
            "aircraft_model": pl.Utf8,
            "airline_code": pl.Int32,
            "error_free": pl.Boolean,
            "departure_airport": pl.Utf8,
            "arrival_airport": pl.Utf8,
            "flight_distance": pl.Int32,
            "departure_time": pl.Datetime,
            "arrival_time": pl.Datetime,
        }
    )

    flights_df.write_parquet(target_path, compression="zstd")

    return target_path
