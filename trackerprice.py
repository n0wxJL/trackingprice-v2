# binance tracker price
from distutils.command.build_scripts import first_line_re
from http import client
from binance.client import Client
from pprint import pprint
from songline import Sendline
import time
import pandas as pd
import datetime as dt
from datetime import datetime

# token Line 'Notify Test Bot'
token_noti = 'qLyPnPXQ8LUXGhOORTaS9qgsEqxAsnktH5f0bL7YXf5'
#api key
api_key = 'IJ78NzLVwRberbdYqK990hGZEhIwzjoWIE2hGmSS9II5tQUk0ZLdmMhDVXnw1nd6'
api_secret = 'IRCQk5mYxvaN7Zs7FfGotGRQYwy6DwEGgxWQHcl58qjYdnwu2CKjgH40I3HVvNh9'
client = Client(api_key, api_secret)
messenger = Sendline(token_noti)

prices = client.get_all_tickers()
time_res = client.get_server_time()
todaydate = datetime.fromtimestamp(time_res['serverTime']/1000)
## print(todaydate)
end_date = todaydate + dt.timedelta(days=-1)
## print(end_date)

mycoin = ['ETHUSDT','BTCUSDT']
# symbol = "BTCUSDT" 
interval='1d' 
start_date = str(end_date) #str(time_res['serverTime'])
# klines = client.get_historical_klines(symbol, interval,start_date) 
# data = pd.DataFrame(klines)
# print(data)
# data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
# data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.close_time]
# data.head(7)

while True:
    alltext = ''
    prices = client.get_all_tickers() #request new price
    for p in prices:
        for c in mycoin:
            sym = c
            if p['symbol'] == sym :
              #change
              klines = client.get_historical_klines(sym, interval,start_date)
              # print(klines[0][1])
              # data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
              #price
              pc = float(p['price']) 
              chg =  (pc - float(klines[0][1]))/float(klines[0][1])*100
              text = '{} : {:,.3f} CHG {:,.3f}%'.format(sym,pc,chg)
              alltext += '\n' + text
    print(alltext)
    messenger.sendtext(alltext)
    time.sleep(3600)
