## tracer des graphes de la feuille pour les permanents

## cré la liste des chemins des fichiers

import pandas
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
import datetime


# file direction

base = '/Users/severinejessop/Desktop/GAZVOLC/Bdd/Données/Soufriere/MultiGAS/Data/MGpermanent/'
dossier = base + 'resultsfinaux'

# créer la liste avec tous les chemins

def fichier(dossier):
    fich=[]
    for path, dirs, files in os.walk(dossier):
        for filename in files:
            L=[path,filename]
            j="/".join(L)
            fich.append(j)
    return fich


fichiers=[k for k in fichier(dossier) if '.csv' in k] # liste des chemins pour chaque fichier

## tracé CO2/H2S corrigés (L1-lpf) vs Time

# results-tar.csv

df=pandas.read_csv(fichiers[0], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(1)
plt.ylim(0,4.5)
plt.title('CO2/H2S L1 lpf  vs Time CS permanent')
plt.xlabel('Time')
plt.ylabel('CO2/H2Scorr')
CO21 = np.array(df['CO2/H2Scorr(L1-lpf)'])
plt.plot(time, CO21, 'r', label="CO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()

# results-g56.csv

df=pandas.read_csv(fichiers[1], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(2)
plt.ylim(0,10)
plt.title('CO2/H2S L1 lpf method vs Time G56 permanent')
plt.xlabel('Time')
plt.ylabel('CO2/H2Scorr')
CO21 = np.array(df['CO2/H2Scorr(L1-lpf)'])
plt.plot(time, CO21, 'r', label="CO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()

# results-cs.csv

df=pandas.read_csv(fichiers[2], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(3)
plt.ylim(0,10)
plt.title('CO2/H2S L1 lpf methods vs Time TAS permanent')
plt.xlabel('Time')
plt.ylabel('CO2/H2Scorr')
CO21 = np.array(df['CO2/H2Scorr(L1-lpf)'])
plt.plot(time, CO21, 'r', label="CO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()

## tracé SO2/H2S (L1-lpf) vs Time

# TAR 

df=pandas.read_csv(fichiers[0], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(8)
plt.ylim(0,0.01)
plt.title('SO2/H2S L1 lpf vs Time CS permanent')
plt.xlabel('Time')
plt.ylabel('SO2/H2S')
SO21 = np.array(df['SO2/H2S(L1-lpf)'])
plt.plot(time, SO21, 'r', label="SO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()

# G56

df=pandas.read_csv(fichiers[1], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(9)
plt.ylim(0,0.5)
plt.title('SO2/H2S L1 lpf vs Time G56 permanent')
plt.xlabel('Time')
plt.ylabel('SO2/H2S')
SO21 = np.array(df['SO2/H2S(L1-lpf)'])
plt.plot(time, SO21, 'r.', label="SO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()

# CS

df=pandas.read_csv(fichiers[2], ';')
df['Time']=pandas.to_datetime(df['Time'])
time = np.array(df['Time'])
plt.figure(8)
plt.ylim(0,0.02)
plt.title('SO2/H2S L1 lpf vs Time TAS permanent')
plt.xlabel('Time')
plt.ylabel('SO2/H2S')
SO21 = np.array(df['SO2/H2S(L1-lpf)'])
plt.plot(time, SO21, 'r', label="SO2/H2S L1-lpf method")
plt.legend()
plt.grid()
plt.show()