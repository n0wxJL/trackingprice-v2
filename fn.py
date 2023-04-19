from http import client
import time
import datetime as dt
from datetime import datetime, timezone, timedelta
import pandas as pd
import coin_list
import setup_var as sv
import re
import ta
import yfinance as yf
import lib

token_noti = sv.token_noti_status
messenger = lib

lookback = '300'

next_day = []
next_bar = []
fmt = '%Y-%m-%d %H:%M:%S'
fmt_min = '%Y-%m-%d %H:%M'

def time_next_day():
    time_servers = datetime.utcnow().replace(tzinfo=timezone.utc).replace(minute=0, second=0, microsecond=0).strftime(fmt)
    time_servers = datetime.strptime(time_servers,fmt)
    if not next_day:
        nextd = str(time_servers + dt.timedelta(days=1))
        next_day.append(nextd)
        print('Next Day',next_day[0])
    next_day_date = dt.datetime.strptime(next_day[0],fmt)
    if (next_day_date.day - time_servers.day) == 0:
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

def applytechnical(df):
    df['rsi'] = ta.momentum.rsi(df.Close,window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df['ema12'] = ta.trend.ema_indicator(df.Close,window=12)
    df['ema26'] = ta.trend.ema_indicator(df.Close,window=26)
    df['cdc'] = ta.trend.ema_indicator(df.Close,window=12) - ta.trend.ema_indicator(df.Close,window=26)
    df.dropna(inplace=True)

def get_action_indicator(df):
    print('get_action_indicator()')
    alltext=''
    if (float(df['cdc'].iloc[-1])>0 and float(df['cdc'].iloc[-2]<0)):
        alltext = alltext + '▲CDC_BUY👍\n'
    elif (float(df['cdc'].iloc[-1])<0 and float(df['cdc'].iloc[-2]>0)):
        alltext = alltext +  '▼CDC_SELL👎\n'
    if (float(df['rsi'].iloc[-1])>70):
        alltext = alltext + '▼RSI_OB👎\n'
    elif(float(df['rsi'].iloc[-1])<30):
        alltext = alltext + '▲RSI_OS👍\n'
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
    for i in coin_list.coin_list:
        if coin_list.coin_list[i]['open'] == '1':
            sym = coin_list.coin_list[i]['name']+'-'+coin_list.coin_list[i]['currency']
            precis = coin_list.coin_list[i]['precision']
            print(sym)
            stk_pd = yf.Ticker(sym)
            sym = i
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
            # print(frame)
            if frame.empty == False and frame2.empty == False:
                pr_chg = ((frame['Close'].iloc[-1] - frame['Close'].iloc[-2])/frame['Close'].iloc[-2])*100
                close_chg = frame['Close'].iloc[-1]
                rsi_chg = frame['rsi'].iloc[-1]
                macd_chg = frame['macd'].iloc[-1]
                cdc_chg = frame['cdc'].iloc[-1]
                take_action = get_action_indicator(frame)
                close_chg_txt = '{:.{precis}f}'.format(close_chg, precis=precis)
                all_text = all_text + '▸{}:\nPrice: {}{}\nCHG: {:,.2f}%\nRSI: {:,.2f}\nMACD: {:,.2f}\nCDC: {:,.2f}\n{}-----------\n'.format(sym,cur_sym,close_chg_txt,pr_chg,rsi_chg,macd_chg,cdc_chg,take_action)
    print(all_text)
    messenger.lineSendText(all_text,token_noti)

def datetimeUtcNow():
    return datetime.utcnow()