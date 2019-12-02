# DESCRIPTION
# This imports quarterly CPI and GDP information from FRED to display the US Economy's Hedgeye QUAD.
# All credit to Hedgeye for coming up with the terminology.

import time
import pandas as pd
pd.options.mode.chained_assignment = None

# IMPORTING DATA
GDPl = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GDPC1&scale=left&cosd=1947-01-01&coed=2022-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=pc1&vintage_date=2022-10-04&revision_date=2022-10-04&nd=1947-01-01'
CPIl = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2022-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=pc1&vintage_date=2022-10-04&revision_date=2022-10-04&nd=1947-01-01'

GDP = pd.read_csv(GDPl)
CPI = pd.read_csv(CPIl)

# GDP & CPI CALCULATIONS
GDP = GDP.round(2).rename(columns={'DATE': 'Date', 'GDPC1_PC1': 'GDP'})
CPI = CPI.round(2).rename(columns={'DATE': 'Day', 'CPIAUCSL_PC1': 'CPI'})

# JOINING INFORMATION & CALCULATIONS
GDP = pd.concat([GDP, CPI['CPI']], axis=1, join='inner').set_index('Date')
GDP['CPI'] = GDP['CPI'].astype(float).round(2)
GDP['GDP Chng'] = GDP['GDP'] - GDP['GDP'].shift(1).round(2)
GDP['CPI Chng'] = GDP['CPI'] - GDP['CPI'].shift(1).round(2)
GDP['QUAD'] = 0
GDP['QUAD'][(GDP['GDP Chng'] > 0) & (GDP['CPI Chng'] > 0)] = 2
GDP['QUAD'][(GDP['GDP Chng'] > 0) & (GDP['CPI Chng'] < 0)] = 1
GDP['QUAD'][(GDP['GDP Chng'] < 0) & (GDP['CPI Chng'] > 0)] = 3
GDP['QUAD'][(GDP['GDP Chng'] < 0) & (GDP['CPI Chng'] < 0)] = 4
GDP['Qtr'] = pd.PeriodIndex(pd.to_datetime(GDP.index), freq='Q')
GDP = GDP[['Qtr', 'GDP', 'CPI', 'GDP Chng', 'CPI Chng', 'QUAD']]

GDP = GDP.sort_values('Date', ascending=False)
print(GDP.head(10))

time.sleep(100)
