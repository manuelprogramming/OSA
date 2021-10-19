from osa.tool import BasicTool
from typing import Callable, Dict, Any

tool_creation_funcs: Dict[str, Callable[..., BasicTool]] = {}


def register(tool_type: str, creation_func: Callable[..., BasicTool]):
    """Regsiter a new game Tool type"""
    tool_creation_funcs[tool_type] = creation_func


def unregister(tool_type: str):
    """Unregister a game character type."""
    tool_creation_funcs.pop(tool_type, None)


def create(arguments: Dict[str, Any]) -> BasicTool:
    """Create a game character of a specific type, given a dictionary"""
    args_copy = arguments.copy()
    tool_type = args_copy.pop("type")
    try:
        creation_func = tool_creation_funcs[tool_type]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown tool type {tool_type!r}") from None

