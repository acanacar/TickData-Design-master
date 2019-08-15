from bars_labels_diff.bars import *
import os

bar_frequencies = [('tick_bars', TickBarSeries, [50, 200, 500, 1000]),
                   ('time_bars', BarSeries, ['1Min', '5Min', '15Min', '1H', '4H', '1d']),
                   ('volume_bars', VolumeBarSeries, [200000, 100000, 5000000, 10000000]),
                   # ('dollar_bars', DollarBarSeries, [100000, 5000000, 10000000])
                   ]

data_tick_store_path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick'
