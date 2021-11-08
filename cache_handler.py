import json
from typing import Any
import numpy as np
from typing import Tuple
from result import Result, ResultType, BaseResult


result_dict = {str(res_type): res_type for res_type in ResultType}


def save_to_cache(res: BaseResult) -> None:
    res_type = res.result_type
    formated_res = format_result(res, res_type)
    cache_dict = {str(res_type): formated_res}
    with open("bin/cache.json", "w") as f:
        json.dump(cache_dict, f, indent=4)


def format_result(res: Any, res_type: ResultType) -> Any:
    if res_type == ResultType.noneResult:
        return res.msg
    if res_type == ResultType.dictResult:
        return res.value
    if res_type == ResultType.arrayResult and res.value:
        return list(res.value[0]), list(res.value[1])
    if res_type == ResultType.valueResult:
        return res.value


def load_from_cache() -> Any:
    cache = get_cache_dict()
    res_type = check_loaded_res_type(cache)
    res = cache[str(res_type)]
    return reformat_result(res, res_type)


def get_result_from_cache(cache: dict, res_type: ResultType) -> Any:
    return cache[str(res_type)]


def get_cache_dict() -> dict:
    with open("bin/cache.json", "r") as f:
        return json.load(f)


def reformat_result(res: Any, res_type: ResultType):
    if res_type == ResultType.noneResult:
        return res
    if res_type == ResultType.dictResult:
        return res
    if res_type == ResultType.arrayResult and res:
        return np.array(res[0]), np.array(res[1])
    if res_type == ResultType.valueResult:
        return res[0], res[1]


def check_loaded_res_type(cache: dict) -> ResultType:
    res_type = list(cache.keys())[0]
    return result_dict[res_type]


def load_only_array_results() -> Tuple[np.array, np.array]:
    cache = get_cache_dict()
    res_type = check_loaded_res_type(cache)
    if res_type == ResultType.arrayResult:
        res = get_result_from_cache(cache, res_type)
        return reformat_result(res, res_type)


if __name__ == '__main__':
    myar1 = np.random.random(5)
    myar2 = np.random.random(5)
    mytuple = ("oand", 998)
    save_to_cache("check this")

    print(load_from_cache())
