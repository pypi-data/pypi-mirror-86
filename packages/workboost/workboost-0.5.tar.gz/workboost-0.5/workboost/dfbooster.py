import numpy as np
import pandas as pd
from typing import Any


class Boost_df(object):
    def __init__(self, *args, **kwargs):
        pass

    def merge_df(self, origin_df: pd.DataFrame, df_list: list):
        df_ = pd.DataFrame()
        for df in df_list:
            df_ = pd.merge(origin_df, df, on=['code', 'date'], how='left')
        return df_


