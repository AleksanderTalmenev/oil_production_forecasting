# coding: utf-8
import numpy as np 
import pandas as pd
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
