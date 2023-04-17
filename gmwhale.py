import token_api as tkk
import setup_var as sv
import random
import lib

token_noti = sv.token_noti_status
messenger = lib

def gmwhale():
        print('gmwhale()')
        value_text = 'Good morning 🌞.'+'\n\n'+callQoute()
        print(value_text)
        messenger.lineSendText(value_text)

def callQoute():
        return messenger.lineSendText([random.randrange(len(sv.txt_gm))],token_noti)