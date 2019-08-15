import matplotlib.pyplot as plt
from scipy import stats
import os
from tick_forex import constants
import pandas as pd

data_tick_store_path = constants.data_tick_store_path
bar_frequencies = constants.bar_frequencies
stock = 'AKBNK'

dfs, bar_types = [], []

for name, c, frequencies in bar_frequencies:
    bar_types.append(name)
    l = []
    for freq in frequencies:
        file_path_ = os.path.join(data_tick_store_path + r"\bars\{}_{}_{}.pkl".format(name, freq, stock))
        df = pd.read_pickle(file_path_)
        l.append((str(freq), df))
    dfs.append((name, l))

N_BARS = 1000000

len_rows = max([len(f) for n, c, f in bar_frequencies])

fig, axs = plt.subplots(nrows=len_rows,
                        ncols=len(bar_types),
                        figsize=(12, 12),
                        )

for indice_y, (name, l) in enumerate(dfs):
    for indice_x, (freq, df_bar) in enumerate(l):
        title = '{}_{}'.format(name, freq)
        ax = axs[indice_x, indice_y]
        ax.hist(df_bar.close.pct_change().dropna().values.tolist()[:N_BARS], label=title, alpha=0.5, normed=True,
                bins=50,
                range=(-0.01, 0.01))
        ax.legend()
        ax.set_title(title)
        ax.set(xlabel='return %', ylabel='amount')
        # ax.label_outer()

plt.subplots_adjust(hspace=0.3)
plt.tight_layout()
plt.savefig(r"C:\Users\a.acar\PycharmProjects\Advanced-Deep-Trading-master\distribution_return_graph.png")
plt.show()