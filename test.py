from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
import pandas as pd
import datetime as dt
from datetime import datetime,timezone,date
import token_api as tkk
import coin_list
import setup_var as sv
import re
import fn
import fn_stock

import numpy as np
# import ta

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


# import requests
# from bs4 import BeautifulSoup
# url = 'https://finance.yahoo.com/quote/TSLA'
# headers = {
#     'User-agent': 'Mozilla/5.0',
# }
# r= requests.get(url, headers=headers)
# print(r.status_code)
# soup = BeautifulSoup(r.text, 'html.parser')
# price = soup.find("fin-streamer", {"class":['Fw(b)', 'Fz(36px)', 'Mb(-4px)', 'D(ib)'] })
# print(price.contents)


import yfinance as yf

# tsla = yf.Ticker('TSLA')
# print(tsla.history())
# frame = pd.DataFrame(tsla.history()).reset_index()
# # print(frame)
# frame = frame.iloc[:,:6]
# print(frame)
# frame.columns = ['Date','Open','High','Low','Close','Volume']
# print(frame)
# frame = frame.set_index('Date')
# print(frame)
# frame.index = pd.to_datetime(frame.index, unit='ms')
# frame = frame.astype(float)

def get_stock_price():
    print('get_stock_price()')
    alltext = '\n--Stocks--\n'
    for sym in coin_list.stockd:
        stk_pd = yf.Ticker(sym)
        print(stk_pd)

        frame = pd.DataFrame(stk_pd.history()).reset_index()
        frame = frame.iloc[:,:6]
        frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
        frame.sort_values(by='Date',ascending=True,inplace=True)
        stk_chg = ((frame['Close'][20] - frame['Close'][19])/frame['Close'][19])*100
        alltext += '{}: {:,.2f} CHG: {:,.2f}%\n.\n'.format(sym,frame['Close'][20],stk_chg)
    print(alltext)
    # messenger.sendtext(alltext)


get_stock_price()