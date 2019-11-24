# TODO:
#   1 Capitalization potential. Difference between low and high
#   2 Magnitude of amount gain/loss yesterday, volume, earnings amount, surprise amount --> Machine Learning

# LINKS
#  - https://github.com/wenboyu2/yahoo-earnings-calendar
#  - https://github.com/FinanceData/FinanceDataReader

import requests
import csv
import time
from yahoo_earnings_calendar import YahooEarningsCalendar
import FinanceDataReader as fdr
from datetime import date, timedelta, datetime

f = open('Earnings2.csv', 'w')

start = date(2019, 3, 19)
yec = YahooEarningsCalendar()

with f:
    writer = csv.writer(f)
    writer.writerow(("Report Date", "Ticker", "Report Time", "Earnings", "Earnings Surprise (%)", "Close Before Earnings", "Open After Earnings", "Close After Earnings", "High After Earnings", "Low After Earnings", "Volume Before Earnings"))

    while start < date.today():
        print(start)
        time.sleep(2)

        for stock in yec.earnings_on(start):
            ticker = stock['ticker']
            earningsTime = stock['startdatetimetype']

            if earningsTime == 'TAS':
                et = datetime.strptime(stock['startdatetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                earningsOpen = et.replace(hour=9, minute=30, second=0)
                earningsClose = et.replace(hour=16, minute=00, second=0)
                if et < earningsOpen:
                    earningsTime = 'BMO'
                elif et > earningsClose:
                    earningsTime = 'AMC'
                else:
                    continue

            epsSurprise = stock['epssurprisepct']
            epsActual = stock['epsactual']

            if epsSurprise == None or epsActual == None: continue
            
            if earningsTime == 'BMO': # Earnings reported 'before market open'
                try:
                    df = fdr.DataReader(ticker, start - timedelta(days=5), start)
                    # Get today open, today close from last; yesterday close from n-1
                    todayOpen = df.iloc[-1]['Open']
                    todayClose = df.iloc[-1]['Close']
                    todayHigh = df.iloc[-1]['High']
                    todayLow = df.iloc[-1]['Low']
                    yestClose = df.iloc[-2]['Close']
                    yestVolume = df.iloc[-2]['Volume']
                    writer.writerow((start, ticker, earningsTime, epsActual, epsSurprise, yestClose, todayOpen, todayClose, todayHigh, todayLow, yestVolume)) 
                except:
                    pass
            elif earningsTime == 'AMC': # Earnings reported 'after market close'
                try:
                    df = fdr.DataReader(ticker, start, start + timedelta(days=5))
                    # Get today close from n = 0; tomorrow open, tomorrow close from n = 1
                    todayOpen = df.iloc[1]['Open']
                    todayClose = df.iloc[1]['Close']
                    todayHigh = df.iloc[1]['High']
                    todayLow = df.iloc[1]['Low']
                    yestClose = df.iloc[0]['Close']
                    yestVolume = df.iloc[0]['Volume']
                    writer.writerow((start, ticker, earningsTime, epsActual, epsSurprise, yestClose, todayOpen, todayClose, todayHigh, todayLow, yestVolume)) 
                except:
                    pass
        f.flush()
        start = start + timedelta(days=1)

f.close()