import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pandas.plotting import register_matplotlib_converters
from timeSeriesAnalysis.readWebObsDF import resample_df

register_matplotlib_converters()


# Change the directory name to fit with your file structure
dir_name = './resultstri1/'
files = sorted([k for k in os.listdir(dir_name) if 'G56.csv' in k])


dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%y %H:%M:%S')

df = pd.DataFrame()
mg_names = ('datetime', 'SO2', 'H2S', 'H2', 'CO2', 'Ext', 'RH', 'Tair', 'p', 'Lat', 'Lon', 'V', 'H20')

for file in files:
    df = pd.concat([df, pd.read_csv(dir_name + file, sep=';', names=mg_names,
                                    parse_dates=[0], date_parser=dateparse,
                                    skiprows=1)])

df.index = df['datetime']
df = df.resample('1d').mean()
df['datetime'] = df.index
df.reset_index(inplace=True, drop=True)

df[df['SO2'] < 0.]['SO2'] = np.nan


fig, ax = plt.subplots()
ax1 = ax.twinx()
p0, = ax.plot_date(df['datetime'], df['CO2'], label='CO2', c='C0')
ax.set_ylabel('CO2', color=p0.get_color())
p1, = ax1.plot_date(df['datetime'], df['H2S'], label='H2S', c='C1')
ax1.set_ylabel('H2S', color=p1.get_color())
#ax.plot_date(df['datetime'], df['SO2'], label='SO2')

#ax.legend()

fig.autofmt_xdate()

plt.show()