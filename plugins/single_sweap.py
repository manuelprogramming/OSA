"""Game extenxion that adds a bard character"""

from dataclasses import dataclass
from osa import factory

from time import sleep


@dataclass
class SingleSweap:
    """performs a single sweap and prints message on completion"""
    anri: object
    name: str

    def do_work(self, *args) -> None:
        # self._do_single_sweap()
        print("Sweaped finfished")

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

    def _do_single_sweap(self) -> None:
        self.anri.write(":INIT")
        self._check_status()
        print(f"Completed Sweap")


def initialize() -> None:
    factory.register("single_sweap", SingleSweap)