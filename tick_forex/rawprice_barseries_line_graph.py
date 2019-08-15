import matplotlib.pyplot as plt
from tick_forex import constants
import pandas as pd


def get_between_dates(data, sd, ed):
    mask = (data.index >= sd) & (data.index <= ed)
    return data.loc[mask]


data_tick_store_path = constants.data_tick_store_path
stock = 'AKBNK'

tick_data = pd.read_pickle(data_tick_store_path + r"\{}.pkl".format(stock))

time_bars_freq = '1Min'
time_bars_1min = pd.read_pickle(data_tick_store_path + r"\bars\time_bars_{}_{}.pkl".format(time_bars_freq, stock))

time_bars_freq = '15Min'
time_bars_15min = pd.read_pickle(data_tick_store_path + r"\bars\time_bars_{}_{}.pkl".format(time_bars_freq, stock))

tick_data2 = get_between_dates(data=tick_data, sd='2018-01-15', ed='2018-01-20')
time_bars_1min_2 = get_between_dates(data=time_bars_1min, sd='2018-01-15', ed='2018-01-17')
time_bars_15min_2 = get_between_dates(data=time_bars_15min, sd='2018-01-15', ed='2018-01-17')
time_bars_1min_2['dates'] = time_bars_1min_2.index

"""
plt.figure(figsize=(30, 20))
plt.title('Bars over the prices')
plt.plot(time_bars_1min_2.date.values[:], time_bars_1min_2.close.values[:], label='Raw prices', ls='--', color='black')
plt.plot(time_bars_15min_2.index.values[:], time_bars_15min_2.close.values[:], ls='', markersize=4, marker='.',color='red')

# plt.plot(tick_bars.index.values[:11], tick_bars.close.values[:11], ls='', markersize=10, marker='o', label='100 ticks bars')
# plt.plot(volume_bars.index.values[:30], volume_bars.close.values[:30], ls='', markersize=10, marker='*', label='10K volume bars')
# plt.plot(dollar_bars.index.values[:16], dollar_bars.close.values[:16], ls='', markersize=10, marker='*', label='1M dollar bars ')

for e, t in enumerate(time_bars_15min_2.index.values[:]):
    if e == 0:
        plt.axvline(t, ls='--', label='{} time bars'.format(time_bars_freq))
    else:
        plt.axvline(t, ls='-')

plt.legend()
plt.show()
"""

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from math import pi
from bokeh.models import DatetimeTickFormatter,FixedTicker

output_file("vline_stack.html")

source = ColumnDataSource(time_bars_1min_2)
p = figure(plot_width=2400,
           plot_height=600,
           x_axis_type='datetime',
           x_range=(time_bars_1min_2.dates.min(),time_bars_1min_2.dates.max()))
p.line(x='date', y='close', source=source, legend='1Min Prices')

# p.xaxis.ticker = FixedTicker(ticks=list(time_bars_1min_2.index.values))
# p.xaxis.major_label_orientation = pi / 4
p.xaxis.formatter = DatetimeTickFormatter(
    days=["%m/%d"],
    months=["%m/%d"],
    hours=["%H:%M"],
    minutes=["%H:%M"]
)
p.xaxis.major_label_overrides = {
    i: date.strftime('%H-%M') for i, date in enumerate(time_bars_1min_2["dates"])
}
p.xgrid.minor_grid_line_color = 'navy'
p.xgrid.minor_grid_line_alpha = 0.1
show(p)
