# coding: utf-8
import scipy.stats as scs
import pandas as pd

def make_stationary(series, n_season):
    """
    Делает стационарным временной ряд
    series - временной ряд
    n_season - параметр сезонных разностей
    
    Возвращает: 
    series_stationary - стационарный ряд,
    lmbda_yj - параметр в преобразовании yeo-johnson
    n_season_value, n_season_values - значения для обратного преобразования в исходный ряд
    """
    series_yj, lmbda_yj = scs.yeojohnson(series)
    series_yj = pd.Series(series_yj, index=series.index)
    series_yj_n_seasons = series_yj - series_yj.shift(n_season)
    series_stationary = series_yj_n_seasons - series_yj_n_seasons.shift(1)
    n_season_value = series_yj_n_seasons[n_season] 
    n_season_values = series_yj[: n_season]
    
    return series_stationary, lmbda_yj, n_season_value, n_season_values 
