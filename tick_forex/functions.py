import time
import pandas as pd


def read_data(stock):
    path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\{}-since-2017-10.csv'.format(stock)
    df = pd.read_csv(path, sep=',', header=0, cache_dates=True,
                     names=['date', 'contract', 'quantity', 'volume', 'price', 'side_1', 'side_2'])
    return df


def resample_data(data, timeframe):
    ohlc = data['price'].resample(rule=timeframe).ohlc()
    ohlc[['quantity', 'volume']] = data[['quantity', 'volume']].resample(rule=timeframe).sum()
    return ohlc


def tickstore(stocks):
    dfs = []
    for stock in stocks:
        df = read_data(stock=stock)
        df['symbol'] = stock
        dfs.append(df)

    main_df = pd.concat(dfs)
    main_df['date'] = pd.to_datetime(main_df['date'])
    main_df.set_index('date', inplace=True)
    main_df.index = main_df.index.tz_convert('Europe/Istanbul')
    # main_df2.set_index(pd.to_datetime(main_df2['date']),inplace=True) --> slower a bit
    return main_df


