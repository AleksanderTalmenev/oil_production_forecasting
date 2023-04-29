# coding: utf-8
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

class Holt_Winters:
    """
    Модель Хольта-Винтерса с методом Брутлага для детектирования аномалий (тройное экспоненциальное сглаживание)
    
    data - исходный временной ряд
    slen - длина сезона
    alpha, beta, gamma - коэффициенты в модели Хольта-Винтерса
    n_preds - количество точек в предсказании
    scaling_factor - задает ширине доверительного интервала по Брутлагу (обычно от 2 до 3)
    
    """
    
    def __init__(self, data, slen, alpha, beta, gamma, n_preds, scaling_factor):
        
        self.data = data
        self.slen = slen
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_preds = n_preds
        self.scaling_factor = scaling_factor
    
    def initial_trend(self):
        count = 0.0
        for i in range(self.slen):
            count += float(self.data[i + self.slen] - self.data[i]) / self.slen
        return count / self.slen
    
    def initial_seasonal_components(self):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(self.data) / self.slen)
        
        for i in range(n_seasons):
            season_averages.append(
                sum(self.data[self.slen * i : self.slen * i  + self.slen]) /
                     float(self.slen)
            )
        for i in range(self.slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += self.data[self.slen * j + i] - season_averages[j]
            seasonals[i] = sum_of_vals_over_avg / n_seasons

        return seasonals
    def triple_exponential_smoothing(self):
        self.result = []
        self.Smooth = []
        self.Season = []
        self.Trend = []
        self.PredictedDeviation = []
        self.UpperBond = []
        self.LowerBond = []
        
        seasonals = self. initial_seasonal_components()
        
        for i in range(len(self.data) + self.n_preds):
            if i == 0:
                smooth = self.data[0]
                trend = self.initial_trend()
                self.result.append(self.data[0])
                self.Smooth.append(smooth)
                self.Trend.append(trend)
                self.Season.append(seasonals[i])
                
                self.PredictedDeviation.append(0)
                self.UpperBond.append(self.result[0] + 
                                      self.scaling_factor * 
                                      self.PredictedDeviation[0])
                self.LowerBond.append(self.result[0] - 
                                      self.scaling_factor * 
                                      self.PredictedDeviation[0])
                continue
            if i >= len(self.data):
                m = i - len(self.data) + 1
                self.result.append((smooth + m * trend) + seasonals[i % self.slen])
                
                self.PredictedDeviation.append(self.PredictedDeviation[-1] * 1.01)
            else:
                value = self.data[i]
                last_smooth, smooth = smooth, (self.alpha * 
                                      (value - seasonals[i % self.slen] + 
                                      (1 - self.alpha) * (smooth + trend)))
                
                trend = self.beta * (smooth - last_smooth) + (1 - self.beta) * trend
                seasonals[i % self.slen] = (self.gamma * (value - smooth) + 
                                           (1 - self.gamma) * seasonals[i % self.slen]
                                           ) 
                
                self.result.append(smooth + trend + seasonals[i % self.slen])
                
                self.PredictedDeviation.append(
                        self.gamma * np.abs(self.data[i] - self.result[i]) +
                        (1 - self.gamma) * self.PredictedDeviation[-1]
                )
            self.UpperBond.append(self.result[-1] +
                                  self.scaling_factor * 
                                  self.PredictedDeviation[-1])
            
            self.LowerBond.append(self.result[-1] - 
                                  self.scaling_factor * 
                                  self.PredictedDeviation[-1])
            
            self.Smooth.append(smooth)
            self.Trend.append(trend)
            self.Season.append(seasonals[i % self.slen])
            
def timedataCVscore(params, train_data, cv):
    '''
    Кросс-валидация для тройного экспоненциального сглаживания.
    params - параметры alpha, beta, gamma.
    train_data - столбец тренировочных данных.
    cv - количество разбиений в кросс-валидации
    
    '''
    errors = []
    
    values = train_data.values
    alpha, beta, gamma = params
    
    tscv = TimeSeriesSplit(n_splits=cv)
    
    for train, test in tscv.split(values):
        model = Holt_Winters(data=values,
                             slen=7,
                             alpha=alpha, 
                             beta=beta, 
                             gamma=gamma,
                             n_preds=len(test),
                             scaling_factor=1.96)
        model.triple_exponential_smoothing()
        
        predictions = model.result[- len(test) :]
        actual = values[test]
        error = mean_squared_error(predictions, actual)
        errors.append(error)
        
    return np.mean(np.array(errors))

def plotHot_Winters(model, data, test_size):
    '''
    График для модели тройного экспоненциального сглаживания
    model - обученная модель тройного экспоненциального сглаживания
    data - временной ряд
    test_size - размер предсказания
    '''
    Anomalies = np.array([np.nan] * len(data))
    Anomalies[data.values < model.LowerBond] = data.values[data.values < model.LowerBond]
    
    plt.figure(figsize=(10, 5))
    plt.plot(model.result, label='Тройное экспоненциальное сглаживание')
    plt.plot(model.UpperBond, 'r--', alpha=0.5, label='Верхняя/Нижняя границы уверенности')
    plt.plot(model.LowerBond, 'r--', alpha=0.5)
    plt.fill_between(x=range(0, len(data)),
                     y1=model.UpperBond,
                     y2=model.LowerBond,
                     alpha=0.5,
                     color='grey')
    plt.plot(data.values, label='Данные с месторождения', color='yellow')
    plt.plot(Anomalies, 'o', markersize=5, label='Аномалии', color='red')
    plt.axvspan(xmin=(len(data) - test_size), xmax=len(data), alpha=0.5, color='lightgrey')
    plt.grid(True)
    
    plt.axis('tight')
    plt.legend(loc='best', fontsize=8)
