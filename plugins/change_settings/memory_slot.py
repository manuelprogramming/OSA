from dataclasses import dataclass
import json


from osa import factory
from handlers.result import BaseResult
from handlers.file import get_valid_memory_slots, get_settings_path, get_settings_dict


@dataclass
class ChangeMemorySlot:
    """
    Change the MemorySlot where the Data is read from by the GetData class
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        memory_slot = self.ask_memory_slot()
        self._change_memory_slot(memory_slot, settings)
        return self.result

    def _change_memory_slot(self, memory_slot, settings) -> None:
        if memory_slot not in get_valid_memory_slots():
            self._fail_result(memory_slot)
        else:
            settings["memory_slot"] = memory_slot
            with open(get_settings_path(), "w", encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            self._success_result(memory_slot)

    def _success_result(self, memory_slot:str) -> None:
        self.result.msg = f"memory_slot changed to {memory_slot}"
        self.result.value = memory_slot

    def _fail_result(self, memory_slot: str) -> None:
        self.result.msg = f"Memory slot not valid '{memory_slot}' \n" \
                          f"Valid memory slots: {get_valid_memory_slots()}"
        self.result.value = memory_slot

    @staticmethod
    def ask_memory_slot() -> int or str:
        print("#### Specify The Memory Slot. Valid Slots are", get_valid_memory_slots())
        return input()


def initialize() -> None:
    factory.register("change_memory_slot", ChangeMemorySlot)