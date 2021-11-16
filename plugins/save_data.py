from dataclasses import dataclass

import numpy as np
import pandas as pd
from os import path

from osa import factory
from result import BaseResult
from file_handler import get_latest_file_path, get_settings_dict
from cache_handler import load_only_array_results


@dataclass
class SaveData:
    """
    Saves the Data from the Cache to the last file created in the saving_folder perform "get_data" before executing
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_results = load_only_array_results()
        if not array_results:
            self._fail_result_no_data()
            return self.result
        file_path = get_latest_file_path()
        if not file_path:
            self._fail_result_no_file()
            return self.result
        if path.getsize(file_path) == 0:
            self._save_data(file_path, array_results)
            return self.result
        else:
            self._append_and_save_data(file_path, array_results)
            return self.result

    def _save_data(self, file_path: str, array_results: tuple) -> None:
        wavelength, trace = array_results

        if self._is_points_data(wavelength):
            self._save_as_points_data(file_path, wavelength, trace)
        else:
            self._save_as_trace_data(file_path, wavelength, trace)

        self._success_result()

    def _append_and_save_data(self, file_path: str, array_result: tuple) -> None:
        wavelength, trace = array_result
        df = pd.read_csv(file_path, index_col=0)

        if not len(df) == len(trace):
            self._fail_result_no_match(len(df), len(trace))
        elif self._is_points_data(trace):
            self._append_and_save_as_points_data(file_path, wavelength, trace)
            self._success_result()
        else:
            self._append_and_save_as_trace_data(df, file_path, trace)
            self._success_result()

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
    def _is_points_data(array: np.array):
        return len(array) < get_settings_dict()["max_length_ref_data"]

    def _success_result(self):
        self.result.msg = "data saved successfully"

    def _fail_result_no_data(self):
        self.result.msg = "retrieve Data before plotting"

    def _fail_result_no_match(self, len_df: int, len_trace: int) -> None:
        self.result.msg = "for appending data to file the sample points must match\n" \
                          f"data points in file: {len_df}, data points appended: {len_trace}"

    def _fail_result_no_file(self):
        self.result.msg = "no file in directory use CreateNewFile ('CNF') command to create a new file"

    @staticmethod
    def _ask_column_name() -> str:
        print("#### Column Name? (eg. bending radius: '6.25_up')")
        return input()


def initialize() -> None:
    factory.register("save_data", SaveData)
