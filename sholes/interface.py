import streamlit as st
from sholes import BlackSholesModel, Stock, hv
import plotly as plt
import math
import numpy as np
from datetime import datetime, timedelta
#https://docs.streamlit.io/develop/api-reference/widgets

st.title('Hudson\'s Black Sholes')

st.write()

def truncate(number: float, decimals: int) -> float:
    stepper = 10.0 ** decimals
    return math.trunc(stepper * number) / stepper

def volatilitycalc(ticker, period = '1 day'):
    current = datetime.now()
    if ticker == '':
        return 0.00000000
    if period == '1 day':
        print('what')
        return hv(ticker, 1, current - timedelta(days = 1), current)
    if period == '1 week':
        print('what')
        return hv(ticker, 1, current - timedelta(days = 7), current)
    if period == '1 month (30 days)':
        print('what')
        return hv(ticker, 1, current - timedelta(days = 30), current)
    if period == '1 year':
        print('what')
        return hv(ticker, 1, current - timedelta(days = 365), current)
    
with st.sidebar:
    currentassetprice = st.number_input('Current Asset Price ($)', value =100)
    strikeprice = st.number_input('Strike Price ($)', value = 115)
    riskfreerate = st.number_input('Risk Free Rate', value = 0.05)
    volatilityperiod = st.pills("Volatility Period", ['1 day', '1 week', '1 month (30 days)', '1 year'])
    ticker = st.text_input('Ticker', placeholder='AAPL')
    if ticker == '':
        st.write('Please select a ticker!')
    if ticker != '':
        st.write(f'Volatility for {volatilityperiod or '1 day'}: {truncate(volatilitycalc(ticker, volatilityperiod), 3)}')
    timeuntilexp = st.number_input('Time until expiration (days)', value=30)

bsm_call = BlackSholesModel(currentassetprice, strikeprice, timeuntilexp, riskfreerate, volatilitycalc(ticker, volatilityperiod)).call_option_price()

st.write('price of the call option:', bsm_call)

# function that calcs voltaility