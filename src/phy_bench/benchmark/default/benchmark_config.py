from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Callable


ReadFunction = Callable[[Path], Any]
WriteFunction = Callable[[Any, Path], None]
UnaryOperation = Callable[[Any], Any]
BinaryOperation = Callable[[Any, Any], Any]


@dataclass(frozen=True)
class OperationConfig:
    function: UnaryOperation | BinaryOperation
    result_directory: str
    method_name: str
    write_method_name: str
    needs_other_dataset: bool = False


@dataclass(frozen=True)
class EngineConfig:
    output_dir: Path
    read_for_benchmark: ReadFunction
    read_for_operation: ReadFunction
    write: WriteFunction
    operations: dict[str, OperationConfig]
