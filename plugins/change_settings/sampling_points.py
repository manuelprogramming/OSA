from dataclasses import dataclass

from osa import factory
from handlers.file import get_valid_setting, set_setting
from handlers.result import BaseResult


@dataclass
class ChangeSamplingPoints:
    """
    Change the Sampling Points in the settings.json file {51|101|251|501|1001|2001|5001|10001|20001|50001}
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        sampling_points = self._ask_sampling_points()
        self._change_sampling_points(sampling_points)
        return self.result

    def _change_sampling_points(self, sampling_points: int) -> None:
        if sampling_points not in get_valid_setting("sampling_points"):
            self._fail_result(sampling_points)
        else:
            set_setting("sampling_points", sampling_points)
            self._success_result(sampling_points)

    def _success_result(self, sampling_points) -> None:
        self.result.msg = f"number of sampling points changed to {sampling_points}"
        self.result.value = sampling_points

    def _fail_result(self, sampling_points) -> None:
        self.result.msg = f"number of sampling points invalid '{sampling_points}'"
        self.result.value = sampling_points

    @staticmethod
    def _ask_sampling_points() -> int or str:
        ans = input("#### How many sampling points? {51|101|251|501|1001|2001|5001|10001|20001|50001}\n")
        try:
            return int(ans)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_sampling_points", ChangeSamplingPoints)