import pandas as pd

url_sp500 = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url_sp500)
# print(tables)
df_sp500 = tables[0]
df_sp500 = df_sp500[['Symbol', 'Security']]
df_sp500.columns = ['Ticker', 'Company']

url_nasdaq = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
# print(tables)
df_nasdaq = pd.read_csv(url_nasdaq, sep='|')
df_nasdaq = df_nasdaq[['Symbol', 'Security Name']]
df_nasdaq.columns = ['Ticker', 'Company']