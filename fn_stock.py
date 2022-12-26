import pandas as pd
import setup_var as sv
from bs4 import BeautifulSoup as soup
from urllib.request import Request,urlopen as req
from songline import Sendline
import token_api as tkk
import coin_list
import yfinance as yf

token_noti = tkk.token_noti
messenger = Sendline(token_noti)

def get_exchangerate():
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
    alltext = '\n--Stocks--\n'
    for sym in coin_list.stockd:
        stk_pd = yf.Ticker(sym)
        frame = pd.DataFrame(stk_pd.history()).reset_index()
        frame = frame.iloc[:,:6]
        frame['Date'] = pd.to_datetime(frame['Date'].dt.strftime('%Y-%m-%d'))
        # frame.sort_values(by='Date',ascending=True)
        stk_close = frame['Close'][20]
        stk_chg = ((stk_close - frame['Close'][19])/frame['Close'][19])*100
        alltext += '{}: {:,.2f} CHG: {:,.2f}%\n'.format(sym,stk_close,stk_chg)
    print(alltext)
    messenger.sendtext(alltext)
