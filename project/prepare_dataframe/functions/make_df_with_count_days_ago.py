# coding: utf-8
import pandas as pd

def make_df_with_count_days_ago(dataframe, count_days, target):
    """
    dataframe - DataFrame откуда будут браться данные.
    count_days - количество прошлых измерений (в прошлые дни), которые будут в таблице.
    target - название столбца, который будет использоваться для создания временного ряда.
    
    """
    list_df = []

    for well in dataframe['WELL_NAME'].unique():

        data = dataframe[dataframe['WELL_NAME'] == well]
        data.set_index('MEASURED_IN_DATE', inplace=True)

        target_series = data[target]

        df = pd.DataFrame()
        
        df['WELL_NAME'] = data['WELL_NAME'][count_days :].reset_index(drop=True)

        for i in range(count_days):
            df[f'{target}_{count_days - i}_days_ago'] = \
                target_series[i : target_series.count() - count_days + i].reset_index(drop=True)

        df.index = target_series.index[count_days :]
        df[f'TARGET_{target}'] = target_series[count_days :]
        list_df.append(df)
    df = pd.concat(list_df)
    return df
