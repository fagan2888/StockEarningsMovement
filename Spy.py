# TODO:
#   1 Capitalization potential. Difference between low and high
#   2 Magnitude of amount gain/loss yesterday, volume, earnings amount, surprise amount --> Machine Learning

# LINKS
#  - https://github.com/wenboyu2/yahoo-earnings-calendar
#  - https://github.com/FinanceData/FinanceDataReader

import requests
import csv
import time
import FinanceDataReader as fdr
from datetime import date, timedelta, datetime

f = open('SPY2.csv', 'w')

start = date(2019, 3, 18)

with f:
    writer = csv.writer(f)
    df = fdr.DataReader('SPY', start, date.today())
    for i in range(0,len(df)-1):
        todayOpen = df.iloc[i+1]['Open']
        yestClose = df.iloc[i]['Close']
        writer.writerow((yestClose, todayOpen)) 
        f.flush()

f.close()