"""
This is a system to control the Optical Spectrum Analyzer MS9740B by Anritsu from a remote computer
"""

import json

from osa.anritsu_wrapper import Anritsu

from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandardEventStatusRegister
from file_handler import get_data_dict, get_visa_search_term


def main() -> None:

    res = None
    running = True

    # register a couple of BasicTools

    factory.register("identify", Identify)
    factory.register("clear_registers", ClearRegisters)
    factory.register("standard_event_status_register", StandardEventStatusRegister)

    # read data from a JSON file

    data = get_data_dict()

    # load plugins

    loader.load_plugins(data["plugins"])

    # create the tools and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.command for tool in tools]
    toolbox = dict(zip(tool_names, tools))

    # create the anritsu class

    anri = Anritsu(get_visa_search_term())

    # anri = ""                     # used for offline mode

    # apply the anritsu class to the tools who need that
    for tool in tools:
        if hasattr(tool, "anri"):
            tool.anri = anri
        print(tool, end="\t\n\n")

    # main programm loop
    while running:
        print("\n\n#### Send Command:\n")
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