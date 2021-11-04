import json
from typing import Any
import numpy as np
from enum import Enum, auto


class ResultType(Enum):
    strResult = auto()
    arrayResult = auto()
    strValueResult = auto()


result_dict = {str(res_type): res_type for res_type in ResultType}


def save_to_cache(res: Any) -> None:
    res_type = check_type(res)
    formated_res = format_result(res, res_type)
    mydict = {str(res_type): formated_res}
    with open("cache.json", "w") as f:
        json.dump(mydict, f, indent=4)


def format_result(res: Any, res_type: ResultType) -> Any:
    if res_type == ResultType.strResult:
        return res
    if res_type == ResultType.arrayResult:
        return list(res[0]), list(res[1])
    if res_type == ResultType.strValueResult:
        return res[0], res[1]


def check_type(res: Any) -> ResultType:
    myarr = np.array([])
    if isinstance(res, str):
        return ResultType.strResult
    if isinstance(res[0], type(myarr)) and isinstance(res[1], type(myarr)):
        return ResultType.arrayResult
    else:
        return ResultType.strValueResult


def load_from_cache() -> Any:
    with open("cache.json", "r") as f:
        cache = json.load(f)
    res_type = check_loaded_res_type(cache)
    res = cache[str(res_type)]
    return reformat_result(res, res_type)


def reformat_result(res, res_type):
    if res_type == ResultType.strResult:
        return res
    if res_type == ResultType.arrayResult:
        return np.array(res[0]), np.array(res[1])
    if res_type == ResultType.strValueResult:
        return res[0], res[1]


def check_loaded_res_type(cache) -> ResultType:
    res_type = list(cache.keys())[0]
    return result_dict[res_type]


if __name__ == '__main__':
    myar1 = np.random.random(5)
    myar2 = np.random.random(5)
    mytuple = ("oand", 998)
    save_to_cache("check this")

    print(load_from_cache())
