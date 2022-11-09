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

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)

next_day = []
fmt = '%Y-%m-%d %H:%M:%S'

def time_next_day():
    time_server = client.get_server_time()
    time_server = dt.datetime.fromtimestamp(time_server['serverTime']/1000).strftime(fmt)
    time_server = dt.datetime.strptime(time_server,fmt)
    # print(time_server)
    if not next_day:
        nextd = str(time_server + dt.timedelta(days=1))
        next_day.append(nextd)
        print('Add Next Day',next_day[0])

    next_day_date = dt.datetime.strptime(next_day[0],fmt)
    if (next_day_date.day - time_server.day) == 0:
        print('New Day :)')
        next_day.pop(0)
        # print('Delete Day in next_day')
        return True
    else:
        print('Old Day')
        return False
