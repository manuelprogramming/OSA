"""Represents a basic game character."""

from typing import Protocol, Dict, Any


class BasicTool(Protocol):
    """Basic representation of a Tool"""
    command: str

    def do_work(self, settings: Dict[str, Any], *args) -> Any:
        """Does Some work"""