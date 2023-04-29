# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import statsmodels.tsa.api as smt

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
        ts_ax.set_title(f'Критерий Дики-Фуллера p-value={np.round(sm.tsa.adfuller(data)[1], decimals=2)}',
                        fontsize=12)
        smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5, markersize=4)
        smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5, markersize=4)
        
        
        plt.tight_layout()
