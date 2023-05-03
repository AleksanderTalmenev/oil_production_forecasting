# coding: utf-8
def code_with_mean(data, cat_feature, real_feature):
    """
    Создает словарь для кодирования категориального признака при помощи среднего у числового
    data - dataframe
    cat_feature - категориальный признак
    real_feature - числовой признак
    """
    return dict(data.groupby(cat_feature)[real_feature].mean())
    
