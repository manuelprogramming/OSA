from dataclasses import dataclass
from handlers.result import BaseResult
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
import sys
from handlers.file import reset_selected_file


@dataclass
class ClearRegisters:
    """
    Clears all the common registers
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        self._clear_registers()
        self.result.msg = "registers Cleared"
        return self.result

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
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        esr = self._get_standard_event_status_register()
        res = "Standard Event Status Register: ", esr
        self.result.msg = f"Standard Event Status Register: {esr}"
        self.result.value = esr
        return self.result

    def _get_standard_event_status_register(self):
        return self.anri.query("*ESR?")


@dataclass
class Identify:
    """ Identifies the OSA and gives the response from an `*IDN?`query."""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        msg = self._identify()
        self.result.msg = f"Connected to {msg}"
        return self.result

    def _identify(self):
        return self.anri.query('*IDN?')


@dataclass
class CloseApp:
    """
    Closes the Application
    """
    command: str
    result: BaseResult


    def do_work(self) -> BaseResult or None:
        reset_selected_file()
        print("Shutting down...")
        sys.exit(0)
