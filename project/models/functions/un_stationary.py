# coding: utf-8
from functions.unyeo_johnson import unyeo_johnson
def un_stationary(series, lmbda, n_season_elem, n_season_elements):
    '''
    Возвращате временной ряд в первоначальный вид
    series - стационарный ряд
    lmbda - параметр в преобразовании yeo-johnson
    n_season_elem - элемент с индексом n_season
    n_season_elements - элементы до n_season
    '''
    
    n_season = len(n_season_elements)

    series[n_season] = n_season_elem
    series = series.cumsum()

    series[: n_season] = n_season_elements

    for i in range(n_season):
        series[range(i, len(series), n_season)] = series[range(i, len(series), n_season)].cumsum()

    series = unyeo_johnson(series, lmbda=lmbda) 
    
    return series
