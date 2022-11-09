from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
# import pandas as pd
import datetime as dt
from datetime import datetime
import token_api as tkk
import coin_list
import setup_var as sv
import re

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

interval_bef = sv.interval
interval_tf = '3m' # sv.interval_candle
mycoin = coin_list.mycoin
fmt = '%Y-%m-%d %H:%M:%S'

while True:
    time_server = client.get_server_time()
    time_server_date = dt.datetime.fromtimestamp(time_server['serverTime']/1000).strftime(fmt)
    time_server_date = dt.datetime.strptime(time_server_date,fmt)
    print('Timer Sever:',time_server_date)
    candle_bef = client.get_historical_klines('BTCUSDT', interval=interval_bef,limit=1)
    candle_bef_date = dt.datetime.fromtimestamp(candle_bef[0][0]/1000).strftime(fmt)
    candle_bef_date = dt.datetime.strptime(candle_bef_date,fmt)
    print('Timer Candle:',candle_bef_date)
    time_diff_min = ((time_server_date - candle_bef_date).total_seconds()/60)
    print(time_diff_min)


    time.sleep(1)
    # all_text = ''
    # time_res = client.get_server_time()
    # for sym in mycoin:
    #     candle_bef = client.get_historical_klines(sym, interval=interval_bef,limit=1)
    #     candle_tf = client.get_historical_klines(sym, interval=interval_tf,limit=1)
    #     now_server_date = dt.datetime.strptime(dt.datetime.fromtimestamp(time_res['serverTime']/1000).strftime(fmt),fmt)
    #     now_server_int = int(now_server_date.timestamp())
    #     close_candle_date = dt.datetime.strptime(dt.datetime.fromtimestamp(candle_tf[0][6]/1000).strftime(fmt),fmt)
    #     close_candle_int = int(close_candle_date.timestamp())
    #     print('',close_candle_date,now_server_date,':',close_candle_int,now_server_int)
    #     if ((close_candle_int - now_server_int) <= 0):
    #         candle_tf_fl = float(candle_tf[0][4])
    #         candle_bef_fl = float(candle_bef[0][1])
    #         candle_chg = ((candle_tf_fl-candle_bef_fl)/candle_bef_fl)*100
    #         all_text += '{}:{:,.3f} CHG:{:,.2f}%\n'.format(sym,candle_tf_fl,candle_chg)
    #     else:
    #         all_text = ''
    # if all_text:
    #     print(all_text)
    #     # messenger.sendtext(all_text)
    # time.sleep(1)