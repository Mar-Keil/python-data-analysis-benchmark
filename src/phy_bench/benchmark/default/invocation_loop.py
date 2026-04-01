from threading import Timer

from phy_bench.benchmark.default.default_values import BENCHMARK_DURATION_SECONDS


class InvocationLoop:
    def __init__(self) -> None:
        self.is_looping = False
        self.timer: Timer | None = None

    def start(self) -> None:
        self.is_looping = True
        timer = Timer(BENCHMARK_DURATION_SECONDS, self.stop_invocation)
        self.timer = timer
        timer.start()

    def stop_invocation(self) -> None:
        self.is_looping = False

    def cancel(self) -> None:
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def get_is_looping(self) -> bool:
        return self.is_looping
