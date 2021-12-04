import json
from typing import Any
import numpy as np
from typing import Tuple, Dict
from handlers.result import get_result_types_dict, ResultType, BaseResult
from handlers.file import get_cache_path


def save_to_cache(res: BaseResult) -> None:
    res_type = res.result_type
    cache_dict = {str(res_type): format_result(res, res_type)}
    with open(get_cache_path(), "w") as f:
        json.dump(cache_dict, f, indent=4)


def format_result(res: Any, res_type: ResultType) -> Any:
    if res_type == ResultType.noneResult:
        return res.msg
    if res_type == ResultType.valueResult:
        return res.value
    if res_type == ResultType.arrayResult and res.value:
        return list(res.value[0]), list(res.value[1])


def load_from_cache() -> Any:
    cache = get_cache_dict()
    res_type = check_loaded_res_type(cache)
    res = get_result_from_cache(cache, res_type)
    return reformat_result(res, res_type)


def get_cache_dict() -> Dict[str, Any]:
    with open(get_cache_path(), "r") as f:
        return json.load(f)


def check_loaded_res_type(cache: dict) -> ResultType:
    res_type = list(cache.keys())[0]
    return get_result_types_dict()[res_type]


def get_result_from_cache(cache: dict, res_type: ResultType) -> Any:
    return cache[str(res_type)]


def reformat_result(res: Any, res_type: ResultType) -> Tuple[np.array, np.array]:
    if res_type == ResultType.arrayResult and res:
        return np.array(res[0]), np.array(res[1])
    else:
        return res


def load_only_array_results() -> Tuple[np.array, np.array]:
    cache = get_cache_dict()
    res_type = check_loaded_res_type(cache)
    if res_type == ResultType.arrayResult:
        res = get_result_from_cache(cache, res_type)
        return reformat_result(res, res_type)


if __name__ == '__main__':
    print(load_from_cache())
