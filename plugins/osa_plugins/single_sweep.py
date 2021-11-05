"""Game extenxion that adds a bard character"""

from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu

from time import sleep


@dataclass
class SingleSweep:
    """performs a single sweap and prints message on completion"""
    command: str
    anri: BaseAnritsu

    def do_work(self) -> str:
        self._do_single_sweep()
        return "Sweaped finfished"

    def _check_status(self) -> None:
        """
        when sweapo_completed != 0 then it breaks the while loop and more commands can be send
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
        print(f"Completed Sweap")


def initialize() -> None:
    factory.register("single_sweep", SingleSweep)