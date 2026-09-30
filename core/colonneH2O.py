## traitement de tous les fichiers ajout colonne H20

import pandas
import numpy as np
import os
import os.path
import sys

from . import ldir_mg_files, base_by_system, read_mgfile
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
    base    = base_by_system()
    dossier = base + 'Data/MGportable/Goodata/'
    
    fichiers = ldir_mg_files(dossier)
    
    for file in fichiers:
        if Path(file).is_file():
            df = read_mgfile(file)
    
            # transforme les colonnes de type object en float64
            df['Pressure'] = pandas.to_numeric(df['Pressure'], errors='coerce')
            df['Tair'] = pandas.to_numeric(df['Tair'], errors='coerce')
            df['Rh'] = pandas.to_numeric(df['Rh'], errors='coerce')
        
            df['H20'] = calc_H20(df)
            df = df.set_index('Time')
            df.to_csv(file, ';', date_format='%Y/%m/%d %H:%M:%S')
        
