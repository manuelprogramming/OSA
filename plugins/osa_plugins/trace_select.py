
from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult
from handlers.file import get_setting


@dataclass
class TraceSelect:
    """Selects the active trace given in the settings.json file"""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        active_trace = get_setting('memory_slot').strip('DM')
        self.anri.write(f"TSL {active_trace}")
        self.result.msg = f"Active Trace selected as {active_trace}"
        self.result.value = active_trace
        return self.result


def initialize():
    factory.register("trace_select", TraceSelect)