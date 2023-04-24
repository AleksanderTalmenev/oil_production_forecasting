# coding: utf-8
import pandas as pd

def uppend_p_zab(preproc_df, train_df):
    '''
    Добавляет в preproc_df забойое давление P_ZAB
    preproc_df - dataframe, в который нужно добавить данные о давлении.
    train_df - dataframe откуда мы берем данные по давлению.
    
    '''
    if 'P_ZAB' in preproc_df.columns:
        return preproc_df
    
    data = preproc_df.reset_index()
    train_pressure = train_df[['MEASURED_IN_DATE', 'WELL_NAME', 'P_ZAB']]


    data_pressure = pd.merge(data, train_pressure, on=['MEASURED_IN_DATE', 'WELL_NAME'])
    cols = list(data_pressure.columns)
    cols.insert(1, cols.pop(cols.index('P_ZAB')))
    data_pressure = data_pressure.loc[:, cols]
    return data_pressure 
