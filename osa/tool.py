"""Represents a basic tool."""

from typing import Protocol, Any


class BasicTool(Protocol):
    """Basic representation of a Tool"""
    command: str

    def do_work(self) -> Any:
        """Does Some work"""