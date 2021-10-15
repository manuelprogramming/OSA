"""Represents a basic game character."""

from typing import Protocol


class BasicTool(Protocol):
    """Basic representation of a Tool"""

    def do_work(self) -> None:
        """Does Some work"""