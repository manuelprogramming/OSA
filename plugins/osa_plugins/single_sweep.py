from time import sleep
import sys

from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult



@dataclass
class SingleSweep:
    """Performs a single sweep and prints message on completion"""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
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
        bar = 0
        while sweap_completed == 0:
            sweap_completed = int(self.anri.query(":STAT:EVEN:COND?"))
            sys.stdout.write(f"\rSweeping: {'=' * bar}>")
            sys.stdout.flush()
            sleep(0.5)
            bar += 1

        print("")

    def _do_single_sweep(self) -> None:
        self.anri.write(":INIT")
        self._check_status()




def initialize() -> None:
    factory.register("single_sweep", SingleSweep)