from dataclasses import dataclass

from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult

from handlers.file import get_setting


@dataclass
class SetSamplingPoints:
    """
    Sets the Sampling Points given in the settings.json file.
    Valid sampling_points: {51|101|251|501|1001|2001|5001|10001|20001|50001}
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        sampling_points = int(get_setting("sampling_points"))
        self._set_sampling_points(sampling_points)
        return self._success_result(sampling_points)

    def _set_sampling_points(self, sampling_points) -> None:
        self.anri.write(f"MPT {sampling_points}")

    def _success_result(self, sampling_points: int) -> BaseResult:
        self.result.msg = f"number of sampling points set to {sampling_points}"
        self.result.value = sampling_points
        return self.result


def initialize() -> None:
    factory.register("set_sampling_points", SetSamplingPoints)