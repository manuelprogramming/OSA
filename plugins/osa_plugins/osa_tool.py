"""Represents a basic OSA plugin tool."""

from typing import Protocol, Any
from osa.anritsu_wrapper import BaseAnritsu
from result import BaseResult


class BasicOSATool(Protocol):
    """Basic representation of a OSA plugin tool."""
    command: str
    result: BaseResult
    anri: BaseAnritsu

    def do_work(self) -> BaseResult:
        """Does Some work with a connection to the OSA"""