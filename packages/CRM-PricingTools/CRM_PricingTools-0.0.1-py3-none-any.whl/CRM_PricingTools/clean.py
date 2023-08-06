
import pandas as pd
from sklearn import preprocessing


class CleanData():
    
    def __init__(self, df) -> None:
        """Contructor

        Args:
            df (DataFrame): Pandas Dataframe
        """

        self.dataframe = df.copy()



    @property
    def shape(self):
        return self.dataframe.shape

    def head(self, n=5):
        return self.dataframe.head(n)

    def get_null_columns(self):
        return self.dataframe.columns[self.dataframe.shape[0] - self.dataframe.count() > 0].tolist()

    def remove_null_columns_threshold(self, threshold=1):
        df_nulls = self.dataframe.loc[:, self.dataframe.isnull().sum() < (
            threshold * self.dataframe.shape[0])]
        col_nulls_remove = list(
            set(self.dataframe.columns.tolist()) - set(df_nulls.columns.tolist()))

        print(f"Removed null columns: {col_nulls_remove}")
        self.dataframe.drop(col_nulls_remove, axis=1, inplace=True)

    def remove_unique_columns(self):
        uniform_columns = []

        for columns in self.dataframe.columns:
            if len(self.dataframe[columns].unique()) == 1:
                uniform_columns.append(columns)

        print(f"Removed uniform columns: {uniform_columns}")
        self.dataframe = self.dataframe[(
            [column for column in self.dataframe.columns if column not in uniform_columns])]
