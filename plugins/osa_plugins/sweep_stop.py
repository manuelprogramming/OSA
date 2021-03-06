
from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult


@dataclass
class SweepStop:
    """Performs a single sweep and prints message on completion"""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        self.anri.write("SST")
        self.result.msg = "Sweep stopped"
        return self.result


def initialize():
    factory.register("sweep_stop", SweepStop)