"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import json

from osa.anritsu_wrapper import Anritsu

from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandardEventStatusRegister
from file_handler import get_settings_dict, get_data_dict


def create_anritsu():
    with open('settings.json') as json_file:
        data = json.load(json_file)
    visa_search_term = data["visa_search_term"]
    return Anritsu(visa_search_term)


def main() -> None:

    res = None
    running = True

    # register a couple of BasicTools
    factory.register("identify", Identify)
    factory.register("clear_registers", ClearRegisters)
    factory.register("standard_event_status_register", StandardEventStatusRegister)

    # read data from a JSON file

    data = get_data_dict()

    # read out Settings

    settings = get_settings_dict()

    # load plugins

    loader.load_plugins(data["plugins"])

    # create the tools and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.command for tool in tools]
    toolbox = dict(zip(tool_names, tools))


    # create the anritsu class
    anri = create_anritsu()
    # anri = ""

    # apply the anritsu class to each tool
    for tool in tools:
        if hasattr(tool, "anri"):
            tool.anri = anri
        print(tool, end="\t\n\n")

    while running:
        print("#### Send Command:")
        command_str = input()
        if command_str == "exit":
            running = False
        elif command_str not in tool_names:
            print("wrong command")
        else:
            res = toolbox[command_str].do_work(res)
            print(res)


if __name__ == "__main__":
    main()