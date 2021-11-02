"""functions for Handling the files"""
from os import path, listdir
import json
from typing import Dict, Any, List
from datetime import datetime


def get_base_path() -> str:
    return path.dirname(__file__)


def get_settings_path() -> str:
    base_path = get_base_path()
    return path.join(base_path, "settings.json")


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


def get_data_dict() -> json:
    base_path = get_base_path()
    data_path = path.join(base_path, "data.json")
    with open(data_path) as file:
        data = json.load(file)
    return data


def _convert_str_to_datetime(timestampStr):
    dt_format = get_file_name_format()
    return datetime.strptime(timestampStr, dt_format)


if __name__ == '__main__':
    print(find_latest_file())

