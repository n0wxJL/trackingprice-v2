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


def test():
    tf_num = re.findall(r'\d+', sv.interval_candle)
    all_text = '\n'
    for i in coin_list.coin_list:
        if coin_list.coin_list[i]['open'] == '1':
            print(coin_list.coin_list[i]['name']+'-'+coin_list.coin_list[i]['currency'])
            sym = coin_list.coin_list[i]['name']+'-'+coin_list.coin_list[i]['currency']
            stk_pd = yf.Ticker(sym)
            # print(stk_pd)
            cur_sym = fn.cur_symbol(stk_pd.fast_info['currency'])
            frame = pd.DataFrame(stk_pd.history(period='5d',interval='1h')).reset_index()
            frame = frame.iloc[:,:6]
            # print(frame)
            prc_close = frame['Close'].iloc[-1]
            prc_pre_close = frame['Close'].iloc[-1*(int(tf_num[0])+1)]
            prc_chg = (prc_close-prc_pre_close)/prc_pre_close*100
            all_text += '▸{}:\nPrice: {}{:,.2f}\nCHG: {:,.2f}%\n-----------\n'.format(sym,cur_sym,prc_close,prc_chg)
    print(all_text)
    # messenger.sendtext(all_text)

test()