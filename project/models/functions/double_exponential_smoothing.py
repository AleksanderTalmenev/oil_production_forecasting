# coding: utf-8
import pandas as pd
def double_exponential_smoothing(data, alpha, beta):
    '''
    Применяет к столбцу двойное экспоненциальное сглаживание с параметром alpha и beta.
    l_t = alpha * y_t + (1 - alpha) (l_t-1 + b_t-1)
    b_t = beta * (l_t - l_t-1) + (1 - beta) * b_t-1
    y^_t = l_t + b_t
    data - Series данных
    alpha - сглаживающий фактор, отвечающий за уровень
    beta - сглаживающий фактор, отвечающий за тренд
    '''
    result = [data[0]]
    for t in range(1, len(data)):
        if t == 1:
            level, trend = data[0], data[1] - data[0]
            result.append(data[1])
        else:
            last_level, level = level, alpha * data[t] + (1 - alpha) * (level + trend)
            trend = beta * (last_level - level) + (1 - beta) * trend
            result.append(level + trend)
    return pd.Series(result, index=data.index)
