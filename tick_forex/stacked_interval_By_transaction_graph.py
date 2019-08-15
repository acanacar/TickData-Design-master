from tick_forex.functions import *
import numpy as np

stock = 'AKBNK'
path = r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\data_tick\{}.pkl'.format(stock)
data = pd.read_pickle(path)

"""
frequencylerde islem gerceklesmis aralik sayisini ve toplam aralik sayisini oranlayip grafigini ciziyoruz.
"""
dfs = []
timeframes = ['30S', '1Min', '5Min', '15Min', '30Min', '1H', '4H', '1d']
for timeframe in timeframes:
    df = resample_data(data=data, timeframe=timeframe)
    df = df.replace(np.float64(0), np.nan)
    df = df[df.index.dayofweek < 5]
    df_ = df.dropna(how='all')
    dfs.append((timeframe, df, df_))

    print('{} resampling is finished'.format(timeframe))

'''
[(i[0],len(i[1]),len(i[2])) for i in dfs]
[('30S', 1389150, 352105),
 ('1Min', 694575, 191417),
 ('5Min', 138915, 40375),
 ('30Min', 23154, 7897),
 ('1H', 11578, 4639),
 ('4H', 2895, 1395),
 ('1d', 483, 466)]
 '''
##  GRAPH

from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure

output_file("stacked_IntervalByTransactions.html")

groups = ['percentage of interval w/o transaction', 'percentage of interval w/ transaction']
colors = ["#36802d", "#e84d60"]

data = {'timeframes': [i[0] for i in dfs],
        'percentage of interval w/o transaction': [1 - (len(i[2]) / len(i[1])) for i in dfs],
        'percentage of interval w/ transaction': [len(i[2]) / len(i[1]) for i in dfs],
        }

p = figure(x_range=timeframes, plot_height=500, title="percentage of interval counts by w/ or w/o transaction",
           toolbar_location=None, tools="")

p.vbar_stack(groups, x='timeframes', width=0.9, color=colors, source=data,
             legend=[value(x) for x in groups])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "vertical"

show(p)

