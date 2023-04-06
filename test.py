from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
import pandas as pd
import datetime as dt
from datetime import datetime,timezone,date
import token_api as tkk
import coin_list
import setup_var as sv
import re
import fn
import fn_stock
import ta
import yfinance as yf
import numpy as np

import requests

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)



# def Lineconfig(command):
# 		url = 'https://notify-api.line.me/api/notify'
# 		token = tkk.token_noti #self.tok ## EDIT
# 		header = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
# 		return requests.post(url, headers=header, data = command)


# def sendtext(message):
# 		# send plain text to line
# 		command = {'message':message}
# 		return Lineconfig(command)

# def test():
#     while True:
#         msg = sendtext('tesfewfewfweqfqwfwefewfwefsdfsdfffewfweqfwefwefewewdsfsdafaefwfwerwrewrewt')
#         print(msg)
#         time.sleep(2)

# test()