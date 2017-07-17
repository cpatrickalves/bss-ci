# -*- coding: utf-8 -*-
"""
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

year0 = 2000
year1 = 2015
year2 = 2061
yearsObs =  np.arange(2000, 2015, 1)   

PIB = [3916915239480.42, 3971356303559.63, 4092620153487.88, 4139309951008.42,
       4377732740396.53, 4517913524072.55, 4696912747778.46, 4982009274107.88,
       5235802563774.39, 5229215295696.24, 5622882431672.01, 5842692830451.35,
       5954754663080.98, 6134207156833.72, 6140596986002.71, 5904331214709.13]
POP = [173447387, 175894625, 178288012, 180627489,
       182912972, 185144393, 187321684, 189444772,
       191513595, 193528069, 195488139, 197393721,
       199244754, 201041158, 202782873, 204469821]

### Calcula a diferença dos logaritmos do PIB

diffLnPIB = np.zeros(len(PIB)-1)

for i in range(0,len(diffLnPIB)):
    # Calcula a diferença do Log natural do PIB
    diffLnPIB[i] = np.log(PIB[i+1]) - np.log(PIB[i])

print('diffLnPIB:')       
print(diffLnPIB) 

# Calcula estatísticas
mean = np.mean(diffLnPIB)
std = np.std(diffLnPIB, ddof=1)
var = np.var(diffLnPIB, ddof=1)

print('mean:')       
print(mean)
print('std:')       
print(std) 
print('var:')       
print(var) 

### Realiza o teste estatístico Kolmogorov–Smirnov
print('Kolmogorov–Smirnov test (95%):')     

# Normaliza os dados   
normed_data = (diffLnPIB - mean) / std

# Realiza o Teste              
D, pval = st.kstest(normed_data, 'norm')

print('K–S statistic:')
print(D)       
print('p-value:')
print(pval)       

# Avalia se o pval está dentro do intervalo de confiança definido
if pval < 0.95:
    print('resullt: REJECT')
else:
    print('resullt: ACCEPT')

    
aEst = mean
bEst = std

years = np.arange(year0, year2, 1)
PIBmed = np.zeros(len(years))
PIBinf = np.zeros(len(years))
PIBsup = np.zeros(len(years))

# Coloca os valores na escala de trilhões e savla os valores de PIB conhecidos
for i in range(year0, year1+1):
    PIBmed[i-year0] = PIB[i-year0]/1.0e12
    PIBinf[i-year0] = PIB[i-year0]/1.0e12
    PIBsup[i-year0] = PIB[i-year0]/1.0e12
          
conf = [0.99, 0.95, 0.50]
strConf = ['99%', '95%', '50%']

# Armazena o primeiro valor estimado (que é conhecido, tendo erro 0)
PIBEst0 = PIBmed[year1-year0]

# Estima o PIB para os anos restantes
for i in range(year1+1, year2):
   PIBmed[i-year0] = PIBEst0*np.exp((aEst+bEst*bEst/2)*(i-year1))

time=0
for c in range(0,len(conf)):
    for i in range(year1+1, year2):
        time = i-year1
        stdi = bEst*np.sqrt(time)
        lb = aEst*time - stdi*sp.stats.norm.ppf((1+conf[c])/2.)
        ub = aEst*time + stdi*sp.stats.norm.ppf((1+conf[c])/2.)
        PIBinf[i-year0] = PIBEst0*np.exp(lb)
        PIBsup[i-year0] = PIBEst0*np.exp(ub)
    plt.fill_between(years, PIBinf, PIBsup,
                     color=(0.8-0.20*c, 0.8-0.20*c, 1.0),     
                     facecolor=(0.8-0.20*c, 0.8-0.20*c, 1.0),
                     label=strConf[c])     

plt.plot(years, PIBmed, color=(0, 0, 0), label='GDP')

gPIBLDO = [-0.039241125, -0.030965125, 0.00995, 0.0285795, 0.031488,
          0.03785502, 0.036219195, 0.0363155, 0.035448395, 0.03977582,
          0.034290995, 0.03380832, 0.031584795, 0.03090702, 0.029258955,
          0.027899555, 0.027608, 0.025662, 0.02527232, 0.023419155,
          0.02293088, 0.022051355, 0.02117102, 0.02019192, 0.019897995,
          0.020289875, 0.019505955, 0.018721395, 0.01823072, 0.017150355,
          0.016363875, 0.01606878, 0.015379875, 0.0148875, 0.01449342,
          0.01429632, 0.013606155, 0.013014195, 0.012224355, 0.012026795,
          0.011631555, 0.011433875, 0.011236155, 0.011038395, 0.01074168,
          0.010642755]

PIBLDO = np.zeros(len(years))
for i in range(year0, year1+1):
    PIBLDO[i-year0] = PIB[i-year0]/1.0e12
for i in range(year1+1, year2):
    PIBLDO[i-year0] = PIBLDO[i-year0-1]*np.exp(gPIBLDO[i-year1])
yearsPlot =  np.arange(year1, year2, 1)   
PIBLDOPlot = PIBLDO[year1-year0:year2-year0]
plt.plot(yearsPlot, PIBLDOPlot, color=(1, 0, 0), label='GDP LDO')

plt.xlabel('YEAR')    
plt.ylabel('GDP (TRILLIONS OF REAIS)')    
plt.legend(loc='upper left')
#plt.savefig('GDP2060.png', dpi=600, format='png')
plt.show()

