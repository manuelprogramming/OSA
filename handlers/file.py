"""functions for Handling the files"""
from os import path, listdir, mkdir
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime


# Path Getters


def get_base_path() -> str:
    return path.dirname(path.dirname(__file__))


def get_saving_path() -> str:
    return path.join(get_base_path(), get_setting("saving_folder"))


def get_bin_files_path(file_name: str) -> str:
    full_file_name = "bin/" + file_name
    return path.join(get_base_path(), full_file_name)


def get_selected_file_path() -> str:
    """
    returns the selected file path if no filepath is selected returns latest file created in the saving folder
    """
    selected_file_name = get_setting("selected_file")
    if _selected_file_exists(selected_file_name):
        return selected_file_name
    latest_file = _find_latest_file_name()
    if latest_file:
        return path.join(get_saving_path(), latest_file)


def _selected_file_exists(selected_file_name: str) -> bool:
    return len(selected_file_name) != 0


def selected_file_is_empty() -> bool:
    return path.getsize(get_selected_file_path()) == 0


# valid settings getters


def get_valid_settings_dict() -> dict:
    with open(path.join(get_base_path(), "bin/valid_settings.json"), "r") as f:
        return json.load(f)


def get_valid_setting(valid_setting_key: str) -> List[int]:
    return get_valid_settings_dict()[valid_setting_key]


# Settings getters

def get_settings_dict() -> Dict[str, Any]:
    settings_path = get_bin_files_path("settings.json")
    with open(settings_path) as file:
        return json.load(file)


def get_setting(setting_key: str) -> Any:
    return get_settings_dict()[setting_key]


# Settings setters

def dump_settings_dict(settings: Dict[str, Any]) -> None:
    with open(get_bin_files_path("settings.json"), "w", encoding='utf-8') as file:
        json.dump(settings, file, indent=4)


def set_setting(setting_key: str, setting_value: Any) -> None:
    settings = get_settings_dict()
    settings[setting_key] = setting_value
    dump_settings_dict(settings)


def reset_selected_file() -> None:
    set_setting("selected_file", "")


# Datetime Functions

def _convert_str_to_datetime(timestampStr: str) -> datetime:
    dt_format = get_setting("file_name_format")
    try:
        return datetime.strptime(timestampStr, dt_format)
    except ValueError:
        pass


def _convert_datetime_to_str(dateTimeObj: datetime, time_format: str = get_setting("file_name_format")) -> str:
    return dateTimeObj.strftime(time_format)


def get_current_date_time_str(time_format: str = get_setting("file_name_format")) -> str:
    dateTimeObj = datetime.now()
    timestampStr = _convert_datetime_to_str(dateTimeObj, time_format)
    return timestampStr


# Some more getters used in the main function

def get_start_text() -> str:
    with open(get_bin_files_path("start.txt"), "r") as t:
        return t.read()


def get_visa_search_term() -> str:
    with open(get_bin_files_path("visa_search_term.json")) as visa_json:
        return json.load(visa_json)["visa_search_term"]


def get_tools_data_dict() -> dict:
    with open(get_bin_files_path("tools_data.json")) as file:
        data = json.load(file)
    return data


# Other

def create_new_folder(folder_name: str) -> bool:
    try:
        mkdir(path.join(get_base_path(), folder_name))
        return True
    except FileExistsError:
        return False


def _find_latest_file_name() -> str:
    files_in_saving_path = listdir(get_saving_path())
    if files_in_saving_path:
        all_files = [_convert_str_to_datetime(f.strip(".csv")) for f in files_in_saving_path if f.endswith(".csv")]
        if all_files:
            all_files.sort()
            return _convert_datetime_to_str(all_files[-1]) + ".csv"


def check_file() -> Tuple[bool, str]:
    file_path = get_selected_file_path()
    if not file_path:
        return False, "No file in the given directory"
    if selected_file_is_empty():
        return False, f"Selected File {file_path} is empty"
    else:
        return True, "file is valid"


if __name__ == '__main__':
    print(get_visa_search_term())
