#!/usr/env/python3

## ajout colonne rapports corrigé CO2/H2S

import pandas
import numpy as np
import os

from process_mg_data.code.mg_common import config, ldir_mg_files

base    = config['DEFAULT']['perm']
dossier = base + 'resultstries'
dos_out = base + 'resultsfinaux'

# créer la liste avec tous les chemins
fichiers, names = ldir_mg_files(dossier, names=True)

for file_in, file_out in zip(fichiers, names):
    df = pandas.read_csv(file_in, sep=';', parse_dates=['Time'])
    df['CO2/H2Scorr(L2)'] = df['CO2/H2S(L2)']*(df['mean(P)']/1013.0)
    df['CO2/H2Scorr(L1)'] = df['CO2/H2S(L1)']*(df['mean(P)']/1013.0)
    df['CO2/H2Scorr(L2-lpf)'] = df['CO2/H2S(L2-lpf)']*(df['mean(P)']/1013.0)
    df['CO2/H2Scorr(L1-lpf)'] = df['CO2/H2S(L1-lpf)']*(df['mean(P)']/1013.0)
    df = df.set_index('Time')
    fname_out = "/".join([dos_out, file_out])
    df.to_csv(fname_out, sep=';', date_format='%Y/%m/%d %H:%M:%S')
