import coin_list
import setup_var as sv
import re
import yfinance as yf
import pandas as pd
import fn
import lib

token_noti = sv.token_noti_status
messenger = lib

def pricetrack():
    tf_num = re.findall(r'\d+', sv.interval_candle)
    all_text = '\n'
    for i in coin_list.coin_list:
        if coin_list.coin_list[i]['open'] == '1':
            sym = coin_list.coin_list[i]['name']+'-'+coin_list.coin_list[i]['currency']
            precis = coin_list.coin_list[i]['precision']
            stk_pd = yf.Ticker(sym)
            sym = i
            cur_sym = fn.cur_symbol(stk_pd.fast_info['currency'])
            frame = pd.DataFrame(stk_pd.history(period='2d',interval='1h')).reset_index()
            frame = frame.iloc[:,:6]
            if frame.empty == False:
                prc_close = frame['Close'].iloc[-1]
                prc_pre_close = frame['Close'].iloc[-1*(int(tf_num[0])+1)]
                prc_chg = (prc_close-prc_pre_close)/prc_pre_close*100
                prc_close_txt = '{:.{precis}f}'.format(prc_close, precis=precis)
                all_text += '▸{}:\nPrice: {}{}\nCHG: {:,.2f}%\n-----------\n'.format(sym,cur_sym,prc_close_txt,prc_chg)
    print(all_text)
    stats = messenger.lineSendText(all_text,token_noti)
    return stats
    # if stats != 200:
    #     print(stats)
    #     time.sleep(2)
    #     pricetrack()
    # else:
    #     print(stats)
    #     return

print(pricetrack())