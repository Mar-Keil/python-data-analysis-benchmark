from phy_bench.benchmark.default.default_values import AIRLINES_INPUT_PATH
from phy_bench.benchmark.run.benchmark_operation import benchmark_operation
from phy_bench.benchmark.run.benchmark_read import benchmark_read
from phy_bench.benchmark.run.engine_config import ENGINE_CONFIGS
from phy_bench.benchmark.default.print_csv import PrintCSV


class BenchmarkRunner:
    def __init__(self) -> None:
        self.engine_configs = ENGINE_CONFIGS

    def run_engine_benchmarks(self, engine_name: str) -> None:
        config = self.engine_configs[engine_name]
        print_csv = PrintCSV(config.output_dir)

        benchmark_read(print_csv, config.read_for_benchmark)

        for operation in ("filter", "sort", "pivot", "group_count", "join"):
            operation_config = config.operations[operation]
            other_dataset = None

            if operation_config.needs_other_dataset:
                other_dataset = config.read_for_operation(AIRLINES_INPUT_PATH)

            benchmark_operation(
                print_csv,
                config.output_dir,
                config.read_for_operation,
                config.write,
                operation_config.function,
                operation_config.result_directory,
                operation_config.method_name,
                operation_config.write_method_name,
                other_dataset=other_dataset,
            )

    def run_selected_benchmark(self, selected_benchmark: str) -> None:
        if selected_benchmark not in {"polars", "pandas", "duckdb", "all"}:
            raise ValueError(
                "Invalid benchmark selection. Please choose Polars, Pandas, DuckDB, or All."
            )

        if selected_benchmark in {"polars", "all"}:
            self.run_engine_benchmarks("polars")
        if selected_benchmark in {"pandas", "all"}:
            self.run_engine_benchmarks("pandas")
        if selected_benchmark in {"duckdb", "all"}:
            self.run_engine_benchmarks("duckdb")


def main() -> None:
    selected_benchmark = input(
        "What benchmark do you want to run?\n"
        "- Polars\n"
        "- Pandas\n"
        "- DuckDB\n"
        "- All\n"
    ).strip().lower()

    BenchmarkRunner().run_selected_benchmark(selected_benchmark)


if __name__ == "__main__":
    main()
