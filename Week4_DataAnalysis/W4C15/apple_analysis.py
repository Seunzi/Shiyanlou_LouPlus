# -*- coding:utf-8 -*-

import pandas as pd

def quarter_volume():
    data = pd.read_csv('./apple.csv',header=0)
    ndata = data['Volume']
    ndata.index = pd.to_datetime(data['Date'])
    nndata = ndata.resample('3MS').sum()
    second_volume = nndata.nlargest(2)[1]
    return second_volume
