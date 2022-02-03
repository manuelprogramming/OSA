from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult


@dataclass
class LightOutput:
    """Queries the light output. And sets turns it ON or OFF accordingly"""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        light = self.query_light()
        light_dict = {"OFF": "ON",
                      "ON": "OFF"}
        light = light_dict[light.strip()]
        self.anri.write(f"OPT {light}")

        self.result.msg = f"Turned optical light output {self.query_light()}"
        return self.result

    def query_light(self) -> str:
        return self.anri.query("OPT?")


def initialize():
    factory.register("light_output", LightOutput)
