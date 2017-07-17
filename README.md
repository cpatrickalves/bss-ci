# bssf-ci
*Brazilian Social Security Forecast with Confidence Intervals*

This project implements a simple long-term Social Security forecast model to estimates the revenues and expenses of National Pensions.

Forecasts are explicitly probabilistic but no reference to error margins are ever made in Brazilian government documents. Even worse, forecast results are presented with a presumption of certainty with serious social and political consequences as they have embedded confidence intervals that are unknown to the audience. 
What would be the confidence intervals for the predicted series published in the budget guidelines? 
A simple exercise can be made starting from the GDP series.

We have built a simple GDP/National Pensios forecasts model from the informations taken from [Banco Central](https://www.bcb.gov.br/pec/Indeco/Port/indeco.asp) and Annex IV of [Budget Guidelines Laws (LDO)]((http://www12.senado.leg.br/orcamento/documentos/ldo).

The method assumes the behavior of GDP by 2060 will follow that of the calibration period, from 2000 to 2015. In this period, the growth rate of the GDP is modeled by a **Normal distribution** with mean and variance calculated from the data samples. The forecast of the GDP starts from the last observed point and assumes that its growth follows the laws of a **Brownian motion** up to the forecast horizon, taking as growth rates of the GDP those obtained from the calibration period. 

The purpose of this implementation is to forecasts GPD, revenues and expenses of National Pensions and compute the confidence intevals of such estimations.

The forecast model were implemented using Python.

# Instructions

1. Download/clone the files 
2. Download and install the [Anaconda](https://www.continuum.io/downloads) open source distribution of the Python.
3. In **Spyder** software (Anaconda's IDE), run each file:
    * *ForecastingGDP.py* - forecasts Brazilian GDP 
    * *ForecastingRGPS.py* - forecast revenues and expenses of National Pensions
    * *ForecastingRGPSPDeficit.py* - forecast financial results of National Pensions

