from urllib.request import Request,urlopen as req
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import ta

# def request_price_html(ticker_name,url,span_txt):
#     #get data from request html return string
#     #ticker_name - ex GOLD
#     all_text = ''
#     reqs = Request(url=url,headers={'User-Agent': 'Mozilla/5.0'})
#     webopen = req(reqs)
#     page_html = webopen.read()
#     webopen.close()
#     data = soup(page_html,'html.parser')
#     temp = data.findAll('span',span_txt)
#     print(temp[0])
#     all_text = '\n►{}:'.format(ticker_name)
#     return all_text

def lineSendText(message,token):
    payload = {'message' : message}
    r = requests.post('https://notify-api.line.me/api/notify'
        , headers={'Authorization' : 'Bearer {}'.format(token)}
        , params = payload)
    return r.status_code
    
def lineSendSticker(stickerpack_id, sticker_id,token, message=' '):
    # sticker code https://developers.line.biz/en/docs/messaging-api/sticker-list/
    payload = {'message' : message,
            'stickerPackageId' : stickerpack_id,
            'stickerId' : sticker_id}
    r = requests.post('https://notify-api.line.me/api/notify'
        , headers={'Authorization' : 'Bearer {}'.format(token)}
        , params = payload)
    return r.status_code

def datetimeUtcNow():
    return datetime.utcnow()

def nameOfWeek():
    # return Monday,tuesday,Wednesday,Thursday,Friday,...
    return datetimeUtcNow().strftime('%A')

def formatPrecis(precis,val1,val2):
    # precis -- precision
    # val1 -- get the value to set precision
    if val1 is None:
        val1 = val2
    return '{:.{precis}f}'.format(val1,precis=precis)

def price_last(ticker_his,period,interval,precis,iloc):
    #tiker_his - ticker
    frame = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
    frame = frame.iloc[:,:6]
    return '{:.{precis}f}'.format(frame['Close'].iloc[iloc],precis=precis)

def price_change_percent(ticker_his,period,interval,precis,last_price,iloc):
    # return string
    try:
        lp = float(last_price)
        frame = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
        frame = frame.iloc[:,:6]
        pricestr = '{:.{precis}f}'.format(((lp - frame['Open'].iloc[iloc])/frame['Open'].iloc[iloc])*100,precis=precis)
    except Exception as e:
        pricestr = '-'
    return pricestr

def price_ret_dataframe(ticker_his,period,interval):
    #return dataframe
    dataframe = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
    dataframe = dataframe.iloc[:,:6]
    dataframe['Date'] = pd.to_datetime(dataframe['Date'].dt.strftime('%Y-%m-%d'))
    dataframe.sort_values(by='Date',ascending=True,inplace=True)
    return dataframe

def applytechnical(df):
    # return signal string
    df['rsi'] = ta.momentum.rsi(df.Close,window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df['ema12'] = ta.trend.ema_indicator(df.Close,window=12)
    df['ema26'] = ta.trend.ema_indicator(df.Close,window=26)
    df['cdc'] = ta.trend.ema_indicator(df.Close,window=12) - ta.trend.ema_indicator(df.Close,window=26)
    df.dropna(inplace=True)