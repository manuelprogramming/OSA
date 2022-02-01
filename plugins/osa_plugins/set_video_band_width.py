from dataclasses import dataclass

from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult

from handlers.file import get_setting


@dataclass
class SetVideoBandWidth:
    """
    Sets the Video Band Width given in the settings.json file.
    Valid Video Band Widths: 10HZ|100HZ|200HZ|1KHZ|2KHZ|10KHZ|100KHZ|1MHZ|200HZFAST|1KHZFAST
                           |10|100|200|1000|2000|10000|100000|1000000|200FAST|1000FAST
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        video_band_width = get_setting("video_bandwidth")
        self._set_video_bandwidth(video_band_width)
        return self._success_result(video_band_width)

    def _set_video_bandwidth(self, video_band_width: str) -> None:
        self.anri.write(f"VBW {video_band_width}")

    def _success_result(self, video_band_width: str) -> BaseResult:
        self.result.msg = f"Video Band Width set to {video_band_width}"
        self.result.value = video_band_width
        return self.result


def initialize() -> None:
    factory.register("set_video_band_width", SetVideoBandWidth)
