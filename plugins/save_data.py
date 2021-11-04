from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from os import path

from osa import factory
from file_handler import get_latest_file_path


@dataclass
class SaveData:
    """
    Plots the Data from the Cache perform "get_data" before executing
    """
    command: str

    def do_work(self, *args) -> Any:
        arg = args[0]
        my_arr = np.array([])
        if not arg:
            return "retrieve Data before plotting"
        if not (isinstance(arg[0], type(my_arr)) or isinstance(arg[1], type(my_arr))):
            return "retrieve Data before plotting"



        file_path = get_latest_file_path()
        if path.getsize(file_path) == 0:
            return self._save_data(file_path, args)
        else:
            return self._append_and_save_data(file_path, args)

    def _save_data(self, file_path, args) -> str:
        wave_length, intensity = args[0]
        column_name = self._ask_column_name()
        df = pd.DataFrame(data=intensity, index=wave_length, columns=[column_name])
        df.index.name = "wavelength [nm]"
        df.to_csv(file_path)
        return "data_saved"

    def _append_and_save_data(self, file_path, args) -> str:
        _, intensity = args[0]
        df = pd.read_csv(file_path, index_col=0)
        column_name = self._ask_column_name()
        if len(df) == len(intensity):
            df[column_name] = intensity
            df.to_csv(file_path)
            return "data_saved"
        else:
            return "for appending data to file the sample points must match\n" \
                   f"data points in file: {len(df)}, data points appended data: {len(intensity)}"

    @staticmethod
    def _ask_column_name() -> str:
        print("#### Column Name? (eg. bending radius: '6.25_up')")
        return input()


def initialize() -> None:
    factory.register("save_data", SaveData)






