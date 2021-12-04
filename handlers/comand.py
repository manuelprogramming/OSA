from typing import List


class CommandHandler:
    def __init__(self, tool_commands: List[str]):
        self.tool_commands = tool_commands

    def __call__(self, command_str: str) -> List[str]:
        command_list = self.split_commands(command_str)
        return [command.strip() for command in command_list]

    @staticmethod
    def split_commands(command_str: str) -> List[str]:
        return command_str.split(";")


if __name__ == '__main__':
    pass
