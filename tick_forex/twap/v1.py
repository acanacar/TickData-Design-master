# data 30 min

# data 1 min

# ---------{-5,-4,-3,-2,-1,0}--------

import numpy as np
import pandas as pd
import time

from tick_forex.twap.findingDist import *
import scipy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import scipy.stats
import matplotlib.pyplot as plt

paths = {
    '30Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_30Min_AKBNK.pkl',
    '5Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_5Min_AKBNK.pkl',
    '1Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_1Min_AKBNK.pkl',
}
data_30Min = pd.read_pickle(paths['30Min'])
data_5Min = pd.read_pickle(paths['5Min'])
data_1Min = pd.read_pickle(paths['1Min'])

twap = data_30Min.loc[:, 'open':'close'].mean(axis=1)
twap = twap.rename('twap')
_ = pd.Series(list(range(len(twap))), index=twap.index, name='twap30_id')
twap = pd.concat([twap, _], axis=1)

data_1Min['30MinCeil'] = data_1Min.index.ceil('30Min')
data_1Min = data_1Min.merge(twap, how='left', left_on='30MinCeil', right_index=True)

data_1Min['twap30_group_indice'] = data_1Min.groupby('30MinCeil').cumcount()
gb_twap30id = data_1Min.groupby('twap30_id', as_index=False)
data_1Min.loc[gb_twap30id.nth(-5).index, 'twap30_estimate_point'] = 1
"""
def kontrol(first_df, sec_df, sec_df_column_to_lookup, column_to_check, checks: list):
    '''
    first_df arg must be dataframe consist of only one column and index
    :param first_df: yollanan dataframe 1
    :param sec_df: yollanan dataframe 2
    :param sec_df_column_to_lookup: lookup column name in second dataframe
    :param column_to_check: value column name in second dataframe
    :param checks: check edilecek value larin indexleri
    :return: True means no problem ,False means that 2 dataframe not merged properly,some values for same column value are different for dataframes
    '''
    for i in checks:
        if first_df[i] == sec_df.loc[sec_df[sec_df_column_to_lookup] == first_df.index[i], column_to_check].values[0]:
            continue
        else:
            return False
    return True


checks = list(np.random.randint(0, len(twap), size=10))
xx = data_1Min.drop_duplicates(subset=['30MinRound', 'twap']).reset_index()[['30MinRound', 'twap']]
res = kontrol(first_df=twap, sec_df=xx, sec_df_column_to_lookup='30MinRound', column_to_check='twap', checks=checks)
"""


def get_sample(data, date):
    high_es = data.loc[data.index <= date, ['H-O']].sample().values[0]
    low_es = data.loc[data.index <= date, ['L-O']].sample().values[0]
    close_es = data.loc[data.index <= date, ['C-O']].sample().values[0]
    return high_es[0], low_es[0], close_es[0]


data_5Min['H-O'] = (data_5Min['high'] - data_5Min['open']) / data_5Min['open']
data_5Min['L-O'] = (data_5Min['low'] - data_5Min['open']) / data_5Min['open']
data_5Min['C-O'] = (data_5Min['close'] - data_5Min['open']) / data_5Min['open']

for indice, r in data_1Min.iterrows():
    if r['twap30_estimate_point'] == 1:
        twap_group_indice = r['twap30_group_indice']
        twap_id = r['twap30_id']

        mask1 = data_1Min['twap30_group_indice'] < twap_group_indice
        mask2 = data_1Min['twap30_id'] == twap_id
        dd = data_1Min.loc[mask1 & mask2, :]

        data_1Min.loc[indice, 'twap_open'] = dd['open'].values[0]
        data_1Min.loc[indice, 'twap_current_high'] = dd['high'].max()
        data_1Min.loc[indice, 'twap_current_low'] = dd['low'].min()

        high_es, low_es, close_es = get_sample(data=data_5Min, date=indice)
        data_1Min.loc[indice, 'high_es'] = r['open'] * (1 + high_es)
        data_1Min.loc[indice, 'low_es'] = r['open'] * (1 + low_es)
        print(twap_id)

df = data_1Min.copy()
df2 = df[df['twap30_estimate_point'] == 1]
for i, r in df2.iterrows():
    _, _, close_es = get_sample(data_5Min, date=i)
    df2.loc[i, 'close_es'] = r['open'] * +(1 + close_es)

df2['twap_es'] = df2.loc[:, ['twap_open', 'close_es', 'high_es', 'low_es']].mean(axis=1)
df2['percent_twap'] = df2['twap_es'] / df2['twap']
df3 = df2.merge(data_30Min.loc[:, 'open':'close'], suffixes=('', '_twap'), left_on='30MinCeil', right_index=True)
for i in ['high', 'twap', 'close', 'low']:
    df3['percent_{}'.format(i)] = df3['{}_es'.format(i)] / df3['{}'.format(i)]

df3.iloc[:, -4:].describe()

'''
       percent_high  percent_twap  percent_close  percent_low
count   6492.000000   6492.000000    6492.000000  6492.000000
mean       1.000591      0.999993       1.000009     0.999344
std        0.001668      0.001674       0.002368     0.001893
min        0.986577      0.979580       0.983926     0.981022
25%        0.999876      0.999026       0.998712     0.998611
50%        1.000072      0.999997       1.000000     0.999815
75%        1.001366      1.000918       1.001311     1.000247
max        1.015957      1.010620       1.017186     1.007143
'''
