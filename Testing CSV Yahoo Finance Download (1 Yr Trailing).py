import pandas as pd
from datetime import datetime

tickers = ['AAPL', 'AAL']
start_date = int(datetime(2015, 1, 1).timestamp())-1
end_date = int(datetime(2016, 1, 1).timestamp())+1

# ---------------- YAHOO CALCULATIONS ----------------

def yahoo_download(tickers, start, end ,OHLC):
    df = pd.DataFrame()
    for ticker in tickers:
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' + ticker + \
            '?period1=' + str(start) + '&period2=' + str(end) + '&interval=1d&events=history'
        price = pd.read_csv(url)
        df[ticker] = price[OHLC]
    df['Date'] = price['Date']
    return df

df = yahoo_download(tickers, start_date, end_date, 'Adj Close')
df.head()
