#!/usr/bin/env python
# coding: utf-8

''' 
    MGportable_split_df_by_site.py
    ------------------------------

    Splits a raw MG data file by site according to a user-defined configuration 
    file.  The split-off segments are then saved as csv files in a sub-directory
    of where the raw data file was stored, whose name corresponds to the date 
    of the measurements.

    CONFIGURATION FILE
    ------------------
    The format of this file is _very_ important.  It should contain one line 
    per site/style of measurement (e.g. flux and pure concentration 
    measurements are counted separately) each consisting of the following 
    information:
        <SITE> <START TIME> <END TIME>
    where <START/END TIME> is in ISO format ('%Y-%m-%dT%H:%M:%S').  To avoid 
    errors, each of these fields MUST be entered.
    Note that the <SITE> variable cannot contain whitespace characters though 
    hyphens (-) and underscores (_) are allowed.

    RUNNING THE SCRIPT
    ------------------
    From the command line, type 
        $ python MGportable_split_df_by_site.py <RAW_DATA_FILE> <CONFIG_FILE>
    where <RAW_DATA_FILE> is the absolute or relative path to the bulk raw 
    data.


    AUTHOR
    ------
    D. E. Jessop (OVSG-IPGP), 18 March 2020
'''

def site_start_stop_times(config_file):
    '''
    Return a dict of sites with start & stop times for the MG traverses 
    read from a text file.  Datetime strings are expected to be of the format
        '%Y-%m-%dT%H:%M:%S'
    and are then converted to datetime objects.
    '''
    from datetime import datetime as DT

    dtstr_format = '%Y-%m-%dT%H:%M:%S'
    sites_dict   = {}
    with open(config_file, 'r') as f:
        for line in f:
            site, *times = line.split()
            sites_dict[site] = [DT.strptime(t, dtstr_format) for t in times] 
    return sites_dict


if __name__ == '__main__':
    import os
    import sys
    import pandas as pd
    # Ensure that filename points to the right location.  This will 
    # necessarily be different for each MG outing.
    filename = sys.argv[1]     # '../data/MGportable/guada_20191220141504.csv'
    confname = './config.txt'  # Default 
    if len(sys.argv) == 3:
        confname = sys.argv[2]  
    mg_df = pd.read_csv(filename, parse_dates=[0], sep=';')

    # Split the filename to keep only the essential information: file location 
    # and date.  If time is required in addition to date, extend the range of 
    # the slice, i.e. ...split_fn[1][1:13] for 'YYYYMMDDHHMM'
    # or   ...split_fn[1][1:15] for 'YYYYMMDDHHMMSS'
    split_fn = filename.split('guada')
    filedate = split_fn[1][1:9]
    new_dirn = split_fn[0] + filedate + '/'
    if not os.path.isdir(new_dirn):
        os.mkdir(new_dirn)
    outfile  = new_dirn + filedate

    # Define a dictionary of sites with 'start' and 'stop' times for each.
    sites_dict = site_start_stop_times(confname)

    # Do not touch anything in this loop
    for site in sites_dict.keys():
        date_range = sites_dict[site]
        site_df = mg_df[mg_df['Time'] >
                        date_range[0]][mg_df['Time'] <= date_range[-1]]
        site_df.to_csv(outfile + '_' + site + '.csv', index=False, sep=';')
