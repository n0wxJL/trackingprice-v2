from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
import pandas as pd
import datetime as dt
from datetime import datetime,timezone
import token_api as tkk
import coin_list
import setup_var as sv
import re
import fn

import numpy as np
import ta

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

interval_bef = sv.interval
interval_tf = '1d' # sv.interval_candle
mycoin = coin_list.mycoin
fmt = '%Y-%m-%d %H:%M:%S'
fmt_min = '%Y-%m-%d %H:%M'

def get_bar_data(symbol,interval,lookback):
        # time_servers = fn.time_server()
        # interval with lookback in a relationship time min hour day
        frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + ' day ago UTC'))
        # print(frame)
        frame = frame.iloc[:,:6]
        # print(frame)
        frame.columns = ['Time','Open','High','Low','Close','Volume']
        # print(frame)
        frame = frame.set_index('Time')
        frame.index = pd.to_datetime(frame.index, unit='ms')
        frame = frame.astype(float)
        # print(frame)
        return frame


def applytechnical(df):
        df['rsi'] = ta.momentum.rsi(df.Close,window=14)

def getReport():
        all_text = '\nRSI\n'
        for sym in mycoin:
                df = get_bar_data(sym,interval_tf,'30')
                applytechnical(df)
                all_text = all_text + '{}: {:,.2f}\n'.format(sym,df['rsi'][-2])
        print(all_text)
        messenger.sendtext(all_text)

# while True:
#         df = get_bar_data(mycoin[0],interval_tf,'30')
#         # print(df)
#         applytechnical(df)
#         print(df['rsi'][-2])
#         time.sleep(1)

# from urllib.request import Request,urlopen as req
# from bs4 import BeautifulSoup as soup

# url = 'https://th.investing.com/currencies/usd-thb'
# reqs = Request(url,headers={'User-Agent': 'Mozilla/5.0'})

# webopen = req(reqs)
# page_html = webopen.read()
# webopen.close()

# # print(page_html)
# data = soup(page_html,'html.parser')
# # print(data)

# temp = data.findAll('span',{'data-test':'instrument-price-last'})
# print(temp[0].text)