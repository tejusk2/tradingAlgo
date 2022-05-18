import numpy as np
import pandas as pd

import yfinance as yf

import math

timerange='1y'
timebetween='1d'

buyFactors = []
#Lists of tickers I can algo trade
techStocks = "AMZN GOOG TSLA AAPL MSFT NVDA INTC FB BABA CRM AMD PYPL"

travelStocks = "BKNG LUV MAR ABNB DIS JBLU BA HLT WH CCL RCL"

spaceStocks = "SPCE LMT NOC MAXR BA DISH GSAT IRDM"

weedStocks = "CGC CRON TLRY GRWG VFF HYFM SNDL IIPR ARNA"

pharmaStocks = "REGN LLY AMGN MRNA JNJ BNTX JAZZ ABBV ABT NVAX NVO AZN PFE"

nrgStocks = "CVX OAS DTE IDA ETR PWR ATO DUK AEE PSX NEE SPWR PLUG"

realEstateStocks = "JLL AVB ALX MAA EGP EXR SUI FSV PLD SPG LSI FRT BXP"
#This is what stocks it uses, choose one of the above to conserve memory
stocks = nrgStocks
#^^^^^^^^
companies = stocks.split()

numStocks = len(companies)

companies.sort()

stocks = ""
for x in range(numStocks):
    stocks += companies[x]
    stocks += " "
    buyFactors.append(0)

data = yf.download(tickers = stocks , period = timerange , interval = timebetween)
# tickers downloads to the dataframe in alphabetical order



#Stochastic Oscillator
stochastics = []
for x in range(numStocks):
    
    C = data.iloc[-1]['Adj Close'].iloc[x]
    L14 = data.iloc[-14:]['Low'].min()
    L14 = L14.iloc[x]
    H14 = data.iloc[-14:]['High'].max()
    H14 = H14.iloc[x]

    StochasticOsc = C-L14
    StochasticOsc/= H14-L14
    StochasticOsc *= 100

    
    stochastics.append(StochasticOsc)

    if StochasticOsc < 20:
        buyFactors[x] += 2
    elif StochasticOsc > 80:
        buyFactors[x] -= 2
#Check how many std deviations the stock is from mean and bollinger bands sorta
zScores = []
zScore = 0
stdDevs = []
totDays = len(data['Adj Close'])
trends = []
trend = 0
for x in range(numStocks):
    totalDev = 0
    deviation = 0

    C = data.iloc[-1]['Close'].iloc[x]
    
    

    mean = data.iloc[totDays-20 : totDays]['Adj Close'].mean()
    mean = mean.iloc[x]

    upper = data.iloc[-1]['Adj Close'].iloc[x]
    lower =  data.iloc[-81]['Adj Close'].iloc[x]
    trend = (upper-lower)/lower
    trends.append(trend)
    
    #CalcStdDeviations
    for j in range(20):
        day = totDays - j
        
        
        
        deviation = data.iloc[day-1]['Adj Close']
        
        
        
        deviation = deviation.iloc[x]
        
        
        
        deviation = deviation - mean
        deviation *= deviation
        
        totalDev += deviation

    

    
    totalDev /= 20
    totalDev = math.sqrt(totalDev)
    
    
    
    
    


    
    zScore = C - mean
    zScore /= totalDev
    zScores.append(zScore)
    if trend > 0.04 and zScore <= -2:
        buyFactors[x] += 3
    elif trend < 0:
        buyFactors[x] -= 3
        


    




#Money Flow
moneyFlows = []

for x in range(numStocks):
    close = data.iloc[-1]['Adj Close'].iloc[x]
    H = data.iloc[-1]['High'].iloc[x]
    L = data.iloc[-1]['Low'].iloc[x]
    V = data.iloc[-1]['Volume'].iloc[x]
    flow = close + H + L
    flow /=3
    flow *= V


    close = data.iloc[-2]['Adj Close'].iloc[x]
    H = data.iloc[-2]['High'].iloc[x]
    L = data.iloc[-2]['Low'].iloc[x]
    V = data.iloc[-2]['Volume'].iloc[x]
    yflow = close + H + L
    yflow /=3
    yflow *= V

    if flow>yflow:
        moneyFlows.append("Positive")
        buyFactors[x] += 1
    else:
        moneyFlows.append("Negative")
        buyFactors[x] -= 1



for x in range(numStocks):
  print(companies[x] + ": " + str(buyFactors[x]))
 

    
    
