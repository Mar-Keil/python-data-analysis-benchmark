from pathlib import Path

from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement
from phy_bench.logic.duckdb_logic import materialize_dataset
from phy_bench.logic.duckdb_logic import pivot_dataset
from phy_bench.logic.duckdb_logic import read_parquet
from phy_bench.logic.duckdb_logic import write_parquet


def run_pivot_benchmark(
    logic_measurement: TimeCPUMeasurement,
    write_measurement: TimeCPUMeasurement,
    output_dir: Path,
) -> None:
    for path in PARAM:
        flights = read_parquet(path)

        for _ in range(BENCHMARK_ITERATIONS):
            invocation_loop_logic = InvocationLoop()
            invocation_loop_logic.start()

            while invocation_loop_logic.get_is_looping():
                logic_measurement.start()

                pivoted_flights = materialize_dataset(pivot_dataset(flights))

                logic_measurement.stop()

                del pivoted_flights

            invocation_loop_logic.cancel()

            pivoted_flights = materialize_dataset(pivot_dataset(flights))

            invocation_loop_write = InvocationLoop()
            invocation_loop_write.start()

            while invocation_loop_write.get_is_looping():
                write_measurement.start()

                write_parquet(pivoted_flights, output_dir / "pivot")

                write_measurement.stop()

            invocation_loop_write.cancel()

            del pivoted_flights

        logic_measurement.write_results(path.stem.replace("Flights", ""), "Pivot")
        write_measurement.write_results(path.stem.replace("Flights", ""), "WritePivot")
