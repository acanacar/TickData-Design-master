# data 30 min

# data 1 min

# ---------{-5,-4,-3,-2,-1,0}--------

import pandas as pd

paths = {
    'windows': {
        '30Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data\tick\bars\time_bars_30Min_AKBNK.pkl',
        '5Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data\tick\bars\time_bars_5Min_AKBNK.pkl',
        '1Min': r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data\tick\bars\time_bars_1Min_AKBNK.pkl',
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
paths = paths['windows']
data_1Min = pd.read_pickle(paths['1Min'])

df = data_1Min.copy()

for i in [10, 15, 20, 25, 30]:
    df['twap_{}_open'.format(i)] = df.open.shift(i - 1)
    df['twap_{}_high'.format(i)] = df.high.rolling(min_periods=i, window=i).max()
    df['twap_{}_low'.format(i)] = df.low.rolling(min_periods=i, window=i).min()
    df['twap_{}_close'.format(i)] = df.close.shift(i - 1)
for i in [10, 15, 20, 25, 30]:
    df['twap_{}'.format(i)] = df.loc[:, "twap_{}_open".format(i):"twap_{}_close".format(i)].mean(axis=1)

# ilk openi shift ettir
d = {10: 1, 15: 2, 20: 2, 25: 3, 30: 10}
for i in [10, 15, 20, 25, 30]:
    df['future_twap_{}_open'.format(i)] = df['twap_{}_open'.format(i)].shift(-d[i])
    df['future_twap_{}_current_high'.format(i)] = df.high.rolling(min_periods=i - d[i], window=i - d[i]).max()
    df['future_twap_{}_current_low'.format(i)] = df.low.rolling(min_periods=i - d[i], window=i - d[i]).min()
    df['future_twap_{}_current_volume'.format(i)] = df.low.rolling(min_periods=i - d[i],
                                                                   window=i - d[i]).sum()
    df['future_twap_{}'.format(i)] = df['twap_{}'.format(i)].shift(-d[i])

df = df.dropna(how='any', axis=0)

from sklearn.linear_model import LinearRegression
import numpy as np

train_size = .4
split_point = int(len(df) * train_size)

res = {}
for i in [10, 15, 20, 25, 30]:
    independent_cols = ['future_twap_{}_open'.format(i),
                        'future_twap_{}_current_high'.format(i),
                        'future_twap_{}_current_low'.format(i),
                        'close'.format(i),
                        'future_twap_{}_current_volume'.format(i)]
    X = df[independent_cols].values[:split_point]
    y = df['future_twap_{}'.format(i)].values[:split_point]
    print(X.shape, y.shape)
    reg = LinearRegression().fit(X, y)

    X_test = df[independent_cols].values[split_point:]
    y_test = df['future_twap_{}'.format(i)].values[split_point:]
    y_predictions = reg.predict(X_test)
    d = {i: {'score': reg.score(X_test, y_test), 'coef': reg.coef_, 'intercept': reg.intercept_}}
    res.update(d)

    df['prediction_future_twap_{}'.format(i)] = np.concatenate((y, y_predictions), axis=0)

df = df.iloc[split_point:]

cols = []
for i in [10, 15, 20, 25, 30]:
    cols.append('prediction_future_twap_{}'.format(i))
    cols.append('future_twap_{}'.format(i))
df2 = df[cols]
for i in [10, 15, 20, 25, 30]:
    df2['error_twap_{}'.format(i)] = \
        df2['prediction_future_twap_{}'.format(i)] - df2['future_twap_{}'.format(i)]

df.to_pickle(r'C:\Users\a.acar\PycharmProjects\ITCH\twap_regression.pkl')
df2.to_pickle(r'C:\Users\a.acar\PycharmProjects\ITCH\twap_regression_with_error.pkl')
