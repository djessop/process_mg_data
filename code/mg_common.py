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
