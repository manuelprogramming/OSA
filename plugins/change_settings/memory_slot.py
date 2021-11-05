from dataclasses import dataclass
from typing import Tuple
import json


from osa import factory
from file_handler import get_valid_memory_slots, get_settings_dict, get_settings_path


@dataclass
class ChangeMemorySlot:
    """
    Change the MemorySlot where the Data is read from by the GetData class
    """
    command: str

    def do_work(self) -> Tuple[str, str]:
        settings = get_settings_dict()
        memory_slot = self.ask_memory_slot()
        return self._change_memory_slot(memory_slot, settings)

    @staticmethod
    def _change_memory_slot(memory_slot, settings) -> Tuple[str, str]:
        if memory_slot in get_valid_memory_slots():
            settings["memory_slot"] = memory_slot
            with open(get_settings_path(), "w", encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            return "memory_slot changed to", memory_slot
        else:
            return "memory slot not valid", memory_slot

    @staticmethod
    def ask_memory_slot() -> int or str:
        print("#### Specify The Memory Slot. Valid Slots are", get_valid_memory_slots())
        return input()


def initialize() -> None:
    factory.register("change_memory_slot", ChangeMemorySlot)