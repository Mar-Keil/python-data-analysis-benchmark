from pathlib import Path

from phy_bench.benchmark.default.benchmark_config import EngineConfig
from phy_bench.benchmark.default.benchmark_config import OperationConfig
from phy_bench.benchmark.default.benchmark_config import ReadFunction
from phy_bench.benchmark.default.benchmark_config import UnaryOperation
from phy_bench.benchmark.default.benchmark_config import BinaryOperation
from phy_bench.benchmark.default.benchmark_config import WriteFunction
from phy_bench.benchmark.default.default_values import DUCKDB_OUT_DIR
from phy_bench.benchmark.default.default_values import PANDAS_OUT_DIR
from phy_bench.benchmark.default.default_values import POLARS_OUT_DIR
from phy_bench.logic import duckdb_logic
from phy_bench.logic import pandas_logic
from phy_bench.logic import polars_logic


def create_operation_configs(
    filter_function: UnaryOperation,
    sort_function: UnaryOperation,
    pivot_function: UnaryOperation,
    group_count_function: UnaryOperation,
    join_function: BinaryOperation,
) -> dict[str, OperationConfig]:
    return {
        "filter": OperationConfig(
            function=filter_function,
            result_directory="filter",
            method_name="Filter",
            write_method_name="WriteFilter",
        ),
        "sort": OperationConfig(
            function=sort_function,
            result_directory="sort",
            method_name="Sort",
            write_method_name="WriteSort",
        ),
        "pivot": OperationConfig(
            function=pivot_function,
            result_directory="pivot",
            method_name="Pivot",
            write_method_name="WritePivot",
        ),
        "group_count": OperationConfig(
            function=group_count_function,
            result_directory="group_count",
            method_name="GroupCount",
            write_method_name="WriteGroupCount",
        ),
        "join": OperationConfig(
            function=join_function,
            result_directory="join",
            method_name="Join",
            write_method_name="WriteJoin",
            needs_other_dataset=True,
        ),
    }


def create_engine_config(
    output_dir: Path,
    read_for_benchmark: ReadFunction,
    read_for_operation: ReadFunction,
    write_function: WriteFunction,
    filter_function: UnaryOperation,
    sort_function: UnaryOperation,
    pivot_function: UnaryOperation,
    group_count_function: UnaryOperation,
    join_function: BinaryOperation,
) -> EngineConfig:
    return EngineConfig(
        output_dir=output_dir,
        read_for_benchmark=read_for_benchmark,
        read_for_operation=read_for_operation,
        write=write_function,
        operations=create_operation_configs(
            filter_function,
            sort_function,
            pivot_function,
            group_count_function,
            join_function,
        ),
    )


ENGINE_CONFIGS: dict[str, EngineConfig] = {
    "pandas": create_engine_config(
        output_dir=PANDAS_OUT_DIR,
        read_for_benchmark=pandas_logic.read_parquet,
        read_for_operation=pandas_logic.read_parquet,
        write_function=pandas_logic.write_parquet,
        filter_function=pandas_logic.filter_dataset,
        sort_function=pandas_logic.sort_dataset,
        pivot_function=pandas_logic.pivot_dataset,
        group_count_function=pandas_logic.group_count_dataset,
        join_function=pandas_logic.join_dataset,
    ),
    "polars": create_engine_config(
        output_dir=POLARS_OUT_DIR,
        read_for_benchmark=polars_logic.read_parquet,
        read_for_operation=polars_logic.read_parquet,
        write_function=polars_logic.write_parquet,
        filter_function=polars_logic.filter_dataset,
        sort_function=polars_logic.sort_dataset,
        pivot_function=polars_logic.pivot_dataset,
        group_count_function=polars_logic.group_count_dataset,
        join_function=polars_logic.join_dataset,
    ),
    "duckdb": create_engine_config(
        output_dir=DUCKDB_OUT_DIR,
        read_for_benchmark=duckdb_logic.read_parquet,
        read_for_operation=duckdb_logic.read_parquet,
        write_function=duckdb_logic.write_parquet,
        filter_function=duckdb_logic.filter_dataset,
        sort_function=duckdb_logic.sort_dataset,
        pivot_function=duckdb_logic.pivot_dataset,
        group_count_function=duckdb_logic.group_count_dataset,
        join_function=duckdb_logic.join_dataset,
    ),
}
