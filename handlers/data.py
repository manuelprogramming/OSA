from typing import Tuple
import pandas as pd
import numpy as np


class DataReader:

    def __init__(self, file_path: str):
        self.path: str = file_path
        self.points_data: bool = self._is_points_data(file_path)
        self.df = self._create_df()

    @staticmethod
    def _is_points_data(file_path: str) -> bool:

        df = pd.read_csv(file_path, index_col=0)
        return df.index.name == "bending_radius"

    def _create_df(self):
        if self.points_data:
            return pd.read_csv(self.path, index_col=["bending_radius", "wavelength [nm]"])
        else:
            return pd.read_csv(self.path, index_col="wavelength [nm]")

    def get_valid_sets(self) -> set:
        if self.points_data:
            return set(self.df.index.get_level_values(0))
        else:
            return set(self.df.columns)

    def user_input_is_valid(self, user_input: str):
        return user_input in self.get_valid_sets()


class DataSaver(DataReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def save_data(self):
        self.df.to_csv(self.path)


class DataDeleter(DataReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def delete_data(self, user_input: str) -> bool:
        if not self.user_input_is_valid(user_input):
            return False
        if self.points_data:
            self.df.drop(user_input, inplace=True)
            self.df.to_csv(self.path)
        else:
            self.df.drop(user_input, axis=1, inplace=True)
            self.df.to_csv(self.path)
        return True


class DataGetter(DataReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def get_data(self, user_input: str) -> Tuple[np.array, np.array]:
        if not self.user_input_is_valid(user_input):
            return np.array(False), np.array(False)
        if self.points_data:
            return self.df.loc[user_input].index.to_numpy(), self.df.loc[user_input].to_numpy().flatten(GFF)
        else:
            return self.df.index.to_numpy(), self.df[user_input].to_numpy()

