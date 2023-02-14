from songline import Sendline
import token_api as tkk
import setup_var as sv
import random

token_noti = tkk.token_noti
messenger = Sendline(token_noti)

def gmwhale():
        print('gmwhale()')
        value_text = 'Good morning 🌞.'+'\n\n'+callQoute()
        print(value_text)
        messenger.sendtext(value_text)

def callQoute():
        return sv.txt_gm[random.randrange(len(sv.txt_gm))]