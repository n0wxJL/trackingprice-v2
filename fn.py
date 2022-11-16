from http import client
from binance.client import Client
# from pprint import pprint
from songline import Sendline
import time
import datetime as dt
from datetime import datetime
import token_api as tkk
import pandas as pd
import coin_list
import setup_var as sv
import re
import ta

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti
client = Client(api_key, api_secret)

messenger = Sendline(token_noti)

mycoin = coin_list.mycoin
lookback = '300'

next_day = []
next_bar = []
fmt = '%Y-%m-%d %H:%M:%S'
fmt_min = '%Y-%m-%d %H:%M'

def time_server():
    time_server = client.get_server_time()
    time_server = dt.datetime.fromtimestamp(time_server['serverTime']/1000).strftime(fmt)
    time_server = dt.datetime.strptime(time_server,fmt)
    return time_server

def time_next_day():
    time_servers = time_server()
    if not next_day:
        nextd = str(time_servers + dt.timedelta(days=1))
        next_day.append(nextd)
        print('Next Day',next_day[0])

    next_day_date = dt.datetime.strptime(next_day[0],fmt)
    if (next_day_date.day - time_servers.day) == 0:
        # print('New Day :)')
        next_day.pop(0)
        return True
    else:
        return False

def bar_time(interval,server_time):
    start_time = dt.datetime.combine(server_time, dt.time.min) # + dt.timedelta(hours=7)
    if not next_bar:
        interval_text = interval_find(interval)
        server_time = dt.datetime.strptime(dt.datetime.strftime(server_time,fmt_min),fmt_min)
        if interval_text[1] == 'm':
            minute = ((int(int(dt.datetime.strftime(server_time,'%M'))/int(interval_text[0])))+1)*int(interval_text[0])
            round_bar_next = int(dt.datetime.strftime(server_time - dt.timedelta(hours=int(dt.datetime.strftime(start_time,'%H'))),'%H'))
            minute = minute + (round_bar_next*60)
        if interval_text[1] == 'h':
            round_bar_next = int(dt.datetime.strftime(server_time - dt.timedelta(hours=int(dt.datetime.strftime(start_time,'%H'))),'%H'))
            round_bar_next = int(((round_bar_next/int(interval_text[0]))+1))*int(interval_text[0])
            minute = round_bar_next*60
        if interval_text[1] == 'd':
            minute = int(interval_text[0]) * 1440
        print(minute)
        time_set_start = start_time
        server_time_next = time_set_start + dt.timedelta(minutes=minute)
        sec = dt.datetime.strptime(dt.datetime.strftime(server_time_next,fmt_min),fmt_min)
        next_bar.append(sec)
        print('Next Bar',next_bar[0])
    next_bar_time = dt.datetime.strftime(next_bar[0],fmt_min)
    server_time = dt.datetime.strftime(server_time,fmt_min)
    if server_time == next_bar_time:
        next_bar.pop(0)
        print('pop',next_bar)
        return True
    else:
        return False

def interval_find(interval):
    interval_time = re.findall(r'\d+', interval)
    interval_text = re.sub('\d+', '', interval)
    interval_ret = [interval_time[0],interval_text]
    return interval_ret

def get_report():
    all_text = '\n--Report--\n'
    for sym in mycoin:
        df = get_bar_data(sym,sv.interval,lookback)
        applytechnical(df)
        # print(df)
        all_text = all_text + '{}\nRSI: {:,.2f}\nMACD: {:,.2f}\n------\n'.format(sym,df['rsi'][-2],df['macd'][-2])
    print(all_text)
    messenger.sendtext(all_text)

def get_bar_data(sym,interval,lookback):
    frame = pd.DataFrame(client.get_historical_klines(sym,interval,lookback + ' day ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

def applytechnical(df):
    df['rsi'] = ta.momentum.rsi(df.Close,window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df.dropna(inplace=True)