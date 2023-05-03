# coding: utf-8
import pandas as pd
def train_test_wells(df, target, test_size):
    '''
        Разбивает df на тестовый и тренировочный dataframe
        
        df- dataframe
        target - признак, которыый предсказываем, например 'OIL_RATE'
        test_size - количество дней предсказания для каждой скважины, например 30.
    '''

    df_train = pd.DataFrame(columns=df.columns)
    df_test = pd.DataFrame(columns=df.columns)
    
    for well in list(df['WELL_NAME'].unique()):

        data_train_well = df[df['WELL_NAME'] == well].iloc[: - test_size, :]
        data_test_well = df[df['WELL_NAME'] == well].iloc[- test_size:, :]
        
        df_train = pd.concat([df_train, data_train_well])
        df_test = pd.concat([df_test, data_test_well])

    X_train = df_train.drop(columns=f'TARGET_{target}', axis=1)
    y_train = df_train[['WELL_NAME', f'TARGET_{target}']]

    X_test = df_test.drop(columns=f'TARGET_{target}', axis=1)
    y_test = df_test[['WELL_NAME', f'TARGET_{target}']]

    return X_train, X_test, y_train, y_test
