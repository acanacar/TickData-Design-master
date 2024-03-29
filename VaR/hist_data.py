import yfinance as yf

from analysistemporary.VaR.constants import *

# from temporary_analysis.Value_at_Risk.constants import *

tickers = Tickers()

import datetime

today = datetime.date.today() - datetime.timedelta(days=1)
ScenariosNo = 500  # Define the number of scenarios you want to run


def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))


def dateforNoOfScenarios(date):
    i = 0
    w = 0
    while i < ScenariosNo:
        if (is_business_day(today - datetime.timedelta(days=w)) == True):
            i = i + 1
            w = w + 1
        else:
            w = w + 1
            continue
    return (today - datetime.timedelta(
        days=w * 1.04 + 1))  # 4% is an arbitary number i've calculated the holidays to be in 500days.


startDate = dateforNoOfScenarios(today)
endDate = today

df = yf.download(' '.join(tickers), '2014-01-01', '2018-01-31', group_by='ticker')

tahvils = ['tahvil2y', 'tahvil5y', 'tahvil10y', 'bist30']
for tahvil in tahvils:
    path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\analysistemporary\VaR\{}.csv'.format(
        tahvil)
    dframe = pd.read_csv(path, sep=';', decimal=',')
    dframe['Date'] = pd.to_datetime(dframe['Date'])
    dframe.set_index('Date', inplace=True)
    df[tahvil] = dframe

with pd.HDFStore(hist_store) as store:
    store.put('all', df)
