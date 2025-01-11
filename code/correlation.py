## graphes avec la nappe d'eau

import pandas
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
import datetime

from mg_common import ldir_mg_files
# file direction

base = '/Users/severinejessop/Desktop/GAZVOLC/Bdd/Données/Soufriere/MultiGAS/Data/'
rover = base + 'MGportable/resultsfinaux'
perm = base + 'MGpermanent/resultsfinaux'

# créer la liste avec tous les chemins
fichiers  = ldir_mg_files(rover)
permanent = ldir_mg_files(perm)

# données permanentes
ta = pandas.read_csv(permanent[0], ';')
taco2 = np.array(ta.loc[:, ('CO2/H2Scorr(L1-lpf)')])
ta['Time'] = pandas.to_datetime(ta['Time'])
TTACO2 = np.array(ta['Time'])
g = pandas.read_csv(permanent[1], ';')
g['Time'] = pandas.to_datetime(g['Time'])
TG56CO2 = np.array(g['Time'])
g56co2 = np.array(g['CO2/H2Scorr(L1-lpf)'])
c = pandas.read_csv(permanent[2], ';')
c['Time'] = pandas.to_datetime(c['Time'])
csco2 = np.array(c['CO2/H2S(L1-lpf)'])
TCSCO2 = np.array(c['Time'])

# données de la nappe d'eau

na = pandas.read_csv(base + 'Othersparameters/GWL_model_soufriere.csv', ';')
na['Time'] = pandas.to_datetime(na['Time'])
tnappe = np.array(na['Time'])
gwl = np.array(na['GWL(m)'])

# données portables 


g56 = []
tas = []
cs = []
napn = []
tg56 = []
ttas = []
tcs = []
tnapn = []
for file in fichiers:
    df = pandas.read_csv(file, ';')
    m = len(df['Time'])
    for i in range(0,m):
        if df.loc[i, ('Site Name')] =  = 'G56' or df.loc[i, ('Site Name')] =  = 'FLUX-G56':
            g56.append(df.loc[i, ('CO2/H2Scorr(L1)')])
            tg56.append(df.loc[i, ('Time')])
        if df.loc[i, ('Site Name')] =  = 'TAS' or df.loc[i, ('Site Name')] =  = 'FLUX-TAS' or df.loc[i, ('Site Name')] =  = 'TASE':
            tas.append(df.loc[i, ('CO2/H2Scorr(L1)')])
            ttas.append(df.loc[i, ('Time')])
        if df.loc[i, ('Site Name')] =  = 'FLUX-CS' or df.loc[i, ('Site Name')] =  = 'FLUX-CSS' or df.loc[i, ('Site Name')] =  = 'CSS' or df.loc[i, ('Site Name')] =  = 'CSC' or df.loc[i, ('Site Name')] =  = 'CSN':
            cs.append(df.loc[i, ('CO2/H2Scorr(L1)')])
            tcs.append(df.loc[i, ('Time')])
        if df.loc[i, ('Site Name')] =  = 'NapN' or df.loc[i, ('Site Name')] =  = 'NapN2' or df.loc[i, ('Site Name')] =  = 'NapN1':
            napn.append(df.loc[i, ('CO2/H2Scorr(L1)')])
            tnapn.append(df.loc[i, ('Time')])

G56 = np.array(g56)
TAS = np.array(tas)
CS = np.array(cs)
NAPN = np.array(napn)
timeg56 = np.array(tg56)
timecs = np.array(tcs)
timetas = np.array(ttas)
timenapn = np.array(tnapn)
TG56 = np.array([datetime.datetime.strptime(d, '%Y/%m/%d %H:%M:%S') for d in timeg56])
TTAS = np.array([datetime.datetime.strptime(d,'%Y/%m/%d %H:%M:%S') for d in timetas])
TCS = np.array([datetime.datetime.strptime(d,'%Y/%m/%d %H:%M:%S') for d in timecs])
TNAPN = np.array([datetime.datetime.strptime(d,'%Y/%m/%d %H:%M:%S') for d in timenapn])

# données tamburello

dt = pandas.read_csv(base + 'MGportable/litteraturedata/tamburello.csv', ';')

a = [] # G56
b = [] # CS
c = [] # TAS
d = [] # NapN
aa = [] # G56 SO2
bb = [] # CS SO2
cc = [] # TAS SO2
dd = [] # NapN SO2
ta = [] # time G56
tb = [] # time CS
tc = [] # time TAS
td = [] # time NapN

l = len(dt['Time'])
for k in range(0,l):
    if dt.loc[k, ('Site Name')] =  = 'G56' or dt.loc[k, ('Site Name')] =  = 'FLUX-G56':
        a.append(dt.loc[k, ('CO2/H2S')])
        aa.append(dt.loc[k, ('SO2/H2S')])
        ta.append(dt.loc[k, ('Time')])
    if dt.loc[k, ('Site Name')] =  = 'CSS' or dt.loc[k, ('Site Name')] =  = 'CSN':
        b.append(dt.loc[k, ('CO2/H2S')])
        tb.append(dt.loc[k, ('Time')])
        bb.append(dt.loc[k, ('SO2/H2S')])
    if dt.loc[k, ('Site Name')] =  = 'TAS':
        c.append(dt.loc[k, ('CO2/H2S')])
        cc.append(dt.loc[k, ('SO2/H2S')])
        tc.append(dt.loc[k, ('Time')])
    if dt.loc[k, ('Site Name')] =  = 'NapN':
        d.append(dt.loc[k, ('CO2/H2S')])
        dd.append(dt.loc[k, ('SO2/H2S')])
        td.append(dt.loc[k, ('Time')])


g56tam = np.array(a)
cstam = np.array(b)
tastam = np.array(c)
napntam = np.array(d)
g56tamS = np.array(aa)
cstamS = np.array(bb)
tastamS = np.array(cc)
napntamS = np.array(dd)
tg56tam = np.array([datetime.datetime.strptime(f, '%d/%m/%Y %H:%M') for f in ta])
tcstam = np.array([datetime.datetime.strptime(f, '%d/%m/%Y %H:%M') for f in tb])
ttastam = np.array([datetime.datetime.strptime(f, '%d/%m/%Y %H:%M') for f in tc]) 
tnapntam = np.array([datetime.datetime.strptime(f, '%d/%m/%Y %H:%M') for f in td])

# données webObs (pH + hauteur TAS)

do = pandas.read_csv(base + 'Othersparameters/OVSG_EAUX_2019-07-23.csv', ';')
times = np.array([datetime.datetime.strptime(d, '%Y-%m-%d') for d in do['Date']])
pH = np.array(do['pH'])
h = np.array(-1*do['Niveau (m)'])

## graphes

# base de données complètes + nappe d'eau 
fig, ax1  =  plt.subplots()
ax2 = ax1.twinx()
ax1.plot(TG56, G56, 'bo', label = "G56 L1")
ax1.plot(tg56tam, g56tam, 'bo')
ax1.plot(TTAS, TAS, 'ro', label = "TAS L1")
ax1.plot(ttastam, tastam, 'ro')
ax1.plot(TCS, CS, 'mo', label = "CS L1")
ax1.plot(tcstam, cstam, 'mo')
ax1.plot(TNAPN, NAPN, 'co', label = "NapN L1")
ax1.plot(tnapntam, napntam, 'co')
ax1.plot(TTACO2, taco2, 'r', label = "TAS permanent L1-lpf")
ax1.plot(TG56CO2, g56co2, 'b', label = "G56 permanent L1-lpf")
ax1.plot(TCSCO2, csco2, 'm', label = "CS permanent L1-lpf")
ax2.plot(tnappe, gwl, 'k', label = "hauteur nappe")
ax1.set_xlabel('Time')
ax1.set_ylabel('CO2/H2S')
ax2.set_ylabel('GWL (m)')
plt.title('CO2/H2S vs Time pour la base de données complètes')
ax1.set_ylim(0,10)
ax1.legend(loc = 'best')
ax2.legend(loc = 'best')
plt.grid()
#plt.show()


# tarissan perm et rover+ tamburello et nappe eau + pH+ h lac

fig, ax1  =  plt.subplots()
ax2 =  ax1.twinx()
ax1.plot(TTAS, TAS, 'r.', label = "TAS rover")
ax1.plot(TTACO2, taco2, 'r', label = "TAS permanent")
ax1.plot(ttastam, tastam, 'r.')
ax1.plot(times, pH, 'g', label = "pH")
ax2.plot(tnappe, gwl, 'k', label = "hauteur nappe")
ax2.plot(times, h, 'b', label = "hauteur lac Tarissan")
ax1.legend(loc = 'best')
ax2.legend(loc = 'uppper left')
ax1.set_xlabel('Time')
ax1.set_ylabel('CO2/H2S + pH')
ax2.set_ylabel('GWL (m) et Niveau (m)')
plt.title('CO2/H2S + pH + hauteur lac Tarissan + nappe vs Time')
ax1.set_ylim(-1,8)
plt.grid()
#plt.show()


## CS CO2/H2S + Température + Nappe


# Continuous temperature data

def dateparser(y, m, d, H = None, M = None, S = None, s = None):
    # Base case dt and format string.  
    dt  =  y + '-' + m + '-' + d
    fmtStr  =  '%Y-%m-%d'
    
    # Build dt and fmtStr according to case
    if H is not None:
        dt + =  " " + H           # Add 'T' between parenthesis for iso format
        fmtStr + =  " %H"         # fmtStr is now '%Y-%m-%d %H'
        if M is not None:       # Only do this if H AND M are not None
            dt + =  ':' + M
            fmtStr + =  ":%M"     # fmtStr is now '%Y-%m-%d %H:%M'
            if S is not None:   # Only do this if H AND M AND S are not None
                dt + =  ':' + S
                fmtStr + =  ":%S" # fmtStr is now '%Y-%m-%d %H:%M:%S'
                if s is not None:
                    dt + =  '.' + s
                    fmtStr + =  ".%f" # fmtStr is now '%Y-%m-%d %H:%M:%S.%f'

    return pandas.datetime.strptime(dt, fmtStr)

TFContNames  =  ('y','m','d','H','M','S','CSC','CSN','CSS','CS_57',
               'CS_SOUP','CS_28','CS_14')

fname  =  base + 'Othersparameters/GGWCSD_all.csv'

def readTimeSeries(fname, names, sep = ' '):
    return pandas.read_csv(fname, sep = sep, comment = '#', names = names,
                           parse_dates = {'datetime' : ['y','m','d','H','M','S']},
                           date_parser = dateparser)

dt  =  readTimeSeries(fname, names = TFContNames, sep = ' ')


dt['CSC']
fig, ax1 =  plt.subplots()
ax2 = ax1.twinx()
ax1.plot(TCS, CS, 'r.', label = "CS rover")
ax1.plot(tcstam, cstam, 'r.')
ax1.plot(TCSCO2, csco2, 'r', label = "CS permanent")
ax2.plot(tnappe, gwl, 'k', label = "nappe d'eau")
ax2.plot(dt['datetime'], dt['CSC'], 'b.', label = "temperature CSC")
# ax2.plot(ti, tcsn, 'b.')
# ax2.plot(ti, tcss, 'b.')
ax1.set_xlabel('Time')
ax1.set_ylabel('CO2/H2S')
ax2.set_ylabel('GWL (m) et T°')
ax1.legend(loc = 'best')
ax2.legend(loc = 'best')
plt.title('CO2/H2S + T° + nappe vs Time pour CS')
plt.grid()


plt.show()

