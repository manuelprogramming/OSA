from dataclasses import dataclass
from typing import Tuple

from osa import factory
from handlers.file import get_valid_setting, set_setting, get_setting
from handlers.result import BaseResult


@dataclass
class ChangeSavgolFilter:
    """
    Change the Savatzki Golay Filter settings in the settings.json file
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        ans = self._ask_filter_settings()
        if isinstance(ans, str):
            self._fail_result_wrong_input(ans)
            return self.result
        window_length, poly_order = ans
        if not poly_order < window_length < get_setting("sampling_points"):
            self._fail_result_wrong_values(ans)
            return self.result
        if window_length%2 == 0:
            self._fail_result_wrong_window_length(window_length)
            return self.result
        self._set_savgol_settings(window_length, poly_order)
        self._success_result(ans)
        return self.result

    @staticmethod
    def _set_savgol_settings(window_length: int, poly_order: int) -> None:
        savgol_settings = {"window_length": window_length,
                           "poly_order": poly_order}
        set_setting("savgol_settings", savgol_settings)

    def _success_result(self, ans: Tuple[int, int]) -> None:
        self.result.msg = f"Savatzki Golay Filter settings changed to {ans}"
        self.result.value = ans

    def _fail_result_wrong_input(self, ans: str):
        self.result.msg = "The input must be two integer 'window_length, poly_order'"
        self.result.value = ans

    def _fail_result_wrong_window_length(self, window_length: int):
        self.result.msg = "And the window_length must be odd"
        self.result.value = window_length

    def _fail_result_wrong_values(self, ans: Tuple[int, int]):
        self.result.msg = "The window_length must be smaller than the poly_order\n" \
                          "And the window_length must be bigger than the sampling points \n"\
                          f"Given input is: {ans}"
        self.result.value = ans



    @staticmethod
    def _ask_filter_settings() -> int or str:
        ans = input("#### What should be the (window_length, polyorder) \n"
                    "#### window_length <= sampling_points (size of the data) \n"
                    "#### polyorder < window_length \n"
                    "#### window length must be odd \n")
        window_length, poly_order = ans.split(",")
        try:
            return int(window_length), int(poly_order)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_savgol_filter", ChangeSavgolFilter)
