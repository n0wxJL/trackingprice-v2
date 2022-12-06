from forex_python.converter import CurrencyRates
import token_api as tkk
from songline import Sendline

# https://pypi.org/project/forex-python/ #
c = CurrencyRates()
token_noti = tkk.token_noti
messenger = Sendline(token_noti)

def getrate():
    text = ''
    text = 'USDTHB: {:,.3f}'.format(c.get_rate('USD','THB'))
    print(text)
    messenger.sendtext(text)
