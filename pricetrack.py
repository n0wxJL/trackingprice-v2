# from http import client
# from binance.client import Client
# from pprint import pprint
from songline import Sendline
# import datetime as dt
# from datetime import datetime
import token_api as tkk
import coin_list
import setup_var as sv
import re
import yfinance as yf
import pandas as pd
import fn

# api_key = tkk.api_key
# api_secret = tkk.api_secret
token_noti = tkk.token_noti
messenger = Sendline(token_noti)

def pricetrack():
    tf_num = re.findall(r'\d+', sv.interval_candle)
    all_text = '\n'
    for i in coin_list.coin_list:
        if coin_list.coin_list[i]['open'] == '1':
            sym = coin_list.coin_list[i]['name']+'-'+coin_list.coin_list[i]['currency']
            precis = coin_list.coin_list[i]['precision']
            stk_pd = yf.Ticker(sym)
            sym = i
            # print(stk_pd)
            cur_sym = fn.cur_symbol(stk_pd.fast_info['currency'])
            frame = pd.DataFrame(stk_pd.history(period='4d',interval='1h')).reset_index()
            frame = frame.iloc[:,:6]
            # print(frame)
            if frame.empty == False:
                prc_close = frame['Close'].iloc[-1]
                prc_pre_close = frame['Close'].iloc[-1*(int(tf_num[0])+1)]
                prc_chg = (prc_close-prc_pre_close)/prc_pre_close*100
                prc_close_txt = '{:.{precis}f}'.format(prc_close, precis=precis)
                all_text += '▸{}:\nPrice: {}{}\nCHG: {:,.2f}%\n-----------\n'.format(sym,cur_sym,prc_close_txt,prc_chg)
    print(all_text)
    stats = messenger.sendtext(all_text)
    if stats != '200':
        pricetrack()