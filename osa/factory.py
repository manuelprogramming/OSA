from osa.tool import BasicTool

from typing import Callable, Dict, Any

tool_creation_funcs: Dict[str, Callable[..., BasicTool]] = {}


def register(tool_name: str, creation_func: Callable[..., BasicTool]):
    """Register a new tool"""
    tool_creation_funcs[tool_name] = creation_func


def unregister(tool_name: str):
    """Unregister a tool type."""
    tool_creation_funcs.pop(tool_name, None)


def create(arguments: Dict[str, Any]) -> BasicTool:
    """Create a tool with a specific command, given a dictionary"""
    args_copy = arguments.copy()
    tool_name = args_copy.pop("name")
    try:
        creation_func = tool_creation_funcs[tool_name]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown tool name {tool_name!r}") from None

