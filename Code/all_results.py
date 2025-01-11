#!/usr/bin/env python3

from glob import glob

import pandas as pd


def read_all_results():
    '''
    Docstring
    '''
    filenames = sorted(list(glob('20*.csv')))
    df = pd.read_csv(filenames[0], sep=';') #, parse_dates=['Time'])
    temp_df = pd.DataFrame(columns=df.columns)
    df = pd.DataFrame(columns=df.columns)
    for filename in filenames:
        temp_df = pd.read_csv(filename, sep=';', parse_dates=['Time'])
        df = pd.concat([temp_df, df])


    return df.replace(
        regex=['DUPUY', 'Ty(-|)[123]', 'CS[NCS]', 'LC(inf|up)', '^56',
               'FLUX-', '^Nap$', '^NapN2', 'TASE'],
        value=['Dupuy', 'Ty', 'CS', 'LC', 'G56',
               '', 'NAP', 'NapN', 'TAS']).sort_values(
            by='Site Name').reset_index(drop=True)



def drop_sites_containing(df, contains_strings):
    ## DROP ROWS FROM DATAFRAME WHOSE NAME CONTAINS 'contains_string'.
    ## For example, you want to drop all FTY 
    ## measurements, whose site code contains 'Ty':
    ## df = df[~df['Site Name'].str.contains('Ty')]

    if type(contains_strings) is list:
        for contains_string in contains_strings:
            df = df[~df['Site Name'].str.contains(contains_string)]

    elif type(contains_strings) is str:
        df = df[~df['Site Name'].str.contains(contains_strings)]

    else:
        Warning('Unknown data type')
        
    return df



def drop_columns(df, contains_string):
    '''Returns a dataframe with no COLUMNS WHOSE NAME CONTAINS 'contains_string' FROM DATAFRAME.
   
    Currently, column names are:
    'Time','Site Name', 'CO2/H2S(L2)', 'err_ratio', 'CO2base', 'err_base', 'R2',
    'CO2/H2S(L1)', 'err_ratio.1', 'CO2base.1', 'err_base.1', 'R2.1', 'delay(s)',
    'CO2/H2S(L2-lpf)', 'err_ratio.2', 'CO2base.2', 'err_base.2', 'R2.2',
    'CO2/H2S(L1-lpf)', 'err_ratio.3', 'CO2base.3', 'err_base.3', 'R2.3',
    'delay(s).1',
    'SO2/H2S(L2)', 'err_ratio.4', 'SO2base', 'err_base.4', 'R2.4',
    'SO2/H2S(L1)', 'err_ratio.5', 'SO2base.1', 'err_base.5', 'R2.5',
    'delay(s).2',
    'SO2/H2S(L2-lpf)', 'err_ratio.6', 'SO2base.2', 'err_base.6', 'R2.6',
    'SO2/H2S(L1-lpf)', 'err_ratio.7', 'SO2base.3', 'err_base.7', 'R2.7',
    'delay(s).3',
    'H2/H2S(L2)', 'err_ratio.8', 'H2base', 'err_base.8', 'R2.8',
    'H2/H2S(L1)', 'err_ratio.9', 'H2base.1', 'err_base.9', 'R2.9',
    'delay(s).4',
    'H2/H2S(L2-lpf)', 'err_ratio.10', 'H2base.2', 'err_base.10', 'R2.10',
    'H2/H2S(L1-lpf)', 'err_ratio.11', 'H2base.3', 'err_base.11', 'R2.11',
    'delay(s).5',
    'H2O/H2S(L2)', 'err_ratio.12', 'H2Obase', 'err_base.12', 'R2.12',
    'H2O/H2S(L1)', 'err_ratio.13', 'H2Obase.1', 'err_base.13', 'R2.13',
    'delay(s).6',
    'H2O/H2S(L2-lpf)', 'err_ratio.14', 'H2Obase.2', 'err_base.14', 'R2.14',
    'H2O/H2S(L1-lpf)', 'err_ratio.15', 'H2Obase.3', 'err_base.15', 'R2.15',
    'delay(s).7',
    'min(CO2)', 'mean(CO2)', 'max(CO2)', 'min(H2S)', 'mean(H2S)', 'max(H2S)',
    'min(SO2)', 'mean(SO2)', 'max(SO2)', 'min(H2)', 'mean(H2)', 'max(H2)',
    'min(H2O)', 'mean(H2O)', 'max(H2O)', 'min(Rh)', 'mean(Rh)', 'max(Rh)',
    'min(T)', 'mean(T)',  'max(T)', 'min(P)', 'mean(P)', 'max(P)', 
    'CO2/H2Scorr(L2)', 'CO2/H2Scorr(L1)',
    'CO2/H2Scorr(L2-lpf)', 'CO2/H2Scorr(L1-lpf)']
    
    To drop (for example) all 'R2' columns (which start with 'R2...':
    df = df[df.columns[~df.columns.str.startswith('R2')]]'''
    
    return df[df.columns[~df.columns.str.startswith(contains_string)]]


if __name__ == '__main__':

    df = read_all_results()
              
    df.to_csv('all_results.csv', index=False)
    df.to_excel('all_results.xlsx', index=False)
