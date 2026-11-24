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
          [-o <OUTPUT_FILE>] [-d <DATE_FORMAT>] [-t <TIMES_FILE>]
    where arguments in square brackets are optional, <INPUT_FILE> and 
    <OUTPUT_FILE> are the paths to the input data and save location.  
    <START> and <END> are the (inclusive) start and end times in 
    YYYYmmddHHMM[SS] format (the seconds field is optional), <DATE_FORMAT>
    specifies the format of the datetime field (default: %Y/%m/%d %H:%M:%S).  
    The optional argument <TIMES_FILE> contains a list of start and end times,
    and output file names for splitting <INPUT_FILE> into several sub files.
    The contents of <TIMES_FILE> should be in comma-separated form with no
    header, and of the format
        start_time,end_time,output_fname
    where start_time and end_time are in YYYYmmddHHMM[SS] time format.  If
    output_fname is missing, sub files will be produced with the naming
    convention <INPUT_FILE>_[0,1,...].csv for each row in <TIMES_FILE>.

    AUTHOR
    ------
    D. E. Jessop (OPGC), 18 Sept 2026
'''


def _process_datetimes(args, data):
    stime = args.stime
    etime = args.etime

    if stime == '':
        stime = None
    if etime == '':
        etime = None

    if isinstance(stime, str) and len(stime) == 12:
        stime += '00'
        stime = dt(int(stime[:4]),   int(stime[4:6]),   int(stime[6:8]), 
                   int(stime[8:10]), int(stime[10:12]), int(stime[12:14]))
    if isinstance(etime, str) and len(etime) == 12:
        etime += '00'
        etime = dt(int(etime[:4]),   int(etime[4:6]),   int(etime[6:8]), 
                   int(etime[8:10]), int(etime[10:12]), int(etime[12:14]))

    if stime is None: # and tfile is None:
        stime = data['Time'].iloc[0]
    if etime is None: # and tfile is None:
        etime = data['Time'].iloc[-1]

    args.stime = stime
    args.etime = etime

    return args, stime, etime


def mg_split_by_datetime():
    from pathlib import Path
    from datetime import datetime as dt
    from process_mg_data.core.mg_common import read_mgfile

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
    parser.add_argument('-t', '--timesfile', default=None,
                        help=('Location of the times file'))

    args = parser.parse_args()

    #print(f"fname: {args.filename}\nstart: {args.start}\nend:   {args.end}")

    fname = Path(args.filename)
    oname = Path(args.output)
    dtfmt = args.dtfmt
    tfile = args.timesfile
    data  = read_mgfile(fname)
    #data  = pd.read_csv(fname, date_format=dtfmt, parse_dates=['Time'])
    
    # print(f"fname: {fname}\nstart: {stime}\nend:   {etime}")
    if tfile is None:
        args, stime, etime = _process_datetimes(args, data)

        sub_data = data.query('@stime <= Time <= @etime')
        sub_data.to_csv(oname, sep=';', index=False, date_format=dtfmt)
    else:
        with open(tfile, 'r') as f:
            for ind, line in enumerate(f):
                l = line.strip().split(',')
                # print(ind, l)

                args.stime, args.etime = l[:2]
                args, stime, etime = _process_datetimes(args, data)

                if len(l) == 3:
                    oname = l[2]
                else:
                    oname = fname.with_suffix('').as_posix() + f'_{ind}.csv'

                args.oname = oname

                sub_data = data.query('@stime <= Time <= @etime')
                sub_data.to_csv(oname, sep=';', index=False, date_format=dtfmt)

    return


if __name__ == '__main__':
    mg_split_by_datetime()
                
