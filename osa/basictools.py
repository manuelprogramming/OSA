from dataclasses import dataclass
from typing import Tuple

from osa.anritsu_wrapper import BaseAnritsu


@dataclass
class ClearRegisters:
    """
    Clears all the common registers
    """
    anri: BaseAnritsu
    command: str

    def do_work(self, settings) -> str:
        self._clear_registers()
        return "registers Cleared"

    def _clear_registers(self) -> None:
        self.anri.write("*CLS")


@dataclass
class StandartEventStatusRegister:
    """
    This command queries the standard event status register value.
    The standard event status register value is cleared after readout.
    This value is the logical product of the 8 bits set by *ESE.
    """
    anri: BaseAnritsu
    command: str

    def do_work(self, settings) -> Tuple[str, str]:
        esr = self._get_standard_event_status_register()
        res = "Standart Event Status Register: ", esr
        return res

    def _get_standard_event_status_register(self):
        return self.anri.query("*ESR?")


@dataclass
class Identify:
    anri: BaseAnritsu
    command: str

    def do_work(self, settings) -> str:
        msg = self._identify()
        return f"Connected to {msg}"

    def _identify(self):
        """
        Returns:
            str: The response from an `*IDN?`query.
        """
        return self.anri.query('*IDN?')
