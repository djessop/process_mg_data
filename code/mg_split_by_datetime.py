#!/usr/bin/env python
# coding: utf-8

''' 
    mg_split_by_datetime.py
    -----------------------
    Splits a raw MG data file by datetime according to user-defined bounds.
    The split-off segments are saved as individual csv files.

    RUNNING THE SCRIPT
    ------------------
    From the command line, type
        $ python mg_split_by_datetime.py <INPUT_FILE> [-s <START>] [-e <END>]
          [-o <OUTPUT_FILE>] [-d <DATE_FORMAT>]
    where arguments in square brackets are optional, <INPUT_FILE> and 
    <OUTPUT_FILE> are the paths to the input data and save location.  
    <START> and <END> are the (inclusive) start and end times in 
    YYYYmmddHHMM[SS] format (the seconds field is optional), <DATE_FORMAT>
    specifies the format of the datetime field (default: %Y/%m/%d %H:%M:%S).  

    AUTHOR
    ------
    D. E. Jessop (OPGC), 18 Sept 2026
'''


if __name__ == '__main__':
    from pathlib import Path
    from datetime import datetime as dt
    from process_mg_data.code.mg_common import read_mgfile

    import argparse
    import pandas as pd


    parser = argparse.ArgumentParser(
        description='Optional arguments for start and end datetimes')
    parser.add_argument('filename')
    parser.add_argument('-o', '--output', default='output.csv',
                        help=('Location of the output file'))
    parser.add_argument('-s', '--start', default=None,
                        help=('Start time for splitting in '
                              + 'YYYYmmddHHMM[SS] format'))
    parser.add_argument('-e', '--end', default=None,
                        help=('End time for splitting in '
                              + 'YYYYmmddHHMM[SS] format'))
    parser.add_argument('-d', '--dtfmt', default='%Y/%m/%d %H:%M:%S',
                        help=('End time for splitting in '
                              + 'YYYYmmddHHMM[SS] format'))

    args = parser.parse_args()

    #print(f"fname: {args.filename}\nstart: {args.start}\nend:   {args.end}")

    fname = Path(args.filename)
    oname = Path(args.output)
    stime = args.start #dt(start[:4], start[5:6], start[7:8]
    etime = args.end
    dtfmt = args.dtfmt

    data = read_mgfile(fname, dtfmt=dtfmt)

    if stime is not None and len(stime) != 14:
        stime += '00'
        stime = dt(int(stime[:4]),   int(stime[4:6]),   int(stime[6:8]), 
                   int(stime[8:10]), int(stime[10:12]), int(stime[12:14]))
    if etime is not None and len(etime) != 14:
        etime += '00'
        etime = dt(int(etime[:4]),   int(etime[4:6]),   int(etime[6:8]), 
                   int(etime[8:10]), int(etime[10:12]), int(etime[12:14]))
    if stime is None:
        stime = data['Time'].iloc[0]
    if etime is None:
        etime = data['Time'].iloc[-1]
    
    # print(f"fname: {fname}\nstart: {stime}\nend:   {etime}")
    
    sub_data = data.query('Time >= @stime and Time <= @etime')
    
    sub_data.to_csv(oname, sep=';', index=False, date_format=dtfmt)
