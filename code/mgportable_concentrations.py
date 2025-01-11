import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

from datetime import datetime as DT


plt.close('all')

# Change the directory name to fit with your file structure
dir_name = './calculationdata/'
files = [k for k in os.listdir(dir_name) if k[-3:] == 'csv']

df = pd.DataFrame()
mg_names = ('datetime', 'site', 'SO2/H2S', 'H2/H2S', 'H20/H2S', 'CO2/H2S',
            'C/S', 'H2O%', 'CO2%', 'H2S%', 'SO2%', 'H2%', 'logK')

for file in files:
    df = pd.concat([df, pd.read_csv(dir_name + file, sep=';', names=mg_names,
                                    parse_dates=[0], skiprows=1)])
    
df = df[df['H2O%'] == 0]
#df = df[df['site'].str.contains('G56')]
df.reset_index(inplace=True, drop=True)


# Keep only measurements with non-zero logK values
df = df[~df['logK'].isna()]

# Simplify site names
df.replace(r'.*[Tt][Yy].*', 'FTY', regex=True, inplace=True)
df.replace(r'Breislack', 'BLK', regex=True, inplace=True)
df.replace(r'.*[Nn][Aa][pP][eE].*', 'NAPE', regex=True, inplace=True)
df.replace(r'.*[Nn][Aa][pP][nN].*', 'NAPN', regex=True, inplace=True)
df.replace(r'.*[Cc][Ss].*', 'CS', regex=True, inplace=True)
df.replace(r'.*[lL][Cc].*', 'LCX', regex=True, inplace=True)
df.sort_values(by='site', inplace=True)

alpha = .6

fig, ax = plt.subplots()
#ax.plot_date(df['datetime'], df['logK'], label='logK', alpha=.8)
# ax.plot_date(df['datetime'], df['H2S%'], label='H2S %', alpha=.6)
# ax.plot_date(df['datetime'], df['SO2%'], label='SO2 %', alpha=.6)

# Use seaborn scatter plot
sns.scatterplot('datetime', 'logK', data=df, ax=ax, 
                hue='site', alpha=alpha, edgecolor='k') #, edgewidth=.3)

ax.legend()
ax.set_xlim((736296.7703125001, 737281.4956597222))

fig.autofmt_xdate()

plt.show()
