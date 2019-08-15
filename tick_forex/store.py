from tick_forex.functions import *
from tick_forex import constants

bar_frequencies = constants.bar_frequencies
data_tick_store_path = constants.data_tick_store_path

# Stocklarin ayri ayri ve main_df olarak pickle formatinda store edilmesi
stocks = ['AKBNK', 'GARAN', 'SAHOL', 'THYAO', 'TUPRS']

tickstore = tickstore(stocks=stocks)
tickstore.to_pickle(r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\tickAll.pkl')

tickstore = pd.read_pickle(r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\tickAll.pkl')
for stock in stocks:
    contract = '{}.E.BIST'.format(stock)
    df = tickstore.loc[tickstore.contract == contract, :]
    path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\{}.pkl'.format(stock)
    df.to_pickle(path)
    print(stock, ' pickle olarak store edildi')

# Akbank bar series lerinin farkli frekanslarda pickle formatinda store edilmesi
import os

stock = 'AKBNK'
path = os.path.join(data_tick_store_path + r"\{}.pkl".format(stock))
data = pd.read_pickle(path)
data['DateTime'] = data.index
data.rename(columns={'quantity': 'Size', 'price': 'Price'}, inplace=True)

for name, c, frequencies in bar_frequencies:
    print(name, ' is started')
    for freq in frequencies:
        path_for_pickle = os.path.join(data_tick_store_path + r"\bars\{}_{}_{}.pkl".format(name, str(freq), stock))
        if os.path.exists(path_for_pickle):
            print('{} is already exist'.format(path_for_pickle))
            continue
        bars = c(data)
        df = bars.process_ticks(frequency=freq)
        if name == 'time_bars':
            df = df.dropna(subset=['close'])
        df.to_pickle(path_for_pickle)
        print('{}_{}_{} is finished'.format(stock, name, str(freq)))
