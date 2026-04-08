from pathlib import Path
from typing import Any
from typing import Callable

from phy_bench.benchmark.default.default_values import AIRLINES_INPUT_PATH
from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.print_csv import PrintCSV
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement


def benchmark_read(
    print_csv: PrintCSV,
    read_function: Callable[[Path], Any],
) -> None:
    time_measurement = TimeCPUMeasurement(print_csv)

    for path in PARAM:
        for _ in range(BENCHMARK_ITERATIONS):
            invocation_loop = InvocationLoop()
            invocation_loop.start()

            while invocation_loop.get_is_looping():
                time_measurement.start()

                flights = read_function(path)
                airlines = read_function(AIRLINES_INPUT_PATH)

                time_measurement.stop()

                del flights
                del airlines

            invocation_loop.cancel()

        time_measurement.write_results(path.stem.replace("Flights", ""), "Read")
