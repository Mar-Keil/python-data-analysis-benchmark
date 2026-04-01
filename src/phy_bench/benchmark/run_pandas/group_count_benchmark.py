from pathlib import Path

from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement
from phy_bench.logic.pandas_logic import group_count_dataset
from phy_bench.logic.pandas_logic import read_parquet
from phy_bench.logic.pandas_logic import write_parquet

def run_group_count_benchmark(
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

                grouped_flights = group_count_dataset(flights)

                logic_measurement.stop()

                del grouped_flights

            invocation_loop_logic.cancel()

            grouped_flights = group_count_dataset(flights)

            invocation_loop_write = InvocationLoop()
            invocation_loop_write.start()

            while invocation_loop_write.get_is_looping():
                write_measurement.start()

                write_parquet(grouped_flights, output_dir / "group_count")

                write_measurement.stop()

            invocation_loop_write.cancel()

            del grouped_flights

        logic_measurement.write_results(path.stem.replace("Flights", ""), "GroupCount")
        write_measurement.write_results(path.stem.replace("Flights", ""), "WriteGroupCount")
