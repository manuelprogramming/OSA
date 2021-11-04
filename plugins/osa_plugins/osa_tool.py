"""Represents a basic OSA plugin tool."""

from typing import Protocol, Any
from osa.anritsu_wrapper import BaseAnritsu


class BasicOSATool(Protocol):
    """Basic representation of a OSA plugin tool."""
    command: str
    anri: BaseAnritsu

    def do_work(self, *args) -> Any:
        """Does Some work with a connection to the OSA"""