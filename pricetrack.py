from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
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
interval_tf = sv.interval_candle
mycoin = coin_list.mycoin
dict_tf = {'M':'MINUTE','H':'HOUR','D':'DAY'}

fmt = '%Y-%m-%d %H:%M:%S'
tf_num = re.findall(r'\d+', interval_tf)
tf_text = re.sub('\d+', '', interval_tf)
tf_type_text = ''

for i in range(len(dict_tf)):
    if tf_text.upper() in dict_tf:
        tf_type_text = dict_tf[tf_text.upper()]
        break

def pricetrack():
    all_text = 'Time Frame : {} {}\n'.format(tf_num[0],tf_type_text)
    for sym in mycoin:
        candle_bef = client.get_historical_klines(sym, interval=interval_bef,limit=1)
        candle_tf = client.get_historical_klines(sym, interval=interval_tf,limit=1)
        candle_tf_fl = float(candle_tf[0][4])
        candle_bef_fl = float(candle_bef[0][1])
        candle_chg = ((candle_tf_fl-candle_bef_fl)/candle_bef_fl)*100
        all_text += '{}: {:,.2f} CHG: {:,.2f}%\n'.format(sym,candle_tf_fl,candle_chg)
    print(all_text)
    messenger.sendtext(all_text)