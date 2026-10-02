## tri des données avant traitement par Arnaud

import pandas
import numpy as np
import os
import os.path

base='/Users/severinejessop/Desktop/GAZVOLC/Bdd/Donnees/Soufriere/MultiGAS/Data/MGportable/'
dossier= base + 'Goodata'
modif = base + 'resultstri1' # nom du dossier où il y aura les résultats triés


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

fichiers = [k for k in fichier(dossier) if k.endswith('.csv')]
name = [k for k in filena(dossier) if k.endswith('.csv')]

for ind, file in enumerate(fichiers):
    df=pandas.read_csv(file, ';')
    m=len(df['SO2'])
    for i in range(0,m):
        if df.loc[i, ('CO2serial')]<0:
            df.loc[i, ('CO2serial')]=np.nan
        if df.loc[i, ('H2S')]<0:
            df.loc[i, ('H2S')]=np.nan
    df=df.set_index('Time')
    u=[modif, name[ind]]
    r="/".join(u)
    df.to_csv(r, ';')



    