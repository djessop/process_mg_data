#!/usr/env/python3
'''
   mg_common.py : common utilities for reading, combining, analysing
   and treating multigas data files.
'''

from glob import glob

import pandas as pd
import numpy as np
import os
import sys


rename_dict = {'CO2base.1': 'CO2base',
               'CO2base.2': 'CO2base',
               'CO2base.3': 'CO2base',
               'H2Obase.1': 'H2Obase',
               'H2Obase.2': 'H2Obase',
               'H2Obase.3': 'H2Obase',
               'SO2base.1': 'SO2base',
               'SO2base.2': 'SO2base',
               'SO2base.3': 'SO2base',
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
               'delay(s).1': 'delay(s)',
               'delay(s).2': 'delay(s)',
               'delay(s).3': 'delay(s)',
               'delay(s).4': 'delay(s)',
               'delay(s).5': 'delay(s)',
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
               'R2.11': 'R2'}


ratio_minmax = {'CO2/H2S(L2)': [0, 10],
                'CO2/H2S(L1)': [0, 10],
                'CO2/H2S(L2-lpf)': [0, 10],
                'CO2/H2S(L1-lpf)': [0, 10],
                'SO2/H2S(L2)': [0, 10],
                'SO2/H2S(L1)': [0, 10],
                'SO2/H2S(L2-lpf)': [0, 10],
                'SO2/H2S(L1-lpf)': [0, 10],
                'H2O/H2S(L2)': [0, np.nan],
                'H2O/H2S(L1)': [0, np.nan],
                'H2O/H2S(L2-lpf)': [0, np.nan],
                'H2O/H2S(L1-lpf)': [0, np.nan]}

def proc_mg_dir():
    '''Returns the directory where the process_mg_data module is located'''
    import process_mg_data

    ## module.__file__ is the path to module.py, __init__.py or submodule.py 
    pmgd_dir = '/'.join(process_mg_data.__file__.split('/')[:-1]) + '/'
    print(pmgd_dir)


def base_by_system():
    '''
    Create base of filename according to the type of system being used
    '''
    if sys.platform == 'linux':
        base = '/media/david/KINGSTON/'
    elif sys.platform == 'darwin':
        base = '/Users/severinejessop/Desktop/GAZVOLC/Bdd/Donnees/Soufriere/'
    return base + 'MultiGAS/'


def ldir_mg_files(directory='./', ending='.csv', names=False):
    ''' 
    Return a list of all multigas data files (i.e. files ending in *.csv) 
    in the current directory and all subdirectories.
    '''
    L = []
    for path, dirs, files in os.walk(directory):
        for f in files:
            if '._' not in f and f.endswith(ending) and not f.endswith('#'):
                L.append(os.path.join(path, f))
    L.sort()
    if names:
        return L, [f.split('/')[-1] for f in L]
    else:
        return L


def df_all(directory, sep=','):
    '''
    Return a pd dataframe containing all data (all sites, all sorties) 
    from the current stage of processing.
    '''
    files = ldir_mg_files(directory)
    # Create an empty dataframe to which the data from each file will be
    # added.
    df = pd.DataFrame()
    for f in files:
        temp_df = pd.read_csv(f, sep=sep, parse_dates=['Time'])
        df = pd.concat([df, temp_df])
    return replace_sitenames(df.reset_index(drop=True))


def replace_sitenames(df, search_strings=[], replace_strings=[]):
    '''
    Replace site names in a dataframe according to a regex
    '''
    for search, replace in zip(search_strings, replace_strings):
        df.replace(search, replace, regex=True, inplace=True)
    return df


def sort_by_site_datetime(df_all):
    '''
    Return a dataframe sorted by sites and then by datetime
    '''
    return df.sort_values(by=['Site Name', 'Time'], inplace=True)
