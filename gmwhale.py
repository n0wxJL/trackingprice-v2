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

def gmwhale():
        value_text = 'Good morning. :)'+'\n\n'+callQoute()
        print(value_text)
        messenger.sendtext(value_text)

def callQoute():
    return sv.txt_gm[random.randrange(len(sv.txt_gm))]
