import pandas as pd
from tick_forex.functions import *
import numpy as np

stock = 'AKBNK'
path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\{}.pkl'.format(stock)
data = pd.read_pickle(path)

data['30Min'] = data.index.floor('30Min')
data['15Min'] = data.index.floor('15Min')
data['5Min'] = data.index.floor('5Min')
data['1Min'] = data.index.floor('1Min')
data['day'] = data.index.floor('1d')

data['minutes'] = data['1Min'] - data['day']
data['H_M'] = data['5Min'] - data['day']

H_M_count = data['minutes'].value_counts()
H_M_count.index = pd.to_datetime(H_M_count.index)
H_M_count.sort_index(inplace=True)
