# coding: utf-8
import numpy as np
def unboxcox(y, lmbda):
    '''
    Обратная функция преобразованию Бокса-Кокса
    y - значение, преобразованных данных
    lmbda - параметр преобразования
    '''
    if lmbda == 0:
        return np.exp(y)
    else:
        return np.exp(np.log(lmbda * y + 1) / lmbda)
    
