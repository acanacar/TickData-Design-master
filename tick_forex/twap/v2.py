# data 30 min

# data 1 min

# ---------{-5,-4,-3,-2,-1,0}--------

import pandas as pd

paths = {
    'windows': {
        '30Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_30Min_AKBNK.pkl',
        '5Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_5Min_AKBNK.pkl',
        '1Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\bars\time_bars_1Min_AKBNK.pkl',
    },
    'ubuntu':
        {
            '30Min': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/time_bars_30Min_AKBNK.pkl',
            '5Min': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/time_bars_5Min_AKBNK.pkl',
            '1Min': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/time_bars_1Min_AKBNK.pkl',
            '1000Tick': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/tick_bars_1000_AKBNK.pkl',
            '250Tick': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/tick_bars_250_AKBNK.pkl',
            '200Tick': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/tick_bars_200_AKBNK.pkl',
            '100Tick': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/tick_bars_100_AKBNK.pkl',
            '150Tick': '/home/acanacar/Desktop/projects/pycharm/TickData-Design-master-master/data/bars/tick_bars_150_AKBNK.pkl',
        }
}
paths = paths['ubuntu']
data_30Min = pd.read_pickle(paths['30Min'])
data_5Min = pd.read_pickle(paths['5Min'])
data_1Min = pd.read_pickle(paths['1Min'])
data_1000Tick = pd.read_pickle(paths['1000Tick'])
data_250Tick = pd.read_pickle(paths['250Tick'])
data_150Tick = pd.read_pickle(paths['150Tick'])

df = data_1Min.copy()

for i in [10, 15, 20, 25, 30]:
    df['twap_{}_open'.format(i)] = df.open.shift(i - 1)
    df['twap_{}_high'.format(i)] = df.high.rolling(min_periods=i, window=i).max()
    df['twap_{}_low'.format(i)] = df.low.rolling(min_periods=i, window=i).min()
    df['twap_{}_close'.format(i)] = df.close.shift(i - 1)
for i in [10, 15, 20, 25, 30]:
    df['twap_{}'.format(i)] = df.loc[:, "twap_{}_open".format(i):"twap_{}_close".format(i)].mean(axis=1)

