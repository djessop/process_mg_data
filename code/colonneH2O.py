## traitement de tous les fichiers ajout colonne H20

import pandas
import numpy as np
import os
import os.path
import sys

from mg_common import ldir_mg_files, base_by_system


base    = base_by_system()
dossier = base + 'Data/MGportable/Goodata/'

fichiers = ldir_mg_files(dossier)

# supprimer les dossiers cachés dans le shell genre .DS_Store sinon ils apparaissent dans fichiers


for file in fichiers:
    df = pandas.read_csv(file, ';', parse_dates=['Time'])
    # transforme les colonnes de type object en float64
    if df['Pressure'].dtypes == object or \
       df['Tair'].dtypes == object or \
       df['Rh'].dtypes == object: 
        df['Pressure'] = pandas.to_numeric(df['Pressure'], errors='coerce')
        df['Tair'] = pandas.to_numeric(df['Tair'], errors='coerce')
        df['Rh'] = pandas.to_numeric(df['Rh'], errors='coerce')

    # mets les colonnes en float si jamais il y en a qui sont en int
    df['Pressure'] = df['Pressure'].astype(float) 
    df['Tair'] = df['Tair'].astype(float)
    df['Rh'] = df['Rh'].astype(float)
    df['H20'] = (6.1121 * (1.0007 + 3.46 * df['Pressure']**(-6)) * \
                 np.exp((17.502 * df['Tair']) / (240.9 + df['Tair'])) * \
                 (df['Rh'] / 100.0) * (10**6)) / df['Pressure']
    df = df.set_index('Time')
    df.to_csv(file, ';', date_format='%Y/%m/%d %H:%M:%S')
