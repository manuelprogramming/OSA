from dataclasses import dataclass
from typing import Any
import pandas as pd
from os import path

from osa import factory


@dataclass
class SaveData:
    """
    Plots the Data from the Cache perform "get_data" before executing
    """
    command: str

    def do_work(self, settings, *args) -> Any:
        arg = args[0]
        if not isinstance(arg, tuple):
            return "retrieve Data before plotting"

        file_path = self._get_saving_path(settings)
        self._save_data(file_path, args)
        return "data saved"

    @staticmethod
    def _save_data(file_path, args) -> None:
        wave_length, intensity = args[0]
        df = pd.DataFrame(data=intensity, index=wave_length)
        df.to_csv(file_path)

    @staticmethod
    def _get_saving_path(settings):
        saving_path = settings["saving_path"]
        file_name = settings["file_name"]
        return path.join(saving_path, file_name)


def initialize() -> None:
    factory.register("save_data", SaveData)
