


'''
print(pd.Series.autocorr(time_bars.close.pct_change().dropna()[:N_BARS]))
print(pd.Series.autocorr(tick_bars.close.pct_change().dropna()[:N_BARS]))
print(pd.Series.autocorr(volume_bars.close.pct_change().dropna()[:N_BARS]))
print(pd.Series.autocorr(dollar_bars.close.pct_change().dropna()[:N_BARS]))

print('-' * 10)

print(np.var(time_bars.close.pct_change().dropna()[:N_BARS]))
print(np.var(tick_bars.close.pct_change().dropna()[:N_BARS]))
print(np.var(volume_bars.close.pct_change().dropna()[:N_BARS]))
print(np.var(dollar_bars.close.pct_change().dropna()[:N_BARS]))
print('-' * 10)

print(stats.jarque_bera(time_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.jarque_bera(tick_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.jarque_bera(volume_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.jarque_bera(dollar_bars.close.pct_change().dropna()[:N_BARS]))

print('-' * 10)
print(stats.shapiro(time_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.shapiro(tick_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.shapiro(volume_bars.close.pct_change().dropna()[:N_BARS]))
print(stats.shapiro(dollar_bars.close.pct_change().dropna()[:N_BARS]))
'''
