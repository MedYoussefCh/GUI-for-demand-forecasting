#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
import numpy as np



def prediction_arima(tsA):
    if not tsA:
        print("tsA videeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        os.chdir("C:\\Users\\YOUSSEF\\Desktop\\Interface_pyqt_GOP\\data")
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
        #print("sdata.read().split('\n') = \n",sdata.read().split('\n'))
        print("done")
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
    # split into train and test sets
    size = int(len(tsA) * 0.66)
    train, test = tsA[0:size], tsA[size:len(tsA)]
    history = [x for x in train]
    predictions = list()

    LADATA = [x for x in train]
    LAPREDICTION = [x for x in train]

    # walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat);LAPREDICTION.append(yhat)
        obs = test[t];LADATA.append(test[t])
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))
    # evaluate forecasts
    rmse = sqrt(mean_squared_error(test, predictions))
    rmse=100000000000000
    print('Test RMSE: %.3f' % rmse)
    print("predit!!!!!!!! à len = ", len(predictions))
    # plot forecasts against actual outcomes
    # pyplot.plot(test)
    # pyplot.plot(predictions, color='red')
    # pyplot.show()
    return(LAPREDICTION,rmse,LADATA) #prediction et erreur quadratique

# In[ ]:



if __name__ == "__main__":
    # load dataset

    os.chdir("C:\\Users\\YOUSSEF\\Desktop\\Interface_pyqt_GOP\\data")
    try:
        sdata = open('data\\sampledata.csv')
    except:
        sdata = open('sampledata.csv')
    #print("sdata.read().split('\n') = \n",sdata.read().split('\n'))
    print("done")
    tsA = sdata.read().split('\n')
    tsA = list(map(int, tsA))
    print("-------------------------------")
    print("database.type(): ", type(tsA)) #tsA est une liste
    print("done")
    p=prediction_arima(tsA)

    print("-------------------------------")
    print("p[0]: ",type(p[0]))
    A = np.array(tsA)
    print("database in array(): ", A)
    print("done")
    print("database in array(): ", A.shape)
    print("done")
    #print("database.describe(): ", tsA.describe())
    print("done")
    #print("arima(tsA) = ", arima(tsA))



# In[ ]:




