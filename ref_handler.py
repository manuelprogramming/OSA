import json
from typing import Dict, List


def save_as_ref_data(ref_dict: Dict[str, List[float]]):
    with open("bin/ref.json", "w") as f:
        json.dump(ref_dict, f, indent=4)


def load_ref_data() -> dict:
    with open("bin/ref.json", "r") as f:
        ref_dict = json.load(f)
    return ref_dict

def load_only_max_ref() -> dict:
    ref_dict = load_ref_data()
    if "wavelength_max" and "trace_max" in ref_dict.keys():
        return ref_dict


if __name__ == '__main__':
    ref_dict = load_ref_data()
    print([value for value in ref_dict.values()])

    # wavelength_max_ref = np.array(ref_dict["wavelength_max"])
    # trace_max_ref = np.array(ref_dict["trace_max"])