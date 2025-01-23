1## traitement des fichiers RESULTS tri des données permanentes

import pandas as pd
import numpy as np
import os
import os.path

from mg_common import ldir_mg_files
from configparser import ConfigParser

config = ConfigParser()
conffl = '/home/david/FieldWork/Soufriere-Guadeloupe/process_mg_data/' \
    + 'process.cfg'
if os.path.isfile(conffl):
    config.read(conffl)
else:
    raise FileNotFoundError(f'Config file {conffl} not found')


rename_dict = {'CO2base.1': 'CO2base',
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
               'delay(s).1': 'delay(s)',
               'delay(s).2': 'delay(s)',
               'delay(s).3': 'delay(s)',
               'delay(s).4': 'delay(s)',
               'delay(s).5': 'delay(s)',
               'SO2base.1': 'SO2base',
               'SO2base.2': 'SO2base',
               'SO2base.3': 'SO2base',
               'H2Obase.1': 'H2Obase',
               'H2Obase.2': 'H2Obase',
               'H2Obase.3': 'H2Obase'}

def col_filter(df, pattern, is_regex=True):
    return df.columns[df.columns.str.contains(pattern, regex=is_regex)]

def remove_bad_data(df):
    '''
    Returns a dataframe where data below certain thresholds has been removed.
    '''
    df_c = df.copy()
    # for ind, row in df.iterrows():
    # Columns containing R2 correlation coefficients below .6
    for col in col_filter(df_c, 'R2'):
        rows_to_change = df_c[col] < .6
        df_c.loc[rows_to_change, col]           = np.nan
        df_c.loc[rows_to_change, 'CO2/H2S(L2)'] = np.nan
        df_c.loc[rows_to_change, 'err_ratio']   = np.nan

    # filter ratios
    cols = col_filter(df_c, r'.*/.*\(L')
    for col in cols:
        rows_to_change = np.logical_or(df_c[col] < 0., df_c[col] > 10.)
        df_c.loc[rows_to_change, col]           = np.nan
        df_c.loc[rows_to_change, 'err_ratio']   = np.nan

    # tri les baseline CO2 et enlève l'erreur sur la baseline
    for col in col_filter(df_c, 'CO2base'):
        rows_to_change = np.logical_or(df_c[col] < 350, df_c[col] > 475)
        df_c.loc[rows_to_change, col]           = np.nan
        df_c.loc[rows_to_change, 'CO2/H2S(L2)'] = np.nan
        df_c.loc[rows_to_change, 'err_ratio']   = np.nan

    # tri les shifts
    for col in col_filter(df_c, 'delay(s)'):
        rows_to_change = df_c[col] > 10  # delays > 10 s
        df_c.loc[rows_to_change, col] = np.nan
        if col[-1] == ')' or int(col[-1]) % 2 == 0:
            df_c.loc[rows_to_change, 'CO2/H2S(L1)']     = np.nan
            df_c.loc[rows_to_change, 'CO2/H2S(L2)']     = np.nan
        else:
            df_c.loc[rows_to_change, 'CO2/H2S(L1-lpf)'] = np.nan
            df_c.loc[rows_to_change, 'CO2/H2S(L2-lpf)'] = np.nan

    return df_c


if __name__ == '__main__':
    import sys
    import warnings
    # Suppress the warning arising 
    warnings.simplefilter(action='ignore', category=UserWarning)
                        
    base    = config['DEFAULT']['perm']
    dossier = base + 'results' 
    dos_out = base + 'resultstries'
    sep     = config['DEFAULT']['sep']

    # créer la liste avec tous les chemins
    fichiers = ldir_mg_files(dossier)
    if len(sys.argv) > 1:
        fichiers = sys.argv[1:]
    names = [f.split('/')[-1] for f in fichiers]

    # enlève les NAN car ils ne respectent aucune des conditions
    for fin, fout in zip(fichiers, names):
        # print(fin, fout)
        df = pd.read_csv(fin, sep=sep, parse_dates=['Time'])        
        df = remove_bad_data(df)
        # df = df.rename(columns=rename_dict)
        df = df.drop(labels=rename_dict.keys(), axis=1)

        
        file_out  = "/".join([dos_out, fout])
        # print(file_out)
        df.to_csv(file_out,
                  sep=sep,
                  index=False,
                  date_format='%Y/%m/%d %H:%M:%S')
