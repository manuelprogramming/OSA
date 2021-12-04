"""functions for Handling the files"""
from os import path, listdir, mkdir
import json
from typing import Dict, Any, List
from datetime import datetime


def create_new_folder(folder_name: str) -> bool:
    try:
        mkdir(path.join(get_base_path(), folder_name))
        return True
    except FileExistsError:
        return False


def get_start_text() -> str:
    with open(path.join(get_base_path(), "bin/start.txt"), "r") as t:
        return t.read()


def get_visa_search_term() -> str:
    base_path = get_base_path()
    visa_path = path.join(base_path, "bin/visa_search_term.json")
    with open(visa_path) as visa_json:
        return json.load(visa_json)["visa_search_term"]


def find_all_timestampStrs() -> List[str]:
    saving_path = get_saving_path()
    timestampStrs = [f[:-4] for f in listdir(saving_path) if f.endswith(".csv")]
    return timestampStrs


def find_latest_file_name() -> str:
    saving_path = get_saving_path()
    if listdir(saving_path):
        all_files = [_convert_str_to_datetime(f.strip(".csv")) for f in listdir(saving_path) if f.endswith(".csv")]
        all_files.sort()
        return _convert_datetime_to_str(all_files[-1]) + ".csv"


def change_selected_file(file_path: str) -> None:
    settings = get_settings_dict()
    settings["selected_file"] = file_path
    with open(get_settings_path(), "w", encoding='utf-8') as file:
        json.dump(settings, file, indent=4)


def reset_selected_file() -> None:
    change_selected_file("")


def _selected_file(selected_file_name: str) -> bool:
    return len(selected_file_name) != 0


def get_data_tools_dict() -> json:
    data_path = path.join(get_base_path(), "bin/tools_data.json")
    with open(data_path) as file:
        data = json.load(file)
    return data


def _convert_str_to_datetime(timestampStr: str) -> datetime:
    dt_format = get_file_name_format()
    return datetime.strptime(timestampStr, dt_format)


def _convert_datetime_to_str(dateTimeObj: datetime) -> str:
    return dateTimeObj.strftime(get_file_name_format())


def get_current_date_time_str():
    dateTimeObj = datetime.now()
    timestampStr = _convert_datetime_to_str(dateTimeObj)
    return timestampStr


def get_valid_settings_dict() -> dict:
    with open(path.join(get_base_path(), "bin/valid_settings.json"), "r") as f:
        return json.load(f)


def get_valid_sampling_points() -> List[int]:
    return get_valid_settings_dict()["sampling_points"]


def get_valid_memory_slots() -> List[str]:
    return get_valid_settings_dict()["memory_slots"]


# Settings Getters

def get_settings_dict() -> Dict[str, Any]:
    settings_path = get_settings_path()
    with open(settings_path) as file:
        return json.load(file)


def get_sampling_points() -> int:
    return get_settings_dict()["sampling_points"]


def get_start_wavelenght() -> float:
    return get_settings_dict()["start_wavelength"]


def get_stop_wavelength() -> float:
    return get_settings_dict()["stop_wavelength"]


def get_memory_slot() -> str:
    return get_settings_dict()["memory_slot"]


def get_selected_file() -> str:
    return get_settings_dict()["selected_file"]


def get_file_name_format() -> str:
    return get_settings_dict()["file_name_format"]


def get_saving_folder() -> str:
    return get_settings_dict()["saving_folder"]


def get_max_length_ref_data() -> int:
    return get_settings_dict()["max_length_ref_data"]


def get_savgol_settings() -> Dict[str, int]:
    return get_settings_dict()["savgol_settings"]

# Path functions


def get_base_path() -> str:
    return path.dirname(path.dirname(__file__))


def get_saving_path() -> str:
    base_path = get_base_path()
    saving_folder = get_saving_folder()
    saving_path = path.join(base_path, saving_folder)
    return saving_path


def get_selected_file_path() -> str:
    """ returns the selected file path if no filepath is selected returns latest file
    """
    saving_path = get_saving_path()
    selected_file_name = get_selected_file()
    if _selected_file(selected_file_name):
        return selected_file_name
    latest_file = find_latest_file_name()
    if latest_file:
        return path.join(saving_path, latest_file)


def get_settings_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "bin/settings.json")


def get_dummy_data_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "bin/dummy.csv")


def get_cache_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "bin/cache.json")


def get_ref_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "bin/ref.json")




if __name__ == '__main__':
    print(get_saving_path())