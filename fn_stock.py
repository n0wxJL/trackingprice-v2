from urllib.request import Request,urlopen as req
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
# from lxml import html
import os
import pandas as pd
import yfinance as yf
import ta
import requests, lxml
import lib
import fn
import setup_var as sv
import coin_list

token_noti = sv.token_noti_status
messenger = lib
currentYear = str(datetime.now().year)+'-01-01'

def get_exchangerate():
    #return string
    all_text = ''
    reqs = Request(url=sv.url,headers={'User-Agent': 'Mozilla/5.0'})
    webopen = req(reqs)
    page_html = webopen.read()
    webopen.close()
    data = soup(page_html,'html.parser')
    temp = data.findAll('span',{'data-test':'instrument-price-last'})
    all_text = '\n►USD/THB: '+temp[0].text
    # messenger.lineSendText(all_text,token_noti)
    return all_text

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
    count = 0
    all_text = '\n►Top Dividend Yield◄'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    r = requests.get(url,headers=headers)
    print('status site:',r.status_code)
    browser = load_chrome_driver('')
    browser.get(url)
    html = browser.page_source
    so = soup(html,'html.parser')
    ret = so.find_all('div',{'class':['symbol pt-1']})
    df = {'symbol':[],'last':[],'yield':[],'rate':[]}
    for val in ret:
        count = count + 1
        ticker = (val.text).strip()+'.BK'
        ticker_y = yf.Ticker(ticker)
        pricelast = price_last(ticker_y,'1wk','1d','2',-1)
        yieldlast = '{:.{precis}f}'.format(ticker_y.info.get('lastDividendValue'), precis=2) 
        yieldrate = '{:.{precis}f}'.format((float(ticker_y.info.get('trailingAnnualDividendYield'))*100),precis=2) 
        df['symbol'].append(ticker)
        df['last'].append(pricelast)
        df['yield'].append(yieldlast)
        df['rate'].append(yieldrate)
    df1 = pd.DataFrame(df).sort_values(by=['yield'],ascending=False).reset_index()
    # print(df1)
    for row in range(len(df1)):
        print(df1.loc[row,'symbol'])
        all_text = all_text+'\n'+'►{}\nPrice: {}\nYield: {}\nRate: {}%\n-----------'.format(df1.loc[row,'symbol'],df1.loc[row,'last'],df1.loc[row,'yield'],df1.loc[row,'rate'])
        if row == 9:
            break
    print(all_text)
    messenger.lineSendText(all_text,token_noti)

def price_last(ticker_his,period,interval,precis,iloc):
    """
    ticker_his -- ticker symbol
    period -- period
    interval -- candle time frame
    precis -- precision 
    iloc -- loc index
    """
    frame = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
    frame = frame.iloc[:,:6]
    return '{:.{precis}f}'.format(frame['Close'].iloc[iloc],precis=precis)

def price_change_percent(ticker_his,period,interval,precis,last_price,iloc):
    #return string
    try:
        lp = float(last_price)
        frame = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
        frame = frame.iloc[:,:6]
        # print(ticker_his,'-','last_price',lp,frame)
        pricestr = '{:.{precis}f}'.format(((lp - frame['Open'].iloc[iloc])/frame['Open'].iloc[iloc])*100,precis=precis)
    except:
        pricestr = '-'
    return pricestr

def price_ret_dataframe(ticker_his,period,interval):
    dataframe = pd.DataFrame(ticker_his.history(period=period,interval=interval)).reset_index()
    dataframe = dataframe.iloc[:,:6]
    dataframe['Date'] = pd.to_datetime(dataframe['Date'].dt.strftime('%Y-%m-%d'))
    dataframe.sort_values(by='Date',ascending=True,inplace=True)
    return dataframe

def get_report_stock_v2():
    #return list of stock report
    all_text = '\n►List Stock◄\n'
    ls = []
    pePrice = ''
    trailPE = 0
    forPE = 0
    iloc_price = -1
    for i in sorted(coin_list.stock_list):
        try:
            if coin_list.stock_list[i]['open'] == '1':
                sym = coin_list.stock_list[i]['name']
                precis = coin_list.stock_list[i]['precision']
                stk_pd = yf.Ticker(sym)
                cur_sym = fn.cur_symbol(coin_list.stock_list[i]['currency'])
                price_close_day = price_last(stk_pd,'7d','1d',precis,iloc_price)
                price_chg_day = price_change_percent(stk_pd,'1wk','1d',precis,price_close_day,iloc_price)
                price_chg_month = price_change_percent(stk_pd,'1y','1mo',precis,price_close_day,iloc_price)
                price_chg_month6 = price_change_percent(stk_pd,'1y','1mo',precis,price_close_day,-5)
                price_chg_year = lib.price_change_percent_for_year(stk_pd,currentYear,'1mo',precis,price_close_day,-2)
                # print(sym,price_close_day,price_chg_day,price_chg_month,price_chg_month6)
                dataframe = price_ret_dataframe(stk_pd,'2mo','1d')
                if dataframe.empty == False:
                    applytechnical(dataframe)
                    # take_action = get_action_indicator(dataframe)
                    rsi_chg = dataframe['rsi'].iloc[-1]
                    macd_chg = dataframe['macd'].iloc[-1]
                    cdc_chg = dataframe['cdc'].iloc[-1]
                    # pause errro authorize 
                    # if 'trailingPE' not in stk_pd.info:
                    #     trailPE = 0
                    # else:
                    #     trailPE = stk_pd.info['trailingPE']
                    # if 'forwardPE' not in stk_pd.info:
                    #     forPE = 0
                    # else:
                    #     forPE = stk_pd.info['forwardPE']
                    trailPE = 0
                    forPE = 0
                    pePrice = lib.formatPrecis(precis,trailPE,forPE)
                    ls.append('►{}:\nPrice: {}{}\nCHG(1D): {}%\nCHG(1M): {}%\nCHG(6M): {}%\nCHG(1Y): {}%\nRSI(1D): {:,.2f}\nMACD(1D): {:,.2f}\nCDC(1D): {:,.2f}\n-----------\n'.format(sym,cur_sym,price_close_day,price_chg_day,price_chg_month,price_chg_month6,price_chg_year,rsi_chg,macd_chg,cdc_chg))
        except Exception as e:
            print(e)
            pass
    fn.page_print(ls,7,all_text)