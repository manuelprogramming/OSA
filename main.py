"""
This is a system to control the Optical Spectrum Analyzer MS9740B by Anritsu with a remote computer
"""
from pyvisa.errors import VisaIOError

from osa.anritsu_wrapper import Anritsu
from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandardEventStatusRegister
from handlers.file import get_data_tools_dict, get_visa_search_term, get_start_text, reset_selected_file
from handlers.cache import save_to_cache
from handlers.result import Result, get_result_types_dict
from handlers.comand import CommandHandler
from handlers.plotting import config_matplotlib


def main() -> None:
    # setting the default file for plotting and saving
    reset_selected_file()

    # config matplotlib
    debug_mode = True
    config_matplotlib(debug_mode)

    # register a couple of BasicTools
    factory.register("identify", Identify)
    factory.register("clear_registers", ClearRegisters)
    factory.register("standard_event_status_register", StandardEventStatusRegister)

    # read bin from a tools_data.json file
    data = get_data_tools_dict()

    # load plugins
    loader.load_plugins(data["plugins"])

    # extracting the result_types
    result_types_str = [item.pop("result_type") for item in data["tools"]]
    result_types_dict = get_result_types_dict()
    result_types = [result_types_dict[res_type] for res_type in result_types_str]

    # create the tools and toolbox
    tools = [factory.create(item) for item in data["tools"]]
    tool_commands = [tool.command for tool in tools]
    toolbox = dict(zip(tool_commands, tools))

    # starting text
    print(get_start_text())

    # create the anritsu class
    try:
        anri = Anritsu(get_visa_search_term())
    except VisaIOError:
        anri = None  # used for offline mode
        print("!!!! Couldn't connect to OSA working in offline Mode!!!! \n\n")

    # show the tools available
    for idx, tool in enumerate(tools):
        if hasattr(tool, "anri"):
            tool.anri = anri            # apply the anritsu class to the plugins who need that
        tool.result = Result(result_type=result_types[idx])
        print("####", tool, end="\t\n\n")

    # Create Command Handler Instants
    command_handler = CommandHandler(tool_commands)

    # main program loop
    running = True
    while running:
        print("\n\n#### Send Command:\n")
        command_list: list = command_handler(input())
        for command in command_list:
            if command == "exit":
                running = False
            elif command not in tool_commands:
                print("wrong command")
            else:
                res = toolbox[command].do_work()
                save_to_cache(res)
                print(res)

    # resetting the selected file after closing the program
    reset_selected_file()


if __name__ == "__main__":
    main()

