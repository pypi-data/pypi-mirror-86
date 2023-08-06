import pandas as pd


class Boost_df(object):
    def __init__(self, *args, **kwargs):
        pass

    def merge_df(self, origin_df: pd.DataFrame, df_list: list):
        for df in df_list:
            origin_df = pd.merge(origin_df, df, on=['code', 'date'], how='left')
        return origin_df


