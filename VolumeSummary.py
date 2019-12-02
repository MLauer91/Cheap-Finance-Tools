# DESCRIPTION
# This project shows exchange volume, as reported by the CBOE, for the past 1-2 years.
# Z-scores are used to show variations over different time series.
# Major credit to Hedgeye for highlighting this data and how to interpret it using z-scores.

# ALL RELEVANT IMPORTATIONS
import datetime
import time
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from pandas.plotting import register_matplotlib_converters
yf.pdr_override()
register_matplotlib_converters()

# LINKS TO Cboe INFORMATION
CboeToday = 'https://markets.Cboe.com/us/equities/market_share/market/'
CboeY0 = 'https://markets.Cboe.com/us/equities/market_statistics/historical_market_volume/market_history_' + \
         str(datetime.date.today().year) + '.csv-dl'
CboeY1 = 'https://markets.Cboe.com/us/equities/market_statistics/historical_market_volume/market_history_' + \
         str(datetime.date.today().year - 1) + '.csv-dl'

# IMPORTING TODAY'S VOLUME DATA
MarketVolToday = int(pd.read_html(CboeToday)[1].iloc[12, 4])
today = datetime.datetime.today().strftime('%Y-%m-%d')
MarketVolToday = pd.DataFrame({'Day': [today], 'Total Shares': [MarketVolToday]})
# print(MarketVolToday)

# IMPORT SPY TICKER TO DISPLAY MARKET MOVE
ticker = 'SPY'
start = datetime.datetime(datetime.date.today().year - 1, 1, 1)
try:
    LoadIndex = web.get_data_yahoo(ticker, start, datetime.datetime.today())
except TimeoutError:
    pass
LoadIndex['% Chng'] = ((LoadIndex['Adj Close'].pct_change()) * 100).round(2)
LoadIndex = LoadIndex.rename_axis('Day')

# WRITING CURRENT YEAR AND ADDING CURRENT DAY INFORMATION
MarketVolY0 = pd.read_csv(CboeY0)
MarketVolY0 = MarketVolY0['Total Shares'].groupby(MarketVolY0['Day']).sum()
MarketVolY0 = MarketVolY0.reset_index()
MarketVolCurrent = MarketVolY0['Day'].count() - 1
if str(MarketVolY0.at[MarketVolCurrent, 'Day']) != str(today) and str(MarketVolY0.at[MarketVolCurrent, 'Total Shares']) \
        != str(MarketVolToday.at[0, 'Total Shares']):
    MarketVolY0 = MarketVolY0.append(MarketVolToday, ignore_index=True)
MarketVolY0 = MarketVolY0.sort_values('Day', ascending=False)
# print(MarketVolY0.at[MarketVolCurrent, 'Total Shares'])
# print(MarketVolToday.at[0, 'Total Shares'])

# WRITING PREVIOUS YEAR
MarketVolY1 = pd.read_csv(CboeY1)
MarketVolY1 = MarketVolY1['Total Shares'].groupby(MarketVolY1['Day']).sum()
MarketVolY1 = MarketVolY1.reset_index()
MarketVolY1 = MarketVolY1.sort_values('Day', ascending=False)

# JOINING PREVIOUS YEAR
MarketVolCur = MarketVolY0.append(MarketVolY1, ignore_index=True)

# Z-SCORE CALCULATIONS
MarketVolCur = MarketVolCur.sort_values('Day', ascending=True)
MarketVolCur['Prior Day'] = (MarketVolCur['Total Shares'].pct_change() * 100).round(0)
MarketVolCur['1M'] = ((MarketVolCur['Total Shares'] - MarketVolCur['Total Shares'].shift(1).rolling(20).mean())
                      / MarketVolCur['Total Shares'].shift(1).rolling(20).mean() * 100).round(0)
MarketVolCur['3M'] = ((MarketVolCur['Total Shares'] - MarketVolCur['Total Shares'].shift(1).rolling(60).mean())
                      / MarketVolCur['Total Shares'].shift(1).rolling(60).mean() * 100).round(0)
MarketVolCur['1Y'] = ((MarketVolCur['Total Shares'] - MarketVolCur['Total Shares'].shift(1).rolling(240).mean())
                      / MarketVolCur['Total Shares'].shift(1).rolling(240).mean() * 100).round(0)
MarketVolCur['12th EL'] = 1 + (MarketVolCur['Prior Day'].apply(lambda x: 2 if x >= 0 else 0) +
                               MarketVolCur['1M'].apply(lambda x: 2 if x >= 0 else 0) +
                               MarketVolCur['3M'].apply(lambda x: 2 if x >= 0 else 0) +
                               MarketVolCur['1Y'].apply(lambda x: 2 if x >= 0 else 0))
MarketVolCur = MarketVolCur.sort_values('Day', ascending=False).set_index('Day').join(LoadIndex['% Chng'])


# TESTING DATA FRAMES & SAVING TO CSV
print(MarketVolCur.head(10))
# MarketVolY0.to_csv('MarketVolY0.csv')

time.sleep(100)
