from tick_forex.pr.functions import *
from tick_forex import constants
import pandas as pd
import matplotlib.pyplot as plt


def graphandsave(pattern_parameters, arr2):
    xrange = list(range(pattern_parameters['patternlength']))

    for plot_arr in arr2:
        plt.figure(figsize=(10, 6))
        for past_pattern in plot_arr[2]:
            plt.plot(xrange, past_pattern['pattern'][:-1], marker='', color='grey', linewidth=1, alpha=0.4)
            plt.scatter(35, past_pattern['pattern'][-1], c='black', alpha=.4)
        plt.plot(xrange, plot_arr[1][:-1], marker='', color='orange', linewidth=3, alpha=0.6)
        plt.scatter(40, plot_arr[1][-1], c='red', alpha=.4)
        plt.savefig(r'C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\tick_forex\pr\{}-{}-{}.png'.format(
            pattern_parameters['patternlength'],
            pattern_parameters['similarity'],
            plot_arr[1].index[-1]. \
                strftime("%m%d%Y-%H%M")))
        # plt.show()
        plt.close()


data_tick_store_path = constants.data_tick_store_path

pattern_parameters = {
    'stock': 'AKBNK',
    'patternlength': 24,
    'similarity': 70,
    'timeframe': 'D'
}

time_bars_freq = '1H'
pattern_data = pd.read_pickle(data_tick_store_path + r"\bars\time_bars_{}_{}.pkl".format(time_bars_freq, pattern_parameters['stock']))

patterns = getPatterns(data=pattern_data,
                       patternlength=pattern_parameters['patternlength'],
                       col='close', outcome_shift=2)
patterns.reverse()
arr = []

for indice in range(-100, 0):

    current_pattern, similar_paths = getSimilarPaths(indice=indice,
                                                     patterns=patterns,
                                                     similarity=pattern_parameters['similarity'])
    if len(similar_paths) > 0:
        arr.append((indice, current_pattern, similar_paths))
        print('similar_path bulundu')
    else:
        print('there is no similar path for current pattern')
print('0000---0000')
graphandsave(pattern_parameters=pattern_parameters, arr2=arr)
