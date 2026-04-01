from time import perf_counter
from time import process_time

from phy_bench.benchmark.default.print_csv import PrintCSV


class TimeCPUMeasurement:
    def __init__(self, print_csv: PrintCSV) -> None:
        self.print_csv = print_csv
        self.time = 0.0
        self.cpu = 0.0
        self.invocations = 0
        self.start_time = 0.0
        self.start_cpu = 0.0

    def reset(self) -> None:
        self.time = 0.0
        self.cpu = 0.0
        self.invocations = 0

    def start(self) -> None:
        self.invocations += 1
        self.start_time = perf_counter()
        self.start_cpu = process_time()

    def stop(self) -> None:
        self.time += perf_counter() - self.start_time
        self.cpu += process_time() - self.start_cpu

    def write_results(self, benchmark_size: str, method: str) -> None:
        time = self.time / self.invocations
        cpu = self.cpu / self.invocations
        cpu_cores = cpu / time

        self.print_csv.write_result(benchmark_size, method, "Time", time, "s/op")
        self.print_csv.write_result(benchmark_size, method, "CPU", cpu_cores, "cores")

        self.reset()
