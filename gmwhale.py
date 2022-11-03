from http import client
from binance.client import Client
import time
import datetime as dt
from datetime import datetime
import token_api as tkk

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)

def gmwhale():
    while True:
        nexttoday = (datetime.utcnow().date()) + dt.timedelta(days=1)
        time_res = client.get_server_time()
        todaydate = datetime.fromtimestamp(time_res['serverTime']/1000).date()
        if todaydate == nexttoday:
            value_text = 'Good morning,Dolphin.'
            print(value_text)
        time.sleep(1)
