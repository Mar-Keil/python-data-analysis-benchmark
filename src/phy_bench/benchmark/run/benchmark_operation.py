import shutil

from pathlib import Path
from typing import Any
from typing import Callable

from phy_bench.benchmark.default.default_values import BENCHMARK_ITERATIONS
from phy_bench.benchmark.default.default_values import PARAM
from phy_bench.benchmark.default.invocation_loop import InvocationLoop
from phy_bench.benchmark.default.print_csv import PrintCSV
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement


def prepare_result_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def clear_result_directory(path: Path) -> None:
    if not path.exists():
        return

    for child in path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def benchmark_operation(
    print_csv: PrintCSV,
    output_dir: Path,
    read_function: Callable[[Path], Any],
    write_function: Callable[[Any, Path], None],
    operation_function: Callable[..., Any],
    result_directory: str,
    method_name: str,
    write_method_name: str,
    other_dataset: Any | None = None,
) -> None:
    logic_measurement = TimeCPUMeasurement(print_csv)
    write_measurement = TimeCPUMeasurement(print_csv)

    for path in PARAM:
        dataset = read_function(path)
        result_path = output_dir / result_directory
        prepare_result_directory(result_path)

        for iteration_index in range(BENCHMARK_ITERATIONS):
            invocation_loop_logic = InvocationLoop()
            invocation_loop_logic.start()

            while invocation_loop_logic.get_is_looping():
                logic_measurement.start()

                if other_dataset is None:
                    operation_result = operation_function(dataset)
                else:
                    operation_result = operation_function(dataset, other_dataset)

                logic_measurement.stop()

                del operation_result

            invocation_loop_logic.cancel()

            if other_dataset is None:
                operation_result = operation_function(dataset)
            else:
                operation_result = operation_function(dataset, other_dataset)

            invocation_loop_write = InvocationLoop()
            invocation_loop_write.start()
            write_invocation = 0

            while invocation_loop_write.get_is_looping():
                write_invocation += 1
                write_output_path = (
                    result_path / f"{write_invocation}_{result_directory}.parquet"
                )
                write_measurement.start()

                write_function(operation_result, write_output_path)

                write_measurement.stop()

            invocation_loop_write.cancel()

            del operation_result

            is_last_iteration = iteration_index == BENCHMARK_ITERATIONS - 1
            if not is_last_iteration:
                clear_result_directory(result_path)

        benchmark_size = path.stem.replace("Flights", "")
        logic_measurement.write_results(benchmark_size, method_name)
        write_measurement.write_results(benchmark_size, write_method_name)
