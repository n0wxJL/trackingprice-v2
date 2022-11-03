from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
# import pandas as pd
import datetime as dt
from datetime import datetime
import token_api as tkk
import coin_list

api_key = tkk.api_key
api_secret = tkk.api_secret
token_noti = tkk.token_noti

client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

interval='1h'
mycoin = coin_list.mycoin

# prices = client.get_all_tickers()
# time_res = client.get_server_time()
# todaydate = datetime.fromtimestamp(time_res['serverTime']/1000)
# ## print(todaydate)
# end_date = todaydate + dt.timedelta(days=-2)
# ## print(end_date)



 
# start_date = str(end_date) #str(time_res['serverTime'])
# # print(start_date)

# symbol = "BTCUSDT" 
# klines = client.get_historical_klines(symbol, interval,start_date) 
# # print(klines)
# data = pd.DataFrame(klines)
# print(data)
# data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
# data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.close_time]
# data.head(7)

# while True:
#     alltext = ''
#     prices = client.get_all_tickers() #request new price
#     for p in prices:
#         for c in mycoin:
#             sym = c
#             if p['symbol'] == sym :
#               #change
#               klines = client.get_historical_klines(sym, interval,start_date)
#               #print(klines[0][1])
#               # data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
#               #price
#               pc = float(p['price']) 
#               chg =  (pc - float(klines[0][1]))/float(klines[0][1])*100
#               text = '{} : {:,.3f} CHG {:,.3f}%'.format(sym,pc,chg)
#               alltext += '\n' + text
#     print(alltext)
#     # messenger.sendtext(alltext)
#     time.sleep(1)


# def prictrack():
#     while True:
#         time_res = client.get_server_time()
#         alltext = ''
#         for c in mycoin:
#             sym = c
#             print(c)
#             klines = client.get_historical_klines(sym, interval,end_str=time_res['serverTime'],limit=2)
#             for i in len(klines):
#                 pprint(klines[0][i])

#         #     pc = float(p['price']) 
#         #     # chg =  (pc - float(klines[0][1]))/float(klines[0][1])*100
#         #     # text = '{} : {:,.3f} CHG {:,.3f}%'.format(sym,pc,chg)
#         #     text = '{} : {:,.3f}'.format(sym,pc)
#         #     alltext += '\n' + text
#         # print(alltext)
#         # messenger.sendtext(alltext)
#         time.sleep(5)

# prictrack()