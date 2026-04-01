from pathlib import Path

from phy_bench.benchmark.default.default_values import AIRLINES_INPUT_PATH
from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement
from phy_bench.logic.polars_logic import join_dataset
from phy_bench.logic.polars_logic import read_parquet
from phy_bench.logic.polars_logic import write_parquet

def run_join_benchmark(
    logic_measurement: TimeCPUMeasurement,
    write_measurement: TimeCPUMeasurement,
    output_dir: Path,
) -> None:
    airlines = read_parquet(AIRLINES_INPUT_PATH)

    for path in PARAM:
        flights = read_parquet(path)

        for _ in range(BENCHMARK_ITERATIONS):
            invocation_loop_logic = InvocationLoop()
            invocation_loop_logic.start()

            while invocation_loop_logic.get_is_looping():
                logic_measurement.start()

                joined_flights = join_dataset(flights, airlines)

                logic_measurement.stop()

                del joined_flights

            invocation_loop_logic.cancel()

            joined_flights = join_dataset(flights, airlines)

            invocation_loop_write = InvocationLoop()
            invocation_loop_write.start()

            while invocation_loop_write.get_is_looping():
                write_measurement.start()

                write_parquet(joined_flights, output_dir / "join")

                write_measurement.stop()

            invocation_loop_write.cancel()

            del joined_flights

        logic_measurement.write_results(path.stem.replace("Flights", ""), "Join")
        write_measurement.write_results(path.stem.replace("Flights", ""), "WriteJoin")
