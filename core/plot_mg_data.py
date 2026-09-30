import matplotlib
matplotlib.use('agg')

from datetime import date
from cycler import cycler
from dateparser import dateparser
from matplotlib.dates import (DateFormatter, 
                              MonthLocator, 
                              DayLocator)

import numpy as np
import matplotlib.pyplot as plt
import pandas
import itertools


"""
plot_mg_data : as the name suggests, this core takes multigas data and plots it.
There are two sorts of plot: 
i)      correlation of molar ratios, notably for H2O/H2S-H2O/CO2
ii)     time series of either the absolute concentrations or of molar ratios

The data comes from either the rover instrument or the permenant installations.

"""


# Use itertools.cycle to switch between point colours and symbols
# See https://matplotlib.org/examples/color/color_cycle_demo.html for details.
# Colour list obtained by calling plt.rcParams['axes.prop_cycle'].
# The rover data has 16 points to plot, so repeat the first 8 colours in this
# list twice, and change symbol for the second set of 8.
colourList = itertools.cycle(('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                              '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'))

# , '#bcbd22', '#17becf
markerList = itertools.cycle(('o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
                              '^', '^', '^', '^', '^', '^', '^', '^'))


# MG Rover data.
# Open the excel file as a dataframe.
# Contains the following fields:
#       'SITE', 'Reference', 'Date', 'H2O/H2S', 'H2O/CO2', 'CO2/H2S', 'SO2/H2S',
#       'CO2/Stot', 'H2O/Stot', 'H2/H2S', 'H2O/CO2_calc',
filename = './Soufrière GASVOLC - MultiGAS mobile DJ.xls'
df = pandas.read_excel(filename, sheet_name='Tableau Data', index_col=None,
                       parse_dates=[3])

# Actually we only want to plot the data more recent that 2016-01-01, and we
# filter out other unwanted data such as nans, sites other than Cratère Sud,
# the Villemant et al., 2014 data...
# Eventually, this should be done according to a set of criteria, but for now
# just use the following hack...
# keepIndex = []
# for ind, site, ref in zip(df.index, df['SITE'], df['Reference']):     
#     if 'SC' in site or 'CS' in site and 'Villemant et al. 2014' is not ref:
#         keepIndex.append(ind) 
# df = df.iloc[keepIndex]

# df = df[df.Date > datetime(2016, 1, 1)]
df = df.iloc[:34]

# Create a list of the unique dates in the data frame
uniqueDates = []
for d in df.Date:
    if d not in uniqueDates:                                       
        uniqueDates.append(d)

# Plot the H2O/H2S - H2O/CO2 data
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel(r'H$_2$O/H$_2$S')
ax.set_ylabel(r'H$_2$O/CO$_2$ (calc.)')

ax.set_xlim((0, 135))
ax.set_ylim((0, 89.5))
for UD in uniqueDates:                   
    plt.plot(df[df.Date == UD]['H2O/H2S'], df[df.Date == UD]['H2O/CO2_calc'],
             marker=next(markerList), c=next(colourList), linestyle='',
             label='%s' % UD.date())



ax.grid(True)
ax.legend(loc=2, ncol=2)
ax.set_title('Multigas Cratère Sud')

fig.tight_layout()
fig.savefig('./Multigas_CS_all.pdf')

# plt.show()


# Read the seismic data frames and combine them.
temp    = pandas.read_csv('./z_vs_time.dat', parse_dates=True,
                          names=['datetime', 'z'], sep=';', index_col=None)
seismic = pandas.read_csv('./tx_vs_time.dat', parse_dates=True,
                          names=['datetime', 'tx'], sep=';', index_col=None)
seismic['z'] = temp['z']


# Create a plot of 1) seismic, 2) multigas, 3) fumerole temperature 
fig, ax = plt.subplots(4, 1, sharex=True, figsize=(10,12))

d1   = date(2018, 1, 1)
d2   = date(2018, 5, 7)
# XLim = (736398.7925555556, 736814.3135324074)

# Plot the seismic data
dates = pandas.to_datetime(seismic.datetime)
c = next(colourList)
ax2 = ax[0].twinx()
ax[0].plot_date(dates, seismic.tx, '-', c=c, label='tx')
ax[0].set_ylabel(r'taux sismicité', color=c)
ax[0].set_xlim((d1, d2))
ax[0].set_title('seismic data')
# GU has some sort of funky upside down interpretation of 'z', and plots it on
# a secondary 'y' axis.
c = next(colourList)
ax2.plot_date(dates, -seismic.z, '-', c=c, label='z')
ax2.axhline(y=.0, c='k', ls='--', lw=1.) # A dashed horizontal line
#plt.hlines(seismic.datetime, 0, 'k--')
ax2.set_ylabel(r'Depth/[km]', color=c)


# First multigas plot is for Cratère Sud
# Read the multigas data, taking note of the column separated timestamp.
# Call the 'dateparser' function 
MGCS = pandas.read_csv('./GCMCSN1_all.txt', sep=' ', skiprows=13,
                       names=['y', 'm', 'd', 'H', 'M', 'S', 'SO2',
                              'H2S', 'CO2', 'RH', 'T', 'p', 'V'],
                       parse_dates={'datetime':
                                    ['y', 'm', 'd', 'H', 'M', 'S']},
                       date_parser=dateparser)


CO2_H2S_CS = np.divide(MGCS.CO2, MGCS.H2S)
SO2_H2S_CS = np.divide(MGCS.SO2, MGCS.H2S)
dates      = pandas.to_datetime(MGCS.datetime)
skip       = 1200                   # Plot once per 20 minutes
ax2        = ax[1].twinx()
c          = next(colourList)
ax[1].plot_date(dates[::skip], CO2_H2S_CS[::skip], '.', c=c,
                label=r'CO$_2$/H$_2$S')
ax[1].set_ylabel(r'CO$_2$/H$_2$S', color=c)

c = next(colourList)
ax2.plot_date(dates[::skip], SO2_H2S_CS[::skip], '.', c=c,
              label=r'SO$_2$/H$_2$S')
ax2.set_ylabel(r'SO$_2$/H$_2$S', color=c)
ax[1].set_title('Permanent Multigas, Cratère Sud')


# Now plot G56
# Read the multigas data, taking note of the column separated timestamp.
# Call the 'dateparse' function 
MGG56 = pandas.read_csv('./GCMG56_all.txt', sep=' ', skiprows=13,
                        names=['y', 'm', 'd', 'H', 'M', 'S', 'SO2',
                               'H2S', 'CO2', 'RH', 'T', 'p', 'V'],
                        parse_dates={'datetime':
                                     ['y', 'm', 'd', 'H', 'M', 'S']},
                        date_parser=dateparser)


CO2_H2S_G56 = np.divide(MGG56.CO2, MGG56.H2S)
SO2_H2S_G56 = np.divide(MGG56.SO2, MGG56.H2S)
dates   = pandas.to_datetime(MGG56.datetime)
skip    = 1200                   # Plot once per 20 minutes
ax2     = ax[2].twinx()
c = next(colourList)
ax[2].plot_date(dates[::skip], CO2_H2S_G56[::skip], '.', c=c,
                label=r'CO$_2$/H$_2$S')
ax[2].set_xlabel('Date')
ax[2].set_ylabel(r'CO$_2$/H$_2$S', color=c)
ax[2].set_title('Permanent Multigas, Goufre 56')

c = next(colourList)
ax2.plot_date(dates[::skip], SO2_H2S_G56[::skip], '.', c=c,
              label=r'SO$_2$/H$_2$S')
ax2.set_ylabel(r'SO$_2$/H$_2$S', color=c)


# Plot the fumarole temperature data
tempsFname   = '../temperatureFumaroles/CSFumaroleTemperatures_all.csv'
temperatures = pandas.read_csv(tempsFname,
                               names=('datetime', 'CSN', 'CSC', 'CSS',
                                      'CSS2', 'Flex'),
                               parse_dates=[0])

skip=1200
c = next(colourList)
ax[3].plot_date(temperatures.datetime[::skip], temperatures.CSN[::skip],
                '.', c=c, label='CSN')
c = next(colourList)
ax[3].plot_date(temperatures.datetime[::skip], temperatures.CSC[::skip],
                '.', c=c, label='CSC')
c = next(colourList)
ax[3].plot_date(temperatures.datetime[::skip], temperatures.CSS[::skip],
                '.', c=c, label='CSS')

ax[3].legend()
ax[3].set_ylim((0, 120))

fig.tight_layout()
fig.savefig('CompareTimeseries.pdf')
plt.show()
