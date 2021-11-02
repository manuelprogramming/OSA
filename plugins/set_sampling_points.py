from dataclasses import dataclass

from osa import factory
from osa.anritsu_wrapper import BaseAnritsu
from typing import Tuple
from file_handler import get_settings_dict

@dataclass
class SetSamplingPoints:
    """
    Sets the Sampling Points {51|101|251|501|1001|2001|5001|10001|20001|50001}
    """
    command: str
    anri: BaseAnritsu

    def do_work(self, *args) -> Tuple[str, int]:
        settings = get_settings_dict()
        sampling_points = int(settings["sampling_points"])
        self._set_sampling_points(sampling_points)
        return "number of sampling points set to", sampling_points

    def _set_sampling_points(self, sampling_points) -> None:
        self.anri.write(f"MPT {sampling_points}")


def initialize() -> None:
    factory.register("set_sampling_points", SetSamplingPoints)