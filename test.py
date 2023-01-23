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


# import yfinance as yf

# tsla = yf.Ticker('TSLA')
# print(tsla.history())
# print(date.today() - dt.timedelta(days=1))
# print(tsla.history(start = date.today() - dt.timedelta(days=1), end = date.today()+dt.timedelta(days=1)))

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

# frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
# # print(frame.sort_values(by='Date',ascending=False))
# print(frame['Date'][20])

# lookback = '300'
# def get_report():
#     all_text = '\n--Report--\n'
#     for sym in mycoin:
#         df = fn.get_bar_data(sym,sv.interval,lookback)
#         fn.applytechnical(df)
#         # print(df)
#         take_action = get_action_indicator(df)
#         all_text = all_text + '{}\n  RSI: {:,.2f}\n  MACD: {:,.2f}\n  CDC: {:,.2f}\n{}------\n'.format(sym,df['rsi'][-2],df['macd'][-2],df['cdc'][-2],take_action)
#     print(all_text)
#     # messenger.sendtext(all_text)

# def get_action_indicator(df):
#     if (float(df['cdc'][-2])>0 and float(df['cdc'][-3]<0)):
#         return print('CDC_BUY_NEXT_BAR')
#     return

# get_report()
