from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import set_setting, get_valid_setting


@dataclass
class ChangeMemorySlot:
    """
    Change the MemorySlot where the Data is read from by the GetData class
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        memory_slot = self.ask_memory_slot()
        self._change_memory_slot(memory_slot)
        return self.result

    def _change_memory_slot(self, memory_slot) -> None:
        if memory_slot not in get_valid_setting("memory_slots"):
            self._fail_result(memory_slot)
        else:
            set_setting("memory_slot", memory_slot)
            self._success_result(memory_slot)

    def _success_result(self, memory_slot:str) -> None:
        self.result.msg = f"memory_slot changed to {memory_slot}"
        self.result.value = memory_slot

    def _fail_result(self, memory_slot: str) -> None:
        self.result.msg = f"Memory slot not valid '{memory_slot}' \n" \
                          f"Valid memory slots: {get_valid_setting('memory_slots')}"
        self.result.value = memory_slot

    @staticmethod
    def ask_memory_slot() -> int or str:
        return input(f"#### Specify The Memory Slot. Valid Slots are {get_valid_setting('memory_slots')}\n")


def initialize() -> None:
    factory.register("change_memory_slot", ChangeMemorySlot)