from time import sleep

from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu
from result import BaseResult


@dataclass
class SingleSweep:
    """Performs a single sweep and prints message on completion"""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    def do_work(self) -> BaseResult:
        self._do_single_sweep()
        self.result.msg = "Sweep finished"
        return self.result

    def _check_status(self) -> None:
        """
        when sweep_completed != 0 then it breaks the while loop and more commands can be send
        Returns: None
        """
        sweap_completed = 0
        self.anri.write("*CLS")
        while sweap_completed == 0:
            sweap_completed = int(self.anri.query(":STAT:EVEN:COND?"))
            print(f"Sweaping... {sweap_completed}")
            sleep(1)

    def _do_single_sweep(self) -> None:
        self.anri.write(":INIT")
        self._check_status()


def initialize() -> None:
    factory.register("single_sweep", SingleSweep)