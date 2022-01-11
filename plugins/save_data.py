from dataclasses import dataclass

import numpy as np
import pandas as pd
from os import path
from typing import Tuple

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_setting, get_selected_file_path
from handlers.cache import load_only_array_results


@dataclass
class SaveData:
    """
    Saves the Data from the Cache to the last file created in the saving_folder perform "get_data" before executing
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_results: Tuple[np.array, np.array] = load_only_array_results()
        if not array_results:
            self._fail_result_no_data()
            return self.result
        try:
            file_path = get_selected_file_path()
        except FileNotFoundError:
            self._fail_result_no_dir()
            return self.result
        if not file_path:
            self._fail_result_no_file()
        elif self._file_is_empty(file_path):
            self._save_data(file_path, array_results)
            self._success_result()
        else:
            self._append_and_save_data(file_path, array_results)
        return self.result

    def _save_data(self, file_path: str, array_results: tuple) -> None:
        wavelength, trace = array_results
        if self._is_points_data(wavelength):
            self._save_as_points_data(file_path, wavelength, trace)
        else:
            self._save_as_trace_data(file_path, wavelength, trace)

    def _append_and_save_data(self, file_path: str, array_result: tuple) -> None:
        wavelength, trace = array_result
        df = pd.read_csv(file_path, index_col=0)
        if self._is_points_data(trace) and self._selected_file_is_points_data(file_path):
            self._append_and_save_as_points_data(file_path, wavelength, trace)
            self._success_result()
        elif self._length_matches(df, trace) and not self._selected_file_is_points_data(file_path):
            self._append_and_save_as_trace_data(df, file_path, trace)
            self._success_result()
        else:
            self._fail_result_no_match(len(df), len(trace))

    def _save_as_points_data(self, file_path, wavelength, trace):
        df = self._create_points_df(wavelength, trace)
        df.to_csv(file_path)

    def _save_as_trace_data(self, file_path, wavelength, trace):
        column_name = self._ask_column_name()
        df = pd.DataFrame(data=trace, index=wavelength, columns=[column_name])
        df.index.name = "wavelength [nm]"
        df.to_csv(file_path)

    def _append_and_save_as_points_data(self, file_path, wavelength, trace):
        df = pd.read_csv(file_path, index_col=[0, 1])
        new_df = self._create_points_df(wavelength, trace)
        df = df.append(new_df)
        df.to_csv(file_path)

    def _append_and_save_as_trace_data(self, df: pd.DataFrame,
                                       file_path: str,
                                       trace: np.array):
        column_name = self._ask_column_name()
        df[column_name] = trace
        df.to_csv(file_path)

    def _create_points_df(self, wavelength, trace, ):
        column_name = self._ask_column_name()
        df = pd.DataFrame(data=trace, columns=["trace [dBm]"])
        df.index = [[column_name for _ in wavelength], wavelength]
        df.index.names = ["bending_radius", "wavelength [nm]"]
        return df

    @staticmethod
    def _file_is_empty(file_path: str) -> bool:
        return path.getsize(file_path) == 0

    @staticmethod
    def _length_matches(df: pd.DataFrame, trace:np.array) -> bool:
        return len(df) == len(trace)

    @staticmethod
    def _is_points_data(array: np.array) -> bool:
        return len(array) < get_setting("max_length_ref_data")

    @staticmethod
    def _selected_file_is_points_data(file_path: str) -> bool:
        df = pd.read_csv(file_path, index_col=0)
        return df.index.name != "wavelength [nm]"

    def _success_result(self) -> None:
        self.result.msg = "data saved successfully"

    def _fail_result_no_data(self) -> None:
        self.result.msg = "retrieve Data before plotting"

    def _fail_result_no_dir(self):
        self.result.msg = f"The system coudn't find the saving_folder: {get_setting('saving_folder')}"

    def _fail_result_no_match(self, len_df: int, len_trace: int) -> None:
        self.result.msg = "for appending data to a selected file they both must be points or trace data\n" \
                          "for trace data the sample points must match the sample points in the selected file\n" \
                          f"selected file:{len_df}, data sample points appended: {len_trace}"

    def _fail_result_no_file(self) -> None:
        self.result.msg = "no csv-file in directory use CreateNewFile ('CNF') command to create a new file"

    @staticmethod
    def _ask_column_name() -> str:
        return input("#### Column Name? (eg. bending radius: '6.25_up')\n")


def initialize() -> None:
    factory.register("save_data", SaveData)


if __name__ == '__main__':
    tool = SaveData("SVD", None)
    print(tool._selected_file_is_points_data("C:/Users/profm/PycharmProjects/OSA/saved_data/2021-Nov-16,-,18;32;06.csv"))