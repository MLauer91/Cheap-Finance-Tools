import pandas as pd
import io
import requests
import datetime
from tabulate import tabulate

ticker = input('Ticker: ').upper()

# ---------------- YAHOO CALCULATIONS ----------------
while ticker != 'QUIT':
    # ticker = 'SPY'
    refmultiply = 86400
    refdateyahoo = 1420156800  # This is 1/2/2015
    refdate = datetime.date(2015, 1, 2)
    startdate = datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day)
    enddate = datetime.date.today()
    enddatetoday = datetime.date(datetime.date.today().year, datetime.date.today().month + 1, datetime.date.today().day)

    if refdate == startdate:
        startdateyahoo = refdateyahoo
    else:
        startdateyahoo = refdateyahoo + (startdate - refdate).days * refmultiply

    if enddate == refdate:
        enddateyahoo = refdateyahoo
    elif enddate == datetime.date.today():
        enddateyahoo = refdateyahoo + (enddatetoday - refdate).days * refmultiply
    else:
        enddateyahoo = refdateyahoo + (enddate - refdate).days * refmultiply

    url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + \
          "?period1=" + str(startdateyahoo) + "&period2=" + str(enddateyahoo) + "&interval=1d&events=history"
    s = requests.get(url).content
    fullLoad = pd.read_csv(io.StringIO(s.decode('utf-8')))
    fullLoad['Date'] = pd.to_datetime(fullLoad['Date'])
    fullLoad = fullLoad.set_index('Date')

    # ------------ DISPLAYING RESULTS -------------
    headers = list(fullLoad.columns.values)
    print(tabulate(fullLoad.sort_index(ascending=False), headers, tablefmt="simple"))

    ticker = input('Ticker: ').upper()

print('Complete')
