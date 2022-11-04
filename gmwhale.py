from http import client
from binance.client import Client
from songline import Sendline
import time
import datetime as dt
from datetime import datetime
import token_api as tkk

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)
# nexttoday = (datetime.utcnow().date()) + dt.timedelta(days=1)
def gmwhale():
    while True:
        messenger.sendtext('test')
        time_res = client.get_server_time()
        todaydate = datetime.fromtimestamp(time_res['serverTime']/1000).date()
        if tdate is None:
            tdate = todaydate
        if tdate != todaydate:
            tdate = todaydate
            value_text = 'Good morning.'
            print(value_text)
            messenger.sendtext(value_text)
        time.sleep(1)
