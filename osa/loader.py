"""A simple plugin loader"""

import importlib

from typing import List


class PluginInterface:
    """A Plugin has a single function called initialize"""

    @staticmethod
    def initialize() -> None:
        """Initialize the plugin."""


def import_module(name: str):
    return importlib.import_module(name)  # type: ignore


def load_plugins(plugins: List[str]) -> None:
    """load the plugins defined in the plugins list."""
    for plugin_name in plugins:
        plugin = import_module(plugin_name)
        plugin.initialize()



