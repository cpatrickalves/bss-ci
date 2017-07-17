# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:39:24 2016

@author: Solon Carvalho
@email: solon@lac.inpe.br
"""
import numpy as np
import scipy as sp
import scipy.stats as st
import matplotlib.pyplot as plt


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), sp.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

year0 = 2002
year1 = 2015
year2 = 2026
yearsObs =  np.arange(2000, 2015, 1)   

RECEITA = [211416.44, 210891.01, 228582.31, 243973.40, 262109.79, 284710.92,
           306351.89, 318166.18, 341564.24, 366503.20, 381411.42, 395658.46,
           403571.86, 351467.00]
DESPESA = [255955.00, 273269.07, 302706.66, 328247.70, 350592.41, 370834.37,
           371060.48, 391793.00, 409060.02, 417717.99, 436508.73, 458503.41,
           470623.25, 440079.70]
RECPREV  = [363240, 394507, 437624, 490864, 527641, 566240, 607752, 651755,
            701969, 751925, 805040, 859964, 918028, 978336, 1041244, 1107827,
            1176433, 1248806, 1323082, 1401133, 1482556, 1567284, 1655160,
            1747603, 1845781, 1948079, 2054318, 2165377, 2279955, 2398682,
            2522894, 2651621, 2785567, 2925223, 3071347, 3222548, 3378881,
            3540218, 3708315, 3882904, 4065025, 4254793, 4452738, 4658217,
            4872850]
DESPPREV = [496846, 562136, 615659, 673455, 733644, 790887, 859101, 932707,
            1011802, 1086879, 1174948, 1269292, 1370631, 1478439, 1594309,
            1718566, 1851833, 1994655, 2147988, 2312700, 2489907, 2680461,
            2885382, 3105707, 3342612, 3597290, 3871231, 4165637, 4481695,
            4820867, 5184482, 5574020, 5991217, 6437817, 6915501, 7426179,
            7971796, 8554044, 9174655, 9835584, 10539147, 11287859, 12083458,
            12927729, 13824098]

VAR = np.zeros(len(DESPESA))
for i in range(0,len(DESPESA)): VAR[i]=DESPESA[i]-RECEITA[i]
VARPREV = np.zeros(len(DESPPREV))
for i in range(0,len(DESPPREV)): VARPREV[i]=DESPPREV[i]-RECPREV[i]


varLabel = 'DEFICIT'

plotUnity = ' (TRILLIONS OF REAIS)'
plotFactor = 1000000

diff = np.zeros(len(DESPESA)-1)
for i in range(0,len(diff)):
    diff[i]  = VAR[i+1] - VAR[i]
print('diff:')       
print(diff) 
mean = np.mean(diff)
std = np.std(diff, ddof=1)
var = np.var(diff, ddof=1)

print('mean:')       
print(mean)
print('std:')       
print(std) 
print('var:')       
print(var) 
print('Kolmogorov–Smirnov test (95%):')       
normed_data = (diff - mean) / std
D, pval = st.kstest(normed_data, 'norm')
print('K–S statistic:')
print(D)       
print('p-value:')
print(pval)       
if pval < 0.95:
    print('resullt: REJECT')
else:
    print('resullt: ACCEPT')
    
aEst = mean
bEst = std

years = np.arange(year0, year2, 1)
VARmed = np.zeros(len(years))
VARinf = np.zeros(len(years))
VARsup = np.zeros(len(years))

for i in range(year0, year1+1):
    VARmed[i-year0] = VAR[i-year0]
    VARinf[i-year0] = VAR[i-year0]
    VARsup[i-year0] = VAR[i-year0]
conf = [0.99, 0.95, 0.50]
strConf = ['99%', '95%', '50%']
#VAREst0 = VARmed[year1-year0]
for i in range(year1+1, year2):
   VARmed[i-year0] = VARmed[i-year0-1]+aEst
time=0
for c in range(0,len(conf)):
    for i in range(year1+1, year2):
        time = i-year1
        stdi = bEst*np.sqrt(time)
        lb = VARmed[i-year0] - stdi*sp.stats.norm.ppf((1+conf[c])/2.)
        ub = VARmed[i-year0] + stdi*sp.stats.norm.ppf((1+conf[c])/2.)
        VARinf[i-year0] = lb
        VARsup[i-year0] = ub
    plt.fill_between(years, VARinf/plotFactor, VARsup/plotFactor,
                     color=(0.8-0.20*c, 0.8-0.20*c, 1.0),     
                     facecolor=(0.8-0.20*c, 0.8-0.20*c, 1.0),
                     label=strConf[c])     

plt.plot(years, VARmed/plotFactor, color=(0, 0, 0), label = varLabel)

VARLDO = np.zeros(len(years))
VARPPLDO = np.zeros(len(years))
for i in range(year0, year1+1):
    VARLDO[i-year0] = VAR[i-year0]
for i in range(year1+1, year2):
    VARLDO[i-year0] = VARPREV[i-year1-1]
yearsPlot =  np.arange(year1, year2, 1)   
VARLDOPlot = VARLDO[year1-year0:year2-year0]/plotFactor
plt.plot(yearsPlot, VARLDOPlot, color=(1, 0, 0), label = varLabel+' LDO 2017')

plt.xlabel('YEAR')    
plt.ylabel(varLabel+plotUnity)    
plt.legend(loc='upper left')
#plt.axis(ymax= 1.0)  
#plt.savefig('Deficit2025.png', dpi=600, format='png')
plt.show()
