from phy_bench.benchmark.default.default_values import AIRLINES_INPUT_PATH
from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement
from phy_bench.logic.duckdb_logic import materialize_dataset
from phy_bench.logic.duckdb_logic import read_parquet


def run_read_benchmark(time_measurement: TimeCPUMeasurement) -> None:
    for path in PARAM:
        for _ in range(BENCHMARK_ITERATIONS):
            invocation_loop = InvocationLoop()
            invocation_loop.start()

            while invocation_loop.get_is_looping():
                time_measurement.start()

                flights = materialize_dataset(read_parquet(path))
                airlines = materialize_dataset(read_parquet(AIRLINES_INPUT_PATH))

                time_measurement.stop()

                del flights
                del airlines

            invocation_loop.cancel()

        time_measurement.write_results(path.stem.replace("Flights", ""), "Read")
