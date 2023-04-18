import setup_var as sv
import random
import lib

token_noti = sv.token_noti_status
messenger = lib

def gmwhale():
        print('gmwhale()')
        value_text = 'Good morning 🌞.'+'\n\n'+callQoute()
        print(value_text)
        messenger.lineSendText(value_text,token_noti)

def callQoute():
        return sv.txt_gm[random.randrange(len(sv.txt_gm))]