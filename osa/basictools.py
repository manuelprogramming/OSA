from dataclasses import dataclass
from typing import Tuple
from result import BaseResult
from osa.anritsu_wrapper import BaseAnritsu


@dataclass
class ClearRegisters:
    """
    Clears all the common registers
    """
    command: str
    anri: BaseAnritsu
    result: BaseResult

    def do_work(self) -> str:
        self._clear_registers()
        return "registers Cleared"

    def _clear_registers(self) -> None:
        self.anri.write("*CLS")


@dataclass
class StandardEventStatusRegister:
    """
    This command queries the standard event status register value.
    The standard event status register value is cleared after readout.
    This value is the logical product of the 8 bits set by *ESE.
    """
    command: str
    anri: BaseAnritsu
    result: BaseResult

    def do_work(self) -> Tuple[str, str]:
        esr = self._get_standard_event_status_register()
        res = "Standard Event Status Register: ", esr
        return res

    def _get_standard_event_status_register(self):
        return self.anri.query("*ESR?")


@dataclass
class Identify:
    """ Identifies the OSA and gives the response from an `*IDN?`query."""
    command: str
    anri: BaseAnritsu
    result: BaseResult

    def do_work(self) -> str:
        msg = self._identify()
        return f"Connected to {msg}"

    def _identify(self):
        return self.anri.query('*IDN?')
