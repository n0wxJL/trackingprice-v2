import pandas as pd
import setup_var as sv
from bs4 import BeautifulSoup as soup
from urllib.request import Request,urlopen as req
import coin_list
import yfinance as yf
import ta
import fn
import lib
from datetime import datetime
import requests, lxml
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


token_noti = sv.token_noti_status
messenger = lib

def get_exchangerate():
    print('get_exchangerate()')
    all_text = ''
    reqs = Request(url=sv.url,headers={'User-Agent': 'Mozilla/5.0'})
    webopen = req(reqs)
    page_html = webopen.read()
    webopen.close()
    data = soup(page_html,'html.parser')
    temp = data.findAll('span',{'data-test':'instrument-price-last'})
    all_text = '\nUSDTHB: '+temp[0].text
    messenger.lineSendText(all_text,token_noti)

def get_report_stock():
    print('get_report_stock()')
    all_text = '\nReport Stock\n'
    for i in coin_list.stock_list:
        if coin_list.stock_list[i]['open'] == '1':
            sym = coin_list.stock_list[i]['name']
            precis = coin_list.stock_list[i]['precision']
            print(sym)
            stk_pd = yf.Ticker(sym)
            sym = i
            cur_sym = fn.cur_symbol(stk_pd.fast_info['currency'])
            frame = pd.DataFrame(stk_pd.history(period="6mo",interval='1d')).reset_index()
            frame2 = pd.DataFrame(stk_pd.history(period="2y",interval='1wk')).reset_index()
            frame = frame.iloc[:,:6]
            frame2 = frame2.iloc[:,:6]
            frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
            frame.sort_values(by='Date',ascending=True,inplace=True)
            frame2['Date'] = pd.to_datetime(frame2['Date'].dt.strftime('%Y-%m-%d'))
            frame2.sort_values(by='Date',ascending=True,inplace=True)
            df = frame
            applytechnical(df)
            applytechnical(frame2)
            if frame.empty == False and frame2.empty == False:
                pr_chg = ((df['Close'].iloc[-1] - df['Close'].iloc[-2])/df['Close'].iloc[-2])*100
                close_chg = df['Close'].iloc[-1]
                close_chg_txt = '{:.{precis}f}'.format(close_chg, precis=precis)
                rsi_chg = df['rsi'].iloc[-1]
                macd_chg = df['macd'].iloc[-1]
                cdc_chg = df['cdc'].iloc[-1]
                take_action = get_action_indicator(df)
                all_text = all_text + '▸{}:\nPrice: {}{}\nCHG(1D): {:,.2f}%\nRSI: {:,.2f}\nMACD: {:,.2f}\nCDC: {:,.2f}\n{}-----------\n'.format(sym,cur_sym,close_chg_txt,pr_chg,rsi_chg,macd_chg,cdc_chg,take_action)
    print(all_text)
    messenger.lineSendText(all_text,token_noti)

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
    if (float(df['cdc'].iloc[-1])>0 and float(df['cdc'].iloc[-3]<0)):
        alltext = alltext + '▲CDC_BUY👍\n'
    elif (float(df['cdc'].iloc[-1])<0 and float(df['cdc'].iloc[-3]>0)):
        alltext = alltext +  '▼CDC_SELL👎\n'
    if (float(df['rsi'].iloc[-1])>70):
        alltext = alltext + '▼RSI_OB👎\n'
    elif(float(df['rsi'].iloc[-1])<30):
        alltext = alltext + '▲RSI_OS👍\n'
    return alltext


def load_chrome_driver(proxy):
      options = Options()
      options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
      options.add_argument('--headless')
      options.add_argument('--disable-gpu')
      options.add_argument('--no-sandbox')
      options.add_argument('--remote-debugging-port=9222')
      options.add_argument('--proxy-server='+proxy)

      return webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)


def topyield():
    url = 'https://www.set.or.th/th/market/index/sethd/overview'
    all_text = '\nTop Yield'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    r = requests.get(url,headers=headers)
    print(r.status_code)
    browser = load_chrome_driver('')
    browser.get(url)
    html = browser.page_source
    so = soup(html,'html.parser')
    ret = so.find_all('div',{'class':['symbol pt-1']})
    for val in ret:
        all_text = all_text+'\n'+(val.text).strip()
    # print(all_text)
    messenger.lineSendText(all_text,token_noti)
