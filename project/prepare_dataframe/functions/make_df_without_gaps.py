# coding: utf-8
import pandas as pd 

def make_df_without_gaps(dataframe, date_column, group_params):
    """
    Возвращает dataframe с максимальными интервалами данных без пропусков.
    train_df - исходный dataframe.
    date_column - название столбца с датами. Например MEASURED_IN_DATE.
    group_params - название столбца, по которому происходит группировка данных, для нахождения интервала.Например WELL_NAME.
    """
    dataframe_without_gaps = pd.DataFrame()
    count_rows = 0
    dataframe[date_column] = pd.to_datetime(dataframe[date_column])

    for well in dataframe[group_params].unique():

        data = dataframe[dataframe[group_params] == well]
        data = data.sort_values(by=date_column)

        df_dates = pd.DataFrame()
        df_dates[date_column] = data[date_column]

        df_dates['NUMBER'] = list(range(count_rows, df_dates.shape[0]  + count_rows))
        count_rows += df_dates.shape[0]

        df_dates['DIFF_DATE'] = data[date_column].diff()
        df_dates = df_dates[['NUMBER', date_column, 'DIFF_DATE']]

        intervals = pd.DataFrame()
        intervals['DIFF_COUNT'] = df_dates[df_dates['DIFF_DATE'] != '1 days']['NUMBER'].diff()
        intervals['INDEX_DATE'] = intervals.index
        intervals.reset_index(drop=True, inplace=True)
        intervals = intervals[['INDEX_DATE', 'DIFF_COUNT']]

        max_diff = intervals['DIFF_COUNT'].max()    
    
        end_max_interval = int(intervals[intervals['DIFF_COUNT'] == max_diff]['INDEX_DATE'])
        start_max_interval = int(intervals.iloc[intervals[intervals['DIFF_COUNT'] == max_diff].index - 1]['INDEX_DATE'])

        dataframe_without_gaps = pd.concat([dataframe_without_gaps, 
                                                      dataframe.iloc[start_max_interval : end_max_interval]]) 
    dataframe_without_gaps.reset_index(drop=True, inplace=True)
    return dataframe_without_gaps
