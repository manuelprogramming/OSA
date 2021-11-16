from typing import List


class CommandHandler:
    def __init__(self, tool_commands: List[str]):
        self.tool_commands = tool_commands

    def __call__(self, command_str: str) -> List[str]:
        command_list = self.split_commands(command_str)
        for command in command_list:
            if command not in self.tool_commands:
                command_list.remove(command)
                return [""]
        return command_list

    def split_commands(self, command_str:str) -> List[str]:
        return command_str.split(";")



if __name__ == '__main__':
    valid_commands =["RST", "PLT", "SSI", "CSTAW"]
    command_str = "RST;BLA;PLT"
    command_handler = CommandHandler(valid_commands)
    print(command_handler(command_str))

