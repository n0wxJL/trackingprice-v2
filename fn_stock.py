from forex_python.converter import CurrencyRates
import token_api as tkk
from songline import Sendline
from urllib.request import Request,urlopen as req
from bs4 import BeautifulSoup as soup
import setup_var as sv

# https://pypi.org/project/forex-python/ #
# c = CurrencyRates()
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
