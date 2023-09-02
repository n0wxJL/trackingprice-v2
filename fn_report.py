from datetime import datetime
from bs4 import BeautifulSoup as soup
import pandas as pd
import ta
import yfinance as yf
import setup_var as sv
import coin_list
import fn
import fn_stock
import lib

currentYear = str(datetime.now().year)+'-01-01'

def get_report_fixed():
    all_text = ''
    all_text = fn_stock.get_exchangerate()
    # all_text = all_text + get_price_gold()
    print(all_text)
    lib.lineSendText(all_text,sv.token_noti_status)

def get_report_other():
    #return list of other GOLD,SPY,VOO report
    all_text = '\n►List Anything◄\n'
    ls = []
    pePrice = ''
    trailPE = 0
    forPE = 0
    iloc_price = -1
    for i,val in coin_list.list_anyting.items():
        try:
            print(val['name'])
            stk_pd = yf.Ticker(val['name'])
            cur_symbol = fn.cur_symbol(val['currency'])
            price_close_day = lib.price_last(stk_pd,'7d','1d',val['precision'],iloc_price)
            price_chg_day = lib.price_change_percent(stk_pd,'1wk','1d',val['precision'],price_close_day,iloc_price)
            price_chg_month = lib.price_change_percent(stk_pd,'1y','1mo',val['precision'],price_close_day,iloc_price)
            price_chg_month6 = lib.price_change_percent(stk_pd,'1y','1mo',val['precision'],price_close_day,-5)
            price_chg_year = lib.price_change_percent_for_year(stk_pd,currentYear,'1mo',val['precision'],price_close_day,0)
            # print(price_close_day,price_chg_day,price_chg_month,price_chg_month6,price_chg_year)
            dataframe = lib.price_ret_dataframe(stk_pd,'2mo','1d')
            if dataframe.empty == False:
                lib.applytechnical(dataframe)
                rsi_chg = dataframe['rsi'].iloc[-1]
                macd_chg = dataframe['macd'].iloc[-1]
                cdc_chg = dataframe['cdc'].iloc[-1]
                if 'trailingPE' not in stk_pd.info:
                    trailPE = 0
                else:
                    trailPE = stk_pd.info['trailingPE']
                if 'forwardPE' not in stk_pd.info:
                    forPE = 0
                else:
                    forPE = stk_pd.info['forwardPE']
                pePrice = lib.formatPrecis(val['precision'],trailPE,forPE)
                ls.append('►{}:\nPrice: {}{}\nCHG(1D): {}%\nCHG(1M): {}%\nCHG(6M): {}%\nCHG(1Y): {}%\nPE: {}\nRSI(1D): {:,.2f}\nMACD(1D): {:,.2f}\nCDC(1D): {:,.2f}\n-----------\n'.format(val['name'],cur_symbol,price_close_day,price_chg_day,price_chg_month,price_chg_month6,price_chg_year,pePrice,rsi_chg,macd_chg,cdc_chg))
        except Exception as excep_c:
            print(excep_c)
            pass
    lib.page_print(ls,7,all_text)

# def get_price_gold():
#     #report gold
#     gold = lib.request_price_html('GOLD','https://th.tradingview.com/symbols/XAUUSD/','last-JWoJqCpY js-symbol-last')
#     return gold