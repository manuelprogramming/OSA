"""Represents a basic OSA plugin tool."""

from typing import Protocol
from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult


class BasicOSATool(Protocol):
    """Basic representation of a OSA plugin tool."""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        """Does Some work with a connection to the OSA"""