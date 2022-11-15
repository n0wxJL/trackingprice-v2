from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
import pandas as pd
import datetime as dt
from datetime import datetime
import token_api as tkk
import coin_list
import setup_var as sv
import re
import fn

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

interval_bef = sv.interval
interval_tf = '1h' # sv.interval_candle
mycoin = coin_list.mycoin
fmt = '%Y-%m-%d %H:%M:%S'
fmt_min = '%Y-%m-%d %H:%M'

def get_bar_data(symbol,interval,lookback):
        time_servers = fn.time_server()
        # interval with lookback in a relationship time min hour day
        frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + ' hour ago UTC'))
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

while True:
    get_bar_data(mycoin[0],interval_tf,'50')
    time.sleep(1)