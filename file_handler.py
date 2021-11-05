"""functions for Handling the files"""
from os import path, listdir
import json
from typing import Dict, Any, List
from datetime import datetime
import numpy as np


def get_base_path() -> str:
    return path.dirname(__file__)


def get_start_text() -> str:
    with open(path.join(get_base_path(), "bin/start.txt"), "r") as t:
        return t.read()


def get_visa_search_term() -> str:
    base_path = get_base_path()
    visa_path = path.join(base_path, "bin/visa_search_term.json")
    with open(visa_path) as visa_json:
        return json.load(visa_json)["visa_search_term"]


def get_settings_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "bin/settings.json")


def get_settings_dict() -> Dict[str, Any]:
    settings_path = get_settings_path()
    with open(settings_path) as file:
        return json.load(file)


def get_saving_path() -> str:
    base_path = get_base_path()
    saving_folder = get_settings_dict()["saving_folder"]
    saving_path = path.join(base_path, saving_folder)
    return saving_path


def find_all_timestampStrs() -> List[str]:
    saving_path = get_saving_path()
    timestampStrs = [f[:-4] for f in listdir(saving_path) if f.endswith(".csv")]
    return timestampStrs


def find_latest_file() -> str:
    saving_path = get_saving_path()
    if listdir(saving_path):
        return [f for f in listdir(saving_path) if f.endswith(".csv")][-1]


def get_latest_file_path() -> str:
    saving_path = get_saving_path()
    latest_file = find_latest_file()
    if latest_file:
        return path.join(saving_path, latest_file)


def get_file_name_format() -> str:
    return get_settings_dict()["file_name_format"]


def get_data_tools_dict() -> json:
    data_path = path.join(get_base_path(), "bin/tools_data.json")
    with open(data_path) as file:
        data = json.load(file)
    return data


def _convert_str_to_datetime(timestampStr: str) -> datetime:
    dt_format = get_file_name_format()
    return datetime.strptime(timestampStr, dt_format)


def get_valid_settings_dict() -> dict:
    with open(path.join(get_base_path(), "plugins/change_settings/valid_settings.json"), "r") as f:
        return json.load(f)


def get_valid_sampling_points() -> List[int]:
    return get_valid_settings_dict()["sampling_points"]


def get_valid_memory_slots() -> List[str]:
    return get_valid_settings_dict()["memory_slots"]


if __name__ == '__main__':
    my_data = [list(np.random.random(5)), list(np.random.random(5))]
    print(my_data)
    with open("bin/cache.json", "w") as f:
        json.dump(list(my_data), f, indent=4)
