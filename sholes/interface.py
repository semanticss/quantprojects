import streamlit as st
from scholes import BlackSholesModel, Stock, hv
import plotly as plt
import math
import numpy as np
from datetime import datetime, timedelta

#https://docs.streamlit.io/develop/api-reference/widgets

st.title('Hudson\'s Black Scholes for Stocks')

st.write()

today = datetime.now()

currentstock = Stock('AAPL', today, today - timedelta(days = 32))
currentstock.get_data()
st.write(currentstock.data)

def truncate(number: float, decimals: int) -> float:
    stepper = 10.0 ** decimals
    return math.trunc(stepper * number) / stepper

def vol_and_stock_object(ticker, period = '1 day'):
    current = today
    if ticker == '':
        return 0.00000000
    if period == '1 day':
        currentstock = Stock(ticker, start = today - timedelta(days = 1), end = today)
        return hv(ticker, 1, current - timedelta(days = 1), current)
    if period == '1 week':
        currentstock = Stock(ticker, start = today - timedelta(days = 7), end = today)
        return hv(ticker, 1, current - timedelta(days = 7), current)
    if period == '1 month (30 days)':
        currentstock = Stock(ticker, start = today - timedelta(days = 30), end = today)
        return hv(ticker, 1, current - timedelta(days = 30), current)
    if period == '1 year':
        currentstock = Stock(ticker, start = today - timedelta(days = 365), end = today)
        return hv(ticker, 1, current - timedelta(days = 365), current)
    
with st.sidebar:
    strikeprice = st.number_input('Strike Price ($)', value = 115)
    riskfreerate = st.number_input('Risk Free Rate', value = 0.05)
    currentassetprice = st.number_input('Current Asset Price ($)', value =100)
    volatilityperiod = st.pills("Volatility Period", ['1 day', '1 week', '1 month (30 days)', '1 year'])
    ticker = st.text_input('Ticker', placeholder='AAPL')
    if ticker == '':
        st.write('Please select a ticker!')
    if ticker != '':
        st.write(f'Volatility for {volatilityperiod or '1 day'}: {truncate(vol_and_stock_object(ticker, volatilityperiod), 3)}')
        currentassetprice = currentstock.currentprice
        st.write(currentstock)
        
    timeuntilexp = st.number_input('Time until expiration (days)', value=30)

bsm_call = BlackSholesModel(currentassetprice, strikeprice, timeuntilexp, riskfreerate, vol_and_stock_object(ticker, volatilityperiod)).call_option_price()

st.write('price of the call option:', bsm_call)

# function that calcs voltaility