## graphes avec la nappe d'eau

import pandas
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
import sys


from scipy.signal import medfilt
from matplotlib.ticker import MultipleLocator
from matplotlib.dates import MonthLocator, DateFormatter
from plotting_tools import plotQuakes, plotMaria
from readWebObsDF import readTimeSeries, TFContNames, readWebformData
from dateparser import dateparser
from datetime import datetime as DT
from mg_common import ldir_mg_files, df_all, base_by_system


plt.close('all')
plt.rcParams['legend.fontsize'] = 'small'
plt.subplots_adjust(hspace=0.3)


base = base_by_system()

# créer la liste avec tous les chemins

# données permanentes
perm = base + 'Data/MGpermanent/resultsfinaux'
permanent = ldir_mg_files(perm)  # Attn, alphabetically sorted output
MGPermCS  = pandas.read_csv(permanent[0], sep=';', parse_dates=[0])
MGPermG56 = pandas.read_csv(permanent[1], sep=';', parse_dates=[0])
MGPermTAS = pandas.read_csv(permanent[2], sep=';', parse_dates=[0])

MGPermG56['SO2/H2S(L1-lpf)'][MGPermG56['SO2/H2S(L1-lpf)'] > .3] = np.nan


# données de la nappe d'eau
citerne = pandas.read_csv(base + '../Othersparameters/' \
                          + 'GWL_model_soufriere_from_Citerne.csv', ',')
citerne['Time'] = pandas.to_datetime(citerne['Time'])
citerne = citerne[citerne['Time'] > DT(2016,5,1)]
tnappeciterne = np.array(citerne['Time'])
gwlciterne = np.array(citerne['GWL(m)'])

tarade = pandas.read_csv(base + '../Othersparameters/' \
                         + 'GWL_model_soufriere_from_Tarade.csv', ',')
tarade['Time'] = pandas.to_datetime(tarade['Time'])
tnappetarade = np.array(tarade['Time'])
gwltarade = np.array(tarade['GWL(m)'])


# données rover
rover    = base + 'Data/MGportable/resultsfinaux'
fichiers = ldir_mg_files(rover)
df = pandas.DataFrame()

for file in fichiers:
    df = pandas.concat([df, pandas.read_csv(file, sep=';', parse_dates=[0])])

MGroverTAS  = df[df['Site Name'].str.contains('TAS')]
MGroverG56  = df[df['Site Name'].str.contains('G56')]
MGroverCS   = df[df['Site Name'].str.contains('CS')]
MGroverNAPN = df[df['Site Name'].str.contains('NapN')]
MGroverNPE1 = df[df['Site Name'].str.contains('NapE1')]


## données tamburello
tamburello = pandas.read_csv(
    base + 'Data/MGportable/litteraturedata/tamburello.csv', sep=';')
tamburello['Time'] = pandas.to_datetime(tamburello['Time'])
tamburelloTAS  = tamburello[tamburello['Site Name'].str.contains('TAS')]
tamburelloG56  = tamburello[tamburello['Site Name'].str.contains('G56')]
tamburelloCS   = tamburello[tamburello['Site Name'].str.contains('CS')]
tamburelloNAPN = tamburello[tamburello['Site Name'].str.contains('NapN')]
tamburelloNPE1 = tamburello[tamburello['Site Name'].str.contains('NapE1')]

## données webObs (pH + profondeur TAS)
do    = pandas.read_csv(
    base + '../Othersparameters/OVSG_EAUX_2019-07-23.csv', sep=';')
times = np.array(
    [DT.strptime(d, '%Y-%m-%d') for d in do['Date']])
pH    = np.array(do['pH'])
h     = np.array(-do['Niveau (m)'])


## Continuous temperature data
fname = base + '../Othersparameters/GGWCSD_.csv'

temps = readTimeSeries(fname, names=TFContNames, sep=' ')
temps.index = temps['datetime']
temps = temps.resample('12H').mean()
temps[temps['CSC'] < 85] = np.nan  # Only results for T > 85°C

temps[temps['CSN'] < 85] = np.nan  # Only results for T > 85°C


## Number of VT events per day
seismes = pandas.read_csv(base + '../Othersparameters/' \
                          + 'seisme_cumule_par_jours_2.csv',
                          sep=';', parse_dates=[1],
                          names=['index', 'date', 'nbr'], skiprows=1)

## All VT events
quakes = pandas.read_csv(
    base + '../Othersparameters/BoundingBox_5x5km_20170101_20190531_data.csv',
    sep=';', parse_dates=[2])
quakes = quakes[quakes['Origin_times'].notna()]  # Filter NaTs

##extenso
extenso_names = ('Date;Time;Code;Site;Operateurs;Temp. Air;Meteo;'
                 'Dist. Moy (mm);2*Sigma (mm);Vent Moy;Remarques').split(';')
extenso = readWebformData(base + '../Othersparameters/extenso_2.csv',
                          names=extenso_names, sep=';')
Sites = sorted(list(set(extenso.Site)))


### GRAPHS

plot_date_range = [DT(2016,5,1), DT(2020,7,31)]

fig, ax = plt.subplots(3, 2, sharex=True, figsize=(11, 9))
ax = ax.ravel()

fig.subplots_adjust(hspace=.05)

MS = 2.5


## LH COLUMN

## Water table level and CSC temperature
ax02 = ax[0].twinx()
ax02.yaxis.set_major_locator(MultipleLocator(5))
ax02.yaxis.set_minor_locator(MultipleLocator(1))

p1 = ax[0].plot_date(tnappeciterne, gwlciterne, '-', label="depth of water table")
p2 = ax[0].plot_date(tnappetarade, gwltarade, '-', label="depth of water table")
#p3 = ax02.plot_date(temps.index, medfilt(temps['CSC'], 51), '-',
#                    c='C2', label='CSC')
p4 = ax02.plot_date(temps.index, medfilt(temps['CSN'], 51), '-',
                    c='C2', label='CSN')


# Combine the labels from the above plots
ps = p1 +p2 + p4
labs = [p.get_label() for p in ps]
#ax[0].legend(ps, labs, loc=0, framealpha=.5)
ax[0].yaxis.set_major_locator(MultipleLocator(10))
ax[0].yaxis.set_minor_locator(MultipleLocator(2))

water_table_ylim =(79,111)
ax[0].set_ylim(water_table_ylim)
ax[0].invert_yaxis()
ax[0].set_ylabel('Depth of the water table/[m]')
ax02.set_ylabel('Temp./[°C]', color='C2')
ax02.set_ylim((87,108))


## Number of VT events per day
#ax[2].plot_date(seismes['date'], seismes['nbr'], color='C5')
#ax[2].set_ylabel('VT events/day', color='C5')

## CS + G56 MG data
p0 = ax[2].plot_date(MGroverCS['Time'], MGroverCS['CO2/H2Scorr(L1-lpf)'],
                '.C0', label="CS")
p1 = ax[2].plot_date(tamburelloCS['Time'], tamburelloCS['CO2/H2S'],
                markeredgecolor='k', markeredgewidth=.5,
                marker='s', ms=MS, c='C0', label='Tamburello et al., CS')
p2 = ax[2].plot_date(MGPermCS['Time'], MGPermCS['CO2/H2S(L1-lpf)'],
                '-C0', label="CS permanent L1-lpf")

p3 = ax[2].plot_date(MGroverG56['Time'], MGroverG56['CO2/H2Scorr(L1-lpf)'],
                '.C2', label="G56")
p4 = ax[2].plot_date(tamburelloG56['Time'], tamburelloG56['CO2/H2S'],
                markeredgecolor='k', markeredgewidth=.5,
                marker='s', ms=MS, c='C2', label='Tamburello et al., G56')
p5 = ax[2].plot_date(MGPermG56['Time'], MGPermG56['CO2/H2Scorr(L1-lpf)'],
                '-C2', label="G56 permanent L1-lpf")

# Combine the labels from the above plots
ps = p0 + p3
labs = [p.get_label() for p in ps]
ax[2].legend(ps, labs, loc=2, ncol=2)
ax[2].set_ylabel('CO$_2$/H$_2$S')
echelle = ax[2].get_ylim()
ax[2].set_xlabel('Date')


## CS+G56 Sulfur MG data
p0 = ax[4].plot_date(MGroverCS['Time'], MGroverCS['SO2/H2S(L1-lpf)'],
                '.C0', label="CS")
p1 = ax[4].plot_date(tamburelloCS['Time'], tamburelloCS['SO2/H2S'],
                markeredgecolor='k', markeredgewidth=.5,
                marker='s', ms=MS, c='C0', label='Tamburello et al., CS')
p3 = ax[4].plot_date(MGPermCS['Time'], MGPermCS['SO2/H2S(L1-lpf)'],
                '-C0', label="CS permanent L1-lpf")

p4 = ax[4].plot_date(MGroverG56['Time'], MGroverG56['SO2/H2S(L1-lpf)'],
                '.C2', label="G56 rover L1-lpf")
p5 = ax[4].plot_date(tamburelloG56['Time'], tamburelloG56['SO2/H2S'],
                markeredgecolor='k', markeredgewidth=.5,
                marker='s', ms=MS, c='C2', label='Tamburello et al., G56')
p6 = ax[4].plot_date(MGPermG56['Time'], MGPermG56['SO2/H2S(L1-lpf)'],
                '-C2', label="G56 permanent L1-lpf")


#ax[4].legend(loc=2, ncol=2)
ax[4].set_ylabel('SO$_2$/H$_2$S')
#ax[4].set_ylim((0, 0.25))
echelle2 = ax[4].get_ylim()
#ax[4].set_xlabel('Date')
ax[4].set_xlim(plot_date_range)

## RH COLUMN

ax[1].plot_date(tnappeciterne, gwlciterne, '-', label="depth of water table")
ax[1].plot_date(tnappetarade, gwltarade, '-', label="depth of water table")
ax[1].set_ylabel('Depth fo the water table/[m]')
ax[1].set_ylim(water_table_ylim)
ax[1].invert_yaxis()
ax[1].yaxis.set_major_locator(MultipleLocator(10))
ax[1].yaxis.set_minor_locator(MultipleLocator(2))

ax12 = ax[1].twinx()
ax12.plot_date(seismes['date'], seismes['nbr'], color='C5')
ax12.set_ylabel('VT events/day', color='C5')

## Tarrisan level and pH
#ax32 = ax[3].twinx()
#p1 = ax[3].plot_date(times, h, '-', label="Depth of lac Tarissan")
#p2 = ax32.plot_date(times, pH, '-', c='C2', label="pH")
#ax[3].set_ylabel('Depth/[m]')
#ax32.set_ylabel('pH/[-]', color='C2')

# Combine the labels from the above plots
#ps = p1 + p2
#labs = [p.get_label() for p in ps]
#ax[3].legend(ps, labs, loc=0, framealpha=.5)


## Multigas data for TAS
#ax2 = ax[5].twinx()
p0 = ax[3].plot_date(MGroverTAS['Time'], MGroverTAS['CO2/H2Scorr(L1-lpf)'],
                     '.C3', label="TAS")
p1 = ax[3].plot_date(tamburelloTAS['Time'], tamburelloTAS['CO2/H2S'],
                     's', ms=MS, c='C3', label='Tamburello et al., TAS',
                     markeredgecolor='k', markeredgewidth=.5)

p2 = ax[3].plot_date(MGPermTAS['Time'], MGPermTAS['CO2/H2Scorr(L1-lpf)'],
                     '-C3', label="TAS permanent L1-lpf")

p3 = ax[3].plot_date(MGroverNAPN['Time'], MGroverNAPN['CO2/H2Scorr(L1-lpf)'],
                     '.C4', label="NapN")
p4 = ax[3].plot_date(tamburelloNAPN['Time'], tamburelloNAPN['CO2/H2S'],
                     's', ms=MS, c='C4', label='Tamburello et al., NAPN',
                     markeredgecolor='k', markeredgewidth=.5)
p5 = ax[3].plot_date(MGroverNPE1['Time'], MGroverNPE1['CO2/H2Scorr(L1-lpf)'],
                     '.C1', label="NapE1")
p6 = ax[3].plot_date(tamburelloNPE1['Time'], tamburelloNPE1['CO2/H2S'],
                     's', ms=MS, c='C1', label='Tamburello et al., NPE1',
                     markeredgecolor='k', markeredgewidth=.5)

#p5 = ax2.plot_date(MGPermTAS['Time'], MGPermTAS['SO2/H2S(L1)'], 'v',
#                   c='C2', ms=2*MS, label='TAS SO$_2$/H$_2$S', zorder=0)
#p6 = ax2.plot_date(tamburello['Time'], tamburello['SO2/H2S'], '^',
#                   c='C2', ms=2*MS, markeredgecolor='k', markeredgewidth=.5,
#                   label='Tamburello et al., TAS', zorder=0)

#ax2.set_ylabel('SO$_2$/H$_2$S', color='C2')
#ax2.yaxis.set_major_locator(MultipleLocator(0.02))
#ax2.yaxis.set_minor_locator(MultipleLocator(0.01))


ax[3].set_ylim(echelle)
ax[3].set_ylabel('CO$_2$/H$_2$S')
ax[3].legend(loc=1, ncol=3)

# Combine the labels from the above plots
ps = p0 + p3 + p5
labs = [p.get_label() for p in ps]
ax[3].legend(ps, labs, loc=0, framealpha=.5, ncol=3)


# Extenso
DropSites = ['BAT0', 'BLK2', 'DUP1', 'DUP3', 'FNW1', 'F303']
for Site in Sites:
    if Site not in DropSites:
        df = extenso[extenso['Site'] == Site]
        df.sort_values('datetime', inplace=True)
        ax[5].plot_date(
            df['datetime'], df['Dist. Moy (mm)'] - df['Dist. Moy (mm)'].iloc[0],
            '-o', label='%s' % Site)
ax[5].legend(ncol=2)

ax[4].xaxis.set_minor_locator(MonthLocator())
ax[4].xaxis.set_major_formatter(DateFormatter('%b %Y'))

ax[5].set_xlim(plot_date_range)

## Add vertical bars for major events (quakes with M > 2, hurricanes etc.)
for axis in ax:
    plotMaria(axis)
    plotQuakes(quakes['Origin_times'], quakes['Magnitude'], axis, M0=1.5)

fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(base + 'Graphiques/Figure4.png')

plt.show()
