# coding: utf-8
import scipy.stats as scs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import statsmodels.tsa.api as smt

def unyeo_johnson(y, lmbda):
    '''
    Обратная функция преобразованию yeo-johnson
    y - значение, преобразованных данных
    lmbda - параметр преобразования
    '''
    
    if lmbda != 0:
        return ((y * lmbda + 1) ** (1 / lmbda)) - 1
    else:
        return np.exp(y) - 1

def unboxcox(y, lmbda):
    '''
    Обратная функция преобразованию Бокса-Кокса
    y - значение, преобразованных данных
    lmbda - параметр преобразования
    '''
    if lmbda == 0:
        return(np.exp(y))
    else:
        return(np.exp(np.log(lmbda * y + 1) / lmbda))
   
    
    
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

def tsplot(data, lags=None, figsize=(10, 6), style='bmh'):
    '''
    Строит графики для временного ряда
    data - Series временного ряда.
    lags - задержка между двумя наблюдениями во времени.
    '''
    if not isinstance(data, pd.Series):
        data = pd.Series(data)
    with plt.style.context(style):
        fig = plt.figure(figsize=figsize)
        layout = (2, 2)
        
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        
        
        data.plot(ax=ts_ax)
        ts_ax.set_title(f'Критерий Дики-Фуллера p-value={np.round(sm.tsa.adfuller(data)[1], decimals=3)}',
                        fontsize=12)
        smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5, markersize=4)
        smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5, markersize=4)
        
        
        plt.tight_layout()


    
def tsplot_rus_labels(data, lags=None, figsize=(10, 6), style='bmh'):
    '''
    Строит графики для временного ряда
    data - Series временного ряда.
    lags - задержка между двумя наблюдениями во времени.
    '''
    plt.rcParams['font.family'] = 'Times New Roman'

    mpl.rcParams.update({'font.size': 11})
    
    
    if not isinstance(data, pd.Series):
        data = pd.Series(data)
    with plt.style.context(style):
        fig = plt.figure(figsize=figsize)
        layout = (2, 2)
        
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        
        plt.rcParams['font.size'] = 8
        data.plot(ax=ts_ax)
        ts_ax.set_title(f'Данные скважины с номером 1 \n Критерий Дики-Фуллера p-value={np.round(sm.tsa.adfuller(data)[1], decimals=3)}',
                        fontsize=12)
        ts_ax.set_ylabel('Преобразованные данные \n по дебитам нефти,  $м^3/сут$', fontsize=10)
        ts_ax.set_xlabel('Дата замера', fontsize=10)
        smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5, markersize=4, title='Автокорреляционная функция')
        smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5, markersize=4,title='Частная автокорреляционная функция')
        
        acf_ax.set_xlabel('Номер лага', fontsize=10)
        pacf_ax.set_xlabel('Номер лага', fontsize=10)
    plt.tight_layout()
        
