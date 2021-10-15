"""
Basic example showing how to create objects from data using a dynamic factory with
register/unregister methods.
"""

import json
from os import path

from osa.anritsu_wrapper import Anritsu

from osa import factory, loader
from osa.basictools import Connector, Command, Query


def create_anritsu():
    with open('osa/Settings.json') as json_file:
        data = json.load(json_file)
    visa_search_term = data["visa_search_term"]
    return Anritsu(visa_search_term)


def main() -> None:
    """Creates game characters from a file containg a level definition."""

    # register a couple of BasicTool types
    factory.register("connecter", Connector)
    factory.register("command", Command)
    factory.register("query", Query)

    # read data from a JSON file

    file_path = path.dirname(__file__)
    file_path = path.join(file_path, "level.json")

    with open(file_path) as file:
        data = json.load(file)

    loader.load_plugins(data["plugins"])

    # create the tools and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.name for tool in tools]
    toolbox = dict(zip(tool_names, tools))

    # anri = create_anritsu()

    # do something with the characters
    for tool in tools:
        tool.anri = "Enter Anri"
        print(tool, end="\t")
        tool.do_work(1350, 4000)

    while True:
        print("#### Send Command:")
        comand_str = input()
        if comand_str not in tool_names:
            print("wrong command")
        else:
            toolbox[comand_str].do_work(135, 1450)


if __name__ == "__main__":
    main()