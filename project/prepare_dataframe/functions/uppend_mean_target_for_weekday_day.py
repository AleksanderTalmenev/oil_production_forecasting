# coding: utf-8
from functions.code_with_mean import code_with_mean
import pandas as pd

def uppend_mean_target_for_weekday_day(df, target):
    """
    Добавляет в dataframe столбец со значениями средних target для дня недели и числа календаря.
    df - dataframe
    target - категориальный признак, по которому берутся средние
    """
    df['WEEKDAY'] = df.index.weekday
    df['DAYS'] = df.index.day
    df_buf = pd.DataFrame(index=df.index)
    df_buf['WEEKDAY_AVERAGE'] = df['WEEKDAY'].map(code_with_mean(df, 'WEEKDAY', target))
    df_buf['DAYS_AVERAGE'] = df['DAYS'].map(code_with_mean(df, 'DAYS', target))
    df.drop(['WEEKDAY', 'DAYS'], axis=1, inplace=True)
    df = pd.concat([df_buf, df], axis=1)
    return df
