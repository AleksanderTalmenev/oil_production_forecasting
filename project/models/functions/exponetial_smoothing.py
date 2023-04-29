# coding: utf-8
import pandas as pd
def exponetial_smoothing(data, alpha):
    """
    Применяет к столбцу экспоненциальное сглаживание с параметром alpha.
    y^_t = alpha * y_t + (1 + alpha) * y^_t-1
    data - Series данных
    alpha - сглаживающий фактор
    """
    result = [data[0]]
    for t in range(1, len(data)):
        result.append(alpha * data[t] + (1 - alpha) * data[t - 1])
    return pd.Series(result, index=data.index)
