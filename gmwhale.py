from http import client
from binance.client import Client
from songline import Sendline
import time
import datetime as dt
from datetime import datetime
import token_api as tkk
import setup_var as sv
import random

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)
# nexttoday = (datetime.utcnow().date()) + dt.timedelta(days=1)

def gmwhale():
    tdate = None
    while True:
        time_res = client.get_server_time()
        todaydate = datetime.fromtimestamp(time_res['serverTime']/1000).date()
        if tdate is None:
            tdate = todaydate
        if tdate != todaydate:
            tdate = todaydate
            value_text = 'Good morning.'+'\n'+callQoute()
            print(value_text)
            messenger.sendtext(value_text)
        time.sleep(1)


def callQoute():
    return sv.txt_gm[random.randrange(len(sv.txt_gm))]
    # messenger.sendtext(sv.txt_gm[random.randrange(len(sv.txt_gm))])
