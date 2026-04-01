from phy_bench.benchmark.default.default_values import POLARS_OUT_DIR
from phy_bench.benchmark.default.print_csv import PrintCSV
from phy_bench.benchmark.default.time_cpu_measurement import TimeCPUMeasurement
from phy_bench.benchmark.run_polars import (
    run_read_benchmark,
    run_filter_benchmark,
    run_sort_benchmark,
    run_pivot_benchmark,
    run_group_count_benchmark,
    run_join_benchmark,
)


def main() -> None:
    print_csv = PrintCSV(POLARS_OUT_DIR)

    logic_measurement = TimeCPUMeasurement(print_csv)
    write_measurement = TimeCPUMeasurement(print_csv)

    run_read_benchmark(TimeCPUMeasurement(print_csv))
    run_filter_benchmark(logic_measurement, write_measurement, POLARS_OUT_DIR)
    run_sort_benchmark(logic_measurement, write_measurement, POLARS_OUT_DIR)
    run_pivot_benchmark(logic_measurement, write_measurement, POLARS_OUT_DIR)
    run_group_count_benchmark(logic_measurement, write_measurement, POLARS_OUT_DIR)
    run_join_benchmark(logic_measurement, write_measurement, POLARS_OUT_DIR)


if __name__ == "__main__":
    main()
