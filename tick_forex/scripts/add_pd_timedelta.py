import pandas as pd

df = pd.date_range(start='1/1/2018', periods=10, freq='1H')

df.map(lambda x: x + pd.Timedelta(minutes=30))
