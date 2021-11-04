"""
This is a system to control the Optical Spectrum Analyzer MS9740B by Anritsu with a remote computer
"""
from osa.anritsu_wrapper import Anritsu
from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandardEventStatusRegister
from file_handler import get_data_tools_dict, get_visa_search_term, get_start_text


def main() -> None:
    res = None
    running = True

    # register a couple of BasicTools

    factory.register("identify", Identify)
    factory.register("clear_registers", ClearRegisters)
    factory.register("standard_event_status_register", StandardEventStatusRegister)

    # read data from a tools_data.json file

    data = get_data_tools_dict()

    # load plugins

    loader.load_plugins(data["plugins"])

    # create the plugins and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.command for tool in tools]
    toolbox = dict(zip(tool_names, tools))

    # create the anritsu class

    # anri = Anritsu(get_visa_search_term())

    anri = None  # used for offline mode

    # apply the anritsu class to the plugins who need that

    print(get_start_text())
    for tool in tools:
        if hasattr(tool, "anri"):
            tool.anri = anri
        print("####", tool, end="\t\n\n")

    # main program loop

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
