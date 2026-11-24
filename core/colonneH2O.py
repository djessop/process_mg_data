## traitement de tous les fichiers ajout colonne H20

import pandas as pd
import numpy as np
import os
import os.path
import sys

from . import ldir_mg_files, read_mgfile, config
from pathlib import Path

def calc_H2O(df):
    for col in ['Pressure', 'Tair', 'Rh']:
        if col not in df.columns:
            raise NameError(f'DataFrame does not contain required data: {col}')
    
    H2O = (6.1121 * (1.0007 + 3.46 * df['Pressure']**(-6)) * \
           np.exp((17.502 * df['Tair']) / (240.9 + df['Tair'])) * \
           (df['Rh'] / 100.0) * (10**6)) / df['Pressure']
    return H2O

if __name__ == '__main__':
    sep      = config.get('DEFAULT', 'sep')
    dtfmt    = config.get('DEFAULT', 'dtfmt')
    dtcol    = config.get('DEFAULT', 'dtcol')
    dossier  = config.get('DEFAULT', 'port') / 'Rawdata/'
    fichiers = ldir_mg_files(dossier)
    
    for fname in fichiers:
        if fname.is_fname():
            df = read_mgfname(fname, config)
    
            # Force necessary columns to be in numeric form
            df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
            df['Tair']     = pd.to_numeric(df['Tair'], errors='coerce')
            df['Rh']       = pd.to_numeric(df['Rh'], errors='coerce')
            df['H20']      = calc_H20(df)
            df             = df.set_index(dtcol)
            df.to_csv(fname, sep=sep, date_format=dtfmt)
        
