from dataclasses import dataclass
from typing import Any

import pandas as pd
from os import path

from osa import factory
from file_handler import get_latest_file_path
from cache_handler import load_only_array_results


@dataclass
class SaveData:
    """
    Plots the Data from the Cache perform "get_data" before executing
    """
    command: str

    def do_work(self) -> Any:
        arg = load_only_array_results()
        if not arg:
            return "retrieve Data before plotting"

        file_path = get_latest_file_path()

        if path.getsize(file_path) == 0:
            return self._save_data(file_path, arg)
        else:
            return self._append_and_save_data(file_path, arg)

    def _save_data(self, file_path, arg) -> str:
        wave_length, intensity = arg
        column_name = self._ask_column_name()
        df = pd.DataFrame(data=intensity, index=wave_length, columns=[column_name])
        df.index.name = "wavelength [nm]"
        df.to_csv(file_path)
        return "data_saved"

    def _append_and_save_data(self, file_path, arg) -> str:
        _, intensity = arg
        df = pd.read_csv(file_path, index_col=0)
        column_name = self._ask_column_name()
        if not len(df) == len(intensity):
            return "for appending bin to file the sample points must match\n" \
                   f"bin points in file: {len(df)}, bin points appended bin: {len(intensity)}"
        else:
            df[column_name] = intensity
            df.to_csv(file_path)
            return "data_saved"

    @staticmethod
    def _ask_column_name() -> str:
        print("#### Column Name? (eg. bending radius: '6.25_up')")
        return input()


def initialize() -> None:
    factory.register("save_data", SaveData)






