import pandas as pd
import setup_var as sv
from bs4 import BeautifulSoup as soup
from urllib.request import Request,urlopen as req
from songline import Sendline
import token_api as tkk
import coin_list
import yfinance as yf
import ta

token_noti = tkk.token_noti
messenger = Sendline(token_noti)

def get_exchangerate():
    print('get_exchangerate()')
    text = ''
    reqs = Request(url=sv.url,headers={'User-Agent': 'Mozilla/5.0'})
    webopen = req(reqs)
    page_html = webopen.read()
    webopen.close()
    data = soup(page_html,'html.parser')
    temp = data.findAll('span',{'data-test':'instrument-price-last'})
    text = '\nUSDTHB: '+temp[0].text
    print(text)
    messenger.sendtext(text)

def get_stock_price():
    print('get_stock_price()')
    alltext = '\n--Stocks--\n'
    for sym in coin_list.stockd:
        stk_pd = yf.Ticker(sym)
        frame = pd.DataFrame(stk_pd.history(period='6mo')).reset_index()
        frame = frame.iloc[:,:6]
        frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
        frame.sort_values(by='Date',ascending=True,inplace=True)
        stk_chg = ((frame['Close'][20] - frame['Close'][19])/frame['Close'][19])*100
        alltext += '{}: {:,.2f} CHG: {:,.2f}%\n.\n'.format(sym,frame['Close'][20],stk_chg)
    print(alltext)
    messenger.sendtext(alltext)

def get_report_stock():
    print('get_report_stock()')
    all_text = '\n--Report Stock--\n'
    for sym in coin_list.stockd:
        print(sym)
        stk_pd = yf.Ticker(sym)
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
        for i in range(0,len(frame2.index)):
            df['week18'].iloc[-1*i] = frame2['week18'].iloc[-1*i]
        take_action = get_action_indicator(df)
        all_text = all_text + '{}\n  RSI: {:,.2f}\n  MACD: {:,.2f}\n  CDC: {:,.2f}\n  WEEK18: {:,.2f}\n{}-----------\n'.format(sym,df['rsi'].iloc[-2],df['macd'].iloc[-2],df['cdc'].iloc[-2],df['week18'].iloc[-1],take_action)
    print(all_text)
    messenger.sendtext(all_text)

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
    if (float(df['cdc'].iloc[-2])>0 and float(df['cdc'].iloc[-3]<0)):
        alltext = alltext + '=>CDC_BUY\n'
    elif (float(df['cdc'].iloc[-2])<0 and float(df['cdc'].iloc[-3]>0)):
        alltext = alltext +  '=>CDC_SELL\n'
    if (float(df['rsi'].iloc[-2])>70):
        alltext = alltext + '=>RSI_OVERBOUGHT\n'
    elif(float(df['rsi'].iloc[-2])<30):
        alltext = alltext + '=>RSI_OVERSOLD\n'
    if(float(df['week18'].iloc[-1]) < float(df['Close'].iloc[-1])):
        alltext = alltext + '=>WEEK18_UP\n'
    elif(float(df['week18'].iloc[-1]) > float(df['Close'].iloc[-1])):
        alltext = alltext + '=>WEEK18_DOWN\n'
    return alltext