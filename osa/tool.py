"""Represents a basic tool."""

from typing import Protocol
from handlers.result import BaseResult


class BasicTool(Protocol):
    """Basic representation of a Tool"""
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        """Does Some work"""