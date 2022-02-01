from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import set_setting, get_valid_setting


@dataclass
class ChangeVideoBandWidth:
    """
    Change the Video Band Width in settings.json. Use "VDW" for setting the Video Band Width of the OSA
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        video_band_width: str = self.ask_video_band_width()
        self._change_video_band_width(video_band_width)
        return self.result

    def _change_video_band_width(self, video_band_with: str) -> None:
        if video_band_with not in get_valid_setting("video_band_width"):
            self._fail_result(video_band_with)
        else:
            set_setting("video_band_width", video_band_with)
            self._success_result(video_band_with)

    def _success_result(self, video_band_width: str) -> None:
        self.result.msg = f"Video Band Width changed to {video_band_width}"
        self.result.value = video_band_width

    def _fail_result(self, video_band_width: str) -> None:
        self.result.msg = f"Video Band Width not valid '{video_band_width}' \n" \
                          f"Valid Video Band Widths: {get_valid_setting('memory_slots')}"
        self.result.value = video_band_width

    @staticmethod
    def ask_video_band_width() -> str:
        return input(f"#### Specify The Video Band Width. Valid Band Widths are {get_valid_setting('video_band_width')}\n")


def initialize() -> None:
    factory.register("change_video_band_width", ChangeVideoBandWidth)