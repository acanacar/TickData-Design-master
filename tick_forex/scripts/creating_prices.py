import numpy as np

def _create_prices(t):
    last_average = 100 if t == 0 else source.data['average'][-1]
    returns = np.asarray(np.random.lognormal(mean.value, stddev.value, 1))
    average = last_average * np.cumprod(returns)
    high = average * np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    low = average / np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * np.random.uniform(0.05, 0.95, size=1)
    close = low + delta * np.random.uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]



def create_p(t):
    returns = np.asarray(np.random.lognormal(-2,0.5,10))



ind=[]
a=[]
for s in range(10,5000,10):
    ind.append(s)
    a.append(np.random.gamma(2, 2, size=s).mean())
