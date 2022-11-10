from http import client
from binance.client import Client
# from pprint import pprint
from songline import Sendline
import time
import datetime as dt
from datetime import datetime
import token_api as tkk
# import coin_list
import setup_var as sv
import re

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)

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
        print('Add Next Day',next_day[0])

    next_day_date = dt.datetime.strptime(next_day[0],fmt)
    if (next_day_date.day - time_servers.day) == 0:
        print('New Day :)')
        next_day.pop(0)
        return True
    else:
        return False

def bar_time(interval,server_time):
    if not next_bar:
        minute = interval_find(interval)
        server_time = dt.datetime.strptime(dt.datetime.strftime(server_time,fmt_min),fmt_min)
        server_time_next = server_time + dt.timedelta(minutes=minute)
        sec = dt.datetime.strptime(dt.datetime.strftime(server_time_next,fmt_min),fmt_min)
        next_bar.append(sec)
        print('Next Bar',next_bar[0])
    next_bar_time = next_bar[0]
    if server_time == next_bar_time:
        next_bar.pop(0)
        return True
    else:
        return False

def interval_find(interval):
    # return minute
    minute = 0
    interval_time = re.findall(r'\d+', interval)
    interval_text = re.sub('\d+', '', interval)
    if interval_text == 'm':
        minute = int(interval_time[0])
    if interval_text == 'h':
        minute = int(interval_time[0]) * 60
    if interval_text == 'd':
        minute = int(interval_time[0]) * 1440
    return minute