import polars as pl

from random import Random
from datetime import datetime, timedelta
from geopy.distance import geodesic

from phy_bench.data_gen.config import OUT_DIR
from phy_bench.data_gen.config import AIRCRAFT_MODELS
from phy_bench.data_gen.config import AIRLINE_NAMES
from phy_bench.data_gen.config import AIRPORT_CODES
from phy_bench.data_gen.config import AIRPORT_COORDINATES

def flights_gen(dataset_rows: int, rnd: Random) -> None:

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
        geodesic(AIRPORT_COORDINATES[departure_code], AIRPORT_COORDINATES[arrival_code]).kilometers
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
        departure + timedelta(minutes=rnd.randint(60, 12 * 60))
        for departure in departure_time
    ]

    flights_df = pl.DataFrame(
        schema={
            "flight_number": pl.Utf8,
            "msn": pl.Utf8,
            "aircraft_model": pl.Utf8,
            "airline_code": pl.Int32,
            "error_free": pl.Boolean,
            "departure_airport": pl.Utf8,
            "arrival_airport": pl.Utf8,
            "departure_time": pl.Utf8,
            "arrival_time": pl.Utf8,
            "flight_distance": pl.Int32,
        }
    )