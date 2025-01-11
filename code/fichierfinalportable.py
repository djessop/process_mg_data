## fichier final (ajout colonne C/S + pourcentage et log(K))

import pandas
import numpy as np
import os
import os.path

from glob import glob


base= '/Users/severinejessop/Desktop/GAZVOLC/Bdd/Données/Soufriere/MultiGAS/Data/MGportable/'
#'/home/david/FieldWork/Soufriere-Guadeloupe/multigas/data/MGportable/'
dossier= base + 'resultsfinaux/'
modif = base + 'calculationdata/'

# créer la liste avec tous les chemins

def fichier(dossier):
    fich=[]
    for path, dirs, files in os.walk(dossier):
        for filename in files:
            L=[path,filename]
            j="/".join(L)
            fich.append(j)
    return fich

def filena(dossier):
    filen=[]
    for path, dirs, files in os.walk(dossier):
        for filename in files:
            filen.append(filename)
    return filen


fichiers = sorted(glob(dossier + '*.csv'))
#names    = sorted(glob(modif + '*.csv'))

#[k for k in fichier(dossier) if '.csv' in k]  # liste des chemins pour chaque fichier
names = [k for k in filena(dossier) if '.csv' in k]

# df = pandas.DataFrame()

for file, name in zip(fichiers, names):
    df = pandas.read_csv(file, sep=';', parse_dates=[0])

    df = df.fillna(0)
    denom = 1 + df['H2O/H2S(L1-lpf)'] + df['CO2/H2Scorr(L1-lpf)'] + \
	    df['SO2/H2S(L1-lpf)'] + df['H2/H2S(L1-lpf)']
    df['C/S']  = df['CO2/H2Scorr(L1-lpf)'] / df['SO2/H2S(L1-lpf)'] \
	         * df['SO2/H2S(L1-lpf)'] / (df['SO2/H2S(L1-lpf)'] + 1)
    df['H2O%'] = df['H2O/H2S(L1-lpf)'] * 100. / denom
    df['CO2%'] = df['CO2/H2Scorr(L1-lpf)'] * 100. / denom
    df['H2S%'] = 100. / denom
    df['SO2%'] = df['SO2/H2S(L1-lpf)'] * 100. / denom
    df['H2%']  = df['H2/H2S(L1-lpf)'] * 100. / denom
    # df['logK'] = np.log(df['H2O%']) + np.log(df['H2%']) - \
    #              2 * np.log(df['H2S%'])
    df['logK'] = np.log(df['H2%'])  - 2*np.log(df['H2S%'])
    df.set_index('Time', inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    keep_names = ('Time;Site Name;SO2/H2S(L1-lpf);H2/H2S(L1-lpf);' + 
                 'H2O/H2S(L1-lpf);CO2/H2Scorr(L1-lpf);' + 
                 'C/S;H2O%;CO2%;H2S%;SO2%;H2%;logK').split(';')
    df.drop(df.columns.difference(keep_names), 
            axis=1, inplace=True)
    r = "".join([modif, name])
    df.to_csv(r, sep=';')

    #    ['CO2/H2S(L2)', 'err_ratio',
    #          'CO2base', 'err_base', 'R2',
    #          'CO2/H2S(L1)', 'err_ratio.1',
    #          'CO2base.1', 'err_base.1', 'R2.1',
    #          'delay(s)',
    #          'CO2/H2S(L1-lpf)', 'err_ratio.2', 
    #          'CO2base.2', 'err_base.2', 'R2.2',
    #          'CO2/H2S(L2-lpf)', 'err_ratio.3',
    #          'CO2base.3', 'err_base.3', 'R2.3',
    #          'delay(s).1',
    #          'SO2/H2S(L2)', 'err_ratio.4',
    #          'SO2base', 'err_base.4', 'R2.4',
    #          'SO2/H2S(L1)', 'err_ratio.5',
    #          'SO2base.1', 'err_base.5', 'R2.5',
    #          'delay(s).2',
    #          'SO2/H2S(L2-lpf)', 'err_ratio.6',
    #          'SO2base.2', 'err_base.6', 'R2.6', 'err_ratio.7',
    #          'SO2base.3', 'err_base.7', 'R2.7',
    #          'delay(s).3', 'H2/H2S(L2)', 'err_ratio.8',
    #          'H2base', 'err_base.8', 'R2.8',
    #          'H2/H2S(L1)', 'err_ratio.9',
    #          'H2base.1', 'err_base.9', 'R2.9',
    #          'delay(s).4', 'H2/H2S(L2-lpf)', 'err_ratio.10',
    #          'H2base.2', 'err_base.10', 'R2.10', 'err_ratio.11',
    #          'H2base.3', 'err_base.11', 'R2.11',
    #          'delay(s).5',
    #          'H2O/H2S(L2)', 'err_ratio.12',
    #          'H2Obase', 'err_base.12', 'R2.12',
    #          'H2O/H2S(L1)', 'err_ratio.13',
    #          'H2Obase.1', 'err_base.13', 'R2.13',
    #          'delay(s).6',
    #          'H2O/H2S(L2-lpf)', 'err_ratio.14',
    #          'H2Obase.2', 'err_base.14', 'R2.14', 'err_ratio.15',
    #          'H2Obase.3', 'err_base.15', 'R2.15',
    #          'delay(s).7',
    #          'min(CO2)', 'mean(CO2)', 'max(CO2)',
    #          'min(H2S)', 'mean(H2S)', 'max(H2S)',
    #          'min(SO2)', 'mean(SO2)', 'max(SO2)',
    #          'min(H2)', 'mean(H2)', 'max(H2)',
    #          'min(H2O)', 'mean(H2O)', 'max(H2O)',
    #          'min(Rh)', 'mean(Rh)', 'max(Rh)',
    #          'min(T)', 'mean(T)', 'max(T)',
    #          'min(P)', 'mean(P)', 'max(P)',
    #          'CO2/H2Scorr(L1)', 'CO2/H2Scorr(L2)', 'CO2/H2Scorr(L2-lpf)'],
    