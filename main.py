"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import json
from os import path

from osa.anritsu_wrapper import Anritsu

from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandartEventStatusRegister


def create_anritsu():
    with open('settings.json') as json_file:
        data = json.load(json_file)
    visa_search_term = data["visa_search_term"]
    return Anritsu(visa_search_term)


def main() -> None:

    res = None
    running = True

    # register a couple of BasicTool types
    factory.register("identify", Identify)
    factory.register("clear_registers", ClearRegisters)
    factory.register("standard_event_status_register", StandartEventStatusRegister)

    # read data from a JSON file

    toolbox_path = path.dirname(__file__)
    toolbox_path = path.join(toolbox_path, "toolbox.json")

    with open(toolbox_path) as file:
        data = json.load(file)

    # read out Settings

    settings_path = path.dirname(__file__)
    # print(settings_path)
    settings_path = path.join(settings_path, "settings.json")

    with open(settings_path) as file:
        settings = json.load(file)

    # load plugins

    loader.load_plugins(data["plugins"])

    # create the tools and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.command for tool in tools]
    toolbox = dict(zip(tool_names, tools))

    anri = create_anritsu()

    # do something with the characters
    for tool in tools:
        tool.anri = anri
        print(tool, end="\t\n")

    while running:
        print("#### Send Command:")
        command_str = input()
        if command_str == "exit":
            running = False
        elif command_str not in tool_names:
            print("wrong command")
        else:
            res = toolbox[command_str].do_work(settings, res)
            print(res)


if __name__ == "__main__":
    main()