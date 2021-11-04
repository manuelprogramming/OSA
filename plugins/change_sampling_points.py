from dataclasses import dataclass
from typing import Tuple
import json


from osa import factory
from file_handler import get_settings_dict, get_settings_path, get_valid_sampling_points


@dataclass
class ChangeSamplingPoints:
    """
    Change the Sampling Points in the setting.json file {51|101|251|501|1001|2001|5001|10001|20001|50001}
    """
    command: str

    def do_work(self, *args) -> Tuple[str, int]:
        settings = get_settings_dict()
        sampling_points = self._ask_sampling_points()
        return self._change_sampling_points(sampling_points, settings)

    @staticmethod
    def _change_sampling_points(sampling_points, settings):
        if sampling_points in get_valid_sampling_points():
            settings["sampling_points"] = sampling_points
            with open(get_settings_path(), "w", encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            return "number of sampling points changed to", sampling_points
        else:
            return "number of sampling points invalid", sampling_points

    @staticmethod
    def _ask_sampling_points() -> int or str:
        print("#### How many sampling points? {51|101|251|501|1001|2001|5001|10001|20001|50001}")
        ans = input()
        try:
            return int(ans)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_sampling_points", ChangeSamplingPoints)