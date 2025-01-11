#!/usr/env/python3

## traitement des fichiers RESULTS tri des données permanentes

import pandas
import numpy as np
import os
import os.path
import sys

from mg_common import (df_all, ldir_mg_files, replace_sitenames,
                       base_by_system)


base = base_by_system()
base += 'Data/MGportable/' # chemin
dossier = base + 'results' # nom du dossier
dos_out = base + 'resultstries' # nom du dossier pour les résultats triés

fichiers, names = ldir_mg_files(dossier, names=True)

# Filter out "bad" values and build a new df from the "good" ones.
# Note that building a new dataframe from rows is quite slow.  
# enlève les NAN car ils ne respectent aucune des conditions
for f_in, f_out in zip(fichiers, names):
    df = pandas.read_csv(f_in, sep=',', parse_dates=['Time'])
    df_out = pandas.DataFrame(columns=df.columns)
    for ind, row in df.iterrows():
        # tri les R2
        if row['R2'] < 0.6:
            row['R2'] = np.nan
            row['CO2/H2S(L2)'] = np.nan
            row['err_ratio'] = np.nan
        if row['R2.1'] < 0.6:
            row['R2.1'] = np.nan
            row['CO2/H2S(L1)'] = np.nan
            row['err_ratio.1'] = np.nan
        if row['R2.2'] < 0.6:
            row['R2.2'] = np.nan
            row['CO2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.2'] = np.nan
        if row['R2.3'] < 0.6:
            row['R2.3'] = np.nan
            row['CO2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.3'] = np.nan
        if row['R2.4'] < 0.6:
            row['R2.4'] = np.nan
            row['SO2/H2S(L2)'] = np.nan
            row['err_ratio.4'] = np.nan
        if row['R2.5'] < 0.6:
            row['R2.5'] = np.nan
            row['SO2/H2S(L1)'] = np.nan
            row['err_ratio.5'] = np.nan
        if row['R2.6'] < 0.6:
            row['R2.6'] = np.nan
            row['SO2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.6'] = np.nan
        if row['R2.7'] < 0.6:
            row['R2.7'] = np.nan
            row['SO2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.7'] = np.nan
        if row['R2.8'] < 0.6:
            row['R2.8'] = np.nan
            row['H2/H2S(L2)'] = np.nan
            row['err_ratio.8'] = np.nan
        if row['R2.9'] < 0.6:
            row['R2.9'] = np.nan
            row['H2/H2S(L1)'] = np.nan
            row['err_ratio.9'] = np.nan
        if row['R2.10'] < 0.6:
            row['R2.10'] = np.nan
            row['H2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.10'] = np.nan
        if row['R2.11'] < 0.6:
            row['R2.11'] = np.nan
            row['H2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.11'] = np.nan
        if row['R2.12'] < 0.6:
            row['R2.12'] = np.nan
            row['H2O/H2S(L2)'] = np.nan
            row['err_ratio.12'] = np.nan
        if row['R2.13'] < 0.6:
            row['R2.13'] = np.nan
            row['H2O/H2S(L1)'] = np.nan
            row['err_ratio.13'] = np.nan
        if row['R2.14'] < 0.6:
            row['R2.14'] = np.nan
            row['H2O/H2S(L2-lpf)'] = np.nan
            row['err_ratio.14'] = np.nan
        if row['R2.15'] < 0.6:
            row['R2.15'] = np.nan
            row['H2O/H2S(L1-lpf)'] = np.nan
            row['err_ratio.15'] = np.nan

        # tri les ratios
        if row['CO2/H2S(L2)'] < 0.0000: 
            row['CO2/H2S(L2)'] = np.nan
            row['err_ratio'] = np.nan
        if row['CO2/H2S(L1)'] < 0.0000:
            row['CO2/H2S(L1)'] = np.nan
            row['err_ratio.1'] = np.nan
        if row['CO2/H2S(L2-lpf)'] < 0.0000:
            row['CO2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.2'] = np.nan
        if row['CO2/H2S(L1-lpf)'] < 0.0000:
            row['CO2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.3'] = np.nan
        if row['SO2/H2S(L2)'] < 0.0000:
            row['SO2/H2S(L2)'] = np.nan
            row['err_ratio.4'] = np.nan
        if row['SO2/H2S(L1)'] < 0.0000:
            row['SO2/H2S(L1)'] = np.nan
            row['err_ratio.5'] = np.nan
        if row['SO2/H2S(L2-lpf)'] < 0.0000:
            row['SO2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.6'] = np.nan
        if row['SO2/H2S(L1-lpf)'] < 0.0000:
            row['SO2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.7'] = np.nan
        if row['H2/H2S(L2)'] < 0.0000:
            row['H2/H2S(L2)'] = np.nan
            row['err_ratio.8'] = np.nan
        if row['H2/H2S(L1)'] < 0.0000:
            row['H2/H2S(L1)'] = np.nan
            row['err_ratio.9'] = np.nan
        if row['H2/H2S(L2-lpf)'] < 0.0000:
            row['H2/H2S(L2-lpf)'] = np.nan
            row['err_ratio.10'] = np.nan
        if row['H2/H2S(L1-lpf)'] < 0.0000:
            row['H2/H2S(L1-lpf)'] = np.nan
            row['err_ratio.11'] = np.nan
        if row['H2O/H2S(L2)'] < 0.0000:
            row['H2O/H2S(L2)'] = np.nan
            row['err_ratio.12'] = np.nan
        if row['H2O/H2S(L1)'] < 0.0000:
            row['H2O/H2S(L1)'] = np.nan
            row['err_ratio.13'] = np.nan
        if row['H2O/H2S(L2-lpf)'] < 0.0000:
            row['H2O/H2S(L2-lpf)'] = np.nan
            row['err_ratio.14'] = np.nan
        if row['H2O/H2S(L1-lpf)'] < 0.0000:
            row['H2O/H2S(L1-lpf)'] = np.nan
            row['err_ratio.15'] = np.nan

        # tri les baseline CO2 et enlève l'erreur sur la baseline
        # Apply to all sites except FTY and BLK
        if row.str.match(r'[fF][tT][yY]-?[0-9]?|Breislack')['Site Name']:
            if row['CO2base'] < 320 or row['CO2base'] > 490: 
                row['CO2base'] = np.nan
                row['err_base'] = np.nan
                row['CO2/H2S(L2)'] = np.nan
                row['err_ratio'] = np.nan
            if row['CO2base.1'] < 320 or row['CO2base.1'] > 490:
                row['CO2base.1'] = np.nan
                row['err_base.1'] = np.nan
                row['CO2/H2S(L1)'] = np.nan
                row['err_ratio.1'] = np.nan
            if row['CO2base.2'] < 320 or row['CO2base.2'] > 490:
                row['CO2base.2'] = np.nan
                row['err_base.2'] = np.nan
                row['CO2/H2S(L2-lpf)'] = np.nan
                row['err_ratio.2'] = np.nan
            if row['CO2base.3'] < 320 or row['CO2base.3'] > 490:
                row['CO2base.3'] = np.nan
                row['err_base.3'] = np.nan
                row['CO2/H2S(L1-lpf)'] = np.nan
                row['err_ratio.3'] = np.nan
            
        # tri les shifts
        #if np.abs(row['delay(s)'])>10: 
            row['delay(s)'] = np.nan
            row['CO2/H2S(L2)'] = np.nan
            row['CO2/H2S(L1)'] = np.nan
        #if np.abs(row['delay(s).1'])>10:
            row['delay(s).1'] = np.nan
            row['CO2/H2S(L2-lpf)'] = np.nan
            row['CO2/H2S(L1-lpf)'] = np.nan
        #if np.abs(row['delay(s).2'])>10:
            row['delay(s).2'] = np.nan
            row['SO2/H2S(L2)'] = np.nan
            row['SO2/H2S(L1)'] = np.nan
        #if np.abs(row['delay(s).3'])>10:
            row['delay(s).3'] = np.nan
            row['SO2/H2S(L2-lpf)'] = np.nan
            row['SO2/H2S(L1-lpf)'] = np.nan
        #if np.abs(row['delay(s).4'])>10:
            row['delay(s).4'] = np.nan
            row['H2/H2S(L2)'] = np.nan
            row['H2/H2S(L1)'] = np.nan
        #if np.abs(row['delay(s).5'])>10:
            row['delay(s).5'] = np.nan
            row['H2/H2S(L2-lpf)'] = np.nan
            row['H2/H2S(L1-lpf)'] = np.nan
        #if np.abs(row['delay(s).6'])>10:
            row['delay(s).6'] = np.nan
            row['H2O/H2S(L2)'] = np.nan
            row['H2O/H2S(L1)'] = np.nan
        #if np.abs(row['delay(s).7'])>10:
            row['delay(s).7'] = np.nan
            row['H2O/H2S(L2-lpf)'] = np.nan
            row['H2O/H2S(L1-lpf)'] = np.nan
        df_out = df_out.append(row, ignore_index=True)

    df_out.rename(columns={'CO2base.1': 'CO2base',
                           'CO2base.2': 'CO2base',
                           'CO2base.3': 'CO2base',
                           'err_ratio.1': 'err_ratio',
                           'err_ratio.2': 'err_ratio',
                           'err_ratio.3': 'err_ratio',
                           'err_ratio.4': 'err_ratio',
                           'err_ratio.5': 'err_ratio',
                           'err_ratio.6': 'err_ratio',
                           'err_ratio.7': 'err_ratio',
                           'err_ratio.8': 'err_ratio',
                           'err_ratio.9': 'err_ratio',
                           'err_ratio.10': 'err_ratio',
                           'err_ratio.11': 'err_ratio',
                           'err_ratio.12': 'err_ratio',
                           'err_ratio.13': 'err_ratio',
                           'err_ratio.14': 'err_ratio',
                           'err_ratio.15': 'err_ratio',
                           'R2.1': 'R2',
                           'R2.2': 'R2',
                           'R2.3': 'R2',
                           'R2.4': 'R2',
                           'R2.5': 'R2',
                           'R2.6': 'R2',
                           'R2.7': 'R2',
                           'R2.8': 'R2',
                           'R2.9': 'R2',
                           'R2.10': 'R2',
                           'R2.11': 'R2',
                           'R2.12': 'R2',
                           'R2.13': 'R2',
                           'R2.14': 'R2',
                           'R2.15': 'R2',
                           'err_base.1': 'err_base',
                           'err_base.2': 'err_base',
                           'err_base.3': 'err_base',
                           'err_base.4': 'err_base',
                           'err_base.5': 'err_base',
                           'err_base.6': 'err_base',
                           'err_base.7': 'err_base',
                           'err_base.8': 'err_base',
                           'err_base.9': 'err_base',
                           'err_base.10': 'err_base',
                           'err_base.11': 'err_base',
                           'err_base.12': 'err_base',
                           'err_base.13': 'err_base',
                           'err_base.14': 'err_base',
                           'err_base.15': 'err_base',
                           'delay(s).1': 'delay(s)',
                           'delay(s).2': 'delay(s)',
                           'delay(s).3': 'delay(s)',
                           'delay(s).4': 'delay(s)',
                           'delay(s).5': 'delay(s)',
                           'delay(s).6': 'delay(s)',
                           'delay(s).7': 'delay(s)',
                           'SO2base.1': 'SO2base',
                           'SO2base.2': 'SO2base',
                           'SO2base.3': 'SO2base',
                           'H2Obase.1': 'H2Obase',
                           'H2Obase.2': 'H2Obase',
                           'H2Obase.3': 'H2Obase',
                           'H2base.1': 'H2base',
                           'H2base.2': 'H2base',
                           'H2base.3': 'H2base'},
                  inplace=True) # renomme les colonnes
    file_out  = "/".join([dos_out, f_out])
    df_out.to_csv(file_out,
                  sep=';',
                  index=False,
                  date_format='%Y/%m/%d %H:%M:%S')
