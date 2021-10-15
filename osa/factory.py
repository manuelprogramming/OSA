from osa.tool import BasicTool
from typing import Callable, Dict, Any

character_creation_funcs: Dict[str, Callable[..., BasicTool]] = {}


def register(character_type: str, creation_func: Callable[..., BasicTool]):
    """Regsiter a new game Character type"""
    character_creation_funcs[character_type] = creation_func


def unregister(character_type: str):
    """Unregister a game character type."""
    character_creation_funcs.pop(character_type, None)


def create(arguments: Dict[str, Any]) -> BasicTool:
    """Create a game character of a specific type, given a dictionary"""
    args_copy = arguments.copy()
    character_type = args_copy.pop("type")
    try:
        creation_func = character_creation_funcs[character_type]
        # print(creation_func)
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown character type {character_type!r}") from None

