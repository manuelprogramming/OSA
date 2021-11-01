import time
from dataclasses import dataclass
from typing import Any
import pandas as pd
from pathlib import Path
from os import path
from datetime import datetime

from osa import factory


@dataclass
class SaveData:
    """
    Plots the Data from the Cache perform "get_data" before executing
    """
    command: str

    def do_work(self, settings, *args) -> Any:
        arg = args[0]
        if not isinstance(arg, tuple):
            return "retrieve Data before plotting"

        file_path = self._get_saving_path(settings)
        self._save_data(file_path, args)
        return "data saved"

    @staticmethod
    def _save_data(file_path, args) -> None:
        wave_length, intensity = args[0]
        df = pd.DataFrame(data=intensity, index=wave_length)
        df.to_csv(file_path)




def initialize() -> None:
    factory.register("save_data", SaveData)


if __name__ == '__main__':
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%b-%d,-,%H;%M;%S")
    print('Current Timestamp : ', timestampStr)

    time.sleep(1)
    dateTimeObj2 = datetime.now()
    print(dateTimeObj2 < dateTimeObj)



    # for back and forth converting
    # format = "%Y-%b-%d,-,%H;%M;%S"
    # dt_utc = datetime.strptime(timestampStr, format)
    # print(dt_utc)