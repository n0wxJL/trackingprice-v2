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
import yfinance as yf

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
    print('get_report()')
    all_text = '\n--Report Crypto--\n'
    for sym in mycoin:
        df = get_bar_data(sym,sv.interval,lookback)
        applytechnical(df)
        # print(df)
        take_action = get_action_indicator(df)
        all_text = all_text + '{}\n▸RSI: {:,.2f}\n▸MACD: {:,.2f}\n▸CDC: {:,.2f}\n{}-----------\n'.format(sym,df['rsi'][-2],df['macd'][-2],df['cdc'][-2],take_action)
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
    df['ema12'] = ta.trend.ema_indicator(df.Close,window=12)
    df['ema26'] = ta.trend.ema_indicator(df.Close,window=26)
    df['cdc'] = ta.trend.ema_indicator(df.Close,window=12) - ta.trend.ema_indicator(df.Close,window=26)
    df['week18'] = ta.trend.ema_indicator(df.Close,window=17)
    df.dropna(inplace=True)

def get_action_indicator(df):
    print('get_action_indicator()')
    alltext=''
    if (float(df['cdc'].iloc[-1])>0 and float(df['cdc'].iloc[-2]<0)):
        alltext = alltext + '▲CDC_BUY\n'
    elif (float(df['cdc'].iloc[-1])<0 and float(df['cdc'].iloc[-2]>0)):
        alltext = alltext +  '▼CDC_SELL\n'
    if (float(df['rsi'].iloc[-1])>70):
        alltext = alltext + '▼RSI_OVERBOUGHT\n'
    elif(float(df['rsi'].iloc[-1])<30):
        alltext = alltext + '▲RSI_OVERSOLD\n'
    if(float(df['week18'].iloc[-2]) < float(df['Close'].iloc[-1])):
        alltext = alltext + '▲WEEK18_UP\n'
    elif(float(df['week18'].iloc[-2]) > float(df['Close'].iloc[-1])):
        alltext = alltext + '▼WEEK18_DOWN\n'
    return alltext


def delay(sec):
    time.sleep(sec)

def cur_symbol(cur):
    if cur == 'USD':
        return '$'
    else :
        return '฿'
    
def get_report_crypto():
    print('get_report_crypto()')
    all_text = '\n--Report Crypto--\n'
    for sym in coin_list.coin_list_tf:
        print(sym)
        stk_pd = yf.Ticker(sym)
        cur_sym = cur_symbol(stk_pd.fast_info['currency'])
        frame = pd.DataFrame(stk_pd.history(period="6mo",interval='1d')).reset_index()
        frame2 = pd.DataFrame(stk_pd.history(period="2y",interval='1wk')).reset_index()
        frame = frame.iloc[:,:6]
        frame2 = frame2.iloc[:,:6]
        frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
        frame.sort_values(by='Date',ascending=True,inplace=True)
        frame2['Date'] = pd.to_datetime(frame2['Date'].dt.strftime('%Y-%m-%d'))
        frame2.sort_values(by='Date',ascending=True,inplace=True)
        applytechnical(frame)
        applytechnical(frame2)
        for i in range(0,len(frame2.index)):
            frame['week18'].iloc[-1*i] = frame2['week18'].iloc[-1*i]
        pr_chg = ((frame['Close'].iloc[-1] - frame['Close'].iloc[-2])/frame['Close'].iloc[-2])*100
        close_chg = frame['Close'].iloc[-1]
        rsi_chg = frame['rsi'].iloc[-1]
        macd_chg = frame['macd'].iloc[-1]
        cdc_chg = frame['cdc'].iloc[-1]
        week18_chg = frame['week18'].iloc[-1]
        take_action = get_action_indicator(frame)
        all_text = all_text + '{}: {}{:,.2f} CHG: {:,.2f}%\n▸RSI: {:,.2f}\n▸MACD: {:,.2f}\n▸CDC: {:,.2f}\n▸WEEK18: {:,.2f}\n{}-----------\n'.format(sym,cur_sym,close_chg,pr_chg,rsi_chg,macd_chg,cdc_chg,week18_chg,take_action)
    print(all_text)
    messenger.sendtext(all_text)