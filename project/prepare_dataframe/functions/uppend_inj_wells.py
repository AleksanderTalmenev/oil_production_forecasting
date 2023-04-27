# coding: utf-8
import pandas as pd

def uppend_inj_wells(preproc_df, train_df, distance=False, graph_wells=None):
    '''
    Добавляет закачку нагнетательных скважин, деленную на расстояние до скважины.
    preproc_df - dataframe куда добавляются данные о нагнетательных скважинах
    train_df - dataframe откуда берутся данные о нагнетательных скважинах.
    distance - нужно ли учитывать расстояние до нагнетательных скважин.
    graph_wells - dataframe откуда берутся расстояния между скважинами.
    '''
    if 'MEASURED_IN_DATE' not in preproc_df.columns:
        preproc_df.reset_index(inplace=True)

    train_inj = train_df[train_df['CHARWORK'] == 'НАГ']
    inj_wells = pd.Series(train_inj['WELL_NAME'].unique(), name='WELL_NAME')
    oil_wells = preproc_df['WELL_NAME'].unique()


    first_date = preproc_df['MEASURED_IN_DATE'].min()
    last_date = preproc_df['MEASURED_IN_DATE'].max()

    date_range = pd.Series(pd.date_range(start=first_date, end=last_date, freq='D'), name='MEASURED_IN_DATE')
    cross_date_inj_well = pd.merge(date_range, inj_wells, how='cross')
    cross_date_inj_well.sort_values(by=['WELL_NAME', 'MEASURED_IN_DATE'], inplace=True)


    train_inj_all_date = cross_date_inj_well.merge(train_inj[['MEASURED_IN_DATE', 'WELL_NAME', 'INTAKE']], 
                                                   on=['MEASURED_IN_DATE', 'WELL_NAME'], 
                                                   how='left')
    train_inj_all_date.fillna(value=0, inplace=True)

    

    intake_in_date = pd.pivot_table(data=train_inj_all_date, values='INTAKE', index='MEASURED_IN_DATE', columns='WELL_NAME')
    intake_in_date.reset_index(inplace=True)
    intake_in_date.rename_axis(columns=None, inplace=True)


    data_with_inj_wells = preproc_df.merge(intake_in_date, on='MEASURED_IN_DATE', how='left')

    data_with_inj_wells.set_index('MEASURED_IN_DATE', inplace=True)
    data_with_inj_wells = pd.concat([data_with_inj_wells.iloc[:, - inj_wells.shape[0] :], 
                                    data_with_inj_wells.iloc[:, : - inj_wells.shape[0]]], axis=1)
    
    if not distance:
        return data_with_inj_wells
    
    df_inj_well_with_gaps = pd.DataFrame()

    for well_oil in oil_wells:
        data_well_oil = data_with_inj_wells[data_with_inj_wells['WELL_NAME'] == well_oil]
        data_well_oil.iloc[:, : inj_wells.shape[0]] = (data_well_oil.iloc[:, : inj_wells.shape[0]]  / 
                                                       graph_wells[inj_wells].iloc[well_oil, :])
        
        
        df_inj_well_with_gaps = pd.concat([df_inj_well_with_gaps, data_well_oil])
    df_inj_well_with_gaps.fillna(value=0, inplace=True) 

    return df_inj_well_with_gaps
