"""
This is a system to control the Optical Spectrum Analyzer MS9740B by Anritsu with a remote computer
"""
from osa.anritsu_wrapper import Anritsu
from osa import factory, loader
from osa.basictools import Identify, ClearRegisters, StandardEventStatusRegister
from file_handler import get_data_tools_dict, get_visa_search_term, get_start_text
from cache_handler import save_to_cache
from result import Result, ResultType

def main() -> None:

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
    result_dict = {str(res_type): res_type for res_type in ResultType}
    result_types = [result_dict[res_type] for res_type in result_types_str]

    # create the plugins and toolbox

    tools = [factory.create(item) for item in data["tools"]]
    tool_names = [tool.command for tool in tools]
    toolbox = dict(zip(tool_names, tools))

    # starting text

    print(get_start_text())

    # create the anritsu class

    try:
        anri = Anritsu(get_visa_search_term())
    except Exception:
        anri = None  # used for offline mode
        print("!!!! Couldn't connect to OSA working in offline Mode!!!! \n\n")

    # show the tools available

    for idx, tool in enumerate(tools):
        if hasattr(tool, "anri"):
            tool.anri = anri            # apply the anritsu class to the plugins who need that
        tool.result = Result(result_type=result_types[idx])
        print("####", tool, end="\t\n\n")

    # main program loop

    running = True

    while running:
        print("\n\n#### Send Command:\n")
        command_str = input()
        if command_str == "exit":
            running = False
        elif command_str not in tool_names:
            print("wrong command")
        else:
            res = toolbox[command_str].do_work()
            save_to_cache(res)
            print(res)


if __name__ == "__main__":
    main()
