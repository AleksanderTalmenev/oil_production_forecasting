# coding: utf-8
import plotly.graph_objects as go
from plotly.offline import iplot
import pandas as pd

def graph_with_prediction(y_train, y_test, answer_model, model_name):
    '''
        y_train - столбец y, который используется для обучения модели.
        y_test - столбец y, который используется для проверки модели.
        answer_model - предсказания модели.
        model_name - Название модели.
    '''
    answer = pd.concat([y_train, answer_model])
    y = pd.concat([y_train, y_test])
    
    line_pred = go.Scatter(x=answer.index,
                           y=answer,
                           name=f'Модель - {model_name}',
                           mode='lines')
    line_y_test = go.Scatter(x=y.index,
                             y=y,
                             name='Данные с месторождения',
                             mode='lines')
    lines = [line_pred, line_y_test]
    layout = {'title': f'Сравнение: {model_name} и данные с месторождения'}
    fig = go.Figure(data=lines, layout=layout)
    iplot(fig)
