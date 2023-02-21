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
import ta
import yfinance as yf
import numpy as np

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

interval_bef = sv.interval
interval_tf = '1d' # sv.interval_candle
mycoin = coin_list.stockd
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

# tsla = yf.Ticker('TSLA')
# print(tsla.fast_info['currency'])
# print(tsla.info['exchange'])
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

# def get_stock_price():
#     print('get_stock_price()')
#     alltext = '\n--Stocks--\n'
#     for sym in coin_list.stockd:
#         stk_pd = yf.Ticker(sym)
#         print(stk_pd)

#         frame = pd.DataFrame(stk_pd.history()).reset_index()
#         frame = frame.iloc[:,:6]
#         frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
#         frame.sort_values(by='Date',ascending=True,inplace=True)
#         stk_chg = ((frame['Close'][20] - frame['Close'][19])/frame['Close'][19])*100
#         alltext += '{}: {:,.2f} CHG: {:,.2f}%\n.\n'.format(sym,frame['Close'][20],stk_chg)
#     print(alltext)
#     # messenger.sendtext(alltext)


# get_stock_price()


# def get_report_stock():
#     print('get_report_stock()')
#     all_text = '\n--Report Stock--\n'
#     for sym in mycoin:
#         print(sym)
#         stk_pd = yf.Ticker(sym)
#         frame = pd.DataFrame(stk_pd.history(period="6mo",interval='1d')).reset_index()
#         frame2 = pd.DataFrame(stk_pd.history(period="2y",interval='1wk')).reset_index()
#         frame = frame.iloc[:,:6]
#         frame2 = frame2.iloc[:,:6]
#         frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
#         frame.sort_values(by='Date',ascending=True,inplace=True)
#         frame2['Date'] = pd.to_datetime(frame2['Date'].dt.strftime('%Y-%m-%d'))
#         frame2.sort_values(by='Date',ascending=True,inplace=True)
#         df = frame
#         applytechnical(df)
#         applytechnical(frame2)
#         for i in range(0,len(frame2.index)):
#             df['week18'].iloc[-1*i] = frame2['week18'].iloc[-1*i]
#         take_action = get_action_indicator(df)
#         all_text = all_text + '{}\n  RSI: {:,.2f}\n  MACD: {:,.2f}\n  CDC: {:,.2f}\n  WEEK18: {:,.2f}\n{}-----------\n'.format(sym,df['rsi'].iloc[-2],df['macd'].iloc[-2],df['cdc'].iloc[-2],df['week18'].iloc[-1],take_action)
#     print(all_text)
#     messenger.sendtext(all_text)

# def applytechnical(df):
#     df['rsi'] = ta.momentum.rsi(df.Close,window=14)
#     df['macd'] = ta.trend.macd_diff(df.Close)
#     df['ema12'] = ta.trend.ema_indicator(df.Close,window=12)
#     df['ema26'] = ta.trend.ema_indicator(df.Close,window=26)
#     df['cdc'] = ta.trend.ema_indicator(df.Close,window=12) - ta.trend.ema_indicator(df.Close,window=26)
#     df['week18'] = ta.trend.ema_indicator(df.Close,window=17)
#     df.dropna(inplace=True)

# def get_action_indicator(df):
#     print('get_action_indicator()')
#     alltext=''
#     if (float(df['cdc'].iloc[-2])>0 and float(df['cdc'].iloc[-3]<0)):
#         alltext = alltext + '=>CDC_BUY\n'
#     elif (float(df['cdc'].iloc[-2])<0 and float(df['cdc'].iloc[-3]>0)):
#         alltext = alltext +  '=>CDC_SELL\n'
#     if (float(df['rsi'].iloc[-2])>70):
#         alltext = alltext + '=>RSI_OVERBOUGHT\n'
#     elif(float(df['rsi'].iloc[-2])<30):
#         alltext = alltext + '=>RSI_OVERSOLD\n'
#     if(float(df['week18'].iloc[-1]) < float(df['Close'].iloc[-1])):
#         alltext = alltext + '=>WEEK18_UP\n'
#     elif(float(df['week18'].iloc[-1]) > float(df['Close'].iloc[-1])):
#         alltext = alltext + '=>WEEK18_DOWN\n'
#     return alltext

# get_report_stock()


# messenger.sendtext('☼')


