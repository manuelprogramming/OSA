from typing import List


class CommandHandler:
    def __init__(self, tool_commands: List[str]):
        self.tool_commands = tool_commands

    def __call__(self, command_str: str) -> List[str]:
        command_list = command_str.split(";")
        return [command.strip() for command in command_list]


