import streamlit as st
from typing import Callable
from typing import List
import yfinance as yf
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

class Stock:
    def __init__(self, ticker, interval, start, end):
        self.interval = interval
        self.start = start
        self.end = end
        self.ticker = ticker

    def get_data(self):
        self.data = yf.download(self.ticker, self.start, self.end, self.interval)
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)
        self.close = self.data['Close']


class BlackSholesModel:
    def __init__(self, S, K, T, r, sigma, call: bool = True):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.call = call

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + (0.5 * (self.sigma ** 2)))) / (self.sigma * np.sqrt(self.T))
    
    def d2(self):
        return self.d1() - (self.sigma * np.sqrt(self.T))
    
    def call_option_price(self):
        return (self.S * si.norm.cdf(self.d1(), 0, 1)) - (self.K * np.exp(-1 * self.r * self.T) * si.norm.cdf(self.d2(), 0, 1))
    
    def put_option_price(self):
        return (self.K * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2(), 0, 1) - self.S * si.norm.cdf(-self.d1(), 0, 1))
    
    def greeks(self):
        if self.call:
            return {"Delta": si.norm.cdf(self.d1(),0,1),
                    "Gamma": si.norm.pdf(self.d1(),0,1) / (self.S * self.sigma * np.sqrt(self.T)),
                    "Vega": self.S * si.norm.pdf(self.d1(), 0, 1) * np.sqrt(self.T),
                    "Theta": ((-1 * self.S * si.norm.pdf(self.d1(), 0, 1) * self.sigma) / 2 * np.sqrt(self.T)) - (self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(self.d2())),
                    "Rho": self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(self.d2())}
        


def historical_volatility(ticker: str, interval: int = 4, start: str = '2023-01-01', end = datetime.now()) -> float:
    stock = Stock(ticker, interval, start, end)
    stock.get_data()
    closes = stock.data['Close']
    mean_close = closes.mean()

    differences  = 0
    for close in closes:
        differences += (np.abs(close - mean_close) ** 2)

    volatlity = np.sqrt(differences / len(closes))

    return volatlity

st.title('Black Sholes Heatmap Visualizer')

st.write('yeah this is good')



with st.sidebar:
    st.title('General Information')
    current_asset_price = st.number_input('Current Asset Price')
    strike_price = st.number_input('Strike Price')
    time_to_maturity = st.number_input('Time to Mature (in years)')
    risk_free = st.number_input('Risk Free Interest Rate')
    st.title('Historical Volatility Bounds')
    start = st.date_input('Start date')
    end = st.date_input('End Date')

