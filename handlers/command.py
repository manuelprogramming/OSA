from typing import List, Any

from handlers.cache import save_to_cache


class CommandHandler:
    def __init__(self, toolbox):
        self.tool_commands = toolbox.keys()
        self.toolbox = toolbox

    @staticmethod
    def split(command_str: str) -> List[str]:
        command_list = command_str.split(";")
        return [command.strip() for command in command_list]



