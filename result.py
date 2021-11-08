from dataclasses import dataclass
from typing import Any, Protocol, Optional
from enum import Enum, auto


class ResultType(Enum):
    noneResult = auto()
    arrayResult = auto()
    valueResult = auto()
    dictResult = auto()


class BaseResult(Protocol):
    """Basic Representation of the Result class"""
    msg: str
    value: Any
    result_type: ResultType

    def __repr__(self):
        """prints out the massage of the result"""

    def __str__(self):
        """prints out the massage of the result"""


@dataclass
class Result:
    msg: Optional[str] = None
    value: Optional[Any] = None
    result_type: Optional[ResultType] = None

    def __repr__(self):
        return str(self.msg)

    def __str__(self):
        return str(self.msg)


if __name__ == '__main__':
    print(str({"bla":2}))