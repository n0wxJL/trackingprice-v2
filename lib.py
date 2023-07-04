from urllib.request import Request,urlopen as req
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import requests
import os
import pandas as pd
import ta
import math
import setup_var as sv

token_noti = sv.token_noti_status

def load_chrome_driver(proxy):
      options = Options()
      options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
      options.add_argument('--headless')
      options.add_argument('--disable-gpu')
      options.add_argument('--no-sandbox')
      options.add_argument('--remote-debugging-port=9222')
      options.add_argument('--proxy-server='+proxy)
      return webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)

def request_price_html(ticker_name,url,span_txt):
    #get data from request html return string
    #ticker_name - ex GOLD
    all_text = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    reqs = requests.get(url=url,headers=headers)
    print(reqs.status_code)
    browser = load_chrome_driver('')
    browser.get(url)
    html = browser.page_source
    so = soup(html,'html.parser')
    temp = so.find_all('span',{'class':span_txt})
    # print(temp[0].text)
    all_text = '\n►{}: ${}'.format(ticker_name,temp[0].text)
    return all_text

def lineSendText(message,token):
    #connect line api
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

def page_print(text,maxNum,headText):
    #print Page
    all_text = headText
    count = 1
    inx = 0
    maxPage = math.ceil(len(text)/maxNum)
    for i in range(maxPage):
        while count <= maxNum:
            all_text = all_text + text[inx]
            if count == maxNum or inx+1==len(text):
                all_text = '['+str(i+1)+']'+all_text
                print(all_text)
                lineSendText(all_text,token_noti)
                all_text = headText
                count = 1
                inx = inx + 1
                break
            count = count + 1
            inx = inx + 1