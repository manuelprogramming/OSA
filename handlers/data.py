import pandas as pd


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


class DataSaver(DataReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def save_data(self):
        self.df.to_csv(self.path)


class DataDeleter(DataReader):

    def __init__(self, file_path):
        super().__init__(file_path)

    def get_valid_deletion_set(self) -> set:
        if self.points_data:
            return set(self.df.index.get_level_values(0))
        else:
            return set(self.df.columns)

    def delete_data(self, to_delete: str) -> bool:
        if to_delete not in self.get_valid_deletion_set():
            return False
        if self.points_data:
            self.df.drop(to_delete, inplace=True)
            self.df.to_csv(self.path)
        else:
            self.df.drop(to_delete, axis=1, inplace=True)
            self.df.to_csv(self.path)
        return True
